export function initSuppliers() {
  console.log("initSuppliers loaded");

  fetchSuppliers();

  const saveBtn = document.getElementById("save-supplier-button");
  if (saveBtn) {
    saveBtn.textContent = "Add Supplier"; // Default label
    saveBtn.addEventListener("click", saveSupplier);
  }

  const cancelBtn = document.getElementById("cancel-supplier-edit");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", cancelSupplierEdit);
  }

  async function fetchSuppliers() {
    try {
      const res = await fetch("/lookups/suppliers");
      const data = await res.json();
      const tbody = document.getElementById("suppliers-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.suppliers.forEach(supplier => {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.textContent = supplier.name;
        row.appendChild(nameCell);

        const actionsCell = document.createElement("td");

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.addEventListener("click", () => editSupplier(supplier.id, supplier.name));
        actionsCell.appendChild(editButton);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.style.marginLeft = "8px";
        deleteButton.addEventListener("click", () => deleteSupplier(supplier.id));
        actionsCell.appendChild(deleteButton);

        row.appendChild(actionsCell);
        tbody.appendChild(row);
      });
    } catch (err) {
      console.error("Failed to fetch suppliers:", err);
    }
  }

  async function saveSupplier() {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    if (!idField || !nameField) return;

    const id = idField.value;
    const name = nameField.value;

    if (!name.trim()) return;

    try {
      const method = id ? "PUT" : "POST";
      const url = id ? `/lookups/suppliers/${id}` : "/lookups/suppliers";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });

      if (res.ok) {
        fetchSuppliers();
        cancelSupplierEdit();
      }
    } catch (err) {
      console.error("Failed to save supplier:", err);
    }
  }

  function editSupplier(id, name) {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const cancelBtn = document.getElementById("cancel-supplier-edit");
    const saveBtn = document.getElementById("save-supplier-button");

    if (!idField || !nameField || !cancelBtn || !saveBtn) return;

    idField.value = id;
    nameField.value = name;
    cancelBtn.style.display = "inline";
    saveBtn.textContent = "Update Supplier";
  }

  function cancelSupplierEdit() {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const cancelBtn = document.getElementById("cancel-supplier-edit");
    const saveBtn = document.getElementById("save-supplier-button");

    if (!idField || !nameField || !cancelBtn || !saveBtn) return;

    idField.value = "";
    nameField.value = "";
    cancelBtn.style.display = "none";
    saveBtn.textContent = "Add Supplier";
  }

  async function deleteSupplier(id) {
    try {
      const res = await fetch(`/lookups/suppliers/${id}`, { method: "DELETE" });
      if (res.ok) fetchSuppliers();
    } catch (err) {
      console.error("Failed to delete supplier:", err);
    }
  }
}
