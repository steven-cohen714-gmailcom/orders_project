// File: /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/js/audit_trail_expand.js

export async function expandAuditTrailDetails(orderId, iconElement, detailContainer) {
  console.log(`Expanding Audit Trail details for order ID: ${orderId}`);

  if (!detailContainer) {
    console.error("expandAuditTrailDetails: detailContainer is undefined. Cannot proceed.");
    return;
  }

  const isHidden = detailContainer.style.display === "none";
  detailContainer.style.display = isHidden ? "block" : "none";
  iconElement.textContent = isHidden ? "⬆️" : "⬇️";

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

    const logMap = {};
    for (const log of receiptLogs) {
      if (!log.order_item_id) continue;
      if (!logMap[log.order_item_id]) logMap[log.order_item_id] = [];
      logMap[log.order_item_id].push(log);
    }

    let contentHTML = '';

    // --- RESTRUCTURE TO MATCH MOCKUP (image_fab87e.png) ---

    // 1. Order Items Section
    if (items && items.length > 0) {
      let orderItemsTableHTML = `
        <div class="expanded-section order-items-section" style="margin-bottom: 1rem;">
            <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Order Items</h4>
            <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
              <thead>
                <tr style="background:#f0f0f0;font-weight:bold">
                  <td style="text-align:left;">Item</td>
                  <td style="text-align:left;">Project</td>
                  <td style="text-align:right;">Qty</td>
                  <td style="text-align:right;">Price</td>
                  <td style="text-align:right;">Total</td>
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
        const itemTotal = quantity * unitPrice; 

        const projectLabel = item.project || "N/A"; 

        const formattedPrice = `R${parseFloat(unitPrice).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const formattedTotal = `R${parseFloat(itemTotal).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

        orderItemsTableHTML += `
          <tr>
            <td style="text-align:left;">${itemLabel}</td>
            <td style="text-align:left;">${projectLabel}</td>
            <td style="text-align:right;">${quantity}</td>
            <td style="text-align:right;">${formattedPrice}</td>
            <td style="text-align:right;">${formattedTotal}</td>
          </tr>
        `;
      });
      orderItemsTableHTML += `
              </tbody>
            </table>
        </div>
      `;
      contentHTML += orderItemsTableHTML;
    } else {
      contentHTML += `<div class="expanded-section"><em>No items found.</em></div>`;
    }


    // 2. Receipts Section (Display only if there are logs)
    if (receiptLogs && receiptLogs.length > 0) {
      let receiptsTableHTML = `
        <div class="expanded-section receipts-section" style="margin-bottom: 1rem;">
            <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Receipts</h4>
            <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
              <thead>
                <tr style="background:#f0f0f0;font-weight:bold">
                  <td style="text-align:left;">Item</td>
                  <td style="text-align:left;">Receipt Date</td>
                  <td style="text-align:right;">Qty</td>
                  <td style="text-align:left;">User</td>
                </tr>
              </thead>
              <tbody>
          `;
          
          receiptLogs.forEach(log => {
              const receivedItem = items.find(item => item.id === log.order_item_id);
              const receivedItemLabel = receivedItem ? `${receivedItem.item_code} – ${receivedItem.item_description}` : 'N/A';
              const formattedReceivedDate = log.received_date ? new Date(log.received_date).toLocaleDateString('en-ZA') : 'N/A';

              receiptsTableHTML += `
                <tr>
                  <td style="text-align:left;">${receivedItemLabel}</td>
                  <td style="text-align:left;">${formattedReceivedDate}</td>
                  <td style="text-align:right;">${log.qty_received || 'N/A'}</td>
                  <td>${log.username || 'N/A'}</td>
                </tr>
              `;
          });
          receiptsTableHTML += `
              </tbody>
            </table>
        </div>
      `;
      contentHTML += receiptsTableHTML;
    }


    // 3. Payment Details Section
    const rawPaidAmount = parseFloat(orderData.amount_paid);
    const hasPayment = !isNaN(rawPaidAmount) && rawPaidAmount > 0 && orderData.payment_date;

    if (hasPayment) { 
        const formattedPaidAmount = `R${rawPaidAmount.toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const formattedPaymentDate = orderData.payment_date ? new Date(orderData.payment_date).toLocaleDateString('en-ZA') : 'N/A';
        const paidByUser = orderData.paid_by_user || 'N/A'; 

        contentHTML += `
            <div class="expanded-section payment-table-section" style="margin-bottom: 1rem;">
                <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Payment Details</h4>
                <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
                    <thead>
                        <tr style="background:#e6f7ff;font-weight:bold;">
                            <td style="text-align:left;">Payment Date</td>
                            <td style="text-align:right;">Amt Paid</td>
                            <td style="text-align:left;">User</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="text-align:left;">${formattedPaymentDate}</td>
                            <td style="text-align:right;">${formattedPaidAmount}</td>
                            <td style="text-align:left;">${paidByUser}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="height: 1rem;"></div> `;
    } else {
        contentHTML += `
            <div class="expanded-section payment-table-section" style="margin-bottom: 1rem;">
                <p>No valid payment details available for this order.</p>
            </div>
            <div style="height: 1rem;"></div>
        `;
    }

    // 4. Authorisation Details Section
    const authorisedEntry = auditHistory.find(entry => entry.action === 'Authorised');
    if (authorisedEntry) {
        const formattedAuthDate = authorisedEntry.action_date ? new Date(authorisedEntry.action_date).toLocaleDateString('en-ZA') : 'N/A';
        const authorisedByUser = authorisedEntry.username || 'N/A';

        contentHTML += `
            <div class="expanded-section authorisation-section" style="margin-bottom: 1rem;">
                <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">Authorisation Details</h4>
                <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
                    <thead>
                        <tr style="background:#e6f7ff;font-weight:bold;">
                            <td style="text-align:left;">Authorised Date</td>
                            <td style="text-align:left;">User</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="text-align:left;">${formattedAuthDate}</td>
                            <td style="text-align:left;">${authorisedByUser}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="height: 1rem;"></div>
        `;
    } else {
         contentHTML += `
            <div class="expanded-section authorisation-section" style="margin-bottom: 1rem;">
                <p>No authorisation details available for this order.</p>
            </div>
            <div style="height: 1rem;"></div>
        `;
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