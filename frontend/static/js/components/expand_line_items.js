// File: /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/js/components/expand_line_items.js

export async function expandLineItemsWithReceipts(orderId, iconElement, detailContainer) {
  console.log(`Expanding line items for order ID: ${orderId}`);

  if (!detailContainer) {
    console.error("expandLineItemsWithReceipts: detailContainer is undefined. Cannot proceed.");
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
    const itemsRes = await fetch(`/orders/api/order_items/${orderId}`);

    if (!itemsRes.ok) {
      const itemsErr = await itemsRes.text();
      throw new Error(`Fetch error: items ${itemsRes.status} (${itemsErr})`);
    }

    const items = await itemsRes.json();

    let contentHTML = '';

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
        const quantity = item.quantity || 0; // 'quantity' is aliased from qty_ordered in backend
        const unitPrice = item.unit_price || 0; // 'unit_price' is aliased from price in backend
        const itemTotal = quantity * unitPrice; // Recalculate for display consistency

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

// Export all names in a single block without duplicates
export {
  expandLineItemsWithReceipts as expandLineItems,
  expandLineItemsWithReceipts as expandLineItemsForAudit
};
