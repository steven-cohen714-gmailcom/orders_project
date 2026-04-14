// File: frontend/static/js/report_view.js
import { loadRequesters, loadSuppliers, loadStatuses, normaliseStatus } from "/static/js/components/shared_filters.js";

/* ---- local project loader (keeps us independent of other shared code) ---- */
async function loadProjects(selectId) {
  try {
    const res = await fetch("/lookups/projects");
    const data = await res.json();
    const sel = document.getElementById(selectId);
    if (!sel) return;
    sel.innerHTML = '<option value="All">All</option>';
    // Accept either {projects:[...]} or [...] shapes
    const list = Array.isArray(data) ? data : (data.projects || []);
    list.forEach(p => {
      const code = p.project_code || p.code || p.id || "";
      const name = p.project_name || p.name || "";
      const opt = document.createElement("option");
      opt.value = code || name || "";
      opt.textContent = code && name ? `${code} - ${name}` : (code || name || "");
      sel.appendChild(opt);
    });
  } catch (e) {
    console.error("❌ Failed to load projects:", e);
  }
}

/* ---- title map ---- */
const TITLES = {
  item: "Purchases by Item",
  project: "Purchases by Project",
  supplier: "Supplier Spend",
  requester: "Requester Spend",
  open: "Open Orders / Outstanding",
  partial: "Partially Received (Aging)",
  cod: "COD Tracking",
  variance: "Item Price Variance",
    user_activity: "User Activity (by User)",
};

const groupBy = (() => {
  const v = (window.__REPORT_GROUP_BY__ || "item").toLowerCase();
  return v === "user" ? "user_activity" : v;   // alias for safety
})();



/* ---- helpers ---- */
function getEl(id) { return document.getElementById(id); }

function toCSV(rows) {
  if (!rows || !rows.length) return "";
  const headers = Object.keys(rows[0]);
  const escape = v => {
    if (v == null) return "";
    const s = String(v);
    if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
    return s;
  };
  const lines = [headers.join(",")];
  rows.forEach(r => lines.push(headers.map(h => escape(r[h])).join(",")));
  return lines.join("\n");
}

/* ---- number formatting helpers (money-ish columns to 2dp) ---- */
const MONEY_COL_RE = /(total|spend|amount|value|cost|price)/i; // columns that look like currency
const QTY_COL_RE   = /(qty|quantity)/i;                        // quantities (0–2 dp)

function isNumericLike(v) {
  if (v === null || v === "") return false;
  const n = typeof v === "number" ? v : Number(String(v).replace(/,/g, ""));
  return Number.isFinite(n);
}
function asNumber(v) {
  return typeof v === "number" ? v : Number(String(v).replace(/,/g, ""));
}
function fmtMoney(n) {
  const num = asNumber(n);
  return Number.isFinite(num)
    ? num.toLocaleString("en-ZA", { minimumFractionDigits: 0, maximumFractionDigits: 0 })
    : n;
}
function fmtQty(n) {
  const num = asNumber(n);
  return Number.isFinite(num)
    ? num.toLocaleString("en-ZA", { minimumFractionDigits: 0, maximumFractionDigits: 2 })
    : n;
}
function formatCell(columnName, value) {
  if (!isNumericLike(value)) return value ?? "";
  if (MONEY_COL_RE.test(columnName)) return fmtMoney(value);
  if (QTY_COL_RE.test(columnName))   return fmtQty(value);
  // generic numeric: keep as-is (no forced decimals)
  const num = asNumber(value);
  return num.toLocaleString("en-ZA", { maximumFractionDigits: 6 });
}

/* Pick sensible key columns for grouping/subtotals per report */
function pickGroupKeyColumns(columns) {
  // Try known patterns first
  const prefs = {
    item:      ["item_code", "item_description"],
    project:   ["project", "project_code", "project_name"],
    supplier:  ["supplier", "supplier_name"],
    requester: ["requester", "requester_name"],
  };
  const preferred = prefs[groupBy] || [];
  const found = preferred.filter(c => columns.includes(c));
  if (found.length) return found;
  // fallback: use the first column
  return [columns[0]];
}

/* Build a subtotal row for a set of rows */
function buildSubtotalRow(columns, keyCols, rows) {
  const subtotal = {};
  columns.forEach(col => {
    if (keyCols.includes(col)) {
      // Label the first key col as "Subtotal"
      subtotal[col] = "Subtotal";
    } else if (isNumericLike(rows[0][col])) {
      // Sum numeric-like columns
      let sum = 0;
      rows.forEach(r => { if (isNumericLike(r[col])) sum += asNumber(r[col]); });
      subtotal[col] = sum;
    } else {
      subtotal[col] = "";
    }
  });
  return subtotal;
}

