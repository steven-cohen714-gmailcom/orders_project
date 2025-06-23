export function initSuppliers() {
  console.log("initSuppliers loaded");

  fetchSuppliers();

  const saveBtn   = document.getElementById("save-supplier-button");
  const cancelBtn = document.getElementById("cancel-supplier-edit");

  if (saveBtn)   saveBtn.addEventListener("click", saveSupplier);
  if (cancelBtn) cancelBtn.addEventListener("click", cancelSupplierEdit);

  /* -------------------------------------------------- */
  async function fetchSuppliers() {
    try {
      const res = await fetch("/maintenance/suppliers");
      const data = await res.json();
      const tbody = document.getElementById("suppliers-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.suppliers.forEach(s => tbody.prepend(createRow(s)));
    } catch (err) {
      console.error("Failed to fetch suppliers:", err);
      alert("❌ Failed to fetch suppliers from server.");
    }
  }

  /* -------------------------------------------------- */
  async function saveSupplier() {
    const idField   = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accField  = document.getElementById("supplier-account-number");

    if (!idField || !nameField || !accField) return;

    const id      = idField.value.trim();
    const name    = nameField.value.trim();
    const account = accField.value.trim();

    /* ---- validation ---- */
    if (!name || !account) {
      alert("❌ Supplier name and account number are required.");
      return;
    }

    /* ---- duplicate check (name + account) ---- */
    const isDuplicate = Array.from(document.querySelectorAll("#suppliers-table tr")).some(tr => {
      const [n, a] = tr.querySelectorAll("td");
      return (
        n.textContent.trim().toLowerCase() === name.toLowerCase() &&
        a.textContent.trim()               === account            &&
        (!id || tr.dataset.id !== id)      // allow update of SAME row
      );
    });
    if (isDuplicate) {
      alert("❌ This supplier (name & account) already exists.");
      return;
    }

    try {
      const method = id ? "PUT" : "POST";
      const url    = id
        ? `/maintenance/suppliers/${id}`
        : "/maintenance/suppliers";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, account_number: account })
      });

      if (res.ok) {
        await fetchSuppliers();
        cancelSupplierEdit();          // clear + reset form
        alert(id ? "✅ Supplier updated successfully."
                 : "✅ Supplier added successfully.");
      } else {
        const msg = await res.text();
        alert(`❌ Error: ${msg}`);
      }
    } catch (err) {
      console.error("Failed to save supplier:", err);
      alert("❌ Network or server error.");
    }
  }

  /* -------------------------------------------------- */
  function createRow(s) {
    const tr = document.createElement("tr");
    tr.dataset.id = s.id; // used for duplicate check on edit

    tr.innerHTML = `
      <td>${s.name || ""}</td>
      <td>${s.account_number || ""}</td>
      <td>
        <button class="edit-btn">Edit</button>
        <button class="delete-btn" style="margin-left:8px;">Delete</button>
      </td>
    `;

    tr.querySelector(".edit-btn").onclick   = () => editSupplier(s.id, s.name, s.account_number);
    tr.querySelector(".delete-btn").onclick = () => deleteSupplier(s.id);
    return tr;
  }

  /* -------------------------------------------------- */
  function editSupplier(id, name, account) {
    const idField   = document.getElementById("supplier-id");
    const nameField = document.getElementById("supplier-name");
    const accField  = document.getElementById("supplier-account-number");

    idField.value         = id;
    nameField.value       = name;
    accField.value        = account || "";
    cancelBtn.style.display = "inline";
    saveBtn.textContent     = "Update Supplier";
  }

  /* -------------------------------------------------- */
  function cancelSupplierEdit() {
    document.getElementById("supplier-id").value              = "";
    document.getElementById("supplier-name").value            = "";
    document.getElementById("supplier-account-number").value  = "";
    cancelBtn.style.display = "none";
    saveBtn.textContent     = "Add Supplier";
  }

  /* -------------------------------------------------- */
  async function deleteSupplier(id) {
    try {
      if (!confirm("Are you sure you want to delete this supplier?")) return;

      const res = await fetch(`/maintenance/suppliers/${id}`, { method: "DELETE" });
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
}
