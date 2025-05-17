// /frontend/static/js/maintenance_screen/items.js
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
        tbody.appendChild(row);
      });
    } catch (err) {
      console.error("Failed to fetch items:", err);
    }
  }

  async function addItem() {
    const item_code = document.getElementById("item-code")?.value;
    const item_description = document.getElementById("item-description")?.value;

    try {
      const res = await fetch("/lookups/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_code, item_description })
      });
      if (res.ok) fetchItems();
    } catch (err) {
      console.error("Failed to add item:", err);
    }
  }

  async function deleteItem(id) {
    try {
      const res = await fetch(`/lookups/items/${id}`, { method: "DELETE" });
      if (res.ok) fetchItems();
    } catch (err) {
      console.error("Failed to delete item:", err);
    }
  }
}
