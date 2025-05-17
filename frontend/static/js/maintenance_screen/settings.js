export function initSettings() {
  console.log("initSettings loaded");

  fetchSettings();

  const updateBtn = document.getElementById("update-settings-button");
  if (updateBtn) {
    updateBtn.addEventListener("click", updateSettings);
  }

  async function fetchSettings() {
    try {
      const res = await fetch("/lookups/settings");
      const data = await res.json();

      document.getElementById("order-number-start").value = data.order_number_start || "";
      document.getElementById("auth-threshold-1").value = data.auth_threshold_1 || "";
      document.getElementById("auth-threshold-2").value = data.auth_threshold_2 || "";
      document.getElementById("auth-threshold-3").value = data.auth_threshold_3 || "";
      document.getElementById("auth-threshold-4").value = data.auth_threshold_4 || "";
    } catch (err) {
      console.error("Failed to fetch settings:", err);
    }
  }

  async function updateSettings() {
    const order_number_start = document.getElementById("order-number-start").value;
    const auth_threshold_1 = document.getElementById("auth-threshold-1").value;
    const auth_threshold_2 = document.getElementById("auth-threshold-2").value;
    const auth_threshold_3 = document.getElementById("auth-threshold-3").value;
    const auth_threshold_4 = document.getElementById("auth-threshold-4").value;

    try {
      const res = await fetch("/lookups/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          order_number_start,
          auth_threshold_1,
          auth_threshold_2,
          auth_threshold_3,
          auth_threshold_4
        })
      });
      if (res.ok) fetchSettings();
    } catch (err) {
      console.error("Failed to update settings:", err);
    }
  }
}
