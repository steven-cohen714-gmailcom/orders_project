// File: frontend/static/js/components/payments_modal.js

console.log("💸 payments_modal.js loaded");

export function showCodPaymentModal(orderId, existingAmount = '', existingDate = '') {
  // Create modal container
  const modal = document.createElement("div");
  modal.classList.add("modal-overlay");
  modal.innerHTML = `
    <div class="modal">
      <h2>Mark COD Payment</h2>
      <label for="cod-amount">Amount Paid:</label>
      <input type="number" id="cod-amount" value="${existingAmount}" placeholder="Enter amount" step="0.01" />

      <label for="cod-date">Payment Date:</label>
      <input type="date" id="cod-date" value="${existingDate}" />

      <div class="modal-buttons">
        <button id="cod-cancel">Cancel</button>
        <button id="cod-save">Save</button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // Add button listeners
  document.getElementById("cod-cancel").onclick = () => modal.remove();
  document.getElementById("cod-save").onclick = async () => {
    const amount = parseFloat(document.getElementById("cod-amount").value);
    const date = document.getElementById("cod-date").value;

    if (isNaN(amount) || !date) {
      alert("Please enter a valid amount and payment date.");
      return;
    }

    try {
      const res = await fetch(`/orders/mark_cod_paid/${orderId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ amount_paid: amount, payment_date: date })
      });

      if (!res.ok) {
        let errorMessage = "Failed to save COD payment due to an unknown error.";
        try {
          const errorData = await res.json();
          errorMessage = errorData.detail || errorMessage; // Use backend's 'detail' message if available
        } catch (jsonError) {
          // If response is not JSON, use the status text or a generic message
          errorMessage = `Server error: ${res.status} ${res.statusText || ''}`;
        }
        console.error("Error saving COD payment:", errorMessage); // Keep this console.error for debugging purposes
        alert(`❌ Error saving COD payment: ${errorMessage}`);
        // *** CRITICAL CHANGE: Remove `throw new Error(...)` here ***
        return; // Stop function execution after displaying alert
      }

      const data = await res.json();
      if (data.success) {
        alert("✅ COD payment recorded");
        modal.remove();
        location.reload();
      } else {
        // This case should ideally not be hit if backend always sends 'success: true' on success
        alert("❌ Failed to save payment"); 
      }
    } catch (err) {
      // This catch block will now primarily catch true network errors (e.g., server unreachable)
      // or issues occurring before the `fetch` call resolves.
      console.error("Network or unexpected error saving COD payment:", err);
      alert(`❌ An unexpected error occurred: ${err.message}`);
    }
  };
}