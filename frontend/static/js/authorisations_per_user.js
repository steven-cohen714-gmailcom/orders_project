// File: frontend/static/js/authorisations_per_user.js

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { showPDFModal } from "./components/pdf_modal.js";

console.log("🔐 Authorisations per user screen loaded");

document.addEventListener("DOMContentLoaded", async () => {
  const tableBody = document.getElementById("pending-body");
  const heading = document.getElementById("user-heading");

  const startDateInput = document.getElementById("start-date");
  const endDateInput = document.getElementById("end-date");
  const requesterSelect = document.getElementById("filter-requester");
  const supplierSelect = document.getElementById("filter-supplier");

  await loadRequesters("filter-requester");
  await loadSuppliers("filter-supplier");

  let currentUser = null;

  try {
    const userRes = await fetch("/mobile/get_user_info");
    currentUser = await userRes.json();
    heading.textContent = `${currentUser.username}, here are your authorisations:`;
  } catch (err) {
    console.error("❌ Failed to fetch user info:", err);
    heading.textContent = "❌ Could not load user info.";
    return;
  }

  document.getElementById("run-btn").addEventListener("click", () => {
    renderFilteredOrders();
  });

  document.getElementById("clear-btn").addEventListener("click", () => {
    startDateInput.value = "";
    endDateInput.value = "";
    requesterSelect.value = "All";
    supplierSelect.value = "All";
    renderFilteredOrders();
  });

  async function renderFilteredOrders() {
    tableBody.innerHTML = "<tr><td colspan='7'>Loading...</td></tr>";

    try {
      const res = await fetch("/orders/api/awaiting_authorisation");
      const orders = await res.json();

      const filtered = orders.filter(order => {
        if (Number(order.required_auth_band) !== Number(currentUser.auth_threshold_band)) return false;
        if (requesterSelect.value !== "All" && order.requester_name !== requesterSelect.value) return false;
        if (supplierSelect.value !== "All" && order.supplier_name !== supplierSelect.value) return false;
        if (startDateInput.value && new Date(order.created_date) < new Date(startDateInput.value)) return false;
        if (endDateInput.value && new Date(order.created_date) > new Date(endDateInput.value)) return false;
        return true;
      });

      if (filtered.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='7'>✅ No orders awaiting your authorisation.</td></tr>";
        return;
      }

      tableBody.innerHTML = "";
      for (const order of filtered) {
        const date = new Date(order.created_date);
        const formattedDate = `${date.getDate()} ${date.toLocaleString("default", { month: "short" })} ${date.getFullYear()}`;

        const row = document.createElement("tr");
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

        const viewBtn = row.querySelector(".view-btn");
        viewBtn.onclick = async () => {
          try {
            const res = await fetch(`/orders/api/generate_pdf_for_order/${order.id}`);
            if (!res.ok) {
              const errorText = await res.text();
              console.error(`❌ Failed to fetch PDF:`, errorText);
              alert("❌ Could not load PDF.");
              return;
            }

            const blob = await res.blob();
            window.currentOrderIdForPDF = order.id;
            window.currentOrderNumberForPDF = order.order_number;
            showPDFModal(blob);
          } catch (err) {
            console.error("❌ PDF fetch error:", err);
            alert("❌ Failed to load PDF.");
          }
        };

        const authBtn = row.querySelector(".auth-btn");
        authBtn.onclick = async () => {
          try {
            const res = await fetch(`/orders/api/authorise_order/${order.id}`, { method: "POST" });
            const result = await res.json();
            if (result.message === "Order authorised") {
              row.remove();
            } else {
              alert("❌ Failed to authorise: " + result.message);
            }
          } catch (err) {
            console.error("❌ Authorisation error:", err);
            alert("❌ Error sending authorisation request.");
          }
        };

        tableBody.appendChild(row);
      }
    } catch (err) {
      console.error("❌ Failed to fetch or render orders:", err);
      tableBody.innerHTML = "<tr><td colspan='7'>❌ Could not load orders.</td></tr>";
    }
  }

  renderFilteredOrders();
});
