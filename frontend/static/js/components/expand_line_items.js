// Remove the 'export' keyword here
async function expandLineItemsWithReceipts(orderId, iconElement) {
  console.log(`Expanding with receipts for order ID: ${orderId}`);
  const currentRow = iconElement.closest("tr");
  if (!currentRow) {
    throw new Error("Could not find parent table row for icon element.");
  }

  const existingDetailRow = document.getElementById(`receipt-items-row-${orderId}`);
  if (existingDetailRow) {
    const isHidden = existingDetailRow.style.display === "none";
    existingDetailRow.style.display = isHidden ? "table-row" : "none";
    iconElement.textContent = isHidden ? "⬆️" : "⬇️";
    return;
  }

  try {
    const [itemsRes, logsRes] = await Promise.all([
      fetch(`/orders/api/items_for_order/${orderId}`),
      fetch(`/orders/api/receipt_logs/${orderId}`)
    ]);

    if (!itemsRes.ok || !logsRes.ok) {
      const itemsError = itemsRes.ok ? "" : await itemsRes.text();
      const logsError = logsRes.ok ? "" : await logsRes.text();
      throw new Error(
        `Fetch error: items ${itemsRes.status} (${itemsError}), logs ${logsRes.status} (${logsError})`
      );
    }

    const itemsData = await itemsRes.json().catch((err) => {
      throw new Error(`Failed to parse items JSON: ${err.message}`);
    });
    const logsData = await logsRes.json().catch((err) => {
      throw new Error(`Failed to parse logs JSON: ${err.message}`);
    });
    const receiptLogs = logsData.logs || [];

    const logMap = {};
    for (const log of receiptLogs) {
      if (!log.order_item_id) {
        console.warn(`Skipping log with missing order_item_id:`, log);
        continue;
      }
      if (!logMap[log.order_item_id]) logMap[log.order_item_id] = [];
      logMap[log.order_item_id].push(log);
    }

    const newRow = document.createElement("tr");
    newRow.id = `receipt-items-row-${orderId}`;
    const cell = document.createElement("td");
    cell.colSpan = currentRow.children.length;
    cell.style.padding = "1rem";

    if (!itemsData.items || itemsData.items.length === 0) {
      cell.innerHTML = "<em>No items found.</em>";
    } else {
      const table = document.createElement("table");
      table.style.width = "100%";
      table.style.borderCollapse = "collapse";
      table.style.marginTop = "0.5rem";

      const header = document.createElement("tr");
      header.style.backgroundColor = "#f0f0f0";
      header.style.fontWeight = "bold";
      ["Item Code", "Description", "Qty Ordered", "Price", "Total", "Receipts"].forEach((text) => {
        const th = document.createElement("td");
        th.textContent = text;
        header.appendChild(th);
      });
      table.appendChild(header);

      itemsData.items.forEach((item) => {
        const row = document.createElement("tr");

        const cells = [
          item.item_code || "N/A",
          item.item_description || "N/A",
          item.qty_ordered || 0,
          typeof item.price === "number" ? `R${item.price.toFixed(2)}` : "R0.00",
          typeof item.total === "number" ? `R${item.total.toFixed(2)}` : "R0.00",
        ];

        cells.forEach((text) => {
          const td = document.createElement("td");
          td.textContent = text;
          row.appendChild(td);
        });

        const logCell = document.createElement("td");
        const logs = logMap[item.id] || [];
        if (logs.length === 0) {
          logCell.textContent = "-";
        } else {
          const subTable = document.createElement("table");
          subTable.style.width = "100%";
          subTable.style.borderCollapse = "collapse";
          const subHeader = document.createElement("tr");
          ["Qty", "Date", "User"].forEach((label) => {
            const sh = document.createElement("td");
            sh.style.fontWeight = "bold";
            sh.textContent = label;
            subHeader.appendChild(sh);
          });
          subTable.appendChild(subHeader);

          logs.forEach((log) => {
            const logRow = document.createElement("tr");
            [log.qty_received, log.received_date, log.username || "N/A"].forEach((val) => {
              const td = document.createElement("td");
              td.textContent = val || "N/A";
              logRow.appendChild(td);
            });
            subTable.appendChild(logRow);
          });

          logCell.appendChild(subTable);
        }

        row.appendChild(logCell);
        table.appendChild(row);
      });

      cell.appendChild(table);
    }

    newRow.appendChild(cell);
    if (!currentRow.parentNode) {
      throw new Error("Parent node for current row not found.");
    }
    currentRow.parentNode.insertBefore(newRow, currentRow.nextSibling);
    iconElement.textContent = "⬆️";
  } catch (err) {
    console.error("❌ Error expanding received order:", err);
    alert(`❌ Could not expand received order: ${err.message}`);
  }
}

// Export all names in a single block
export {
  expandLineItemsWithReceipts,
  expandLineItemsWithReceipts as expandLineItems,
  expandLineItemsWithReceipts as expandLineItemsForAudit,
};