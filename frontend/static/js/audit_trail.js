// /static/js/audit_trail.js
import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { expandLineItemsWithReceipts } from "./components/expand_line_items.js";
import {
  showUploadAttachmentsModal,
  checkAttachments,
  showViewAttachmentsModal,
} from "./components/attachment_modal.js";
import {
  showOrderNoteModal,
  showSupplierNoteModal,
} from "./components/order_note_modal.js";
import { showPDFModal } from "./components/pdf_modal.js";

console.log("Loading audit_trail.js");

function escapeHTML(str = "") {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/\'/g, "&#39;");
}

async function loadAuditOrders() {
  const startDate  = document.getElementById("start-date").value;
  const endDate    = document.getElementById("end-date").value;
  const requester  = document.getElementById("filter-requester").value;
  const supplier   = document.getElementById("filter-supplier").value;
  const status     = document.getElementById("filter-status").value;

  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate)   params.append("end_date", endDate);
  if (requester && requester !== "All") params.append("requester", requester);
  if (supplier  && supplier  !== "All") params.append("supplier", supplier);
  if (status    && status    !== "All") params.append("status", status);

  try {
    const res = await fetch(`/orders/api/audit_trail_orders?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const { orders = [] } = await res.json();

    const tbody = document.getElementById("audit-body");
    tbody.innerHTML = "";

    if (orders.length === 0) {
      tbody.innerHTML = "<tr><td colspan='8'>No orders found.</td></tr>";
      return;
    }

    orders.forEach((order, idx) => {
      const sanitizedDate = escapeHTML((order.created_date || "").split(" ")[0]); // date-only
      const sanitizedNumber = escapeHTML(order.order_number || "");
      const sanitizedRequester = escapeHTML(order.requester || "N/A");
      const sanitizedSupplier  = escapeHTML(order.supplier  || "N/A");
      const sanitizedStatus    = escapeHTML(order.status    || "");
      const sanitizedUser      = escapeHTML(order.audit_user || "N/A");
      const sanitizedTotal     = order.total != null ? `R${parseFloat(order.total).toFixed(2)}` : "R0.00";
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${sanitizedDate}</td>
        <td>${sanitizedNumber}</td>
        <td>${sanitizedRequester}</td>
        <td>${sanitizedSupplier}</td>
        <td>${sanitizedTotal}</td>
        <td><span class="status">${sanitizedStatus}</span></td>
        <td>${sanitizedUser}</td>
        <td>
          <span class="expand-icon"  title="Show line-items"        data-id="${order.id}">⬇️</span>
          <span class="clip-icon"    title="View / add attachments" data-id="${order.id}" data-number="${sanitizedNumber}">📎</span>
          <span class="note-icon"    title="Edit order note"        data-id="${order.id}" data-note="${escapeHTML(order.order_note || "")}" id="order-note-${idx}">📝</span>
          <span class="supplier-note-icon" title="View note to supplier" data-note="${escapeHTML(order.note_to_supplier || "")}">📦</span>
          <span class="pdf-icon"     title="View purchase-order PDF" data-id="${order.id}" data-number="${sanitizedNumber}">📄</span>
        </td>`;

      tbody.appendChild(row);

      /* --- per-row handlers --- */
      row.querySelector(".expand-icon").onclick = (e) =>
        expandLineItemsWithReceipts(order.id, e.target);

      row.querySelector(".clip-icon").onclick = async (e) => {
        const tgt = e.target, id = order.id, num = sanitizedNumber;
        const has = await checkAttachments(id);
        if (has) {
          showViewAttachmentsModal(id, num);
        } else {
          showUploadAttachmentsModal(id, num, async () => {
            if (await checkAttachments(id)) tgt.classList.toggle("eye-icon", true);
          });
        }
      };

      row.querySelector(".note-icon").onclick = (e) =>
        showOrderNoteModal(order.order_note || "", order.id, (newNote) =>
          e.target.setAttribute("data-note", escapeHTML(newNote))
        );

      row.querySelector(".supplier-note-icon").onclick = () =>
        showSupplierNoteModal(order.note_to_supplier || "");

      row.querySelector(".pdf-icon").onclick = async () => {
        try {
          const resp = await fetch(`/orders/api/generate_pdf_for_order/${order.id}`);
          if (!resp.ok) throw new Error(`PDF failed: ${resp.status}`);
          const blob = await resp.blob();
          if (!blob.size) throw new Error("Received empty PDF");
          showPDFModal(blob);
        } catch (err) {
          alert(`❌ Could not generate PDF (${err.message})`);
        }
      };
    });
  } catch (err) {
    console.error("❌ Error loading audit trail:", err);
    alert(`Failed to load orders: ${err.message}`);
  }
}

function clearFilters() {
  ["start-date", "end-date"].forEach((id) => (document.getElementById(id).value = ""));
  ["filter-requester", "filter-supplier", "filter-status"].forEach(
    (id) => (document.getElementById(id).value = "All")
  );
  loadAuditOrders();
}

/* ---------- bootstrap ---------- */
window.addEventListener("DOMContentLoaded", async () => {
  await Promise.all([
    loadRequesters("filter-requester"),
    loadSuppliers("filter-supplier"),
  ]);

  document.getElementById("run-btn").onclick   = loadAuditOrders;
  document.getElementById("clear-btn").onclick = clearFilters;

  loadAuditOrders(); // initial fill
});

/* expose for other modules if needed */
window.expandLineItemsWithReceipts = expandLineItemsWithReceipts;
window.showUploadAttachmentsModal  = showUploadAttachmentsModal;
window.checkAttachments            = checkAttachments;
window.showViewAttachmentsModal    = showViewAttachmentsModal;
window.showOrderNoteModal          = showOrderNoteModal;
window.showSupplierNoteModal       = showSupplierNoteModal;
