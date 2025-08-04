// File: frontend/static/js/components/expand_requisition_items.js

export function expandRequisitionItems(row, requisitionId) {
  const existing = row.nextElementSibling;
  if (existing && existing.classList.contains("expanded-row")) {
    existing.remove();
    return;
  }

  fetch(`/api/requisition_items/${requisitionId}`)
    .then((res) => res.json())
    .then((data) => {
      const items = data.items || [];
      const colspan = row.children.length;

      const tr = document.createElement("tr");
      tr.classList.add("expanded-row");

      const td = document.createElement("td");
      td.colSpan = colspan;

      if (items.length === 0) {
        td.textContent = "No line items found.";
      } else {
        const table = document.createElement("table");
        table.style.width = "100%";
        table.style.marginTop = "0.5rem";
        table.innerHTML = `
          <thead>
            <tr>
              <th>Item Code</th>
              <th>Description</th>
              <th>Project</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            ${items
              .map(
                (item) => `
              <tr>
                <td>${item.item_code || "-"}</td>
                <td>${item.item_description || item.description || "-"}</td>
                <td>${item.project || "-"}</td>
                <td>${item.qty_ordered}</td>
                <td>R${item.price?.toFixed(2) || "0.00"}</td>
                <td>R${item.total?.toFixed(2) || "0.00"}</td>
              </tr>
            `
              )
              .join("")}
          </tbody>
        `;
        td.appendChild(table);
      }

      tr.appendChild(td);
      row.parentNode.insertBefore(tr, row.nextSibling);
    })
    .catch((err) => {
      console.error("❌ Failed to load requisition items:", err);
    });
}
