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

      if (res.ok) {
        showToast("✅ Item saved successfully");
        fetchItems();
      } else {
        const errMsg = await res.text();
        showToast(`❌ Failed to save item: ${errMsg}`, false);
      }
    } catch (err) {
      console.error("Failed to add item:", err);
      showToast("❌ Network or server error", false);
    }
  }

  async function deleteItem(id) {
    try {
      const res = await fetch(`/lookups/items/${id}`, { method: "DELETE" });
      if (res.ok) {
        showToast("🗑️ Item deleted");
        fetchItems();
      } else {
        const errMsg = await res.text();
        showToast(`❌ Failed to delete: ${errMsg}`, false);
      }
    } catch (err) {
      console.error("Failed to delete item:", err);
      showToast("❌ Network or server error", false);
    }
  }

  function showToast(message, success = true) {
    const toast = document.createElement("div");
    toast.textContent = message;
    toast.className = success ? "toast toast-success" : "toast toast-error";
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.right = "20px";
    toast.style.background = success ? "#28a745" : "#c01c1c";
    toast.style.color = "white";
    toast.style.padding = "10px 16px";
    toast.style.borderRadius = "6px";
    toast.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
    toast.style.zIndex = "9999";
    toast.style.fontWeight = "bold";

    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }
}
