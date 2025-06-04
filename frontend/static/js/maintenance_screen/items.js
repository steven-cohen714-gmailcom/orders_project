// File: /frontend/static/js/maintenance_screen/items.js

export function initItems() {
  console.log("initItems loaded");

  fetchItems();

  const addBtn = document.getElementById("add-item-button");
  if (addBtn) {
    addBtn.addEventListener("click", addItem);
  }

  async function fetchItems() {
    try {
      const res = await fetch("/lookups/items");
      const data = await res.json();
      const tbody = document.getElementById("items-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.items.forEach(item => {
        const row = createRow(item);
        tbody.appendChild(row);
      });
    } catch (err) {
      console.error("Failed to fetch items:", err);
    }
  }

  async function addItem() {
    const item_code = document.getElementById("item-code")?.value.trim();
    const item_description = document.getElementById("item-description")?.value.trim();

    if (!item_code || !item_description) {
      alert("❌ Please enter both item code and description.");
      return;
    }

    try {
      const res = await fetch("/lookups/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_code, item_description })
      });

      if (res.ok) {
        const newItem = await res.json(); // Should return: { id, item_code, item_description }
        const row = createRow(newItem);

        const tbody = document.getElementById("items-table");
        tbody.insertBefore(row, tbody.firstChild); // Add new item at top

        alert("✅ Item added successfully.");

        document.getElementById("item-code").value = "";
        document.getElementById("item-description").value = "";
      } else {
        const errMsg = await res.text();
        alert(`❌ Failed to save item: ${errMsg}`);
      }
    } catch (err) {
      console.error("Failed to add item:", err);
      alert("❌ Network or server error");
    }
  }

  async function deleteItem(id) {
    try {
      const res = await fetch(`/lookups/items/${id}`, { method: "DELETE" });
      if (res.ok) {
        alert("🗑️ Item deleted");
        fetchItems();
      } else {
        const errMsg = await res.text();
        alert(`❌ Failed to delete: ${errMsg}`);
      }
    } catch (err) {
      console.error("Failed to delete item:", err);
      alert("❌ Network or server error");
    }
  }

  function createRow(item) {
    const row = document.createElement("tr");

    const codeCell = document.createElement("td");
    codeCell.textContent = item.item_code;
    row.appendChild(codeCell);

    const descCell = document.createElement("td");
    descCell.textContent = item.item_description;
    row.appendChild(descCell);

    const actionsCell = document.createElement("td");
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = () => deleteItem(item.id);
    actionsCell.appendChild(deleteButton);

    row.appendChild(actionsCell);
    return row;
  }
}
