// File: frontend/static/js/components/payments_modal.js
// A revised version of the payments modal that now correctly handles VAT.

console.log("💸 payments_modal.js loaded");

// This function is now a named export so it can be imported by other modules.
export async function showCodPaymentModal(orderId, orderNumber) {
    const modal = document.getElementById("cod-payment-modal");
    if (!modal) {
        console.error("Payments modal element with ID 'cod-payment-modal' not found.");
        return;
    }
    const modalContentContainer = modal.querySelector('#modal-content-container');
    let payments = [];
    let paymentsTotal = 0;

    try {
        const historyRes = await fetch(`/orders/payment_history/${orderId}`);
        if (historyRes.ok) {
            const data = await historyRes.json();
            payments = data.payments; // FIX: Access the payments array from the returned object
            paymentsTotal = payments.reduce((sum, p) => sum + p.amount_paid, 0);
        } else {
            console.warn(`⚠️ Failed to load payment history: ${historyRes.status}`);
            paymentsTotal = 0; // Default to 0 if fetch fails
        }
    } catch (err) {
        console.error("⚠️ Error fetching payment history:", err);
        paymentsTotal = 0; // Fallback for error
    }

    // Generate HTML for payment history, styled like receive-modal table
    let historyHtml = '';
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
                                <td class="p-2 border">R${parseFloat(p.amount_paid).toFixed(2)}</td>
                                <td class="p-2 border">${p.payment_date}</td>
                                <td class="p-2 border">${p.payment_status}</td>
                            </tr>`).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // Render modal content, styled like receive-modal
    modalContentContainer.innerHTML = `
        <div class="p-6">
            <h2 class="text-2xl font-bold mb-4 text-center">Mark COD Payment for Order ${orderNumber}</h2>
            <div class="text-center mb-4 p-2 bg-blue-100 text-blue-800 rounded-md">
                <p class="font-bold">Amount Paid So Far: R${paymentsTotal.toFixed(2)}</p>
            </div>
            ${historyHtml}
            <form id="payment-form" class="space-y-4">
                <div class="modal-form-group">
                    <label for="cod-amount" class="block text-sm font-medium text-gray-700">Amount Paid:</label>
                    <input type="number" id="cod-amount" name="cod-amount"
                           value="" step="0.01" required
                           class="mt-1 p-2 w-full border rounded-md focus:ring focus:ring-blue-200">
                </div>
                <div class="modal-form-group">
                    <label for="cod-date" class="block text-sm font-medium text-gray-700">Payment Date:</label>
                    <input type="date" id="cod-date" name="cod-date"
                           value="${new Date().toISOString().split('T')[0]}" required
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
    modal.style.display = 'block'; // Show the modal with your .modal-overlay and .modal-content CSS

    // Toggle save button based on input validity
    function toggleSaveButton() {
        const amount = document.getElementById("cod-amount").value;
        const date = document.getElementById("cod-date").value;
        const statusRadios = document.querySelectorAll('input[name="payment-status"]');
        const isStatusSelected = Array.from(statusRadios).some(radio => radio.checked);
        const saveBtn = document.getElementById("cod-save");
        saveBtn.disabled = !amount || isNaN(amount) || amount <= 0 || !date || !isStatusSelected;
    }

    // Attach event listeners
    document.getElementById("cod-amount").addEventListener("input", toggleSaveButton);
    document.getElementById("cod-date").addEventListener("input", toggleSaveButton);
    document.querySelectorAll('input[name="payment-status"]').forEach(radio => {
        radio.addEventListener("change", toggleSaveButton);
    });
    toggleSaveButton(); // Initial check

    // Button actions
    document.getElementById("cod-cancel").onclick = () => {
        modal.style.display = 'none';
    };
    document.getElementById("cod-save").onclick = async () => {
        const newPaymentAmount = parseFloat(document.getElementById("cod-amount").value);
        const date = document.getElementById("cod-date").value;
        const paymentStatus = document.querySelector('input[name="payment-status"]:checked').value;
        if (isNaN(newPaymentAmount) || newPaymentAmount <= 0 || !date) {
            alert("Please enter a valid amount and payment date.");
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
                console.error(`Failed to save payment: ${res.status} - ${data.detail || 'Unknown error'}`);
                alert(`❌ Failed to save payment: ${data.detail || 'Unknown error'} (Status: ${res.status})`);
                return;
            }
            alert("✅ COD payment recorded");
            modal.style.display = 'none';
            location.reload();
        } catch (err) {
            console.error("❌ Unexpected error:", err);
            alert(`❌ ${err.message}`);
        }
    };
}