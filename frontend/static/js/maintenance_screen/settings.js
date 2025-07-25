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
      document.getElementById("requisition-number-start").value = data.requisition_number_start || "";
      document.getElementById("auth-threshold-1").value = data.auth_threshold_1 || "";
      document.getElementById("auth-threshold-2").value = data.auth_threshold_2 || "";
      document.getElementById("auth-threshold-3").value = data.auth_threshold_3 || "";
      document.getElementById("auth-threshold-4").value = data.auth_threshold_4 || "";
      document.getElementById("auth-threshold-5").value = data.auth_threshold_5 || ""; // ADDED: Fetch auth_threshold_5
    } catch (err) {
      console.error("Failed to fetch settings:", err);
    }
  }

  async function updateSettings() {
    const order_number_start = document.getElementById("order-number-start").value;
    const requisition_number_start = document.getElementById("requisition-number-start").value;
    const auth_threshold_1 = parseInt(document.getElementById("auth-threshold-1").value) || 0;
    const auth_threshold_2 = parseInt(document.getElementById("auth-threshold-2").value) || 0;
    const auth_threshold_3 = parseInt(document.getElementById("auth-threshold-3").value) || 0;
    const auth_threshold_4 = parseInt(document.getElementById("auth-threshold-4").value) || 0;
    const auth_threshold_5 = parseInt(document.getElementById("auth-threshold-5").value) || 0; // ADDED: Get auth_threshold_5 value

    try {
      const res = await fetch("/lookups/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          order_number_start,
          requisition_number_start,
          auth_threshold_1,
          auth_threshold_2,
          auth_threshold_3,
          auth_threshold_4,
          auth_threshold_5 // ADDED: Include auth_threshold_5 in the payload
        })
      });
      if (res.ok) {
        fetchSettings();
        alert("✅ Settings updated successfully.");
      }

    } catch (err) {
      console.error("Failed to update settings:", err);
    }
  }
}