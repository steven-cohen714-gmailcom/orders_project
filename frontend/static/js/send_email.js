document.getElementById('email-po').addEventListener('click', async () => {
    const orderId = currentOrderNumber.replace("URC", "");
    const res = await fetch("/orders/email_purchase_order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_id: parseInt(orderId) })
    });

    if (res.ok) {
        alert("✅ Purchase Order emailed");
    } else {
        const error = await res.json();
        alert("❌ Error: " + (error.detail || "Unknown failure"));
    }
});
