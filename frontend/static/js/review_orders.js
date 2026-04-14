import { escapeHTML, formatCurrency, formatYMD } from './components/utils.js';
// File: frontend/static/js/review_orders.js
// Relative Path: frontend/static/js/review_orders.js

import { loadRequesters, loadSuppliers } from './components/shared_filters.js';
import { showOrderNoteModal } from './components/order_note_modal.js';
import { showPDFModal } from './components/pdf_modal.js';

const inflight = new Set();

console.log("review_orders.js v-onhold-1");

// Currency formatter


async function loadFiltersAndOrders() {
  try {
    await Promise.all([
      loadRequesters("filter-requester"),
      loadSuppliers("filter-supplier")
    ]);
    await loadOrders();
  } catch (error) {
    console.error("❌ Error loading filters/orders:", error);
    const tbody = document.getElementById("pending-body");
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="7">Error loading filters: ${escapeHTML(error.message || String(error))}</td></tr>`;
    }
  }
}

async function loadOrders() {
  const startDate = document.getElementById("start-date")?.value;
  const endDate   = document.getElementById("end-date")?.value;
  const requester = document.getElementById("filter-requester")?.value;
  const supplier  = document.getElementById("filter-supplier")?.value;

  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate)   params.append("end_date", endDate);
  if (requester && requester !== "All") params.append("requester", requester);
  if (supplier  && supplier  !== "All") params.append("supplier", supplier);

  try {
    const res = await fetch(`/orders/api/review_orders?${params.toString()}`);
    if (!res.ok) {
      const txt = await res.text().catch(() => "");
      throw new Error(`HTTP ${res.status}${txt ? `: ${txt}` : ""}`);
    }

    const data = await res.json();
    const orders = Array.isArray(data.orders) ? data.orders : [];

    // Numeric sort by order number (highest first)
    orders.sort((a, b) => (parseInt(b.order_number) || 0) - (parseInt(a.order_number) || 0));

    const tbody = document.getElementById("pending-body"); // reuse same tbody id to avoid HTML churn
    if (!tbody) {
      console.error("❌ Missing tbody#pending-body in template.");
      return;
    }
    tbody.innerHTML = "";

    if (orders.length === 0) {
      tbody.innerHTML = "<tr><td colspan='7'>No orders to review.</td></tr>";
      return;
    }

    orders.forEach((order, idx) => {
      const row = document.createElement("tr");

      const orderNumber = escapeHTML(order.order_number ?? "");
      const created     = escapeHTML(order.created_date ?? "");
      const requesterN  = escapeHTML(order.requester ?? "N/A");
      const supplierN   = escapeHTML(order.supplier ?? "N/A");
      const totalDisp   = formatCurrency(order.total);
      const statusDisp  = escapeHTML(order.status ?? "");
      const orderNote   = escapeHTML(order.order_note ?? "");
      const isOnHold = (statusDisp === "On Hold");
      const editIconHtml = isOnHold ? `<span class="edit-to-draft-icon" title="Edit (make Draft)" style="cursor: pointer;" data-order-id="${order.id ?? ''}" data-order-number="${orderNumber}">✏️</span>` : "";


        row.innerHTML = `
        <td>${created}</td>
        <td>${orderNumber}</td>
        <td>${requesterN}</td>
        <td>${supplierN}</td>
        <td>${totalDisp}</td>
        <td><span class="status">${statusDisp}</span></td>
        <td>
          <button class="view-btn" data-order-id="${order.id ?? ''}" data-order-number="${orderNumber}">View</button>
          <span class="note-icon" title="Edit Order Note" data-order-id="${order.id ?? ''}" data-order-note="${orderNote}" id="order-note-${idx}">📝</span>
          <span class="pdf-icon"  title="View PDF (with projects)" data-order-id="${order.id ?? ''}" data-order-number="${orderNumber}">📄</span>
          <span class="review-icon" style="color: green; cursor: pointer;" title="Mark as Reviewed" data-order-id="${order.id ?? ''}" data-order-number="${orderNumber}">✅</span>
          <span class="hold-icon" title="Put On Hold" style="cursor: pointer;" data-order-id="${order.id ?? ''}" data-order-number="${orderNumber}">🛑</span>
          ${editIconHtml}
        </td>
      `;

      // View button => internal PDF (with projects)
      row.querySelector(".view-btn").addEventListener("click", async (e) => {
        const id  = e.currentTarget.getAttribute("data-order-id");
        const num = e.currentTarget.getAttribute("data-order-number");
        await openInternalPdf(id, num);
      });

      // PDF icon => internal PDF (with projects)
      row.querySelector(".pdf-icon").addEventListener("click", async (e) => {
        const id  = e.currentTarget.getAttribute("data-order-id");
        const num = e.currentTarget.getAttribute("data-order-number");
        await openInternalPdf(id, num);
      });

      // Order Note
      const noteIcon = row.querySelector(`#order-note-${idx}`);
      noteIcon.addEventListener("click", () => {
        const id   = noteIcon.getAttribute("data-order-id");
        const note = noteIcon.getAttribute("data-order-note") || "";
        showOrderNoteModal(note, id, (newNote) => {
          const safe = escapeHTML(newNote);
          noteIcon.setAttribute("data-order-note", safe);
          noteIcon.title = "Edit Order Note\n" + safe;
        });
      });

      // Mark Reviewed (spinner + double-click guard)
      const reviewIcon = row.querySelector(".review-icon");
      reviewIcon.addEventListener("click", async (e) => {
        const el  = e.currentTarget;
        const id  = el.getAttribute("data-order-id");
        const num = el.getAttribute("data-order-number");
        if (!id) return;

        if (inflight.has(id)) return; // guard
        const confirmed = confirm(`Mark order number ${num} as reviewed?`);
        if (!confirmed) return;

        const tr = el.closest("tr");
        const oldText = el.textContent;

        try {
          inflight.add(id);
          el.classList.add("icon-working");
          el.textContent = "⏳";
          if (tr) tr.setAttribute("aria-busy", "true");

          const resp = await fetch(`/orders/api/mark_reviewed/${id}`, { method: "POST" });
          const body = await resp.json().catch(() => ({}));
          if (!resp.ok) throw new Error(body.detail || "Failed to mark reviewed");

          // Prefer backend-provided next_status; fallback to generic message
          const next = (body.next_status || "").trim().toUpperCase();
          let routed = null;
          if (next === "PENDING") routed = "routed to 'pending'";
          else if (next === "AWAITING AUTHORISATION") routed = "routed to 'Awaiting Authorisation'";

          alert(body.message || (routed
            ? `Order ${num} reviewed and ${routed}.`
            : `Order ${num} marked as reviewed.`));

          await loadOrders();

        } catch (err) {
          console.error("❌ Mark reviewed failed:", err);
          alert(`Could not mark as reviewed: ${err.message || String(err)}`);
        } finally {
          inflight.delete(id);
          el.classList.remove("icon-working");
          el.textContent = oldText;
          if (tr) tr.removeAttribute("aria-busy");
        }
      });

      const holdIcon = row.querySelector(".hold-icon");
      holdIcon.addEventListener("click", async (e) => {
        const el  = e.currentTarget;
        const id  = el.getAttribute("data-order-id");
        const num = el.getAttribute("data-order-number");
        if (!id) return;

        if (inflight.has(id)) return;
        const confirmed = confirm(`Put order ${num} On Hold?`);
        if (!confirmed) return;

        const tr = el.closest("tr");
        const oldText = el.textContent;

        try {
          inflight.add(id);
          el.textContent = "⏳";
          if (tr) tr.setAttribute("aria-busy", "true");

          const resp = await fetch(`/orders/api/mark_on_hold/${id}`, { method: "POST" });
          const body = await resp.json().catch(() => ({}));
          if (!resp.ok) throw new Error(body.detail || "Failed to set On Hold");

          alert(body.message || `Order ${num} is now On Hold.`);
          await loadOrders(); // stays on the Review screen and reloads rows
        } catch (err) {
          console.error("On Hold failed:", err);
          alert(`Could not put On Hold: ${err.message || String(err)}`);
        } finally {
          inflight.delete(id);
          el.textContent = oldText;
          if (tr) tr.removeAttribute("aria-busy");
        }
      });

      tbody.appendChild(row);

      // Edit (make Draft) — only present when status is "On Hold"
      const editIcon = row.querySelector(".edit-to-draft-icon");
      if (editIcon) {
        editIcon.addEventListener("click", async (e) => {
          const el  = e.currentTarget;
          const id  = el.getAttribute("data-order-id");
          const num = el.getAttribute("data-order-number");
          if (!id) return;

          if (inflight.has(id)) return; // guard against double-clicks
          const confirmed = confirm(`Convert order ${num} to a Draft so it can be edited?\n(The same order number will be preserved.)`);
          if (!confirmed) return;

          const tr = el.closest("tr");
          const oldText = el.textContent;

          try {
            inflight.add(id);
            el.textContent = "⏳";
            if (tr) tr.setAttribute("aria-busy", "true");

            const resp = await fetch(`/orders/api/convert_on_hold_to_draft/${id}`, { method: "POST" });
            const body = await resp.json().catch(() => ({}));
            if (!resp.ok) throw new Error(body.detail || "Failed to convert to Draft");

            // Success → go to Drafts list where Aaron will pick it up
            alert(body.message || `Order ${num} converted to Draft.`);
            window.location.href = "/orders/draft_orders";
          } catch (err) {
            console.error("❌ Convert to Draft failed:", err);
            alert(`Could not convert to Draft: ${err.message || String(err)}`);
          } finally {
            inflight.delete(id);
            el.textContent = oldText;
            if (tr) tr.removeAttribute("aria-busy");
          }
        });
      }

    });
  } catch (err) {
    console.error("❌ Error loading review orders:", err);
    const tbody = document.getElementById("pending-body");
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="7">Error loading orders: ${escapeHTML(err.message || String(err))}</td></tr>`;
    }
  }
}

// Try dedicated internal-PDF endpoint first; fallback to parameter on the standard one.
async function openInternalPdf(orderId, orderNumber) {
  try {
    // Primary: endpoint dedicated to PDF-with-projects (from review_orders router)
    let resp = await fetch(`/orders/api/generate_pdf_with_projects/${orderId}`);
    if (!resp.ok) {
      // Fallback: unified endpoint with include_projects flag (if you implement it)
      resp = await fetch(`/orders/api/generate_pdf_for_order/${orderId}?include_projects=1`);
    }
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

    const contentType = resp.headers.get('content-type') || '';
    if (!contentType.includes('application/pdf')) {
      const data = await resp.text().catch(() => "");
      throw new Error(`Unexpected response${data ? `: ${data}` : ""}`);
    }
    const blob = await resp.blob();
    if (!blob || blob.size === 0) throw new Error('Received empty PDF');

    showPDFModal(blob, orderId, orderNumber);
  } catch (err) {
    console.error("❌ Could not open internal PDF:", err);
    alert(`Could not open PDF: ${err.message || String(err)}`);
  }
}

function clearFilters() {
  const ids = ["start-date", "end-date", "filter-requester", "filter-supplier"];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (el.tagName === "SELECT") el.value = "All";
    else el.value = "";
  });
  loadOrders();
}

// Wire up
document.getElementById("run-btn")?.addEventListener("click", loadOrders);
document.getElementById("clear-btn")?.addEventListener("click", clearFilters);
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);

// Expose if needed
window.loadOrders = loadOrders;
window.showOrderNoteModal = showOrderNoteModal;
