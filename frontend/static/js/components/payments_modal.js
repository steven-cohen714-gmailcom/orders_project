// File: frontend/static/js/components/payments_modal.js

console.log("💸 payments_modal.js loaded");

// Assumes the modal element with id 'cod-payment-modal' exists in the HTML
// And contains a div with id 'modal-content-container'
export function showCodPaymentModal(orderId, orderNumber, existingAmount = '', existingDate = '') {
  // Get a reference to the existing modal in the HTML
  const modal = document.getElementById("cod-payment-modal");
  if (!modal) {
    console.error("Payments modal element with ID 'cod-payment-modal' not found.");
    return;
  }

  // Find the modal content container to populate it with the form
  const modalContentContainer = modal.querySelector('#modal-content-container');
  modalContentContainer.innerHTML = `
      <div class="modal-content">
          <h2>Mark COD Payment for Order ${orderNumber}</h2>
          <table class="table">
              <tbody>
                  <tr>
                      <td><label for="cod-amount">Amount Paid:</label></td>
                      <td><input type="number" id="cod-amount" value="${parseFloat(existingAmount).toFixed(2)}" placeholder="Enter amount" step="0.01" required class="form-input"></td>
                  </tr>
                  <tr>
                      <td><label for="cod-date">Payment Date:</label></td>
                      <td><input type="date" id="cod-date" value="${existingDate}" required class="form-input"></td>
                  </tr>
              </tbody>
          </table>
          <div class="form-row">
              <button id="cod-cancel" class="btn btn-danger">Cancel</button>
              <button id="cod-save" class="btn btn-primary">Save</button>
          </div>
      </div>
  `;
  
  // Show the modal
  modal.style.display = 'flex';

  // Add button listeners
  document.getElementById("cod-cancel").onclick = () => modal.style.display = 'none';
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
          errorMessage = errorData.detail || errorMessage;
        } catch (jsonError) {
          errorMessage = `Server error: ${res.status} ${res.statusText || ''}`;
        }
        console.error("Error saving COD payment:", errorMessage);
        alert(`❌ Error saving COD payment: ${errorMessage}`);
        return;
      }

      const data = await res.json();
      if (data.success) {
        alert("✅ COD payment recorded");
        modal.style.display = 'none'; // Hide the modal on success
        location.reload();
      } else {
        alert("❌ Failed to save payment");
      }
    } catch (err) {
      console.error("Network or unexpected error saving COD payment:", err);
      alert(`❌ An unexpected error occurred: ${err.message}`);
    }
  };
}