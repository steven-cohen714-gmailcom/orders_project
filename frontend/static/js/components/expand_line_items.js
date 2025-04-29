export async function expandLineItems(orderId, iconElement) {
  console.log(`Expanding line items for order ID: ${orderId}`);
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
    console.log(`Fetching items from /orders/api/items_for_order/${orderId}`);
    const res = await fetch(`/orders/api/items_for_order/${orderId}`);
    console.log(`Response status: ${res.status}`);
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Failed to fetch line items: ${res.status} - ${errorText}`);
    }
    const data = await res.json();
    console.log("Fetched items:", data);

    const newRow = document.createElement("tr");
    newRow.id = `items-row-${orderId}`;
    const cell = document.createElement("td");
    cell.colSpan = currentRow.children.length;
    cell.style.padding = "1rem";

    if (!data.items || data.items.length === 0) {
      console.log("No items found for this order");
      cell.innerHTML = "<em>No items found for this order.</em>";
    } else {
      const table = document.createElement("table");
      table.style.width = "100%";
      table.style.borderCollapse = "collapse";
      table.style.marginTop = "0.5rem";

      const header = document.createElement("tr");
      header.style.backgroundColor = "#f0f0f0";
      header.style.fontWeight = "bold";
      ["Item Code", "Description", "Project Code", "Qty", "Price", "Total"].forEach(text => {
        const th = document.createElement("td");
        th.textContent = text;
        header.appendChild(th);
      });
      table.appendChild(header);

      data.items.forEach(item => {
        const row = document.createElement("tr");

        const cells = [
          item.item_code || "N/A",
          item.item_description || "N/A",
          item.project || "N/A",
          item.qty_ordered || 0,
          item.price != null ? `R${item.price.toFixed(2)}` : "R0.00",
          item.total != null ? `R${item.total.toFixed(2)}` : "R0.00"
        ];

        cells.forEach(text => {
          const td = document.createElement("td");
          td.textContent = text;
          row.appendChild(td);
        });

        table.appendChild(row);
      });

      cell.appendChild(table);
    }

    newRow.appendChild(cell);
    currentRow.parentNode.insertBefore(newRow, currentRow.nextSibling);

    iconElement.textContent = "⬆️";
  } catch (err) {
    console.error("❌ Could not load order line items:", err);
    alert(`❌ Could not load order line items: ${err.message}`);
  }
}