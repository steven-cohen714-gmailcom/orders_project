// File: frontend/static/js/maintenance_screen/requisitioners.js

export function initRequisitioners() {
  console.log("initRequisitioners loaded");

  fetchRequisitioners();

  const addBtn = document.getElementById("add-requisitioner-button");
  if (addBtn) addBtn.addEventListener("click", saveRequisitioner);

  /* -------------------------------------------------- */
  async function fetchRequisitioners() {
    try {
      const res = await fetch("/lookups/requisitioners");
      const data = await res.json();
      const tbody = document.getElementById("requisitioners-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.forEach(r => tbody.prepend(createRow(r)));
    } catch (err) {
      console.error("Failed to fetch requisitioners:", err);
      alert("❌ Failed to fetch requisitioners from server.");
    }
  }

  /* -------------------------------------------------- */
  async function saveRequisitioner() {
    const nameField = document.getElementById("requisitioner-name");
    if (!nameField) return;

    const name = nameField.value.trim();
    if (!name) {
      alert("❌ Requisitioner name is required.");
      return;
    }

    try {
      const res = await fetch("/lookups/requisitioners", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });

      if (res.ok) {
        nameField.value = "";
        await fetchRequisitioners();
        alert("✅ Requisitioner added successfully.");
      } else {
        const msg = await res.text();
        alert(`❌ Error: ${msg}`);
      }
    } catch (err) {
      console.error("Failed to save requisitioner:", err);
      alert("❌ Network or server error.");
    }
  }

  /* -------------------------------------------------- */
  function createRow(r) {
    const tr = document.createElement("tr");
    tr.dataset.id = r.id;

    tr.innerHTML = `
      <td>${r.name || ""}</td>
      <td><button class="delete-btn">Delete</button></td>
    `;

    tr.querySelector(".delete-btn").onclick = () => deleteRequisitioner(r.id);
    return tr;
  }

  /* -------------------------------------------------- */
  async function deleteRequisitioner(id) {
    try {
      if (!confirm("Are you sure you want to delete this requisitioner?")) return;

      const res = await fetch(`/lookups/requisitioners/${id}`, { method: "DELETE" });
      if (res.ok) {
        await fetchRequisitioners();
        alert("🗑️ Requisitioner deleted.");
      } else {
        alert(`❌ Failed to delete requisitioner: ${await res.text()}`);
      }
    } catch (err) {
      console.error("Delete error:", err);
      alert("❌ Network or server error while deleting requisitioner.");
    }
  }
}
