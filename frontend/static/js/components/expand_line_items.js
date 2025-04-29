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
    cell.style.padding = "1rem";

    if (!data.items || data.items.length === 0) {
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
          item.item_code,
          item.item_description,
          item.project,
          item.qty_ordered,
          `R${item.price.toFixed(2)}`,
          `R${(item.qty_ordered * item.price).toFixed(2)}`
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
    alert("❌ Could not load order line items");
  }
}