// File: frontend/static/js/authorisations_per_user.js

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { expandLineItemsWithReceipts } from "./components/expand_line_items.js"; // Ensure this is imported if you're using it

// New function to format currency with thousand separators and 2 decimal places
function formatCurrency(amount) {
  if (amount == null) return "R0.00";
  return `R${parseFloat(amount).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
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

  await loadRequesters("filter-requester");
  await loadSuppliers("filter-supplier");

  await loadOrdersForUser(user);

  async function loadOrdersForUser(user) {
    tableBody.innerHTML = "<tr><td colspan='7'>Loading orders...</td></tr>";

    try {
      const res = await fetch("/orders/api/awaiting_authorisation");
      const orders = await res.json();

      const userBand = parseInt(user.auth_threshold_band); // User's threshold band (e.g., 1, 2, 3, 4)
      
      const eligibleOrders = orders.filter(
        order => {
          // Double check status, though API /awaiting_authorisation should handle this.
          // This check is mainly defensive.
          if (order.status !== 'Awaiting Authorisation') {
              return false;
          }

          const orderRequiredBand = order.required_auth_band; // Value is NULL or INTEGER from DB

          // FIX START: Handle NULL or 0 for required_auth_band - THIS IS THE CRUCIAL CHANGE
          if (orderRequiredBand === null || orderRequiredBand === 0) {
              // If an order has no specific required band (NULL or 0), it should be visible
              // to users with the lowest authorization level.
              // Assuming auth_threshold_band of 1 is the lowest level.
              return userBand === 1;
          }
          // FIX END

          // If order has a specific required_auth_band, it must strictly match the user's band
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

        // Added expand-icon span and an extra column for it if needed
        row.innerHTML = `
          <td>${formattedDate}</td>
          <td>${order.order_number}</td>
          <td>${order.requester_name}</td>
          <td>${order.supplier_name}</td>
          <td>${formatCurrency(order.total)}</td>
          <td>${order.status}</td>
          <td>
            <span class="expand-icon" style="cursor:pointer" title="View Line Items">⬇️</span>
            <button class="view-btn">View</button>
            <button class="auth-btn">Authorise</button>
          </td>
        `;

        tableBody.appendChild(row);

        // ADDED: Create the detailRow and detailContainer, similar to pending/received orders
        const detailRow = document.createElement('tr');
        detailRow.className = 'expanded-details-row';
        const detailCell = document.createElement('td');
        detailCell.colSpan = 7; // Assuming 7 columns (Date, Order Number, Requester, Supplier, Total, Status, Actions)
        const detailContainer = document.createElement('div');
        detailContainer.id = `detail-container-${order.id}`;
        detailContainer.style.display = 'none';
        detailCell.appendChild(detailContainer);
        detailRow.appendChild(detailCell);
        tableBody.appendChild(detailRow); // Append right after the main order row

        // ADDED: Event listener for the expand icon
        row.querySelector(".expand-icon").addEventListener("click", (e) => {
          if (!order.id) {
            console.error("No order ID provided for expanding line items");
            alert("Cannot expand line items: No order ID available");
            return;
          }
          // IMPORTANT: ensure expandLineItemsWithReceipts is correctly imported if you are using this
          expandLineItemsWithReceipts(order.id, e.target, detailContainer, order);
        });


        row.querySelector(".view-btn").addEventListener("click", () => {
          try {
            showPDF(order.id);
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
              body: JSON.stringify({ username: localStorage.getItem("username") })
            });
            const result = await res.json();

            if (result.message === "Order authorised") {
              const msg = `✅ Order ${order.order_number} was successfully authorised.`;
              console.log(msg);
              alert(msg);  // or use a nicer toast if you have one
              onAuthorised(order);
              // FIX: Refresh the orders list after authorization to remove the authorized order
              await loadOrdersForUser(user); 
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
}