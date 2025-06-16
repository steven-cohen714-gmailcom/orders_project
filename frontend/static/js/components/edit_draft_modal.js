export async function showEditDraftModal(orderId, orderNumber) {
    const modal = createModal();
    document.body.appendChild(modal.overlay);
    modal.title.textContent = `Edit Draft Order: ${orderNumber}`;
    modal.body.innerHTML = `<p>Loading items...</p>`;

    try {
        const res = await fetch(`/orders/api/order_items/${orderId}`);
        if (!res.ok) throw new Error(`Failed to fetch line items: ${res.status}`);
        const items = await res.json();

        modal.body.innerHTML = ""; // clear loading

        const table = document.createElement("table");
        table.style.width = "100%";
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Qty</th>
                    <th>Unit Price</th>
                </tr>
            </thead>
            <tbody></tbody>
        `;

        const tbody = table.querySelector("tbody");

        items.forEach((item, index) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.item_code}</td>
                <td>${item.item_description}</td>
                <td><input type="number" min="0" step="1" value="${item.quantity || 0}" data-field="quantity" data-index="${index}"></td>
                <td><input type="number" min="0" step="0.01" value="${item.unit_price || 0}" data-field="unit_price" data-index="${index}"></td>
            `;

            row.dataset.itemId = item.id;
            tbody.appendChild(row);
        });

        modal.body.appendChild(table);

        modal.saveBtn.addEventListener("click", async () => {
            const updatedItems = [];

            tbody.querySelectorAll("tr").forEach((row) => {
                const itemId = row.dataset.itemId;
                const qty = row.querySelector('[data-field="quantity"]').value;
                const price = row.querySelector('[data-field="unit_price"]').value;

                updatedItems.push({
                    item_id: itemId,
                    quantity: parseFloat(qty),
                    unit_price: parseFloat(price)
                });
            });

            try {
                const res = await fetch(`/orders/update_draft/${orderId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ items: updatedItems })
                });

                if (!res.ok) throw new Error(`Failed to update draft: ${res.status}`);
                alert("✅ Draft order updated successfully!");
                modal.overlay.remove();
                await window.loadOrders(); // refresh
            } catch (err) {
                alert("❌ Error saving draft");
                console.error(err);
            }
        });

        modal.cancelBtn.addEventListener("click", () => {
            modal.overlay.remove();
        });

    } catch (err) {
        modal.body.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    }
}

function createModal() {
    const overlay = document.createElement("div");
    overlay.style.position = "fixed";
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = "100vw";
    overlay.style.height = "100vh";
    overlay.style.backgroundColor = "rgba(0,0,0,0.5)";
    overlay.style.display = "flex";
    overlay.style.alignItems = "center";
    overlay.style.justifyContent = "center";
    overlay.style.zIndex = 10000;

    const modal = document.createElement("div");
    modal.style.background = "#fff";
    modal.style.padding = "2rem";
    modal.style.borderRadius = "8px";
    modal.style.width = "80%";
    modal.style.maxHeight = "80vh";
    modal.style.overflowY = "auto";
    modal.style.boxShadow = "0 0 15px rgba(0,0,0,0.2)";

    const title = document.createElement("h2");
    modal.appendChild(title);

    const body = document.createElement("div");
    body.style.marginTop = "1rem";
    modal.appendChild(body);

    const footer = document.createElement("div");
    footer.style.marginTop = "2rem";
    footer.style.display = "flex";
    footer.style.justifyContent = "flex-end";
    footer.style.gap = "1rem";

    const cancelBtn = document.createElement("button");
    cancelBtn.textContent = "Cancel";
    cancelBtn.style.background = "#ccc";
    cancelBtn.style.padding = "0.5rem 1rem";

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save Changes";
    saveBtn.style.background = "green";
    saveBtn.style.color = "#fff";
    saveBtn.style.padding = "0.5rem 1rem";

    footer.appendChild(cancelBtn);
    footer.appendChild(saveBtn);

    modal.appendChild(footer);
    overlay.appendChild(modal);

    return {
        overlay,
        title,
        body,
        saveBtn,
        cancelBtn
    };
}
