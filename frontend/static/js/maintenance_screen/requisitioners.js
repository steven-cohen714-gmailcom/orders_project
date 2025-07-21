// File: frontend/static/js/maintenance_screen/requisitioners.js

export function initRequisitioners() {
  console.log("initRequisitioners loaded");

  fetchRequisitioners();

  const addBtn = document.getElementById("add-requisitioner-button");
  if (addBtn) {
    addBtn.addEventListener("click", addRequisitioner);
  }

  async function fetchRequisitioners() {
    try {
      const res = await fetch("/lookups/requisitioners");
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      // MODIFIED: Expect data to be a direct array, not an object with a 'requisitioners' key
      const data = await res.json(); // data is now the array directly

      const tbody = document.getElementById("requisitioners-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      // Loop directly over 'data' as it's the array
      data.forEach(r => {
        const tr = document.createElement("tr");
        tr.dataset.id = r.id;

        tr.innerHTML = `
          <td>${r.name}</td>
          <td><button class="delete-btn">Delete</button></td>
        `;

        tr.querySelector(".delete-btn").onclick = () => deleteRequisitioner(r.id);
        tbody.appendChild(tr);
      });
    } catch (err) {
      console.error("❌ Failed to fetch requisitioners:", err);
      alert("❌ Failed to fetch requisitioners.");
    }
  }

  async function addRequisitioner() {
    const input = document.getElementById("requisitioner-name");
    if (!input) return;
    const name = input.value.trim();
    if (!name) {
      alert("❌ Please enter a requisitioner name.");
      return;
    }

    try {
      const res = await fetch("/lookups/requisitioners", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });

      if (res.ok) {
        input.value = "";
        await fetchRequisitioners();
        alert("✅ Requisitioner added successfully.");
      } else {
        const msg = await res.text();
        alert(`❌ Failed to add requisitioner: ${msg}`);
      }
    } catch (err) {
      console.error("❌ Failed to add requisitioner:", err);
      alert("❌ Network or server error.");
    }
  }

  async function deleteRequisitioner(id) {
    try {
      if (!confirm("Are you sure you want to delete this requisitioner?")) return;

      const res = await fetch(`/lookups/requisitioners/${id}`, {
        method: "DELETE"
      });

      if (res.ok) {
        await fetchRequisitioners();
        alert("🗑️ Requisitioner deleted.");
      } else {
        const msg = await res.text();
        alert(`❌ Failed to delete requisitioner: ${msg}`);
      }
    } catch (err) {
      console.error("❌ Failed to delete requisitioner:", err);
      alert("❌ Network or server error.");
    }
  }
}