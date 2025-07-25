// File: /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/js/audit_trail.js

import { expandAuditTrailDetails } from "./audit_trail_expand.js"; 
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

// New function to format currency with thousand separators and 2 decimal places
function formatCurrency(amount) {
  if (amount == null) return "R0.00";
  return `R${parseFloat(amount).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

console.log("Loading audit_trail.js for improved display");

function escapeHTML(str = "") {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/\'/g, "&#39;");
}

async function loadAuditOrders() { 
  const params = new URLSearchParams();

  const statusFilter = document.getElementById("status-filter-test").value;
  const requesterFilter = document.getElementById("requester-filter-test").value;
  const supplierFilter = document.getElementById("supplier-filter-test").value;
  const startDateFilter = document.getElementById("start-date-filter-test").value;
  const endDateFilter = document.getElementById("end-date-filter-test").value;
  // ADD THIS LINE for order_number filter:
  const orderNumberFilter = document.getElementById("order-number-filter-test").value; 

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
  // ADD THIS BLOCK for order_number filter:
  if (orderNumberFilter) {
    params.append("order_number", orderNumberFilter);
  }

  try {
    const res = await fetch(`/orders/api/audit_trail_orders?${params.toString()}`); 
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const { orders = [] } = await res.json();

    const tbody = document.getElementById("audit-body-test");
    tbody.innerHTML = "";

    if (orders.length === 0) {
      tbody.innerHTML = "<div class='order-block' style='padding: 1rem; text-align: center; border: none; box-shadow: none;'>No orders found.</div>";
      return;
    }

    orders.forEach((order, idx) => {
      // Determine which date to show in the main list header
      const displayDate = escapeHTML(order.received_date && order.status === 'Received' ?
                                    new Date(order.received_date).toLocaleDateString("en-ZA") :
                                    (order.created_date ? new Date(order.created_date).toLocaleDateString("en-ZA") : "N/A"));

      const sanitizedNumber = escapeHTML(order.order_number || "");
      const sanitizedRequester = escapeHTML(order.requester || "N/A");
      const sanitizedSupplier  = escapeHTML(order.supplier  || "N/A");
      const sanitizedStatus    = escapeHTML(order.status    || "");
      const sanitizedTotal = formatCurrency(order.total);

      // --- START NEW STRUCTURE FOR BLUE RECTANGLE EFFECT ---
      const orderBlock = document.createElement("div");
      orderBlock.classList.add("order-block");
      orderBlock.dataset.orderId = order.id;

      const headerRowDiv = document.createElement("div");
      headerRowDiv.classList.add("order-block-header-row");
      headerRowDiv.innerHTML = `
        <div class="order-cell">${displayDate}</div>
        <div class="order-cell">${sanitizedNumber}</div>
        <div class="order-cell">${sanitizedSupplier}</div>
        <div class="order-cell">${sanitizedRequester}</div>
        <div class="order-cell order-cell-total">${sanitizedTotal}</div> 
        <div class="order-cell"><span class="status">${sanitizedStatus}</span></div>
        <div class="order-cell order-cell-actions">
          <span class="expand-icon"  title="Show order details"        data-id="${order.id}">⬇️</span>
          <span class="clip-icon"    title="View / add attachments" data-id="${order.id}" data-number="${sanitizedNumber}">📎</span>
          <span class="note-icon"    title="Edit order note"        data-id="${order.id}" data-note="${escapeHTML(order.order_note || "")}" id="order-note-test-${idx}">📝</span>
          <span class="supplier-note-icon" title="View note to supplier" data-note="${escapeHTML(order.note_to_supplier || "")}">📦</span>
          <span class="pdf-icon"     title="View purchase-order PDF" data-id="${order.id}" data-number="${sanitizedNumber}">📄</span>
        </div>`;
      
      orderBlock.appendChild(headerRowDiv);

      const detailRowDiv = document.createElement("div");
      detailRowDiv.id = `receipt-items-row-${order.id}`;
      detailRowDiv.classList.add("order-block-detail-row");
      detailRowDiv.style.display = "none";
      orderBlock.appendChild(detailRowDiv);

      tbody.appendChild(orderBlock);

      /* --- per-row handlers (re-using existing modal functions) --- */
      headerRowDiv.querySelector(".expand-icon").onclick = async (e) => {
          // CHANGED: Call the dedicated expandAuditTrailDetails
          await expandAuditTrailDetails(order.id, e.target, detailRowDiv);
      };

      headerRowDiv.querySelector(".clip-icon").onclick = async (e) => {
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

      headerRowDiv.querySelector(`#order-note-test-${idx}`).onclick = (e) =>
        showOrderNoteModal(order.order_note || "", order.id, (newNote) =>
          e.target.setAttribute("data-note", escapeHTML(newNote))
        );

      headerRowDiv.querySelector(".supplier-note-icon").onclick = () =>
        showSupplierNoteModal(order.note_to_supplier || "");

      const currentOrderId = order.id;
      const currentOrderNumber = sanitizedNumber;

      headerRowDiv.querySelector(".pdf-icon").addEventListener("click", async () => {
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
    console.error("❌ Error loading audit trail orders:", err);
    alert(`Failed to load audit trail orders: ${err.message}`);
  }
}

/* ---------- bootstrap for audit trail screen ---------- */
window.addEventListener("DOMContentLoaded", async () => {
  // Populate filter dropdowns
  await loadRequesters("requester-filter-test"); 
  await loadSuppliers("supplier-filter-test");   
  
  loadAuditOrders(); // Initial load of orders

  // Add event listeners for filter buttons
  const runButton = document.getElementById("run-filter-btn-test");
  if (runButton) {
    runButton.addEventListener("click", loadAuditOrders); 
  } else { // Added this else block for debugging purposes
    console.error('Run button with ID "run-filter-btn-test" not found!');
  }

  const clearButton = document.getElementById("clear-filter-btn-test");
  if (clearButton) {
    clearButton.addEventListener("click", () => {
      // Reset all filter dropdowns and date inputs to "All" or empty
      document.getElementById("status-filter-test").value = "All";
      document.getElementById("requester-filter-test").value = "All";
      document.getElementById("supplier-filter-test").value = "All";
      document.getElementById("start-date-filter-test").value = "";
      document.getElementById("end-date-filter-test").value = "";
      // ADD THIS LINE for order_number filter:
      document.getElementById("order-number-filter-test").value = ""; 
      loadAuditOrders(); // Reload orders with cleared filters
    });
  } else { // Added this else block for debugging purposes
    console.error('Clear button with ID "clear-filter-btn-test" not found!');
  }
});

// Expose functions for potential debugging or future needs if modals rely on window scope
// REMOVED: expandLineItemsWithReceipts export/assignment as it's no longer the primary expander here
window.showUploadAttachmentsModal  = showUploadAttachmentsModal;
window.checkAttachments            = checkAttachments;
window.showViewAttachmentsModal    = showViewAttachmentsModal;
window.showOrderNoteModal          = showOrderNoteModal;
window.showSupplierNoteModal       = showSupplierNoteModal;