function renderTable(data) {
  const thead = getEl("rpt-thead");
  const tbody = getEl("rpt-tbody");
  thead.innerHTML = "";
  tbody.innerHTML = "";

  if (!data) return;

  // Support either {columns, rows} or just array
  const rows = Array.isArray(data.rows) ? data.rows
             : (Array.isArray(data) ? data : []);
  if (!rows.length) return;

  const columns = Array.isArray(data.columns) && data.columns.length
    ? data.columns
    : Object.keys(rows[0]);

  // header
  const tr = document.createElement("tr");
  columns.forEach(c => {
    const th = document.createElement("th");
    th.textContent = c;
    tr.appendChild(th);
  });
  thead.appendChild(tr);

  // Should we group duplicates and show subtotals?
  const doSubtotals = !!getEl("chk-subtotal-duplicates")?.checked;

  if (doSubtotals) {
    const keyCols = pickGroupKeyColumns(columns);
    const groups = [];
    const indexMap = new Map(); // keep stable order
    rows.forEach(r => {
      const key = keyCols.map(k => r[k]).join("§");
      if (!indexMap.has(key)) {
        indexMap.set(key, groups.length);
        groups.push({ key, rows: [] });
      }
      groups[indexMap.get(key)].rows.push(r);
    });

    groups.forEach(g => {
      // emit each row in the group
      g.rows.forEach(r => {
        const trb = document.createElement("tr");
        columns.forEach(c => {
          const td = document.createElement("td");
          td.textContent = formatCell(c, r[c]);
          trb.appendChild(td);
        });
        tbody.appendChild(trb);
      });
      // emit subtotal
      const subtotal = buildSubtotalRow(columns, keyCols, g.rows);
      const subTr = document.createElement("tr");
      subTr.className = "subtotal-row";
      columns.forEach(c => {
        const td = document.createElement("td");
        const val = subtotal[c];
        td.textContent = isNumericLike(val) ? formatCell(c, val) : String(val || "");
        subTr.appendChild(td);
      });
      tbody.appendChild(subTr);
    });
    return;
  }

  // plain body (no subtotals)
  rows.forEach(r => {
    const trb = document.createElement("tr");
    columns.forEach(c => {
      const td = document.createElement("td");
      td.textContent = formatCell(c, r[c]);
      trb.appendChild(td);
    });
    tbody.appendChild(trb);
  });
}

/* ---- main run ---- */
async function runReport() {
  const params = new URLSearchParams();

  const start = getEl("start-date").value;
  const end   = getEl("end-date").value;
  const requester = getEl("filter-requester").value;
  const supplier  = getEl("filter-supplier").value;
  const project   = getEl("filter-project").value;
  const status    = getEl("filter-status").value;

  if (start) params.append("start_date", start);
  if (end)   params.append("end_date", end);
  if (requester && requester !== "All") params.append("requester", requester);
  if (supplier  && supplier  !== "All") params.append("supplier", supplier);
  if (project   && project   !== "All") params.append("project", project);

  const canonStatus = normaliseStatus(status);
  if (canonStatus && canonStatus !== "All") params.append("status", canonStatus);

  // checkboxes (send explicit true/false)
  params.append("include_details", getEl("chk-include-details").checked ? "true" : "false");
  params.append("group_monthly",   getEl("chk-group-monthly").checked   ? "true" : "false");
  params.append("only_cod",        getEl("chk-only-cod").checked        ? "true" : "false");
  params.append("show_price_stats",getEl("chk-price-stats").checked     ? "true" : "false");
  params.append("exclude_deleted", getEl("chk-exclude-deleted").checked ? "true" : "false");

  try {
    const url = (groupBy === "user_activity")
      ? `/orders/api/report/user_activity?${params.toString()}`
      : `/orders/api/report/line_items?group_by=${encodeURIComponent(groupBy)}&${params.toString()}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();
    renderTable(data);
}  catch (e) {
    console.error("❌ Report fetch failed:", e);
    renderTable({ columns: ["Error"], rows: [{ Error: e.message }] });
  }
  }
function clearFilters() {
  getEl("start-date").value = "";
  getEl("end-date").value = "";
  getEl("filter-requester").value = "All";
  getEl("filter-supplier").value = "All";
  getEl("filter-project").value = "All";
  getEl("filter-status").value = "All";
  getEl("chk-include-details").checked = false;
  getEl("chk-group-monthly").checked   = false;
  getEl("chk-only-cod").checked        = false;
  getEl("chk-price-stats").checked     = false;
  getEl("chk-exclude-deleted").checked = true;
  // If the new checkbox exists, leave its state as-is (user preference)
  renderTable({ columns: [], rows: [] });
}

async function bootstrap() {
  // title
  const h = getEl("rpt-title");
  h.textContent = TITLES[groupBy] || "Report";

  // filters
  await Promise.all([
    loadRequesters("filter-requester"),
    loadSuppliers("filter-supplier"),
    loadProjects("filter-project"),
  ]);
  loadStatuses("filter-status", { context: "reports" });

  // wire buttons
  getEl("rpt-run-btn").addEventListener("click", runReport);
  getEl("rpt-clear-btn").addEventListener("click", clearFilters);
  getEl("rpt-export-csv").addEventListener("click", () => {
    const rows = [];
    // rebuild rows from current table for quick export
    const thead = getEl("rpt-thead");
    const tbody = getEl("rpt-tbody");
    if (!thead.firstElementChild) return;
    const headers = Array.from(thead.firstElementChild.children).map(th => th.textContent);
    Array.from(tbody.children).forEach(tr => {
      const obj = {};
      Array.from(tr.children).forEach((td, i) => obj[headers[i]] = td.textContent);
      rows.push(obj);
    });
    const csv = toCSV(rows);
    const blob = new Blob([csv], { type: "text/csv" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${groupBy}_report.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
  });
}

document.addEventListener("DOMContentLoaded", bootstrap);
