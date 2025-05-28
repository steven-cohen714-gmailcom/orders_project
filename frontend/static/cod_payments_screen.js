// File: frontend/static/js/cod_payments_screen.js

console.log("💰 COD Payments screen loaded");

document.addEventListener("DOMContentLoaded", () => {
  loadCODOrders();

  document.getElementById("filter-btn").addEventListener("click", loadCODOrders);
  document.getElementById("modal-cancel").addEventListener("click", () => {
    document.getElementById("payment-modal").classList.add("hidden");
  });

  document.getElementById("payment-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const orderId = document.getElementById("modal-order-id").value;
    const paymentDate = document.getElementById("modal-payment-date").value;
    const amountPaid = document.getElementById("modal-amount-paid").value;

    const response = await fetch("/orders/api/mark_cod_paid", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ order_id: orderId, payment_date: paymentDate, amount_paid: parseFloat(amountPaid) })
    });

    if (response.ok) {
      alert("✅ Payment recorded successfully.");
      document.getElementById("payment-modal").classList.add("hidden");
      loadCODOrders();
    } else {
      alert("❌ Error recording payment.");
    }
  });
});

async function loadCODOrders() {
  const tbody = document.getElementById("payments-body");
  tbody.innerHTML = "";

  try {
    const response = await fetch("/orders/api/cod_orders");
    const data = await response.json();

    data.forEach(order => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${order.order_number}</td>
        <td>${order.supplier_name}</td>
        <td>${formatDate(order.created_date)}</td>
        <td>R ${order.total.toFixed(2)}</td>
        <td>${order.payment_terms}</td>
        <td>${order.payment_date || "—"}</td>
        <td>${order.amount_paid ? `R ${order.amount_paid.toFixed(2)}` : "—"}</td>
        <td>
          ${!order.payment_date ? `<button class="mark-paid-btn" data-id="${order.id}" data-total="${order.total}">Mark Paid</button>` : "✅ Paid"}
        </td>
      `;
      tbody.appendChild(tr);
    });

    document.querySelectorAll(".mark-paid-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.getElementById("modal-order-id").value = btn.dataset.id;
        document.getElementById("modal-amount-paid").value = btn.dataset.total;
        document.getElementById("modal-payment-date").value = new Date().toISOString().split("T")[0];
        document.getElementById("payment-modal").classList.remove("hidden");
      });
    });
  } catch (err) {
    console.error("Failed to load COD orders:", err);
    alert("❌ Failed to load COD orders.");
  }
}

function formatDate(dateStr) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-GB");
}
