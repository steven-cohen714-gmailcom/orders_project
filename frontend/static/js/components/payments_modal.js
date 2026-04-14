// File: frontend/static/js/components/payments_modal.js
// COD Payments modal — robust order total (uses audit API first), shows Paid So Far & Remaining,
// posts a new payment that updates order status via backend.

console.log("💸 payments_modal.js loaded");

function formatRand(n) {
  const num = Number(n || 0);
  return `R${num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Named export so other modules can import it.
// Optional 3rd arg orderTotalHint can skip fetching if the list already knows the total.
export async function showCodPaymentModal(orderId, orderNumber, orderTotalHint) {
  const modal = document.getElementById("cod-payment-modal");
  if (!modal) {
    console.error("Payments modal element with ID 'cod-payment-modal' not found.");
    return;
  }
  const modalContentContainer = modal.querySelector("#modal-content-container");

  // ---------- Load payment history ----------
  let payments = [];
  let paymentsTotal = 0;

  try {
    const historyRes = await fetch(`/orders/payment_history/${orderId}`);
    if (historyRes.ok) {
      const data = await historyRes.json();
      payments = (data && Array.isArray(data.payments)) ? data.payments : [];
      paymentsTotal = payments.reduce((sum, p) => sum + Number(p.amount_paid || 0), 0);
    } else {
      console.warn(`⚠️ Failed to load payment history: ${historyRes.status}`);
    }
  } catch (err) {
    console.error("⚠️ Error fetching payment history:", err);
  }

  // ---------- Load order total (hint → audit API, avoid HTML route) ----------
  async function fetchOrderTotal(orderId) {
    // 0) Use hint if provided
    if (typeof orderTotalHint === "number" && !Number.isNaN(orderTotalHint) && orderTotalHint > 0) {
      return Number(orderTotalHint);
    }

    // 1) Preferred JSON endpoint
    try {
      const r = await fetch(`/orders/api/order_details_for_audit/${orderId}`);
      if (r.ok) {
        const j = await r.json();
        if (j && typeof j.total !== "undefined") return Number(j.total || 0);
        console.warn("⚠️ audit details returned no 'total' field:", j);
      } else {
        console.warn(`⚠️ audit details failed: ${r.status}`);
      }
    } catch (e) {
      console.warn("⚠️ audit details fetch error:", e);
    }

    // 2) Last resort → zero (we avoid /orders/{id} because it’s an HTML template route on this app)
    return 0;
  }

  const orderTotal = await fetchOrderTotal(orderId);
  const remaining = Math.max(orderTotal - paymentsTotal, 0);

  // ---------- Payment history table ----------
  let historyHtml = "";
  if (payments.length > 0) {
    historyHtml = `
      <div class="mt-4 p-4 bg-gray-100 rounded-lg">
        <h3 class="text-lg font-bold mb-2">Previous Payments</h3>
        <table class="receive-modal w-full border-collapse">
          <thead class="bg-gray-200">
            <tr>
              <th class="p-2 border">Amount</th>
              <th class="p-2 border">Date</th>
              <th class="p-2 border">Status</th>
            </tr>
          </thead>
          <tbody>
            ${payments.map(p => `
              <tr>
                <td class="p-2 border">${formatRand(p.amount_paid)}</td>
                <td class="p-2 border">${p.payment_date || ""}</td>
                <td class="p-2 border">${p.payment_status || ""}</td>
              </tr>`).join("")}
          </tbody>
        </table>
      </div>
    `;
  }

  // ---------- Render modal ----------
  modalContentContainer.innerHTML = `
    <div class="p-6">
      <h2 class="text-2xl font-bold mb-2 text-center">Mark COD Payment for Order ${orderNumber}</h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mb-4">
        <div class="text-left p-2">
          <p class="font-bold">Order Total</p>
          <p>${formatRand(orderTotal)}</p>
        </div>
        <div class="text-left p-2">
          <p class="font-bold">Amount Paid So Far</p>
          <p>${formatRand(paymentsTotal)}</p>
        </div>
        <div class="text-left p-2">
          <p class="font-bold">Remaining</p>
          <p>${formatRand(remaining)}</p>
        </div>
      </div>

      ${historyHtml}

      <form id="payment-form" class="space-y-4">
        <div class="modal-form-group">
          <label for="cod-amount" class="block text-sm font-medium text-gray-700">Amount Paid:</label>
          <input type="number" id="cod-amount" name="cod-amount"
                 step="0.01" min="0.01" required
                 class="mt-1 p-2 w-full border rounded-md focus:ring focus:ring-blue-200"
                 placeholder="${remaining > 0 ? remaining.toFixed(2) : ''}">
        </div>
        <div class="modal-form-group">
          <label for="cod-date" class="block text-sm font-medium text-gray-700">Payment Date:</label>
          <input type="date" id="cod-date" name="cod-date"
                 value="${new Date().toISOString().split("T")[0]}" required
                 class="mt-1 p-2 w-full border rounded-md focus:ring focus:ring-blue-200">
        </div>
        <div class="modal-form-group">
          <label class="block text-sm font-medium text-gray-700">Payment Status:</label>
          <div class="mt-1 space-x-4">
            <label><input type="radio" name="payment-status" value="Paid"> Paid</label>
            <label><input type="radio" name="payment-status" value="Partially Paid"> Partially Paid</label>
          </div>
        </div>
      </form>

      <div class="mt-6 flex justify-end gap-2">
        <button id="cod-cancel" type="button" class="btn btn-danger py-2 px-4 rounded-md bg-red-500 text-white hover:bg-red-600">Cancel</button>
        <button id="cod-save" type="button" class="btn btn-primary py-2 px-4 rounded-md bg-blue-500 text-white hover:bg-blue-600" disabled>Save</button>
      </div>
    </div>
  `;

  // Show modal
  modal.style.display = "block";

  // ---------- Enable/disable Save ----------
  function toggleSaveButton() {
    const amount = document.getElementById("cod-amount").value;
    const date = document.getElementById("cod-date").value;
    const statusRadios = document.querySelectorAll('input[name="payment-status"]');
    const isStatusSelected = Array.from(statusRadios).some(radio => radio.checked);
    const saveBtn = document.getElementById("cod-save");
    saveBtn.disabled = !amount || isNaN(amount) || Number(amount) <= 0 || !date || !isStatusSelected;
  }

  document.getElementById("cod-amount").addEventListener("input", toggleSaveButton);
  document.getElementById("cod-date").addEventListener("input", toggleSaveButton);
  document.querySelectorAll('input[name="payment-status"]').forEach(radio => {
    radio.addEventListener("change", toggleSaveButton);
  });
  toggleSaveButton();

  // ---------- Buttons ----------
  document.getElementById("cod-cancel").onclick = () => {
    modal.style.display = "none";
  };

  document.getElementById("cod-save").onclick = async () => {
    const saveBtn = document.getElementById("cod-save");
    saveBtn.disabled = true;

    const newPaymentAmount = Number(document.getElementById("cod-amount").value);
    const date = document.getElementById("cod-date").value;
    const selected = document.querySelector('input[name="payment-status"]:checked');
    const paymentStatus = selected ? selected.value : "";

    if (isNaN(newPaymentAmount) || newPaymentAmount <= 0 || !date || !paymentStatus) {
      alert("Please enter a valid amount, payment date, and status.");
      saveBtn.disabled = false;
      return;
    }

    try {
      const res = await fetch(`/orders/mark_cod_paid/${orderId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          amount_paid: newPaymentAmount,
          payment_date: date,
          payment_status: paymentStatus
        })
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        console.error(`Failed to save payment: ${res.status} - ${data.detail || "Unknown error"}`);
        alert(`❌ Failed to save payment: ${data.detail || "Unknown error"} (Status: ${res.status})`);
        saveBtn.disabled = false;
        return;
      }
      alert("✅ COD payment recorded");
      modal.style.display = "none";
      // FULLY_PAID rows should drop from the COD list on reload.
      location.reload();
    } catch (err) {
      console.error("❌ Unexpected error:", err);
      alert(`❌ ${err.message}`);
    } finally {
      if (modal.style.display !== "none") {
        saveBtn.disabled = false;
      }
    }
  };
}
