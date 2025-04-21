export async function expandLineItems(orderId, iconElement) {
    const currentRow = iconElement.closest("tr");
    const existingDetailRow = document.getElementById(`items-row-${orderId}`);
  
    // Toggle visibility
    if (existingDetailRow) {
      const isHidden = existingDetailRow.style.display === "none";
      existingDetailRow.style.display = isHidden ? "table-row" : "none";
      iconElement.textContent = isHidden ? "⬆️" : "⬇️";
      return;
    }
  
    try {
      const res = await fetch(`/orders/api/items_for_order/${orderId}`);
      if (!res.ok) throw new Error("Failed to fetch line items");
      const data = await res.json();
  
      const newRow = document.createElement("tr");
      newRow.id = `items-row-${orderId}`;
      const cell = document.createElement("td");
      cell.colSpan = currentRow.children.length;
      cell.style.textAlign = "left";
  
      if (!data.items || data.items.length === 0) {
        cell.innerHTML = "<em>No items found for this order.</em>";
      } else {
        const list = data.items.map(item =>
          `• ${item.item_description} — Qty: ${item.qty_ordered}`
        ).join("<br>");
        cell.innerHTML = `<div style="padding: 0.5rem 1rem;">${list}</div>`;
      }
  
      newRow.appendChild(cell);
      currentRow.parentNode.insertBefore(newRow, currentRow.nextSibling);
  
      // Update icon
      iconElement.textContent = "⬆️";
    } catch (err) {
      alert("❌ Could not load order line items");
      console.error(err);
    }
  }
  