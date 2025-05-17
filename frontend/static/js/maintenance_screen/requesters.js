// /frontend/static/js/maintenance_screen/requesters.js

export function initRequesters() {
  console.log("initRequesters loaded");

  fetchRequesters();

  const addBtn = document.getElementById("add-requester-button");
  if (addBtn) {
    addBtn.addEventListener("click", addRequester);
  }

  async function fetchRequesters() {
    try {
      const res = await fetch("/lookups/requesters");
      const data = await res.json();

      const tbody = document.getElementById("requesters-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.requesters.forEach(requester => {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.textContent = requester.name;
        row.appendChild(nameCell);

        const actionsCell = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", () => deleteRequester(requester.id));
        actionsCell.appendChild(deleteButton);

        row.appendChild(actionsCell);
        tbody.appendChild(row);
      });
    } catch (err) {
      console.error("Failed to fetch requesters:", err);
    }
  }

  async function addRequester() {
    const input = document.getElementById("requester-name");
    if (!input) return;
    const name = input.value;

    try {
      const res = await fetch("/lookups/requesters", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });
      if (res.ok) fetchRequesters();
    } catch (err) {
      console.error("Failed to add requester:", err);
    }
  }

  async function deleteRequester(id) {
    try {
      const res = await fetch(`/lookups/requesters/${id}`, { method: "DELETE" });
      if (res.ok) fetchRequesters();
    } catch (err) {
      console.error("Failed to delete requester:", err);
    }
  }
}
