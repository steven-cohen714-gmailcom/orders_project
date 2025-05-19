export function initUsers() {
  console.log("initUsers loaded");

  fetchUsers();

  const cancelBtn = document.getElementById("cancel-user-edit");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", cancelUserEdit);
    cancelBtn.style.display = "none";
  }

  const form = document.querySelector("#users form");
  if (form) {
    form.addEventListener("submit", async (event) => {
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
    if (!res.ok) throw new Error("Failed to fetch users");

    const data = await res.json();
    const tbody = document.getElementById("users-table");
    if (!tbody) return;

    tbody.innerHTML = "";
    data.users.forEach(user => {
      const row = document.createElement("tr");

      row.appendChild(createCell(user.username));
      row.appendChild(createCell(user.rights));
      row.appendChild(createCell(user.auth_threshold_band ?? "Not Set"));
      row.appendChild(createActionsCell(user));

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Failed to fetch users:", err);
  }
}

function createCell(content) {
  const cell = document.createElement("td");
  cell.textContent = content;
  return cell;
}

function createActionsCell(user) {
  const cell = document.createElement("td");

  const editBtn = document.createElement("button");
  editBtn.textContent = "Edit";
  editBtn.addEventListener("click", () =>
    populateUserForm(user.id, user.username, user.rights, user.auth_threshold_band)
  );
  cell.appendChild(editBtn);

  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "Delete";
  deleteBtn.style.marginLeft = "8px";
  deleteBtn.addEventListener("click", () => deleteUser(user.id));
  cell.appendChild(deleteBtn);

  return cell;
}

async function addOrUpdateUser() {
  const id = document.getElementById("user-id")?.value;
  const username = document.getElementById("user-username")?.value.trim();
  const password = document.getElementById("user-password")?.value;
  const rights = document.getElementById("user-rights")?.value;
  const bandRaw = document.getElementById("user-auth-threshold-band")?.value;
  const auth_threshold_band = bandRaw === "" ? null : parseInt(bandRaw, 10);

  if (!username || !rights) {
    alert("Username and rights are required.");
    return;
  }

  if (!id && !password) {
    alert("Password is required when adding a new user.");
    return;
  }

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

    if (!res.ok) {
      const error = await res.json();
      throw new Error(
        error.detail
          ? (Array.isArray(error.detail)
              ? error.detail.map(e => e.msg).join(", ")
              : error.detail)
          : "Unknown error"
      );
    }

    fetchUsers();
    cancelUserEdit();
  } catch (err) {
    console.error("Failed to save user:", err);
    alert("Failed to save user. " + err.message);
  }
}

function populateUserForm(id, username, rights, auth_threshold_band) {
  document.getElementById("user-id").value = id;
  document.getElementById("user-username").value = username;
  document.getElementById("user-rights").value = rights;
  document.getElementById("user-auth-threshold-band").value = auth_threshold_band ?? "";
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
  if (!confirm("Are you sure you want to delete this user?")) return;

  try {
    const res = await fetch(`/lookups/users/${id}`, { method: "DELETE" });
    if (res.ok) {
      fetchUsers();
    } else {
      const err = await res.json();
      throw new Error(err.detail || "Delete failed");
    }
  } catch (err) {
    console.error("Failed to delete user:", err);
    alert("Failed to delete user. " + err.message);
  }
}
