/**
 * Sends an email containing a purchase order PDF generated from raw HTML.
 *
 * @param {string} html - The full HTML string to convert into a PDF.
 * @param {string} orderNumber - The order number (e.g. "URC1024").
 * @param {string} recipientEmail - The supplier’s email address.
 */
export async function emailPurchaseOrder(html, orderNumber, recipientEmail) {
    try {
      const response = await fetch("/orders/email_purchase_order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          html: html,
          order_number: orderNumber,
          recipient_email: recipientEmail
        })
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Email sending failed");
      }
  
      const result = await response.json();
      alert(result.message || `✅ Purchase Order ${orderNumber} emailed successfully`);
    } catch (error) {
      console.error(`❌ Failed to email PO ${orderNumber}:`, error);
      alert(`❌ Error emailing PO ${orderNumber}: ${error.message}`);
    }
  }
  