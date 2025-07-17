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

    let contentHTML = `
      <div class="audit-events" style="margin-bottom: 1rem;">
        <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
          <thead>
            <tr style="background:#f0f0f0; font-weight:bold;">
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">Activity</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">Date</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">User</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">Details</td>
            </tr>
          </thead>
          <tbody>
    `;

    if (auditHistory && auditHistory.length > 0) {
      // Sort audit history chronologically (oldest first)
      auditHistory.sort((a, b) => new Date(a.action_date) - new Date(b.action_date));

      auditHistory.forEach(entry => {
        const formattedDate = entry.action_date ? new Date(entry.action_date).toLocaleDateString('en-ZA') : 'N/A';
        const user = entry.username || 'Unknown';
        const activity = entry.action;

        let details = '';

        switch (entry.action) {
          case 'Created':
            details = 'Order created';
            break;
          case 'Authorised':
            details = 'Order authorised';
            break;
          case 'Received':
            details = 'Order received';
            // Parse details for items received
            let receivedItems = [];
            try {
              const detailsContent = entry.details.replace('Order received: ', '');
              receivedItems = JSON.parse(detailsContent) || [];
            } catch (e) {
              console.error('Error parsing received details:', e);
            }
            if (receivedItems.length > 0) {
              details += '<ul style="margin-top: 0.5rem; padding-left: 1.5rem;">';
              receivedItems.forEach(recItem => {
                const itemData = items.find(i => i.id === recItem.item_id);
                const itemLabel = itemData ? `${itemData.item_code} – ${itemData.item_description || ''}` : 'Unknown Item';
                details += `<li>${itemLabel}: ${recItem.received_qty} qty</li>`;
              });
              details += '</ul>';
            }
            break;
          case 'Marked COD Paid':
            const amountMatch = entry.details.match(/Amount: R([\d.,]+)/);
            const amount = amountMatch ? amountMatch[1] : 'Unknown';
            const dateMatch = entry.details.match(/Date: ([\d-]+)/);
            const payDate = dateMatch ? dateMatch[1] : 'Unknown';
            details = `Paid: Amount R${amount}, Date: ${payDate}`;
            break;
          case 'Emailed':
            const emailMatch = entry.details.match(/emailed to ([\w.@]+)/);
            const email = emailMatch ? emailMatch[1] : 'Unknown';
            details = `Purchase order ${orderData.order_number} emailed to ${email}`;
            break;
          case 'Deleted':
            details = 'Order deleted';
            break;
          default:
            details = entry.details || 'No details';
            break;
        }

        contentHTML += `
          <tr>
            <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${activity}</td>
            <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${formattedDate}</td>
            <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${user}</td>
            <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${details}</td>
          </tr>
        `;
      });
    } else {
      contentHTML += `
        <tr>
          <td colspan="4" style="text-align:center; padding: 0.5rem; border: 1px solid #ddd;">No audit trail available for this order.</td>
        </tr>
      `;
    }

    contentHTML += `
          </tbody>
        </table>
      </div>
    `;

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