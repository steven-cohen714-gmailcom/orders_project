// File: /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/js/components/expand_line_items.js

// Remove the 'export' keyword here
// MODIFIED: Make detailContainer and orderHeaderData optional with default values or checks
async function expandLineItemsWithReceipts(orderId, iconElement, detailContainer, orderHeaderData) {
  console.log(`Expanding with receipts for order ID: ${orderId}`);

  // Safely check if detailContainer exists before accessing its properties
  if (!detailContainer) {
    console.error("expandLineItemsWithReceipts: detailContainer is undefined. Cannot proceed.");
    return;
  }

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
    // ── Fetch all necessary data in parallel ───────────────────────────────
    const [itemsRes, logsRes, orderDetailsRes, auditHistoryRes] = await Promise.all([
      fetch(`/orders/api/order_items/${orderId}`),
      fetch(`/orders/api/receipt_logs/${orderId}`),
      fetch(`/orders/api/order_details_for_audit/${orderId}`), // Fetches summary data including created_by_user, paid_by_user
      fetch(`/orders/api/order_audit_history/${orderId}`) // Fetches full chronological audit log
    ]);

    if (!itemsRes.ok || !logsRes.ok || !orderDetailsRes.ok || !auditHistoryRes.ok) {
      const itemsErr = itemsRes.ok ? "" : await itemsRes.text();
      const logsErr  = logsRes.ok  ? "" : await logsRes.text();
      const orderDetailsErr = orderDetailsRes.ok ? "" : await orderDetailsRes.text();
      const auditHistoryErr = auditHistoryRes.ok ? "" : await auditHistoryRes.text();
      throw new Error(`Fetch error: items ${itemsRes.status} (${itemsErr}), logs ${logsRes.status} (${logsErr}), order details ${orderDetailsRes.status} (${orderDetailsErr}), audit history ${auditHistoryRes.status} (${auditHistoryErr})`);
    }

    const items = await itemsRes.json();
    const logsData  = await logsRes.json();
    const orderData = await orderDetailsRes.json(); 
    const auditHistory = await auditHistoryRes.json(); 
    const receiptLogs = logsData.logs || [];

    // ── Group logs by order_item_id for quick look-up ────────────────────────
    const logMap = {};
    for (const log of receiptLogs) {
      if (!log.order_item_id) continue;
      if (!logMap[log.order_item_id]) logMap[log.order_item_id] = [];
      logMap[log.order_item_id].push(log);
    }

    let contentHTML = '';

    // NEW: Order Summary Details (Order Number, Requester, Dates, Created By)
    const formattedCreatedDate = orderData.created_date ? new Date(orderData.created_date).toLocaleDateString('en-ZA') : 'N/A';
    const formattedReceivedDate = orderData.received_date ? new Date(orderData.received_date).toLocaleDateString('en-ZA') : 'N/A';
    const createdByUser = orderData.created_by_user || 'N/A';
    const requesterName = orderData.requester_name || 'N/A'; 
    const orderNumber = orderData.order_number || 'N/A';

    contentHTML += `
        <div class="expanded-section order-summary-details" style="margin-bottom: 1rem;">
            <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Order Summary</h4>
            <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
                <thead>
                    <tr style="background:#e6f7ff;font-weight:bold;">
                        <td style="text-align:left;">Order Number</td>
                        <td style="text-align:left;">Requester</td>
                        <td style="text-align:left;">Created Date</td>
                        <td style="text-align:left;">Created By</td>
                        <td style="text-align:left;">Received Date</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="text-align:left;">${orderNumber}</td>
                        <td style="text-align:left;">${requesterName}</td>
                        <td style="text-align:left;">${formattedCreatedDate}</td>
                        <td style="text-align:left;">${createdByUser}</td>
                        <td style="text-align:left;">${formattedReceivedDate}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div style="height: 1rem;"></div>
    `;

    // Payment Details Section
    const rawPaidAmount = parseFloat(orderData.amount_paid);
    if (!isNaN(rawPaidAmount) && orderData.payment_date) { 
        const formattedPaidAmount = `R${rawPaidAmount.toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const formattedPaymentDate = new Date(orderData.payment_date).toLocaleDateString('en-ZA');
        
        const paidByUser = orderData.paid_by_user || 'N/A'; 
        const rawOriginalTotal = parseFloat(orderData.total);
        const originalTotal = !isNaN(rawOriginalTotal) ? `R${rawOriginalTotal.toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : 'R0.00';
        const supplierName = orderData.supplier_name || 'N/A';

        contentHTML += `
            <div class="expanded-section payment-table-section">
                <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Payment Details</h4>
                <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
                    <thead>
                        <tr style="background:#e6f7ff;font-weight:bold;">
                            <td style="text-align:left;">Date Paid</td>
                            <td style="text-align:right;">Original Amount</td>
                            <td style="text-align:left;">Supplier</td>
                            <td style="text-align:right;">Paid Amount</td>
                            <td style="text-align:left;">Paid By</td> 
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
    } else {
        contentHTML += `
            <div class="expanded-section payment-table-section">
                <p>No valid payment details available for this order.</p>
            </div>
            <div style="height: 1rem;"></div>
        `;
    }

    // Order Items Section
    if (!items || items.length === 0) {
      contentHTML += `<div class="expanded-section"><em>No items found.</em></div>`;
    } else {
      let tableHTML = `
        <div class="expanded-section items-table-section">
            <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Order Items</h4>
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

        const quantity = item.qty_ordered || 0; // Use qty_ordered for original quantity
        const unitPrice = item.price || 0;
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
                <td style="text-align:left;">${log.received_date ? new Date(log.received_date).toLocaleDateString('en-ZA') : "N/A"}</td>
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
    
    // NEW: Full Audit History Section
    if (auditHistory && auditHistory.length > 0) {
        let auditHistoryHTML = `
            <div class="expanded-section audit-history-section" style="margin-top: 1rem;">
                <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Full Audit History</h4>
                <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
                    <thead>
                        <tr style="background:#f0f8ff;font-weight:bold;">
                            <td style="text-align:left;">Date</td>
                            <td style="text-align:left;">Action</td>
                            <td style="text-align:left;">Details</td>
                            <td style="text-align:left;">User</td>
                        </tr>
                    </thead>
                    <tbody>
        `;
        auditHistory.forEach(entry => {
            const formattedActionDate = entry.action_date ? new Date(entry.action_date).toLocaleString('en-ZA', { dateStyle: 'short', timeStyle: 'short' }) : 'N/A';
            auditHistoryHTML += `
                        <tr>
                            <td style="text-align:left;">${formattedActionDate}</td>
                            <td style="text-align:left;">${entry.action || 'N/A'}</td>
                            <td style="text-align:left;">${entry.details || 'N/A'}</td>
                            <td style="text-align:left;">${entry.username || 'N/A'}</td>
                        </tr>
            `;
        });
        auditHistoryHTML += `
                    </tbody>
                </table>
            </div>
        `;
        contentHTML += auditHistoryHTML;
    }


    detailContainer.innerHTML = contentHTML;

  } catch (err) {
    console.error("❌ Error expanding order details:", err);
    alert(`❌ Could not expand order details: ${err.message}`);
    if (detailContainer) {
        detailContainer.innerHTML = `<div class="expanded-section" style="color:red;">Error loading details: ${err.message}</div>`;
        detailContainer.style.display = "block";
    }
    iconElement.textContent = "⬇️";
  }
}

// Export all names in a single block
export {
  expandLineItemsWithReceipts,
  expandLineItemsWithReceipts as expandLineItems,
  expandLineItemsWithReceipts as expandLineItemsForAudit
};