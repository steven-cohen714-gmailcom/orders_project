// File: frontend/static/js/draft_orders_main.js

import { loadRequesters, loadSuppliers } from './components/shared_filters.js';
// We'll reuse expandLineItems from the existing components, though it might need slight adaptation
// if draft_order_items differ significantly (which in our plan, they don't).
import { expandLineItems } from './components/expand_line_items.js'; 

console.log("📝 draft_orders_main.js loaded");

// New function to format currency with thousand separators and 2 decimal places
function formatCurrency(amount) {
  if (amount == null) return "R0.00";
  return `R${parseFloat(amount).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function escapeHTML(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

async function loadFiltersAndDraftOrders() {
  try {
    console.log("Loading filters for draft orders...");
    await Promise.all([
      loadRequesters("filter-requester"),
      loadSuppliers("filter-supplier")
    ]);
    console.log("Filters loaded successfully");
    await loadDraftOrders();
  } catch (error) {
    console.error("Error loading filters or draft orders:", error);
    document.getElementById("draft-orders-body").innerHTML = '<tr><td colspan="6">Error loading filters: ' + escapeHTML(error.message) + '</td></tr>';
  }
}

async function loadDraftOrders() {
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;
  const requester = document.getElementById("filter-requester").value;
  const supplier = document.getElementById("filter-supplier").value;

  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);
  if (requester && requester !== "All") params.append("requester", requester);
  if (supplier && supplier !== "All") params.append("supplier", supplier);

  try {
    console.log("Fetching draft orders with params:", params.toString());
    const res = await fetch(`/draft_orders/pending?${params.toString()}`); // Use the new endpoint
    if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}, Message: ${await res.text()}`);
    const data = await res.json();

    const tbody = document.getElementById("draft-orders-body");
    tbody.innerHTML = "";

    if (data.draft_orders && Array.isArray(data.draft_orders) && data.draft_orders.length > 0) {
      data.draft_orders.forEach((order) => {
        const row = document.createElement("tr");
        const sanitizedOrderNumber = escapeHTML(order.order_number || "");
        const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
        const sanitizedRequester = escapeHTML(order.requester || "N/A");
        const sanitizedDate = escapeHTML(order.created_date || "");
        const sanitizedTotal = formatCurrency(order.total);

        row.innerHTML = `
          <td>${sanitizedDate}</td>
          <td>${sanitizedOrderNumber}</td>
          <td>${sanitizedRequester}</td>
          <td>${sanitizedSupplier}</td>
          <td>${sanitizedTotal}</td>
          <td>
            <span class="expand-icon" data-order-id="${order.id}">⬇️</span>
            <button class="edit-draft-btn" data-draft-id="${order.id}">✏️ Edit</button>
            <button class="delete-draft-btn" data-draft-id="${order.id}">🗑️ Delete</button>
          </td>
        `;
        tbody.appendChild(row);

        // Create the detailRow and detailContainer for expanding line items
        const detailRow = document.createElement('tr');
        detailRow.className = 'expanded-details-row';
        const detailCell = document.createElement('td');
        detailCell.colSpan = 6; // Adjust colspan to match table columns
        const detailContainer = document.createElement('div');
        detailContainer.id = `detail-container-${order.id}`;
        detailContainer.style.display = 'none'; // Initially hidden
        detailCell.appendChild(detailContainer);
        detailRow.appendChild(detailCell);
        tbody.appendChild(detailRow);

        // Attach event listeners
        row.querySelector(".expand-icon").addEventListener("click", (e) => {
          if (!order.id) {
            console.error("No order ID provided for expanding line items");
            alert("Cannot expand line items: No order ID available");
            return;
          }
          // The expandLineItems function expects order_id and target. 
          // We need to pass the detailContainer as the third argument for it to insert content.
          // The fourth argument (the order object itself) is not used by expandLineItems directly, 
          // but expandLineItemsWithReceipts does expect it, so we stick with the former.
          expandLineItems(order.id, e.target, detailContainer, order); // Pass order for consistency if expandLineItems is a shared one
        });

        row.querySelector(".edit-draft-btn").addEventListener("click", () => {
          // Navigate to new_order page with draft ID
          window.location.href = `/orders/new?draft_id=${order.id}`;
        });

        row.querySelector(".delete-draft-btn").addEventListener("click", async () => {
          if (confirm(`Are you sure you want to delete draft order ${sanitizedOrderNumber}? This action cannot be undone.`)) {
            try {
              const deleteRes = await fetch(`/draft_orders/${order.id}`, { method: "DELETE" }); // Use new endpoint
              if (!deleteRes.ok) throw new Error(`Failed to delete draft: ${deleteRes.status} - ${await deleteRes.text()}`);
              alert(`✅ Draft order ${sanitizedOrderNumber} deleted successfully.`);
              loadDraftOrders(); // Reload the list after deletion
            } catch (error) {
              console.error("Error deleting draft order:", error);
              alert(`❌ Failed to delete draft order: ${error.message}`);
            }
          }
        });
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="6">No draft orders found.</td></tr>';
    }
  } catch (error) {
    console.error("Error loading draft orders:", error);
    document.getElementById("draft-orders-body").innerHTML = '<tr><td colspan="6">Error loading draft orders: ' + escapeHTML(error.message) + '</td></tr>';
  }
}

function clearFilters() {
  document.getElementById("start-date").value = "";
  document.getElementById("end-date").value = "";
  document.getElementById("filter-requester").value = "All";
  document.getElementById("filter-supplier").value = "All";
  loadDraftOrders();
}

document.getElementById("run-btn").addEventListener("click", loadDraftOrders);
document.getElementById("clear-btn").addEventListener("click", clearFilters);
document.addEventListener("DOMContentLoaded", loadFiltersAndDraftOrders);

// Expose functions to the window if they are needed by other modules that don't use imports
// window.expandLineItems = expandLineItems; // Not strictly needed if imported where usedx