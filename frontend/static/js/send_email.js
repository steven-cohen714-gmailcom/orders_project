export async function emailPurchaseOrder(orderId, orderNumber) {
    /**
     * Send a purchase order email for the given order ID.
     *
     * @param {number} orderId - The ID of the order
     * @param {string} orderNumber - The order number for display
     */
    try {
        const response = await fetch(`/orders/email_purchase_order/${orderId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include"
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to send email");
        }

        const data = await response.json();
        alert(data.detail || `✅ Purchase Order ${orderNumber} emailed successfully`);
    } catch (error) {
        console.error(`Error emailing purchase order ${orderNumber}:`, error);
        alert(`❌ Error emailing purchase order ${orderNumber}: ${error.message}`);
    }
}

// For new_order.js compatibility
document.getElementById('email-po')?.addEventListener('click', async () => {
    const orderNumber = document.getElementById('order-number')?.textContent || "Unknown";
    const orderIdMatch = orderNumber.match(/URC(\d+)/);
    if (!orderIdMatch) {
        alert("❌ Invalid order number format");
        return;
    }
    const orderId = parseInt(orderIdMatch[1], 10);
    await emailPurchaseOrder(orderId, orderNumber);
});