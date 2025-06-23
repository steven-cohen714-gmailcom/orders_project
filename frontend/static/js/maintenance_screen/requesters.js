// File: /frontend/static/js/maintenance_screen/requesters.js

export function initRequesters() {
  console.log("initRequesters loaded");

  fetchRequesters();

  const addBtn = document.getElementById("add-requester-button");
  if (addBtn) {
    addBtn.addEventListener("click", addRequester);
  }

  /* ----------------------------------------------- */
  async function fetchRequesters() {
    try {
      const res = await fetch("/lookups/requesters");
      const data = await res.json();

      const tbody = document.getElementById("requesters-table");
      if (!tbody) return;

      tbody.innerHTML = "";
        data.requesters.forEach(r => {
          const tr = document.createElement("tr");
          tr.dataset.id = r.id;

          tr.innerHTML = `
            <td>${r.name}</td>
            <td><button class="delete-btn">Delete</button></td>
          `;

          tr.querySelector(".delete-btn").onclick = () => deleteRequester(r.id);
          tbody.appendChild(tr);
        });

    } catch (err) {
      console.error("❌ Failed to fetch requesters:", err);
      alert("❌ Failed to fetch requesters.");
    }
  }

  /* ----------------------------------------------- */
  async function addRequester() {
    const input = document.getElementById("requester-name");
    if (!input) return;
    const name = input.value.trim();
    if (!name) {
      alert("❌ Please enter a requester name.");
      return;
    }

    try {
      const res = await fetch("/lookups/requesters", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });

      if (res.ok) {
        input.value = "";
        await fetchRequesters();
        alert("✅ Requester added successfully.");
      } else {
        const msg = await res.text();
        alert(`❌ Failed to add requester: ${msg}`);
      }
    } catch (err) {
      console.error("❌ Failed to add requester:", err);
      alert("❌ Network or server error.");
    }
  }

  /* ----------------------------------------------- */
  async function deleteRequester(id) {
    try {
      if (!confirm("Are you sure you want to delete this requester?")) return;

      const res = await fetch(`/lookups/requesters/${id}`, {
        method: "DELETE"
      });

      if (res.ok) {
        await fetchRequesters();
        alert("🗑️ Requester deleted.");
      } else {
        const msg = await res.text();
        alert(`❌ Failed to delete requester: ${msg}`);
      }
    } catch (err) {
      console.error("❌ Failed to delete requester:", err);
      alert("❌ Network or server error.");
    }
  }
}
