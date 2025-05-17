export function initUsers() {
  console.log("initUsers loaded");

  fetchUsers();

  const cancelBtn = document.getElementById("cancel-user-edit");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", cancelUserEdit);
    cancelBtn.style.display = "none"; // hidden initially
  }

  const form = document.querySelector("#users form");
  if (form) {
    form.addEventListener("submit", async event => {
      event.preventDefault();
      await addOrUpdateUser();
    });
  }

  const addBtn = document.querySelector("#users button[type='submit']");
  if (addBtn) {
    addBtn.textContent = "Add User";
  }
}

async function fetchUsers() {
  try {
    const res = await fetch("/lookups/users");
    const data = await res.json();
    const tbody = document.getElementById("users-table");
    if (!tbody) return;

    tbody.innerHTML = "";
    data.users.forEach(user => {
      const row = document.createElement("tr");

      const usernameCell = document.createElement("td");
      usernameCell.textContent = user.username;
      row.appendChild(usernameCell);

      const rightsCell = document.createElement("td");
      rightsCell.textContent = user.rights;
      row.appendChild(rightsCell);

      const thresholdBandCell = document.createElement("td");
      thresholdBandCell.textContent = user.auth_threshold_band || "Not Set";
      row.appendChild(thresholdBandCell);

      const actionsCell = document.createElement("td");

      const editButton = document.createElement("button");
      editButton.textContent = "Edit";
      editButton.addEventListener("click", () =>
        editUser(user.id, user.username, user.rights, user.auth_threshold_band)
      );
      actionsCell.appendChild(editButton);

      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.style.marginLeft = "8px";
      deleteButton.addEventListener("click", () => deleteUser(user.id));
      actionsCell.appendChild(deleteButton);

      row.appendChild(actionsCell);
      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Failed to fetch users:", err);
  }
}

async function addOrUpdateUser() {
  const id = document.getElementById("user-id")?.value;
  const username = document.getElementById("user-username")?.value;
  const password = document.getElementById("user-password")?.value;
  const rights = document.getElementById("user-rights")?.value;
  const auth_threshold_band = document.getElementById("user-auth-threshold-band")?.value || null;

  if (!username || !rights) return;

  const method = id ? "PUT" : "POST";
  const url = id ? `/lookups/users/${id}` : "/lookups/users";

  const payload = { username, rights, auth_threshold_band };
  if (method === "POST" || password) {
    payload.password = password;
  }

  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      fetchUsers();
      cancelUserEdit();
    }
  } catch (err) {
    console.error("Failed to add/update user:", err);
  }
}

function editUser(id, username, rights, auth_threshold_band) {
  document.getElementById("user-id").value = id;
  document.getElementById("user-username").value = username;
  document.getElementById("user-rights").value = rights;
  document.getElementById("user-auth-threshold-band").value = auth_threshold_band || "";
  document.getElementById("user-password").value = "";

  document.getElementById("cancel-user-edit").style.display = "inline";
  document.querySelector("#users button[type='submit']").textContent = "Update User";
}

function cancelUserEdit() {
  document.getElementById("user-id").value = "";
  document.getElementById("user-username").value = "";
  document.getElementById("user-password").value = "";
  document.getElementById("user-rights").value = "edit";
  document.getElementById("user-auth-threshold-band").value = "";

  document.getElementById("cancel-user-edit").style.display = "none";
  document.querySelector("#users button[type='submit']").textContent = "Add User";
}

async function deleteUser(id) {
  try {
    const res = await fetch(`/lookups/users/${id}`, { method: "DELETE" });
    if (res.ok) fetchUsers();
  } catch (err) {
    console.error("Failed to delete user:", err);
  }
}
