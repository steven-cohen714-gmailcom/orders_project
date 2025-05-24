// File: frontend/static/js/authorisations_per_user.js

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";

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

      const userBand = parseInt(user.auth_threshold_band);
      const eligibleOrders = orders.filter(
        order => parseInt(order.required_auth_band) === userBand
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
          <td>${formattedDate}</td>
          <td>${order.order_number}</td>
          <td>${order.requester_name}</td>
          <td>${order.supplier_name}</td>
          <td>R${order.total}</td>
          <td>${order.status}</td>
          <td>
            <button class="view-btn">View</button>
            <button class="auth-btn">Authorise</button>
          </td>
        `;

        row.querySelector(".view-btn").addEventListener("click", () => {
          try {
            showPDF(order.id);  // ✅ delegate to external handler
          } catch (err) {
            console.error("❌ Error triggering PDF display:", err);
            onError("❌ Could not open PDF preview.");
          }
        });

        row.querySelector(".auth-btn").addEventListener("click", async () => {
          try {
            const res = await fetch(`/orders/api/authorise_order/${order.id}`, { method: "POST" });
            const result = await res.json();

            if (result.message === "Order authorised") {
              console.log(`✅ Authorised order ${order.order_number}`);
              onAuthorised(order);
              row.remove();
            } else {
              onError("❌ Failed to authorise: " + result.message);
            }
          } catch (err) {
            console.error("❌ Error during authorisation:", err);
            onError("❌ Network or server error while authorising.");
          }
        });

        tableBody.appendChild(row);
      }
    } catch (err) {
      console.error("❌ Could not load orders:", err);
      tableBody.innerHTML = "<tr><td colspan='7'>❌ Error loading orders.</td></tr>";
    }
  }
}
