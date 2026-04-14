export function showReceiveModal(orderId, orderNumber) {
  console.log(`Opening receive modal for order ID: ${orderId}, Order Number: ${orderNumber}`);
  fetch(`/orders/api/items_for_order/${orderId}`)
    .then(res => {
      console.log(`Fetch response status for items: ${res.status}`);
      if (!res.ok) {
        return res.text().then(errorText => {
          throw new Error(`Failed to fetch items: ${res.status} - ${errorText}`);
        });
      }
      return res.json();
    })
    .then(data => {
      console.log("Fetched items for receive modal:", data);
      const modal = document.createElement("div");
      modal.className = "receive-modal";
      modal.style = `
        position: fixed;
        top: 5%;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        max-height: 80%;
        overflow-y: auto;
        background: white;
        border: 1px solid #ccc;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
        z-index: 9999;
      `;

      const closeBtn = document.createElement("button");
      closeBtn.textContent = "X";
      closeBtn.style = "float:right; font-weight:bold; cursor:pointer;";
      closeBtn.onclick = () => document.body.removeChild(modal);

      const title = document.createElement("h3");
      title.textContent = `Mark Order #${orderNumber} as Received`;

      // --- Add receipt date input ---
      const dateLabel = document.createElement("label");
      dateLabel.textContent = "Receipt Date:";
      dateLabel.style = "margin-right: 1rem; font-weight: bold;";

      const dateInput = document.createElement("input");
      dateInput.type = "date";
      dateInput.required = true;
      dateInput.valueAsDate = new Date();

      const dateContainer = document.createElement("div");
      dateContainer.style = "margin-bottom: 1rem;";
      dateContainer.appendChild(dateLabel);
      dateContainer.appendChild(dateInput);
      modal.appendChild(dateContainer);

      const table = document.createElement("table");
      table.className = "receive-modal-table";

      const header = document.createElement("tr");
      [
        "Item Code",
        "Description",
        "Project",
        "Qty Ordered",
        "Qty Received to Date",
        "Price",
        "Total",
        "Qty Received Now"
      ].forEach(h => {
        const th = document.createElement("th");
        th.textContent = h;
        th.style.border = "1px solid #ccc";
        header.appendChild(th);
      });
      table.appendChild(header);

      const inputs = [];

      if (!data.items || data.items.length === 0) {
        console.log("No items found for this order");
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 8;
        cell.textContent = "No items found for this order.";
        row.appendChild(cell);
        table.appendChild(row);
      } else {
        data.items.forEach(item => {
          const row = document.createElement("tr");
          const total = (item.qty_ordered || 0) * (item.price || 0);
          const receivedToDate = item.qty_received || 0;
          const qtyRemaining = Math.max((item.qty_ordered || 0) - receivedToDate, 0);

          [
            item.item_code || "N/A",
            item.item_description || "N/A",
            item.project || "N/A",
            item.qty_ordered || 0,
            receivedToDate,
            item.price != null ? `R${item.price.toFixed(2)}` : "R0.00",
            total != null ? `R${total.toFixed(2)}` : "R0.00"
          ].forEach(text => {
            const td = document.createElement("td");
            td.textContent = text;
            td.style.border = "1px solid #ccc";
            row.appendChild(td);
          });

          const qtyInput = document.createElement("input");
          qtyInput.type = "number";
          qtyInput.min = 0;
          qtyInput.step = 1;
          qtyInput.value = qtyRemaining;
          qtyInput.style.width = "80px";

          inputs.push({ itemId: item.id || item.item_id, input: qtyInput });

          const inputTd = document.createElement("td");
          inputTd.style.border = "1px solid #ccc";
          inputTd.appendChild(qtyInput);
          row.appendChild(inputTd);

          table.appendChild(row);
        });
      }

      const submitBtn = document.createElement("button");
      submitBtn.textContent = "Mark as Received";
      submitBtn.style = "margin-top:1rem; padding:0.5rem 1rem; cursor:pointer;";
      submitBtn.onclick = async () => {
        const receiptDate = dateInput.value;
        if (!receiptDate) {
          alert("❌ Please select a receipt date.");
          return;
        }

        const payload = {
          receipt_date: receiptDate,
          items: inputs.map(i => ({
            item_id: i.itemId,
            received_qty: parseFloat(i.input.value) || 0
          }))
        };
        console.log("Submitting receive payload:", payload);

        try {
          const res = await fetch(`/orders/receive/${orderId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
          console.log(`Receive endpoint response status: ${res.status}`);
          if (!res.ok) {
            const err = await res.json();
            throw new Error(JSON.stringify(err));
          }
          const data = await res.json();
          console.log("Receive response:", data);
          alert("✅ Order marked as received");
          document.body.removeChild(modal);
          location.reload();
        } catch (err) {
          console.error("❌ Failed to mark as received:", err);
          alert(`❌ Failed to mark as received: ${err.message}`);
        }
      };

      modal.appendChild(closeBtn);
      modal.appendChild(title);
      modal.appendChild(table);
      modal.appendChild(submitBtn);
      document.body.appendChild(modal);
    })
    .catch(err => {
      console.error("❌ Error loading receive modal:", err);
      alert(`❌ Could not open receive modal: ${err.message}`);
    });
}
