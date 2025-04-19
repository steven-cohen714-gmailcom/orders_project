import { setDateInputFormat } from "/static/js/date_utils.js";

function populateDropdown(selectId, items, labelFunc) {
  const dropdown = document.getElementById(selectId);
  dropdown.innerHTML = `<option value="">All</option>`;
  items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = item.id;
    opt.textContent = labelFunc(item);
    dropdown.appendChild(opt);
  });
}

function populateTable(data) {
  const tbody = document.getElementById("pending-body");
  tbody.innerHTML = "";

  if (!data.orders || data.orders.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 7;
    cell.textContent = "No pending orders found.";
    return;
  }

  data.orders.forEach(order => {
    const row = tbody.insertRow();
    row.innerHTML = `
      <td>${order.request_date}</td>
      <td>${order.order_number}</td>
      <td>${order.requester}</td>
      <td>${order.supplier}</td>
      <td>R${order.total_value.toFixed(2)}</td>
      <td>${order.status}</td>
      <td><button onclick="alert('Expand feature coming soon')">⬇️</button></td>
    `;
  });
}

async function loadFiltersAndOrders() {
  try {
    const [suppliersRes, requestersRes] = await Promise.all([
      fetch("/lookups/suppliers").then(res => res.json()),
      fetch("/lookups/requesters").then(res => res.json())
    ]);

    populateDropdown("filter-supplier", suppliersRes.suppliers, s => `${s.account_number} — ${s.name}`);
    populateDropdown("filter-requester", requestersRes.requesters, r => r.name);

    runFilters();
  } catch (err) {
    console.error("Failed to load filters", err);
  }
}

async function runFilters() {
  const supplierId = document.getElementById("filter-supplier").value;
  const requesterId = document.getElementById("filter-requester").value;
  const status = document.getElementById("filter-status").value;
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;

  const params = new URLSearchParams();
  if (supplierId) params.append("supplier_id", supplierId);
  if (requesterId) params.append("requester_id", requesterId);
  if (status) params.append("status", status);
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  try {
    const res = await fetch(`/orders/pending?${params.toString()}`);
    const data = await res.json();
    populateTable(data);
  } catch (err) {
    console.error("Failed to fetch filtered orders", err);
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
  setDateInputFormat("start-date");
  setDateInputFormat("end-date");
  loadFiltersAndOrders();

  document.getElementById("run-filters").addEventListener("click", runFilters);
  document.getElementById("clear-filters").addEventListener("click", clearFilters);
});

