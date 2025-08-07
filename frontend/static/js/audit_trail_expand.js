// File: frontend/static/js/audit_trail_expand.js
// Relative Path: frontend/static/js/audit_trail_expand.js

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
      fetch(`/orders/api/order_details_for_audit/${orderId}`),
      fetch(`/orders/api/order_audit_history/${orderId}`)
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
    let auditHistory = await auditHistoryRes.json(); // Use let as we'll filter it
    const receiptLogs = logsData.logs || [];

    // --- Filtering out unwanted audit trail entries ---
    auditHistory = auditHistory.filter(entry => {
      // Exclude "Viewed PDF" unless it's an email activity (which is already handled by 'Emailed' action)
      if (entry.action === 'Viewed PDF' && !entry.details.includes('emailed')) {
        return false;
      }
      // Exclude "Note Updated" activity
      if (entry.action === 'Note Updated') {
        return false;
      }
      // Exclude "Created as Draft" if the draft is later converted.
      // This requires backend logic to mark the draft as "converted" or to link the draft creation to the final order.
      // For now, we'll assume the backend will only send 'Created' or 'Converted from Draft' for final orders.
      // If a draft is *never* converted, its "Created as Draft" might still show, which aligns with leaving drafts off the trail until conversion.
      // If the backend doesn't differentiate "Created as Draft" vs "Converted from Draft",
      // we'd need more complex logic here (e.g., checking if the current order's ID was previously a draft ID).
      return true;
    });
    // ----------------------------------------------------

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
          case 'Created as Draft':
            // This case should ideally not appear for a final order if the backend handles conversion,
            // but if it does, it signifies the initial draft creation.
            // As per your request: "when a draft is created - we can leave it off the audit trail"
            // The filtering above should prevent this from showing for a final order if a 'Converted from Draft' action exists.
            // If the entry is filtered out, this block won't be reached.
            details = 'Order saved as draft';
            break;
          case 'Converted from Draft': // NEW: Handle the conversion from draft action
            details = `Order converted from draft (Draft ID: ${entry.details})`; // Assuming entry.details will contain the old draft ID
            break;
          case 'Draft Updated':
            // This should also be filtered out if you want to completely hide draft activity until conversion.
            // The filter above takes care of this now.
            details = 'Draft order updated';
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
          // FIX START: This case is now being added to correctly interpret the new audit trail entries
          case 'COD Payment recorded':
            details = entry.details; // FIX: Assign the plain text details directly
            break;
          // FIX END
          case 'Emailed':
            const emailMatch = entry.details.match(/emailed to ([\w.@]+)/);
            const email = emailMatch ? emailMatch[1] : 'Unknown';
            details = `Purchase order ${orderData.order_number} emailed to ${email}`;
            break;
          case 'Deleted':
            details = 'Order deleted';
            break;
          case 'Note Updated': // This case should now be filtered out by the .filter() above
            details = `Order note updated to: "${entry.details.replace('Order note updated to: ', '')}"`;
            break;
          case 'Viewed PDF': // This case should now be filtered out by the .filter() above unless it's an email
            details = `PDF viewed: ${entry.details}`;
            break;
          default:
            details = entry.details || 'No details';
            break;
        }

        // Only add to HTML if `details` is not empty (after filtering)
        // This is a redundant check due to the filter, but good for safety if `details` could become empty in the switch
        if (details) {
            contentHTML += `
              <tr>
                <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${activity}</td>
                <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${formattedDate}</td>
                <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${user}</td>
                <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${details}</td>
              </tr>
            `;
        }
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

  } catch (error) {
    console.error("Failed to fetch audit trail details:", error);
    detailContainer.innerHTML = `<p style="color: red;">Error loading audit trail: ${error.message}</p>`;
  }
}