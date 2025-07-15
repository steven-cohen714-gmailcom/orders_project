// File: frontend/static/js/authorisations_per_user.js

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { expandLineItemsWithReceipts } from "./components/expand_line_items.js";

// New function to format currency with thousand separators and 2 decimal places
function formatCurrency(amount) {
  if (amount == null) return "R0.00";
  return `R${parseFloat(amount).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Function to escape HTML for display
function escapeHTML(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export async function setupAuthorisationUI({
  user,
  mountPointId,
  showPDF,
  onAuthorised = () => {},
  onError = () => {}
}) {
  console.log("🔐 My Authorisations screen (desktop) loaded");
  const tableBody = document.getElementById(mountPointId);
  if (!tableBody) {
    console.error(`❌ Mount point '${mountPointId}' not found.`);
    return;
  }

  // Load filter dropdowns
  await loadRequesters("filter-requester");
  await loadSuppliers("filter-supplier");

  // Initial load of orders
  await loadOrdersForUser(user);

  // Attach event listeners for filter buttons
  document.getElementById("run-btn").addEventListener("click", () => loadOrdersForUser(user));
  document.getElementById("clear-btn").addEventListener("click", clearFiltersAndLoadOrders);


  async function loadOrdersForUser(user) {
    tableBody.innerHTML = "<tr><td colspan='7'>Loading orders...</td></tr>";
    
    // Collect filter values
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const requester = document.getElementById("filter-requester").value;
    const supplier = document.getElementById("filter-supplier").value;
    // The status filter for this screen is hardcoded to "Awaiting Authorisation" in HTML
    // We don't need to read it from the UI or send it as it's implied by the endpoint's purpose.
    // const status = document.getElementById("filter-status").value; 

    const params = new URLSearchParams();
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);
    if (requester && requester !== "All") params.append("requester", requester);
    if (supplier && supplier !== "All") params.append("supplier", supplier);
    // if (status && status !== "All") params.append("status", status); // No need for status param on this specific API call

    console.log("Fetching orders for authorisations with params:", params.toString()); // Debug

    try {
      // Call the backend endpoint with collected parameters
      const res = await fetch(`/orders/api/awaiting_authorisation?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
      const orders = await res.json();
      
      const userBand = parseInt(user.auth_threshold_band); // User's threshold band (e.g., 1, 2, 3, 4)
      
      // The backend now filters by required_auth_band matching userBand OR (NULL/0 for band 1).
      // So, the frontend-side filtering here is technically redundant if the backend is perfect,
      // but it serves as a defensive check and aligns with previous logic.
      const eligibleOrders = orders.filter(
        order => {
          if (order.status !== 'Awaiting Authorisation') {
            return false;
          }

          const orderRequiredBand = order.required_auth_band;

          if (orderRequiredBand === null || orderRequiredBand === 0) {
            return userBand === 1;
          }
          return parseInt(orderRequiredBand) === userBand;
        }
      );

      if (eligibleOrders.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='7'>✅ No orders awaiting your authorisation.</td></tr>";
        return;
      }

      tableBody.innerHTML = "";
      for (const order of eligibleOrders) {
        const row = document.createElement("tr");
        const created = new Date(order.created_date);
        const formattedDate = `${created.getDate()} ${created.toLocaleString("default", {
          month: "short"
        })} ${created.getFullYear()}`;
        
        row.innerHTML = `
          <td>${escapeHTML(formattedDate)}</td>
          <td>${escapeHTML(order.order_number)}</td>
          <td>${escapeHTML(order.requester_name)}</td>
          <td>${escapeHTML(order.supplier_name)}</td>
          <td>${formatCurrency(order.total)}</td>
          <td>${escapeHTML(order.status)}</td>
          <td>
            <span class="expand-icon" style="cursor:pointer" title="View Line Items" data-order-id="${order.id}">⬇️</span>
            <button class="view-btn">View</button>
            <button class="auth-btn">Authorise</button>
          </td>
        `;
        tableBody.appendChild(row);

        const detailRow = document.createElement('tr');
        detailRow.className = 'expanded-details-row';
        const detailCell = document.createElement('td');
        detailCell.colSpan = 7;
        const detailContainer = document.createElement('div');
        detailContainer.id = `detail-container-${order.id}`;
        detailContainer.style.display = 'none';
        detailCell.appendChild(detailContainer);
        detailRow.appendChild(detailCell);
        tableBody.appendChild(detailRow);

        row.querySelector(".expand-icon").addEventListener("click", (e) => {
          if (!order.id) {
            console.error("No order ID provided for expanding line items");
            alert("Cannot expand line items: No order ID available");
            return;
          }
          expandLineItemsWithReceipts(order.id, e.target, detailContainer, order);
        });

        row.querySelector(".view-btn").addEventListener("click", () => {
          try {
            showPDF(order.id, order.order_number); // Pass order_number for modal title/filename
          } catch (err) {
            console.error("❌ Error triggering PDF display:", err);
            onError("❌ Could not open PDF preview.");
          }
        });

        row.querySelector(".auth-btn").addEventListener("click", async () => {
          try {
            const res = await fetch(`/orders/api/authorise_order/${order.id}`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              // body: JSON.stringify({ username: localStorage.getItem("username") }) // Backend uses session user, so no need for body
            });
            const result = await res.json();

            if (result.message === "Order authorised") {
              const msg = `✅ Order ${order.order_number} was successfully authorised.`;
              console.log(msg);
              alert(msg);
              onAuthorised(order);
              // Refresh the orders list after authorization
              await loadOrdersForUser(user); 
            } else {
              onError(`❌ Authorisation failed: ${result.detail || result.message}`);
            }

          } catch (err) {
            console.error("❌ Error during authorisation:", err);
            onError("❌ Network or server error while authorising.");
          }
        });
      }
    } catch (err) {
      console.error("❌ Could not load orders:", err);
      tableBody.innerHTML = "<tr><td colspan='7'>❌ Error loading orders.</td></tr>";
      onError("❌ Error loading orders for authorisation.");
    }
  }

  // New function to clear filters and reload orders
  function clearFiltersAndLoadOrders() {
    document.getElementById("start-date").value = "";
    document.getElementById("end-date").value = "";
    document.getElementById("filter-requester").value = "All";
    document.getElementById("filter-supplier").value = "All";
    // Status is intentionally hardcoded/disabled on this page, so no need to clear it.
    loadOrdersForUser(user); // Reload orders with cleared filters
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/mobile/get_user_info");
    const user = await res.json();

    document.getElementById("user-heading").textContent = `${user.username}, here are your authorisations:`;

    // Initialize setupAuthorisationUI
    await setupAuthorisationUI({
      user,
      mountPointId: "pending-body", // The tbody ID for the main table
      showPDF: async (orderId, orderNumber) => { // showPDF now expects orderNumber too
        try {
          const res = await fetch(`/orders/api/generate_pdf_for_order/${orderId}`);
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          const blob = await res.blob();
          // Assuming showPDFModal from components/pdf_modal.js is available globally or imported
          // It needs orderId and orderNumber to handle email/download filenames correctly
          if (window.showPDFModal) {
            window.showPDFModal(blob, orderId, orderNumber); 
          } else {
            console.error("showPDFModal not available globally.");
            alert("PDF modal is not loaded. Cannot display PDF.");
          }
        } catch (err) {
          console.error("❌ PDF modal error:", err);
          alert("❌ Could not load PDF preview.");
        }
      },
      onAuthorised: (order) => {
        console.log(`✅ Authorised order ${order.order_number}`);
        // Optionally, trigger a toast or small notification here.
      },
      onError: (msg) => {
        alert(msg);
      }
    });
  } catch (err) {
    console.error("❌ Failed to load user info or setup UI:", err);
    document.getElementById("pending-body").innerHTML =
      "<tr><td colspan='7'>❌ Could not load user session or orders. Please refresh or contact support.</td></tr>";
  }
});