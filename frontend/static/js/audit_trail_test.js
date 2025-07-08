// File: frontend/static/js/audit_trail_test.js
// For audit trail test only

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
// Re-using shared filter functions from existing components
import { loadRequesters, loadSuppliers } from "./components/shared_filters.js"; 

console.log("Loading audit_trail_test.js (for audit trail test only)");

function escapeHTML(str = "") {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/\'/g, "&#39;");
}

async function loadAuditTestOrders() {
  const params = new URLSearchParams();

  // Get filter values from the HTML elements (using the new test IDs)
  const statusFilter = document.getElementById("status-filter-test").value;
  const requesterFilter = document.getElementById("requester-filter-test").value;
  const supplierFilter = document.getElementById("supplier-filter-test").value;
  const startDateFilter = document.getElementById("start-date-filter-test").value;
  const endDateFilter = document.getElementById("end-date-filter-test").value;

  // Append parameters if they are not "All" or empty
  if (statusFilter && statusFilter.toLowerCase() !== "all") {
    params.append("status", statusFilter);
  }
  if (requesterFilter && requesterFilter.toLowerCase() !== "all") {
    params.append("requester", requesterFilter);
  }
  if (supplierFilter && supplierFilter.toLowerCase() !== "all") {
    params.append("supplier", supplierFilter);
  }
  if (startDateFilter) {
    params.append("start_date", startDateFilter);
  }
  if (endDateFilter) {
    params.append("end_date", endDateFilter);
  }

  try {
    // Call the new dedicated backend endpoint for the test
    const res = await fetch(`/api/audit_trail_test_orders?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const { orders = [] } = await res.json();

    const tbody = document.getElementById("audit-body-test"); // Using new test ID
    tbody.innerHTML = "";

    if (orders.length === 0) {
      tbody.innerHTML = "<tr><td colspan='8'>No orders found.</td></tr>";
      return;
    }

    orders.forEach((order, idx) => {
      const sanitizedDate = escapeHTML(order.created_date ?
        new Date(order.created_date).toLocaleDateString("en-ZA") : "N/A");
      const sanitizedNumber = escapeHTML(order.order_number || "");
      const sanitizedRequester = escapeHTML(order.requester || "N/A");
      const sanitizedSupplier  = escapeHTML(order.supplier  || "N/A");
      const sanitizedStatus    = escapeHTML(order.status    || "");
      const sanitizedUser      = escapeHTML(order.audit_user_for_test_only || "N/A"); // Using placeholder from backend
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
          <span class="note-icon"    title="Edit order note"        data-id="${order.id}" data-note="${escapeHTML(order.order_note || "")}" id="order-note-test-${idx}">📝</span>
          <span class="supplier-note-icon" title="View note to supplier" data-note="${escapeHTML(order.note_to_supplier || "")}">📦</span>
          <span class="pdf-icon"     title="View purchase-order PDF" data-id="${order.id}" data-number="${sanitizedNumber}">📄</span>
        </td>`;
      tbody.appendChild(row);

      /* --- per-row handlers (re-using existing modal functions) --- */
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

      // Note icon uses a unique ID to avoid conflict with main audit_trail.js
      row.querySelector(`#order-note-test-${idx}`).onclick = (e) => 
        showOrderNoteModal(order.order_note || "", order.id, (newNote) =>
          e.target.setAttribute("data-note", escapeHTML(newNote))
        );

      row.querySelector(".supplier-note-icon").onclick = () =>
        showSupplierNoteModal(order.note_to_supplier || "");

      const currentOrderId = order.id;
      const currentOrderNumber = sanitizedNumber;

      row.querySelector(".pdf-icon").addEventListener("click", async () => {
        try {
          const resp = await fetch(`/orders/api/generate_pdf_for_order/${currentOrderId}`);
          if (!resp.ok) throw new Error(`PDF generation failed with status ${resp.status}`);

          const contentType = resp.headers.get('content-type');
          if (contentType && contentType.includes('application/pdf')) {
            const blob = await resp.blob();
            if (blob.size === 0) {
              throw new Error('Received empty PDF file');
            }
            showPDFModal(blob, currentOrderId, currentOrderNumber);
          } else {
            const data = await resp.json(); 
            throw new Error(`Unexpected response: ${JSON.stringify(data)}`);
          }
        } catch (err) {
          alert(`❌ Could not generate PDF (${err.message})`);
          console.error(err);
        }
      });
    });
  } catch (err) {
    console.error("❌ Error loading audit trail test orders:", err);
    alert(`Failed to load audit trail test orders: ${err.message}`);
  }
}

/* ---------- bootstrap for test screen ---------- */
window.addEventListener("DOMContentLoaded", async () => {
  // Populate filter dropdowns using existing functions (new IDs)
  await loadRequesters("requester-filter-test"); 
  await loadSuppliers("supplier-filter-test");   
  
  loadAuditTestOrders(); // Initial load

  // Add event listeners for filter buttons (new IDs)
  const runButton = document.getElementById("run-filter-btn-test");
  if (runButton) {
    runButton.addEventListener("click", loadAuditTestOrders);
  }

  const clearButton = document.getElementById("clear-filter-btn-test");
  if (clearButton) {
    clearButton.addEventListener("click", () => {
      // Reset all filter dropdowns and date inputs to "All" or empty (new IDs)
      document.getElementById("status-filter-test").value = "All";
      document.getElementById("requester-filter-test").value = "All";
      document.getElementById("supplier-filter-test").value = "All";
      document.getElementById("start-date-filter-test").value = "";
      document.getElementById("end-date-filter-test").value = "";
      loadAuditTestOrders(); // Reload orders with cleared filters
    });
  }
});

// Expose functions for potential debugging or future needs if modals rely on window scope
window.expandLineItemsWithReceipts = expandLineItemsWithReceipts;
window.showUploadAttachmentsModal  = showUploadAttachmentsModal;
window.checkAttachments            = checkAttachments;
window.showViewAttachmentsModal    = showViewAttachmentsModal;
window.showOrderNoteModal          = showOrderNoteModal;
window.showSupplierNoteModal       = showSupplierNoteModal;