// File: frontend/static/js/components/shared_filters.js
// Shared filter helpers for Requesters, Suppliers, Requisitioners and Status.
// Single source of truth for order status options + legacy alias normalisation.

//
// ---- Generic helpers ----
//
function byId(id) {
  const el = document.getElementById(id);
  if (!el) console.warn(`⚠️ shared_filters: element #${id} not found`);
  return el;
}

function resetSelect(selectEl, includeAll = true) {
  if (!selectEl) return;
  selectEl.innerHTML = "";
  if (includeAll) {
    const opt = document.createElement("option");
    opt.value = "All";
    opt.textContent = "All";
    selectEl.appendChild(opt);
  }
}

function appendOptions(selectEl, values) {
  if (!selectEl) return;
  for (const v of values) {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = v;
    selectEl.appendChild(opt);
  }
}

//
// ---- Requesters / Suppliers / Requisitioners ----
//
export async function loadRequesters(selectId) {
  try {
    const res = await fetch("/lookups/requesters");
    const data = await res.json();
    const select = byId(selectId);
    if (!select) return;

    resetSelect(select, true);
    (data?.requesters || []).forEach(r => {
      const opt = document.createElement("option");
      opt.value = r.name;
      opt.textContent = r.name;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error(`❌ Failed to load requesters for ${selectId}:`, err);
  }
}

export async function loadSuppliers(selectId) {
  try {
    const res = await fetch("/lookups/suppliers");
    const data = await res.json();
    const select = byId(selectId);
    if (!select) return;

    resetSelect(select, true);
    (data?.suppliers || []).forEach(s => {
      const opt = document.createElement("option");
      opt.value = s.name;
      opt.textContent = s.name;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error(`❌ Failed to load suppliers for ${selectId}:`, err);
  }
}

export async function loadRequisitioners(selectId) {
  try {
    const res = await fetch("/lookups/requisitioners");
    const data = await res.json();

    if (!res.ok) {
      console.error(`❌ Backend error fetching requisitioners (HTTP ${res.status}):`, data);
      throw new Error(
        typeof data === "object" ? (data.detail || data.message || "Unknown error from server.") : String(data)
      );
    }

    const select = byId(selectId);
    if (!select) return;

    resetSelect(select, true);

    if (Array.isArray(data)) {
      data.forEach(r => {
        const opt = document.createElement("option");
        // Use id as value so the filter can target a specific requisitioner if needed.
        opt.value = r.id;
        opt.textContent = r.name;
        select.appendChild(opt);
      });
    } else {
      console.error("❌ Expected an array of requisitioners, but received:", data);
      throw new Error("Invalid data format from server for requisitioners.");
    }
  } catch (err) {
    console.error(`❌ Failed to load requisitioners for ${selectId}:`, err);
    alert(`❌ Failed to load requisitioners: ${err.message}`);
  }
}

//
// ---- Status: single source of truth + normalisation ----
//
export const CANONICAL_STATUSES = [
  "Draft",
  "For Review",
  "On Hold",
  "Awaiting Authorisation",
  "Pending",
  "Authorised",
  "Declined",
  "Partially Received",
  "Received",
  "Partially Paid",
  "Fully Paid",
  "Deleted" // only for Audit Trail views
];

// Legacy / messy labels → canonical (or null to ignore)
export const STATUS_ALIASES = {
  // Review → For Review
  "Review": "For Review",
  "To Review": "For Review",

  // Draft variants
  "Draft Order": "Draft",

  // Awaiting Authorisation (UK spelling canonical)
  "Waiting for Approval": "Awaiting Authorisation",
  "Awaiting Approval": "Awaiting Authorisation",
  "Awaiting Authorization": "Awaiting Authorisation",

  // US → UK spelling
  "Authorized": "Authorised",

  // On Hold variants
  "On hold": "On Hold",

  // Receiving
  "Partially Delivered": "Partially Received",

  // Payments
  "Partially Payed": "Partially Paid",
  "Part Paid": "Partially Paid",
  "Paid": "Fully Paid", // FE sometimes says "Paid" — backend uses "Fully Paid"

  // Not a status
  "COD": null
};

// Build a lowercase lookup so aliasing is case-insensitive.
const STATUS_ALIASES_LC = Object.fromEntries(
  Object.entries(STATUS_ALIASES).map(([k, v]) => [k.toLowerCase(), v])
);

/**
 * Map any raw status coming from UI/DB to a canonical value.
 * Returns:
 *  - canonical string (e.g. "Authorised"),
 *  - null if it should be ignored (e.g. "COD"),
 *  - or the original string if no mapping exists.
 */
export function normaliseStatus(raw) {
  if (raw == null) return raw;
  const v = String(raw).trim();
  const hit = STATUS_ALIASES_LC[v.toLowerCase()];
  return (hit !== undefined) ? hit : v;
}

/**
 * Populate a status <select> consistently across screens.
 * @param {string} selectId
 * @param {{context?: "default"|"pending"|"cod"|"audit", includeAll?: boolean}} opts
 */
export function loadStatuses(selectId, { context = "default", includeAll = true } = {}) {
  const select = byId(selectId);
  if (!select) return;

  // Start with the full canonical list.
  let list = [...CANONICAL_STATUSES];

  // Default views hide Deleted.
  if (context !== "audit") {
    list = list.filter(s => s !== "Deleted");
  }

  // Screen-specific trims (tweak as needed, but keep the source centralised here).
  if (context === "cod") {
    // COD screen focuses on finance states; never show Draft/Deleted.
    list = list.filter(s => !["Draft", "Deleted"].includes(s));
  }

  if (context === "pending") {
    // Pending-centric view: hide Deleted; keep the rest.
    list = list.filter(s => s !== "Deleted");
  }

  resetSelect(select, includeAll);
  appendOptions(select, list);
}
