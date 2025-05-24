import { showMobilePDFModal } from "/static/js/components/mobile_pdf_modal.js";

function showToast(message, success = true) {
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.style.position = "fixed";
  toast.style.bottom = "2rem";
  toast.style.left = "50%";
  toast.style.transform = "translateX(-50%)";
  toast.style.backgroundColor = success ? "#28a745" : "#dc3545";
  toast.style.color = "white";
  toast.style.padding = "0.8rem 1.2rem";
  toast.style.borderRadius = "8px";
  toast.style.fontSize = "0.9rem";
  toast.style.zIndex = 1000;
  toast.style.boxShadow = "0 0 10px rgba(0,0,0,0.2)";
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

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("order-list");

  // 🔍 Fetch username from session via backend
  try {
    const res = await fetch("/mobile/get_user_info");
    const user = await res.json();
    const username = user.username || "";
    const heading = document.querySelector("h2");
    if (heading) {
      heading.innerHTML = `<span style="font-weight: normal;">${username}</span>, please review the orders below which are waiting for you to authorise:`;
    }
  } catch (err) {
    console.error("❌ Failed to fetch user info:", err);
  }

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

    container.innerHTML = ""; // Clear "Loading orders..."

    data.forEach(order => {
      const item = document.createElement("div");
      item.className = "order-row";

      const dateFormatted = formatDate(order.created_date);

      item.innerHTML = `
        <span>${dateFormatted}</span>
        <span>${order.order_number}</span>
        <span>R${Number(order.total).toLocaleString("en-ZA")}</span>
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
          if (result.status === "success") {
            authBtn.textContent = "✅ Authorised";
            showToast("Order authorised successfully.");
            authBtn.disabled = true;
            viewBtn.disabled = true;
            item.style.opacity = 0.6;
          } else {
            alert("❌ Failed to authorise: " + result.message);
          }
        } catch (err) {
          console.error(err);
          alert("❌ Error sending authorisation request.");
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
});

let deferredPrompt;

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault(); // Prevent the automatic mini-infobar
  deferredPrompt = e;

  const installBtn = document.createElement("button");
  installBtn.textContent = "📲 Install App";
  installBtn.style.position = "fixed";
  installBtn.style.bottom = "1rem";
  installBtn.style.right = "1rem";
  installBtn.style.padding = "0.6rem 1.2rem";
  installBtn.style.backgroundColor = "#0066cc";
  installBtn.style.color = "white";
  installBtn.style.border = "none";
  installBtn.style.borderRadius = "6px";
  installBtn.style.fontSize = "0.95rem";
  installBtn.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
  installBtn.style.zIndex = 999;

  installBtn.onclick = async () => {
    installBtn.remove();
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const choice = await deferredPrompt.userChoice;
      if (choice.outcome === "accepted") {
        showToast("✅ App installed!");
      } else {
        showToast("❌ Install dismissed");
      }
      deferredPrompt = null;
    }
  };

  document.body.appendChild(installBtn);
});
