// File: frontend/static/js/payments_modal.js

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

      if (!res.ok) throw new Error("Failed to save COD payment");

      const data = await res.json();
      if (data.success) {
        alert("✅ COD payment recorded");
        modal.remove();
        location.reload();
      } else {
        alert("❌ Failed to save payment");
      }
    } catch (err) {
      console.error("Error saving COD payment:", err);
      alert("❌ Error saving payment");
    }
  };
}
