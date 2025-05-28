export function startCodPolling({ user }) {
  if (user !== "Sam") return;

  setInterval(async () => {
    try {
      const res = await fetch("/orders/api/check_for_cod_orders");
      if (!res.ok) return;

      const data = await res.json();
      if (data.new_cod_orders && data.new_cod_orders.length > 0) {
        const latest = data.new_cod_orders[0];
        showCodToast(`🚨 New COD order placed: ${latest.order_number}`);
        playNotificationSound();
      }
    } catch (err) {
      console.error("Polling error:", err);
    }
  }, 30000); // Every 30 seconds
}

function showCodToast(message) {
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.className = "cod-toast";
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 5000);
}

function playNotificationSound() {
  const audio = new Audio("/static/audio/alert.mp3");
  audio.play().catch(() => {});
}
