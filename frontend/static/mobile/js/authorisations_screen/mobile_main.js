import { showMobilePDFModal } from "/static/js/components/mobile_pdf_modal.js";

function showToast(message, success = true) {
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.className = success ? "toast toast-success" : "toast toast-error";
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2500);
}

console.log("📱 Mobile authorisation screen loaded");

function formatDate(dateStr) {
  if (!dateStr) return "—";
  try {
    const date = new Date(dateStr);
    const day = date.getDate().toString().padStart(2, "0");
    const month = date.toLocaleString("default", { month: "short" });
    const year = date.getFullYear().toString().slice(-2);
    return `${day} ${month} ${year}`;
  } catch {
    return "—";
  }
}

let username = "";

async function loadOrders() {
  const container = document.getElementById("order-list");
  try {
    const res = await fetch("/orders/api/awaiting_authorisation");
    const data = await res.json();

    if (!Array.isArray(data)) {
      container.textContent = "❌ Invalid response from server.";
      console.error("Expected an array but got:", data);
      return;
    }

    if (data.length === 0) {
      container.textContent = "✅ No orders awaiting your authorisation.";
      return;
    }

    container.innerHTML = ""; // Clear loading

    data.forEach(order => {
      const item = document.createElement("div");
      item.className = "order-row";

      const dateFormatted = formatDate(order.created_date);

      item.innerHTML = `
        <span><strong>${dateFormatted}</strong></span>
        <span><strong>${order.order_number}</strong></span>
        <span><strong>R${Number(order.total).toLocaleString("en-ZA")}</strong></span>
        <span class="buttons"></span>
      `;

      const viewBtn = document.createElement("button");
      viewBtn.textContent = "View PDF";
      viewBtn.onclick = () => showMobilePDFModal(order.id);

      const authBtn = document.createElement("button");
      authBtn.textContent = "Authorise";
      authBtn.onclick = async () => {
        try {
          const res = await fetch(`/orders/api/authorise_order/${order.id}`, {
            method: "POST"
          });

          const result = await res.json();

          if (!res.ok || result.status !== "success") {
            const message = result?.detail || result?.message || "Unknown error.";
            showToast(message, false);

            if (message === "Order is not in an authorisable state") {
              item.remove();
            }
            return;
          }

          showToast(`${username}, you authorised order ${order.order_number}.`, true);
          await loadOrders();

        } catch (err) {
          console.error(err);
          showToast("Network or server error.", false);
        }
      };

      item.querySelector(".buttons").appendChild(viewBtn);
      item.querySelector(".buttons").appendChild(authBtn);
      container.appendChild(item);
    });

  } catch (err) {
    container.textContent = "❌ Failed to load orders.";
    console.error("Fetch error:", err);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("order-list");

  document.querySelector(".back-button")?.remove();

  const refreshBtn = document.createElement("button");
  refreshBtn.textContent = "🔄 Load Orders";
  refreshBtn.className = "refresh-button";
  refreshBtn.onclick = () => loadOrders();
  document.body.appendChild(refreshBtn);

  try {
    const res = await fetch("/mobile/get_user_info");
    const user = await res.json();
    username = user.username || "";
    const heading = document.querySelector("h2");
    if (heading) {
      heading.innerHTML = `<strong>${username}</strong>, <strong>please review the orders below which are waiting for you to authorise:</strong>`;
    }
  } catch (err) {
    console.error("❌ Failed to fetch user info:", err);
  }

  await loadOrders();
});

let deferredPrompt;

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  deferredPrompt = e;

  const installBtn = document.createElement("button");
  installBtn.textContent = "📲 Install App";
  installBtn.className = "install-button";

  installBtn.onclick = async () => {
    installBtn.remove();
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const choice = await deferredPrompt.userChoice;
      if (choice.outcome === "accepted") {
        showToast("App installed!");
      } else {
        showToast("Install dismissed", false);
      }
      deferredPrompt = null;
    }
  };

  document.body.appendChild(installBtn);
});
