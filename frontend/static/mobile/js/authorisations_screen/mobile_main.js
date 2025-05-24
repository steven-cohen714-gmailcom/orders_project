// File: frontend/static/js/mobile_main.js

import { setupAuthorisationUI } from "/static/js/authorisations_per_user.js";
import { showMobilePDFModal } from "/static/js/components/mobile_pdf_modal.js";

console.log("📱 Mobile authorisation screen loaded");

function showToast(message, success = true) {
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.className = success ? "toast toast-success" : "toast toast-error";
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2500);
}

function showConfirmationModal(message) {
  const existing = document.getElementById("confirmation-modal");
  if (existing) existing.remove();

  const backdrop = document.createElement("div");
  backdrop.id = "confirmation-modal";

  const inner = document.createElement("div");
  inner.textContent = message;

  backdrop.appendChild(inner);
  document.body.appendChild(backdrop);

  setTimeout(() => {
    backdrop.remove();
  }, 2500);
}

let currentUser = null;

function setupUI(user) {
  currentUser = user;  // Store for refresh
  setupAuthorisationUI({
    mountPointId: "order-list",
    user,
    isMobile: true,
    onAuthorised: (order) => {
      showConfirmationModal(`${user.username}, you authorised order ${order.order_number}.`);
    },
    onError: (msg) => {
      showToast(msg, false);
    },
    showPDF: (orderId) => showMobilePDFModal(orderId)
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  document.querySelector(".back-button")?.remove();

  const refreshBtn = document.createElement("button");
  refreshBtn.textContent = "🔄 Load Orders";
  refreshBtn.className = "refresh-button";
  refreshBtn.onclick = () => {
    if (currentUser) setupUI(currentUser);
  };
  document.body.appendChild(refreshBtn);

  await fetchUserAndSetup();
});

async function fetchUserAndSetup() {
  try {
    const res = await fetch("/mobile/get_user_info");
    const user = await res.json();
    currentUser = user;

    const heading = document.querySelector("h2");
    if (heading) {
      heading.innerHTML = `<strong>${user.username}</strong>, <strong>please review the orders below which are waiting for you to authorise:</strong>`;
    }

    setupUI(user);
  } catch (err) {
    console.error("❌ Failed to fetch user info:", err);
    showToast("Failed to load user session.", false);
  }
}

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
