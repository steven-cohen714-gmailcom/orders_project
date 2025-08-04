// File: /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/js/components/expand_line_items.js

/**
 * Expands line items for an order or a draft, fetching them from the appropriate endpoint.
 *
 * @param {number} orderId - The ID of the order or draft order.
 * @param {HTMLElement} iconElement - The icon element that was clicked (e.g., ⬇️/⬆️).
 * @param {HTMLElement} detailContainer - The container element where the expanded details will be inserted.
 * @param {object} orderData - The full order object, used for some context.
 * @param {string} [orderType='final'] - Specifies the type of order: 'final' for regular orders, 'draft' for draft orders.
 */
export async function expandLineItemsWithReceipts(orderId, iconElement, detailContainer, orderData, orderType = 'final') {
  console.log(`Expanding ${orderType} line items for ID: ${orderId}`);

  if (!detailContainer) {
    console.error("expandLineItemsWithReceipts: detailContainer is undefined. Cannot proceed.");
    return;
  }

  const isHidden = detailContainer.style.display === "none";
  detailContainer.style.display = isHidden ? "block" : "none";
  iconElement.textContent = isHidden ? "⬆️" : "⬇️";

  // If already expanded and content exists, and we're just collapsing, don't re-fetch.
  // Or if it's currently hidden and has content (meaning it was collapsed), just expand without re-fetching.
  if ((!isHidden && detailContainer.innerHTML !== '') || (isHidden && detailContainer.innerHTML !== '')) {
      return;
  }

  try {
    let fetchUrl;
    let headingText;

    if (orderType === 'draft') {
      fetchUrl = `/draft_orders/api/items/${orderId}`;
      headingText = 'Draft Order Items';
    } else { // Default to 'final'
      fetchUrl = `/orders/api/order_items/${orderId}`;
      headingText = 'Order Items';
    }

    const itemsRes = await fetch(fetchUrl);

    if (!itemsRes.ok) {
      const itemsErr = await itemsRes.text();
      throw new Error(`Fetch error: ${orderType} items ${itemsRes.status} (${itemsErr})`);
    }

    const items = await itemsRes.json();

    let contentHTML = '';

    if (items && items.length > 0) {
      let orderItemsTableHTML = `
        <div class="expanded-section order-items-section" style="margin-bottom: 1rem;">
            <h4 style="margin-bottom: 0.5rem; color: #1a3c5e;">${headingText}</h4>
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
        // Use 'quantity' and 'unit_price' (from orders.py API alias) first,
        // then fall back to 'qty_ordered' and 'price' (from draft_orders.py API direct fields).
        const quantity = item.quantity !== undefined ? item.quantity : item.qty_ordered || 0; 
        const unitPrice = item.unit_price !== undefined ? item.unit_price : item.price || 0; 
        const itemTotal = quantity * unitPrice;

        const itemLabel = item.item_description
          ? `${item.item_code} – ${item.item_description}`
          : item.item_code || "N/A";
        
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
      contentHTML += `<div class="expanded-section"><em>No items found for this ${orderType} order.</em></div>`;
    }

    detailContainer.innerHTML = contentHTML;

  } catch (err) {
    console.error(`❌ Error expanding ${orderType} order details:`, err);
    alert(`❌ Could not expand ${orderType} order details: ${err.message}`);
    if (detailContainer) {
        detailContainer.innerHTML = `<div class="expanded-section" style="color:red;">Error loading details: ${err.message}</div>`;
        detailContainer.style.display = "block";
    }
    iconElement.textContent = "⬇️";
  }
}

// Export all names in a single block without duplicates
export {
  expandLineItemsWithReceipts as expandLineItems,
  expandLineItemsWithReceipts as expandLineItemsForAudit
};