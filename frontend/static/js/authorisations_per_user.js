// File: frontend/static/js/authorisations_per_user.js

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { showPDFModal } from "./components/pdf_modal.js";

console.log("🔐 Authorisations per user screen loaded");

export async function setupAuthorisationUI({
  user,
  mountPointId,
  isMobile = false,
  onAuthorised = () => {},
  onError = () => {},
  showPDF = showPDFModal
}) {
  const tableBody = document.getElementById(mountPointId);
  if (!tableBody) {
    console.error(`❌ Could not find mount point with ID '${mountPointId}'`);
    return;
  }

  async function renderFilteredOrders() {
    tableBody.innerHTML = "<tr><td colspan='7'>Loading...</td></tr>";

    try {
      const res = await fetch("/orders/api/awaiting_authorisation");
      const orders = await res.json();

      const filtered = orders.filter(order => {
        if (Number(order.required_auth_band) !== Number(user.auth_threshold_band)) return false;
        return true;
      });

      if (filtered.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='7'>✅ No orders awaiting your authorisation.</td></tr>";
        return;
      }

      tableBody.innerHTML = "";
      for (const order of filtered) {
        const row = document.createElement("tr");
        const date = new Date(order.created_date);
        const formattedDate = `${date.getDate()} ${date.toLocaleString("default", { month: "short" })} ${date.getFullYear()}`;

        row.innerHTML = `
          <td>${formattedDate}</td>
          <td>${order.order_number}</td>
          <td>${order.requester_name}</td>
          <td>${order.supplier_name}</td>
          <td>R${order.total}</td>
          <td>${order.status}</td>
          <td class="actions-cell">
            <button class="view-btn">View</button>
            <button class="auth-btn">Authorise</button>
          </td>
        `;

        row.querySelector(".view-btn").onclick = () => showPDF(order.id);

        row.querySelector(".auth-btn").onclick = async () => {
          try {
            const res = await fetch(`/orders/api/authorise_order/${order.id}`, { method: "POST" });
            const result = await res.json();
            if (result.message === "Order authorised") {
              onAuthorised(order);
              row.remove();
            } else {
              onError("❌ Failed to authorise: " + result.message);
            }
          } catch (err) {
            console.error("❌ Authorisation error:", err);
            onError("❌ Error sending authorisation request.");
          }
        };

        tableBody.appendChild(row);
      }
    } catch (err) {
      console.error("❌ Failed to fetch or render orders:", err);
      tableBody.innerHTML = "<tr><td colspan='7'>❌ Could not load orders.</td></tr>";
    }
  }

  await renderFilteredOrders();
}
