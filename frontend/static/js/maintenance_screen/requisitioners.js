// File: frontend/static/js/maintenance_screen/requisitioners.js

export function initRequisitioners() {
  const nameInput = document.getElementById("requisitioner-name");
  const addButton = document.getElementById("add-requisitioner-button");
  const tableBody = document.getElementById("requisitioners-table");

  if (!nameInput || !addButton || !tableBody) return;

  async function loadRequisitioners() {
    try {
      const res = await fetch("/lookups/requisitioners");
      const data = await res.json();
      tableBody.innerHTML = "";

      data.forEach(r => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${r.name}</td>
          <td><button data-id="${r.id}" class="delete-btn">Delete</button></td>
        `;
        tableBody.appendChild(row);
      });

      document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          const id = btn.getAttribute("data-id");
          await fetch(`/lookups/requisitioners/${id}`, { method: "DELETE" });
          loadRequisitioners();
        });
      });
    } catch (err) {
      console.error("Failed to load requisitioners", err);
    }
  }

  addButton.addEventListener("click", async () => {
    const name = nameInput.value.trim();
    if (!name) return;

    try {
      const res = await fetch("/lookups/requisitioners", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });

      if (res.ok) {
        nameInput.value = "";
        await loadRequisitioners();
        alert("✅ Added successfully.");
      } else {
        const err = await res.json();
        alert(`❌ Failed: ${err.detail}`);
      }
    } catch (err) {
      console.error("Add requisitioner error", err);
    }
  });

  loadRequisitioners();
}
