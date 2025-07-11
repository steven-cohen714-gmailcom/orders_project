// File: /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/js/components/expand_line_items.js

// Remove the 'export' keyword here
// MODIFIED: Added detailContainer and orderHeaderData to parameters
async function expandLineItemsWithReceipts(orderId, iconElement, detailContainer, orderHeaderData) {
  console.log(`Expanding with receipts for order ID: ${orderId}`);

  // Toggle if content already exists and is visible/hidden
  const isHidden = detailContainer.style.display === "none";
  detailContainer.style.display = isHidden ? "block" : "none"; // Use 'block' for div visibility
  iconElement.textContent = isHidden ? "⬆️" : "⬇️"; // Toggle icon immediately

  // If we're hiding, or if content already exists, just toggle and return
  if (!isHidden && detailContainer.innerHTML !== '') {
      return;
  }
  if (isHidden && detailContainer.innerHTML !== '') {
      return;
  }

  try {
    // ── Fetch items, receipt logs, AND main order details in parallel ───────────────────────────────
    const [itemsRes, logsRes, orderDetailsRes] = await Promise.all([
      fetch(`/orders/api/order_items/${orderId}`),
      fetch(`/orders/api/receipt_logs/${orderId}`),
      fetch(`/orders/api/order_details_for_audit/${orderId}`)
    ]);

    if (!itemsRes.ok || !logsRes.ok || !orderDetailsRes.ok) {
      const itemsErr = itemsRes.ok ? "" : await itemsRes.text();
      const logsErr  = logsRes.ok  ? "" : await logsRes.text();
      const orderDetailsErr = orderDetailsRes.ok ? "" : await orderDetailsRes.text();
      throw new Error(`Fetch error: items ${itemsRes.status} (${itemsErr}), logs ${logsRes.status} (${logsErr}), order details ${orderDetailsRes.status} (${orderDetailsErr})`);
    }

    const items = await itemsRes.json();
    const logsData  = await logsRes.json();
    const orderData = await orderDetailsRes.json(); // This is the object containing 'total', 'supplier_name', 'paid_by_user'
    const receiptLogs = logsData.logs || [];

    // ── Group logs by order_item_id for quick look-up ────────────────────────
    const logMap = {};
    for (const log of receiptLogs) {
      if (!log.order_item_id) continue;
      if (!logMap[log.order_item_id]) logMap[log.order_item_id] = [];
      logMap[log.order_item_id].push(log);
    }

    let contentHTML = '';

    // MODIFIED: Re-structure Payment Details as a table section with robust data handling
    // Check if amount_paid is a valid number, otherwise default to 0 for formatting
    const rawPaidAmount = parseFloat(orderData.amount_paid);
    if (!isNaN(rawPaidAmount) && orderData.payment_date) { // Only display if valid amount and date exist
        const formattedPaidAmount = `R${rawPaidAmount.toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const formattedPaymentDate = new Date(orderData.payment_date).toLocaleDateString('en-ZA');
        
        // --- FIX START: Use orderData for values fetched from backend ---
        const paidByUser = orderData.paid_by_user || ''; // Corrected: Reading from orderData
        const rawOriginalTotal = parseFloat(orderData.total); // Corrected: Reading from orderData
        const originalTotal = !isNaN(rawOriginalTotal) ? `R${rawOriginalTotal.toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : '';
        const supplierName = orderData.supplier_name || ''; // Corrected: Reading from orderData and using 'supplier_name'
        // --- FIX END ---


        contentHTML += `
            <div class="expanded-section payment-table-section">
                <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
                    <thead>
                        <tr style="background:#e6f7ff;font-weight:bold;">
                            <td style="text-align:left;">Date Paid</td>
                            <td style="text-align:right;">Original Amount</td>
                            <td style="text-align:left;">Supplier</td>
                            <td style="text-align:right;">Paid Amount</td>
                            <td style="text-align:left;">User</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="text-align:left;">${formattedPaymentDate}</td>
                            <td style="text-align:right;">${originalTotal}</td>
                            <td style="text-align:left;">${supplierName}</td>
                            <td style="text-align:right;">${formattedPaidAmount}</td>
                            <td style="text-align:left;">${paidByUser}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="height: 1rem;"></div> `;
    }

    if (!items || items.length === 0) {
      contentHTML += `<div class="expanded-section"><em>No items found.</em></div>`;
    } else {
      let tableHTML = `
        <div class="expanded-section items-table-section">
            <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
              <thead>
                <tr style="background:#f0f0f0;font-weight:bold">
                  <td style="text-align:left;">Item</td>
                  <td style="text-align:left;">Project</td>
                  <td style="text-align:right;">Qty</td>
                  <td style="text-align:right;">Price</td>
                  <td style="text-align:right;">Total</td>
                  <td style="text-align:left;">Receipts</td>
                </tr>
              </thead>
              <tbody>
          `;

      items.forEach(item => {
        const itemLabel = item.item_description
          ? `${item.item_code} – ${item.item_description}`
          : item.item_code || "N/A";

        const quantity = item.quantity || 0;
        const unitPrice = item.unit_price || 0;
        const total = quantity * unitPrice;

        const projectLabel = item.project_name
          ? `${item.project} – ${item.project_name}`
          : item.project || "N/A";

        const formattedPrice = `R${parseFloat(unitPrice).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const formattedTotal = `R${parseFloat(total).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;


        const logs = logMap[item.id] || [];
        let receiptLogHTML = '-';
        if (logs.length > 0) {
          receiptLogHTML = `
            <table style="width: 100%; border-collapse: collapse;">
              <thead>
                <tr style="font-weight:bold">
                  <td style="text-align:right;">Qty</td>
                  <td style="text-align:left;">Date</td>
                  <td style="text-align:left;">User</td>
                </tr>
              </thead>
              <tbody>
          `;
          logs.forEach(log => {
            receiptLogHTML += `
              <tr>
                <td style="text-align:right;">${log.qty_received || "N/A"}</td>
                <td style="text-align:left;">${log.received_date || "N/A"}</td>
                <td>${log.username || "N/A"}</td>
              </tr>
            `;
          });
          receiptLogHTML += `
              </tbody>
            </table>
          `;
        }

        tableHTML += `
          <tr>
            <td style="text-align:left;">${itemLabel}</td>
            <td style="text-align:left;">${projectLabel}</td>
            <td style="text-align:right;">${quantity}</td>
            <td style="text-align:right;">${formattedPrice}</td>
            <td style="text-align:right;">${formattedTotal}</td>
            <td style="text-align:left;">${receiptLogHTML}</td>
          </tr>
        `;
      });

      tableHTML += `
              </tbody>
            </table>
        </div>
      `;
      contentHTML += tableHTML;
    }

    detailContainer.innerHTML = contentHTML;

  } catch (err) {
    console.error("❌ Error expanding order details:", err);
    alert(`❌ Could not expand order details: ${err.message}`);
    detailContainer.innerHTML = `<div class="expanded-section" style="color:red;">Error loading details: ${err.message}</div>`;
    detailContainer.style.display = "block";
    iconElement.textContent = "⬇️";
  }
}

// Export all names in a single block
export {
  expandLineItemsWithReceipts,
  expandLineItemsWithReceipts as expandLineItems,
  expandLineItemsWithReceipts as expandLineItemsForAudit
};