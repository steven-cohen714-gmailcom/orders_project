export function initSuppliers() {
  console.log("initSuppliers loaded");

  fetchSuppliers();

  const saveBtn = document.getElementById("save-supplier-button");
  if (saveBtn) {
    saveBtn.textContent = "Add Supplier";
    saveBtn.addEventListener("click", saveSupplier);
  }

  const cancelBtn = document.getElementById("cancel-supplier-edit");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", cancelSupplierEdit);
  }

  async function fetchSuppliers() {
    try {
      const res = await fetch("/maintenance/suppliers");
      const data = await res.json();
      const tbody = document.getElementById("suppliers-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.suppliers.forEach(supplier => {
        const row = createRow(supplier);
        tbody.insertBefore(row, tbody.firstChild);
      });
    } catch (err) {
      console.error("Failed to fetch suppliers:", err);
    }
  }

  async function saveSupplier() {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accNumField = document.getElementById("supplier-account-number");

    if (!idField || !nameField || !accNumField) return;

    const id = idField.value;
    const name = nameField.value.trim();
    const account_number = accNumField.value.trim();

    if (!name) {
      alert("❌ Supplier name is required.");
      return;
    }

    try {
      const method = id ? "PUT" : "POST";
      const url = id ? `/maintenance/suppliers/${id}` : "/maintenance/suppliers";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, account_number })
      });

      if (res.ok) {
        fetchSuppliers();
        cancelSupplierEdit();
        alert(id ? "✅ Supplier updated successfully." : "✅ Supplier added successfully.");
      } else {
        const msg = await res.text();
        alert(`❌ Error: ${msg}`);
      }
    } catch (err) {
      console.error("Failed to save supplier:", err);
      alert("❌ Network or server error.");
    }
  }

  function createRow(supplier) {
    const row = document.createElement("tr");

    const nameCell = document.createElement("td");
    nameCell.textContent = supplier.name || "";
    row.appendChild(nameCell);

    const accNumCell = document.createElement("td");
    accNumCell.textContent = supplier.account_number || "";
    row.appendChild(accNumCell);

    const actionsCell = document.createElement("td");

    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.addEventListener("click", () =>
      editSupplier(supplier.id, supplier.name, supplier.account_number)
    );
    actionsCell.appendChild(editBtn);

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.style.marginLeft = "8px";
    deleteBtn.addEventListener("click", () => deleteSupplier(supplier.id));
    actionsCell.appendChild(deleteBtn);

    row.appendChild(actionsCell);
    return row;
  }

  function editSupplier(id, name, account_number) {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accNumField = document.getElementById("supplier-account-number");
    const cancelBtn = document.getElementById("cancel-supplier-edit");
    const saveBtn = document.getElementById("save-supplier-button");

    if (!idField || !nameField || !accNumField || !cancelBtn || !saveBtn) return;

    idField.value = id;
    nameField.value = name;
    accNumField.value = account_number || "";
    cancelBtn.style.display = "inline";
    saveBtn.textContent = "Update Supplier";
  }

  function cancelSupplierEdit() {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accNumField = document.getElementById("supplier-account-number");
    const cancelBtn = document.getElementById("cancel-supplier-edit");
    const saveBtn = document.getElementById("save-supplier-button");

    if (!idField || !nameField || !accNumField || !cancelBtn || !saveBtn) return;

    idField.value = "";
    nameField.value = "";
    accNumField.value = "";
    cancelBtn.style.display = "none";
    saveBtn.textContent = "Add Supplier";
  }

  async function deleteSupplier(id) {
    try {
      const res = await fetch(`/maintenance/suppliers/${id}`, { method: "DELETE" });
      if (res.ok) {
        fetchSuppliers();
        alert("🗑️ Supplier deleted.");
      }
    } catch (err) {
      console.error("Failed to delete supplier:", err);
    }
  }
}
