// File: frontend/static/js/components/receive_modal.js

export function showReceiveModal(orderId, orderNumber) {
  fetch(`/orders/api/items_for_order/${orderId}`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch items");
      return res.json();
    })
    .then(data => {
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

      const table = document.createElement("table");
      table.style = "width:100%; border-collapse:collapse; margin-top:1rem;";

      const header = document.createElement("tr");
      ["Item Code", "Description", "Project", "Qty Ordered", "Price", "Total", "Actual Received Qty"].forEach(h => {
        const th = document.createElement("th");
        th.textContent = h;
        th.style.border = "1px solid #ccc";
        header.appendChild(th);
      });
      table.appendChild(header);

      const inputs = [];

      data.items.forEach(item => {
        const row = document.createElement("tr");
        const total = item.qty_ordered * item.price;

        [
          item.item_code,
          item.item_description,
          item.project,
          item.qty_ordered,
          `R${item.price.toFixed(2)}`,
          `R${total.toFixed(2)}`
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
        qtyInput.value = item.qty_ordered;
        qtyInput.style.width = "80px";

        // Use the correct field name for ID
        inputs.push({ itemId: item.id || item.item_id, input: qtyInput });

        const inputTd = document.createElement("td");
        inputTd.style.border = "1px solid #ccc";
        inputTd.appendChild(qtyInput);
        row.appendChild(inputTd);

        table.appendChild(row);
      });

      const submitBtn = document.createElement("button");
      submitBtn.textContent = "Mark as Received";
      submitBtn.style = "margin-top:1rem; padding:0.5rem 1rem; cursor:pointer;";
      submitBtn.onclick = async () => {
        const payload = inputs.map(i => ({
          order_id: orderId,
          item_id: i.itemId,
          qty_received: parseFloat(i.input.value)
        }));

        const res = await fetch("/orders/receive", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          alert("✅ Order marked as received");
          document.body.removeChild(modal);
          location.reload();
        } else {
          const err = await res.json();
          if (Array.isArray(err.detail)) {
            const messages = err.detail.map(obj => obj.msg || JSON.stringify(obj));
            alert("❌ Failed to mark as received:\n" + messages.join("\n"));
          } else {
            alert("❌ Failed to mark as received: " + (err.detail || "Unknown error"));
          }
          
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
      alert("❌ Could not open receive modal");
    });
}
