export function initItems() {
  console.log("initItems loaded");

  fetchItems();

  const saveBtn   = document.getElementById("add-item-button");
  const cancelBtn = document.getElementById("cancel-item-edit");

  if (saveBtn)   saveBtn.addEventListener("click", saveItem);
  if (cancelBtn) cancelBtn.addEventListener("click", cancelItemEdit);

  /* -------------------------------------------------- */
  async function fetchItems() {
    try {
      const res = await fetch("/lookups/items");
      const data = await res.json();
      const tbody = document.getElementById("items-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.items.forEach(i => tbody.prepend(createRow(i)));
    } catch (err) {
      console.error("Failed to fetch items:", err);
      alert("❌ Failed to fetch items from server.");
    }
  }

  /* -------------------------------------------------- */
  async function saveItem() {
    const idField   = document.getElementById("item-id");
    const codeField = document.getElementById("item-code");
    const descField = document.getElementById("item-description");

    if (!idField || !codeField || !descField) return;

    const id    = idField.value.trim();
    const code  = codeField.value.trim();
    const desc  = descField.value.trim();

    /* ---- validation ---- */
    if (!code || !desc) {
      alert("❌ Item code and description are required.");
      return;
    }

    /* ---- duplicate check (code + description) ---- */
    const isDuplicate = Array.from(document.querySelectorAll("#items-table tr")).some(tr => {
      const [c, d] = tr.querySelectorAll("td");
      return (
        c.textContent.trim().toLowerCase() === code.toLowerCase() &&
        d.textContent.trim().toLowerCase() === desc.toLowerCase() &&
        (!id || tr.dataset.id !== id)
      );
    });
    if (isDuplicate) {
      alert("❌ This item (code & description) already exists.");
      return;
    }

    try {
      const method = id ? "PUT" : "POST";
      const url    = id
        ? `/lookups/items/${id}`
        : "/lookups/items";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_code: code, item_description: desc })
      });

      if (res.ok) {
        await fetchItems();
        cancelItemEdit();
        alert(id ? "✅ Item updated successfully." : "✅ Item added successfully.");
      } else {
        const msg = await res.text();
        alert(`❌ Error: ${msg}`);
      }
    } catch (err) {
      console.error("Failed to save item:", err);
      alert("❌ Network or server error.");
    }
  }

  /* -------------------------------------------------- */
  function createRow(i) {
    const tr = document.createElement("tr");
    tr.dataset.id = i.id;

    tr.innerHTML = `
      <td>${i.item_code || ""}</td>
      <td>${i.item_description || ""}</td>
      <td>
        <button class="edit-btn">Edit</button>
        <button class="delete-btn" style="margin-left:8px;">Delete</button>
      </td>
    `;

    tr.querySelector(".edit-btn").onclick   = () => editItem(i.id, i.item_code, i.item_description);
    tr.querySelector(".delete-btn").onclick = () => deleteItem(i.id);
    return tr;
  }

  /* -------------------------------------------------- */
  function editItem(id, code, desc) {
    const idField   = document.getElementById("item-id");
    const codeField = document.getElementById("item-code");
    const descField = document.getElementById("item-description");

    idField.value           = id;
    codeField.value         = code;
    descField.value         = desc;
    cancelBtn.style.display = "inline";
    saveBtn.textContent     = "Update Item";
  }

  /* -------------------------------------------------- */
  function cancelItemEdit() {
    document.getElementById("item-id").value           = "";
    document.getElementById("item-code").value         = "";
    document.getElementById("item-description").value  = "";
    cancelBtn.style.display = "none";
    saveBtn.textContent     = "Add Item";
  }

  /* -------------------------------------------------- */
  async function deleteItem(id) {
    try {
      if (!confirm("Are you sure you want to delete this item?")) return;

      const res = await fetch(`/lookups/items/${id}`, { method: "DELETE" });
      if (res.ok) {
        await fetchItems();
        alert("🗑️ Item deleted.");
      } else {
        alert(`❌ Failed to delete item: ${await res.text()}`);
      }
    } catch (err) {
      console.error("Delete error:", err);
      alert("❌ Network or server error while deleting item.");
    }
  }
}
