// File: frontend/static/js/audit_trail.js
// Relative Path: frontend/static/js/audit_trail.js
import { escapeHTML, formatCurrency, formatYMD } from "./components/utils.js";
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
import {
  loadRequesters,
  loadSuppliers,
  loadStatuses,
  normaliseStatus,
} from "./components/shared_filters.js";

console.log("Loading audit_trail.js (summary view: one row per order number)");

function toZA(dateStr) {
  if (!dateStr) return null;
  try {
    return new Date(dateStr).toLocaleString("en-ZA", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return null;
  }
}

async function loadAuditOrders() {
  const params = new URLSearchParams();

  const statusFilter = document.getElementById("status-filter-test")?.value || "All";
  const requesterFilter = document.getElementById("requester-filter-test")?.value || "All";
  const supplierFilter = document.getElementById("supplier-filter-test")?.value || "All";
  const startDateFilter = document.getElementById("start-date-filter-test")?.value || "";
  const endDateFilter = document.getElementById("end-date-filter-test")?.value || "";
  const orderNumberFilter = document.getElementById("order-number-filter-test")?.value || "";

  const canonStatus = normaliseStatus(statusFilter);
  if (canonStatus && canonStatus.toLowerCase() !== "all") {
    params.append("status", canonStatus);
  }
  if (requesterFilter && requesterFilter.toLowerCase() !== "all") {
    params.append("requester", requesterFilter);
  }
  if (supplierFilter && supplierFilter.toLowerCase() !== "all") {
    params.append("supplier", supplierFilter);
  }
  if (startDateFilter) params.append("start_date", startDateFilter);
  if (endDateFilter) params.append("end_date", endDateFilter);
  if (orderNumberFilter) params.append("order_number", orderNumberFilter);

  try {
    // Summary endpoint (one row per order_number)
    const res = await fetch(`/orders/api/audit_summary?${params.toString()}`, {
      credentials: "same-origin",
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);

    const { orders = [] } = await res.json();
    const tbody = document.getElementById("audit-body-test");
    if (!tbody) {
      console.error("#audit-body-test not found");
      return;
    }
    tbody.innerHTML = "";

    if (orders.length === 0) {
      tbody.innerHTML =
        "<div class='order-block' style='padding: 1rem; text-align: center; border: none; box-shadow: none;'>No orders found.</div>";
      return;
    }

    orders.forEach((order, idx) => {
      // From summary API:
      // - order.latest_order_id (use this for actions)
      // - order.order_number, order.supplier, order.requester, order.total
      // - order.latest_status, order.latest_created_date
      // - order.created_at, order.edited_at, order.finalised_at
      const latestId = order.latest_order_id;

      // Date column: use created_at if available, otherwise latest_created_date
      const createdAt = order.created_at || order.latest_created_date || null;

      // IMPORTANT: do NOT escape the date (escapeHTML encodes '/')
      const displayDate = createdAt
        ? new Date(createdAt).toLocaleDateString("en-ZA")
        : "N/A";

      const sanitizedNumber = escapeHTML(order.order_number || "");
      const sanitizedRequester = escapeHTML(order.requester || "N/A");
      const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
      const sanitizedStatus = escapeHTML(order.latest_status || "");
      const sanitizedTotal = formatCurrency(order.total);

      const statusUp = String(order.latest_status || "").toUpperCase();
      const CAN_DELETE = window.currentUser?.can_delete_transactions === 1;

      // Only show Delete icon if NOT already Deleted
      const deleteIconHTML =
        statusUp === "DELETED"
          ? ""
          : CAN_DELETE
          ? `<span class="delete-icon" title="Delete order" data-id="${latestId}" data-number="${sanitizedNumber}">🗑️</span>`
          : `<span class="delete-icon disabled" title="No permission">🗑️</span>`;

      // --- structure: one block per order ---
      const orderBlock = document.createElement("div");
      orderBlock.classList.add("order-block");
      orderBlock.dataset.orderId = latestId;

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
          <span class="expand-icon"  title="Show order details" data-id="${latestId}">⬇️</span>
          <span class="clip-icon"    title="View / add attachments" data-id="${latestId}" data-number="${sanitizedNumber}">📎</span>
          <span class="note-icon"    title="Edit order note" data-id="${latestId}" data-note="${escapeHTML(
            order.order_note || ""
          )}" id="order-note-test-${idx}">📝</span>
          <span class="supplier-note-icon" title="View note to supplier" data-note="${escapeHTML(
            order.note_to_supplier || ""
          )}">📦</span>
          ${deleteIconHTML}
          <span class="pdf-icon"     title="View purchase-order PDF" data-id="${latestId}" data-number="${sanitizedNumber}">📄</span>
        </div>`;

      orderBlock.appendChild(headerRowDiv);

      // Timeline row (Created · Edited · Finalised)
      const timelineDiv = document.createElement("div");
      timelineDiv.classList.add("order-block-timeline");
      const c = toZA(order.created_at);
      const e = toZA(order.edited_at);
      const f = toZA(order.finalised_at);
      const bits = [];
      // IMPORTANT: don't escape these; we're using textContent (no HTML parsing)
      if (c) bits.push(`Created: ${c}`);
      if (e) bits.push(`Edited: ${e}`);
      if (f) bits.push(`Finalised: ${f}`);
      timelineDiv.style.fontSize = "0.9rem";
      timelineDiv.style.color = "#555";
      timelineDiv.style.margin = "0.25rem 0 0.5rem 0";
      timelineDiv.textContent = bits.length ? bits.join(" · ") : " ";
      orderBlock.appendChild(timelineDiv);

      const detailRowDiv = document.createElement("div");
      detailRowDiv.id = `receipt-items-row-${latestId}`;
      detailRowDiv.classList.add("order-block-detail-row");
      detailRowDiv.style.display = "none";
      orderBlock.appendChild(detailRowDiv);

      tbody.appendChild(orderBlock);

      // --- Handlers ---
      headerRowDiv.querySelector(".expand-icon").onclick = async (e) => {
        await expandAuditTrailDetails(latestId, e.target, detailRowDiv);
      };

      headerRowDiv.querySelector(".clip-icon").onclick = async (e) => {
        const tgt = e.target;
        const id = latestId;
        const num = sanitizedNumber;
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
        showOrderNoteModal(order.order_note || "", latestId, (newNote) =>
          e.target.setAttribute("data-note", escapeHTML(newNote))
        );

      headerRowDiv.querySelector(".supplier-note-icon").onclick = () =>
        showSupplierNoteModal(order.note_to_supplier || "");

      // Delete icon handler (Audit Trail only)
      const delBtn = headerRowDiv.querySelector(`.delete-icon[data-id="${latestId}"]`);
      if (CAN_DELETE && delBtn) {
        delBtn.addEventListener("click", async () => {
          const num = delBtn.getAttribute("data-number") || latestId;
          if (
            !confirm(
              `Delete order ${num}? This will mark it as Deleted and remove it from all screens except Audit Trail.`
            )
          ) {
            return;
          }
          try {
            const resp = await fetch(`/orders/delete/${latestId}`, {
              method: "DELETE",
              credentials: "same-origin",
            });
            if (!resp.ok) {
              const t = await resp.text();
              throw new Error(`HTTP ${resp.status}: ${t}`);
            }
            await loadAuditOrders(); // refresh view
          } catch (e) {
            alert(`❌ Could not delete: ${e.message}`);
            console.error(e);
          }
        });
      }

      // PDF handler
      headerRowDiv.querySelector(".pdf-icon").addEventListener("click", async () => {
        try {
          const resp = await fetch(`/orders/api/generate_pdf_with_projects/${latestId}`, {
            credentials: "same-origin",
          });
        } catch {}
        try {
          const resp = await fetch(`/orders/api/generate_pdf_with_projects/${latestId}`, {
            credentials: "same-origin",
          });
          if (!resp.ok) throw new Error(`PDF generation failed with status ${resp.status}`);

          const contentType = resp.headers.get("content-type");
          if (contentType && contentType.includes("application/pdf")) {
            const blob = await resp.blob();
            if (blob.size === 0) throw new Error("Received empty PDF file");
            showPDFModal(blob, latestId, sanitizedNumber);
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
  loadStatuses("status-filter-test", { context: "audit" });

  // Initial load
  loadAuditOrders();

  // Filter buttons
  const runButton = document.getElementById("run-filter-btn-test");
  if (runButton) {
    runButton.addEventListener("click", loadAuditOrders);
  } else {
    console.error('Run button with ID "run-filter-btn-test" not found!');
  }

  const clearButton = document.getElementById("clear-filter-btn-test");
  if (clearButton) {
    clearButton.addEventListener("click", () => {
      document.getElementById("status-filter-test").value = "All";
      document.getElementById("requester-filter-test").value = "All";
      document.getElementById("supplier-filter-test").value = "All";
      document.getElementById("start-date-filter-test").value = "";
      document.getElementById("end-date-filter-test").value = "";
      document.getElementById("order-number-filter-test").value = "";
      loadAuditOrders();
    });
  } else {
    console.error('Clear button with ID "clear-filter-btn-test" not found!');
  }
});

// Expose some functions if needed elsewhere
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;
