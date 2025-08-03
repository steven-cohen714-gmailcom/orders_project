export function initSuppliers() {
  console.log("initSuppliers loaded");

  fetchSuppliers();

  const saveBtn = document.getElementById("save-supplier-button");
  const cancelBtn = document.getElementById("cancel-supplier-edit");

  if (saveBtn) saveBtn.addEventListener("click", saveSupplier);
  if (cancelBtn) cancelBtn.addEventListener("click", cancelSupplierEdit);

  async function fetchSuppliers() {
    try {
      const res = await fetch("/admin/suppliers");
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      const data = await res.json();
      const tbody = document.getElementById("suppliers-table");
      if (!tbody) {
        console.error("Suppliers table not found");
        return;
      }

      tbody.innerHTML = "";
      if (data.suppliers && Array.isArray(data.suppliers)) {
        data.suppliers.forEach(s => tbody.prepend(createRow(s)));
      } else {
        console.error("Expected suppliers data to be an array, received:", data);
        tbody.innerHTML = '<tr><td colspan="3">Invalid data format from server.</td></tr>';
      }
    } catch (err) {
      console.error("Failed to fetch suppliers:", err);
      const tbody = document.getElementById("suppliers-table");
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="3">Failed to load suppliers. Please try again.</td></tr>';
      }
    }
  }

  async function saveSupplier() {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accField = document.getElementById("supplier-account-number");

    if (!idField || !nameField || !accField) {
      alert("❌ Form fields missing.");
      return;
    }

    const id = idField.value.trim();
    const name = nameField.value.trim();
    const account = accField.value.trim();

    if (!name || !account) {
      alert("❌ Supplier name and account number are required.");
      return;
    }

    const isDuplicate = Array.from(document.querySelectorAll("#suppliers-table tr")).some(tr => {
      const [n, a] = tr.querySelectorAll("td");
      return (
        n.textContent.trim().toLowerCase() === name.toLowerCase() &&
        a.textContent.trim() === account &&
        (!id || tr.dataset.id !== id)
      );
    });
    if (isDuplicate) {
      alert("❌ This supplier (name & account) already exists.");
      return;
    }

    try {
      const method = id ? "PUT" : "POST";
      const url = id ? `/admin/suppliers/${id}` : "/admin/suppliers";
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, account_number: account })
      });

      if (res.ok) {
        await fetchSuppliers();
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

  function createRow(s) {
    const tr = document.createElement("tr");
    tr.dataset.id = s.id;

    tr.innerHTML = `
      <td>${s.name || ""}</td>
      <td>${s.account_number || ""}</td>
      <td>
        <button class="edit-btn">Edit</button>
        <button class="delete-btn" style="margin-left:8px;">Delete</button>
      </td>
    `;

    tr.querySelector(".edit-btn").onclick = () => editSupplier(s.id, s.name, s.account_number);
    tr.querySelector(".delete-btn").onclick = () => deleteSupplier(s.id);
    return tr;
  }

  function editSupplier(id, name, account) {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accField = document.getElementById("supplier-account-number");

    if (idField && nameField && accField) {
      idField.value = id;
      nameField.value = name;
      accField.value = account || "";
      cancelBtn.style.display = "inline";
      saveBtn.textContent = "Update Supplier";
    }
  }

  async function deleteSupplier(id) {
    if (!confirm("Are you sure you want to delete this supplier?")) return;

    try {
      const res = await fetch(`/admin/suppliers/${id}`, { method: "DELETE" });
      if (res.ok) {
        await fetchSuppliers();
        alert("🗑️ Supplier deleted.");
      } else {
        alert(`❌ Failed to delete supplier: ${await res.text()}`);
      }
    } catch (err) {
      console.error("Delete error:", err);
      alert("❌ Network or server error while deleting supplier.");
    }
  }

  function cancelSupplierEdit() {
    const idField = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accField = document.getElementById("supplier-account-number");

    if (idField && nameField && accField) {
      idField.value = "";
      nameField.value = "";
      accField.value = "";
      cancelBtn.style.display = "none";
      saveBtn.textContent = "Add Supplier";
    }
  }
}