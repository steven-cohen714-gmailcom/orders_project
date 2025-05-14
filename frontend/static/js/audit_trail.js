import { expandLineItemsWithReceipts } from "/static/js/components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "/static/js/components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "/static/js/components/order_note_modal.js";
import { loadRequesters, loadSuppliers } from "/static/js/components/shared_filters.js";

function escapeHTML(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&")
    .replace(/</g, "<")
    .replace(/>/g, ">")
    .replace(/"/g, "\"")
    .replace(/'/g, "\'");
}

async function loadFiltersAndOrders() {
  try {
    await loadRequesters("filter-requester");
    await loadSuppliers("filter-supplier");
    await loadOrders();
  } catch (err) {
    console.error("❌ Failed to load filters or orders:", err);
    document.getElementById("audit-body").innerHTML = `<tr><td colspan="7">Error loading filters: ${escapeHTML(err.message)}</td></tr>`;
  }
}

async function loadOrders() {
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;
  const requester = document.getElementById("filter-requester").value;
  const supplier = document.getElementById("filter-supplier").value;
  const status = document.getElementById("filter-status").value;

  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);
  if (requester && requester !== "All") params.append("requester", requester);
  if (supplier && supplier !== "All") params.append("supplier", supplier);
  if (status && status !== "All") params.append("status", status);

  try {
    const res = await fetch(`/orders/api/audit_trail_orders?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();

    const tbody = document.getElementById("audit-body");
    tbody.innerHTML = "";

    if (data.orders && Array.isArray(data.orders) && data.orders.length > 0) {
      data.orders.forEach((order, index) => {
        const row = document.createElement("tr");
        const sanitizedOrderNote = escapeHTML(order.order_note || "");
        const sanitizedSupplierNote = escapeHTML(order.note_to_supplier || "");
        const sanitizedOrderNumber = escapeHTML(order.order_number);
        const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
        const sanitizedRequester = escapeHTML(order.requester);
        const sanitizedDate = escapeHTML(order.created_date || "");
        const sanitizedTotal = order.total != null ? `R${parseFloat(order.total).toFixed(2)}` : "R0.00";
        const sanitizedStatus = escapeHTML(order.status || "");

        row.innerHTML = `
          <td>${sanitizedDate}</td>
          <td>${sanitizedOrderNumber}</td>
          <td>${sanitizedRequester}</td>
          <td>${sanitizedSupplier}</td>
          <td>${sanitizedTotal}</td>
          <td><span class="status">${sanitizedStatus}</span></td>
          <td>
            <span class="expand-icon" style="cursor:pointer" title="View Line Items">⬇️</span>
            <span class="clip-icon" style="cursor:pointer" title="View/Upload Attachments">📎</span>
            <span class="note-icon" style="cursor:pointer" title="Edit Order Note">📝</span>
            <span class="supplier-note-icon" style="cursor:pointer" title="View Note to Supplier">📦</span>
          </td>`;

        tbody.appendChild(row);

        row.querySelector(".expand-icon").addEventListener("click", (e) => {
          expandLineItemsWithReceipts(order.id, e.target);
        });

        row.querySelector(".clip-icon").addEventListener("click", async (e) => {
          const target = e.target;
          const has = await checkAttachments(order.id);
          if (has) {
            showViewAttachmentsModal(order.id, sanitizedOrderNumber);
          } else {
            showUploadAttachmentsModal(order.id, sanitizedOrderNumber, async () => {
              const newHas = await checkAttachments(order.id);
              target.classList.toggle("eye-icon", newHas);
            });
          }
        });

        row.querySelector(".note-icon").addEventListener("click", (e) => {
          const target = e.target;
          showOrderNoteModal(sanitizedOrderNote, order.id, (newNote) => {
            target.setAttribute("data-order-note", escapeHTML(newNote));
          });
        });

        row.querySelector(".supplier-note-icon").addEventListener("click", () => {
          try {
            showSupplierNoteModal(sanitizedSupplierNote);
          } catch (e) {
            console.error(`Failed to show supplier note for order ${sanitizedOrderNumber}:`, e);
            alert(`Error displaying supplier note: ${e.message}`);
          }
        });
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="7">No audit trail orders found.</td></tr>';
    }
  } catch (err) {
    console.error("❌ Error loading audit trail orders:", err);
    document.getElementById("audit-body").innerHTML = `<tr><td colspan="7">Error loading orders: ${escapeHTML(err.message)}</td></tr>`;
  }
}

function clearFilters() {
  document.getElementById("start-date").value = "";
  document.getElementById("end-date").value = "";
  document.getElementById("filter-requester").value = "All";
  document.getElementById("filter-supplier").value = "All";
  document.getElementById("filter-status").value = "All";
  loadOrders();
}

document.getElementById("run-btn").addEventListener("click", loadOrders);
document.getElementById("clear-btn").addEventListener("click", clearFilters);
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);

window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;
