import { expandLineItems } from "/static/js/components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "/static/js/components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "/static/js/components/order_note_modal.js";
import { loadRequesters, loadSuppliers } from "/static/js/components/shared_filters.js";

function populateDropdown(selectId, items, labelFunc, valueFunc) {
  const dropdown = document.getElementById(selectId);
  dropdown.innerHTML = `<option value="">All</option>`;
  items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = valueFunc(item);
    opt.textContent = labelFunc(item);
    dropdown.appendChild(opt);
  });
}

function escapeHTML(str) {
  if (!str) return "";
  return str.replace(/'/g, "\\'").replace(/"/g, "\\\"").replace(/</g, "<").replace(/>/g, ">").replace(/\n/g, " ").replace(/\r/g, "");
}

function populateTable(data) {
  const tbody = document.getElementById("received-body");
  tbody.innerHTML = "";

  if (!data.orders || data.orders.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 7;
    cell.textContent = "No received orders found.";
    return;
  }

  data.orders.forEach(order => {
    const row = tbody.insertRow();
    row.setAttribute("data-order-id", order.id);

    const sanitizedOrderNote = escapeHTML(order.order_note || "");
    const sanitizedSupplierNote = escapeHTML(order.note_to_supplier || "");
    const sanitizedOrderNumber = escapeHTML(order.order_number);
    const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
    const sanitizedRequester = escapeHTML(order.requester);

    row.innerHTML = `
      <td>${order.created_date}</td>
      <td>${sanitizedOrderNumber}</td>
      <td>${sanitizedRequester}</td>
      <td>${sanitizedSupplier}</td>
      <td>R${order.total.toFixed(2)}</td>
      <td>${order.status}</td>
      <td>
        <span class="expand-icon" onclick="window.expandLineItems(${order.id}, this)">⬇️</span>
        <span class="clip-icon" title="View/Upload Attachments" onclick="window.checkAttachments(${order.id}).then(has => has ? window.showViewAttachmentsModal(${order.id}, '${sanitizedOrderNumber}') : window.showUploadAttachmentsModal(${order.id}, '${sanitizedOrderNumber}', () => window.checkAttachments(${order.id}).then(has => this.classList.toggle('eye-icon', has))))">📎</span>
        <span class="note-icon" title="Edit Continuous Order Note" onclick="window.showOrderNoteModal('${sanitizedOrderNote}', ${order.id})">📝</span>
        <span class="supplier-note-icon" title="View Note to Supplier" onclick="try { window.showSupplierNoteModal('${sanitizedSupplierNote}'); } catch (e) { console.error('Failed to show supplier note for order ${order.order_number}:', e); alert('Error displaying supplier note: ' + e.message); }">📦</span>
      </td>
    `;
  });
}

async function loadFiltersAndOrders() {
  try {
    const [suppliersRes, requestersRes] = await Promise.all([
      fetch("/lookups/suppliers").then(res => res.json()),
      fetch("/lookups/requesters").then(res => res.json())
    ]);

    populateDropdown("filter-supplier", suppliersRes.suppliers, s => `${s.account_number} — ${s.name}`, s => s.name);
    populateDropdown("filter-requester", requestersRes.requesters, r => r.name, r => r.name);

    await runFilters();
  } catch (err) {
    console.error("Failed to load filters", err);
  }
}

async function runFilters() {
  const supplierName = document.getElementById("filter-supplier").value;
  const requesterName = document.getElementById("filter-requester").value;
  let startDate = document.getElementById("start-date").value;
  let endDate = document.getElementById("end-date").value;

  const isValidDate = (dateStr) => {
    if (!dateStr) return true;
    const date = new Date(dateStr);
    return !isNaN(date.getTime()) && dateStr === date.toISOString().split("T")[0];
  };

  if (startDate && !isValidDate(startDate)) {
    alert("Invalid start date. Please select a valid date.");
    return;
  }
  if (endDate && !isValidDate(endDate)) {
    alert("Invalid end date. Please select a valid date.");
    return;
  }

  const params = new URLSearchParams();
  if (supplierName) params.append("supplier", supplierName);
  if (requesterName) params.append("requester", requesterName);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  try {
    const res = await fetch(`/orders/api/received_orders?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();
    populateTable(data);
  } catch (err) {
    console.error("Failed to fetch received orders", err);
    alert("Failed to load orders: " + err.message);
  }
}

function clearFilters() {
  document.getElementById("filter-supplier").value = "";
  document.getElementById("filter-requester").value = "";
  document.getElementById("filter-status").value = "";
  document.getElementById("start-date").value = "";
  document.getElementById("end-date").value = "";
  runFilters();
}

document.addEventListener("DOMContentLoaded", () => {
  loadFiltersAndOrders();

  document.getElementById("run-btn").addEventListener("click", runFilters);
  document.getElementById("clear-btn").addEventListener("click", clearFilters);

  // Periodically refresh the received orders table every 30 seconds
  setInterval(runFilters, 30000);
});

window.expandLineItems = expandLineItems;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;