// File: frontend/static/js/draft_orders_main.js

import { loadRequesters, loadSuppliers } from './components/shared_filters.js';
// We will NOT reuse expandLineItems from expand_line_items.js directly for drafts,
// as its API call is specific to final orders. We'll implement the expansion here.
// import { expandLineItems } from './components/expand_line_items.js';

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
    const res = await fetch(`/draft_orders/pending?${params.toString()}`);
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

        // Attach event listeners for expand icon
        row.querySelector(".expand-icon").addEventListener("click", (e) => {
          if (!order.id) {
            console.error("No order ID provided for expanding line items");
            alert("Cannot expand line items: No order ID available");
            return;
          }
          // NEW: Call a local function to expand draft line items
          expandDraftLineItems(order.id, e.target, detailContainer);
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

// NEW FUNCTION: To expand line items specifically for Draft Orders
async function expandDraftLineItems(draftId, iconElement, detailContainer) {
    console.log(`Expanding Draft Order line items for ID: ${draftId}`);

    const isHidden = detailContainer.style.display === "none";
    detailContainer.style.display = isHidden ? "block" : "none";
    iconElement.textContent = isHidden ? "⬆️" : "⬇️";

    if (!isHidden && detailContainer.innerHTML !== '') {
        return; // Already expanded and visible, no need to re-fetch
    }
    if (isHidden && detailContainer.innerHTML !== '') {
        return; // Just collapsed it, no need to re-fetch
    }

    try {
        // NEW API CALL: Fetch items specifically from the draft_orders endpoint
        const itemsRes = await fetch(`/draft_orders/api/items/${draftId}`);
        if (!itemsRes.ok) {
            const itemsErr = await itemsRes.text();
            throw new Error(`Fetch error: draft items ${itemsRes.status} (${itemsErr})`);
        }

        const items = await itemsRes.json(); // Assuming backend sends just the items array

        let contentHTML = '';

        if (items && items.length > 0) {
            let orderItemsTableHTML = `
                <div class="expanded-section order-items-section" style="margin-bottom: 1rem;">
                    <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Draft Order Items</h4>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
                        <thead>
                            <tr style="background:#f0f0f0;font-weight:bold">
                                <td style="text-align:left;">Item</td>
                                <td style="text-align:left;">Project</td>
                                <td style="text-align:right;">Qty</td>
                                <td style="text-align:right;">Price</td>
                                <td style="text-align:right;">Total</td>
                            </tr>
                        </thead>
                        <tbody>
                    `;

            items.forEach(item => {
                const itemLabel = item.item_description
                    ? `${item.item_code} – ${item.item_description}`
                    : item.item_code || "N/A";
                const quantity = item.qty_ordered || 0; // Use qty_ordered for drafts
                const unitPrice = item.price || 0;
                const itemTotal = quantity * unitPrice;

                const projectLabel = item.project || "N/A";

                const formattedPrice = `R${parseFloat(unitPrice).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
                const formattedTotal = `R${parseFloat(itemTotal).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

                orderItemsTableHTML += `
                            <tr>
                                <td style="text-align:left;">${itemLabel}</td>
                                <td style="text-align:left;">${projectLabel}</td>
                                <td style="text-align:right;">${quantity}</td>
                                <td style="text-align:right;">${formattedPrice}</td>
                                <td style="text-align:right;">${formattedTotal}</td>
                            </tr>
                        `;
            });
            orderItemsTableHTML += `
                        </tbody>
                    </table>
                </div>
            `;
            contentHTML += orderItemsTableHTML;
        } else {
            contentHTML += `<div class="expanded-section"><em>No items found for this draft order.</em></div>`;
        }

        detailContainer.innerHTML = contentHTML;

    } catch (err) {
        console.error("❌ Error expanding draft order details:", err);
        alert(`❌ Could not expand draft order details: ${err.message}`);
        if (detailContainer) {
            detailContainer.innerHTML = `<div class="expanded-section" style="color:red;">Error loading details: ${err.message}</div>`;
            detailContainer.style.display = "block";
        }
        iconElement.textContent = "⬇️";
    }
}
// END NEW FUNCTION


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

// We no longer export expandLineItems from here, as it's not directly used/modified by this script.
// If other scripts still import it and need it, their imports remain valid.
// window.expandLineItems = expandLineItems; // Removed global exposure if not strictly necessary.