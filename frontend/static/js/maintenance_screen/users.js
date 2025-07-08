// File: frontend/static/js/maintenance_screen/users.js
console.log("💥 users.js has been loaded");

// Ensure openEditUserModal is globally accessible as it's defined in edit_user_modal.html
// and needs to be called from this script.
// We now explicitly call it via window.openEditUserModal to ensure global scope access.

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

  const submitBtn = document.querySelector("#users button[type='submit']");
  if (submitBtn) {
    submitBtn.textContent = "Add User";
  }
}

// Expose fetchUsers globally so the modal's save function can call it to refresh the table
window.fetchUsers = async function() {
  try {
    const res = await fetch("/lookups/users");
    if (!res.ok) throw new Error("Failed to fetch users");

    const { users } = await res.json();
    console.log("✅ Users fetched from backend:", users);
    const tbody = document.getElementById("users-table");
    if (!tbody) return;

    tbody.innerHTML = "";
    console.log("➡️ Starting to render user rows...");
    users.forEach(user => {
      const row = document.createElement("tr");

      // --- MODIFIED LOGIC HERE ---
      // Ensure userScreenPermissions is always an array.
      // FastAPI will typically serialize a Python list directly to a JSON array,
      // so user.roles might already be an array in JavaScript, not a JSON string.
      let userScreenPermissions = [];
      if (Array.isArray(user.roles)) {
        userScreenPermissions = user.roles;
      } else if (typeof user.roles === 'string' && user.roles.trim() !== '') {
        try {
          // Fallback in case it's still a JSON string for some reason
          const parsedRoles = JSON.parse(user.roles);
          if (Array.isArray(parsedRoles)) {
            userScreenPermissions = parsedRoles;
          } else {
            console.warn(`User ${user.username} roles were a string but not a valid JSON array after parsing:`, user.roles);
          }
        } catch (e) {
          console.error(`Error parsing roles for user ${user.username}:`, e, user.roles);
        }
      }
      // --- END MODIFIED LOGIC ---

      row.appendChild(createCell(user.username));
      row.appendChild(createCell(user.auth_threshold_band ?? "Not Set"));
      row.appendChild(createCell(user.rights));
      // Pass the full user object including permissions to the actions cell
      row.appendChild(createActionsCell(user, userScreenPermissions)); // Pass the now-guaranteed array

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Failed to fetch users:", err);
    // Use displayMessage for errors
    displayMessage("Failed to fetch users: " + err.message, "error");
  }
}

function createCell(content) {
  const td = document.createElement("td");
  td.textContent = content;
  return td;
}

// Updated to accept screenPermissions for the modal
function createActionsCell(user, screenPermissions) {
  const td = document.createElement("td");

  const editBtn = document.createElement("button");
  editBtn.textContent = "Edit";
  console.log("Attaching edit button for:", user.username);
  editBtn.addEventListener("click", () => {
    // Call the global openEditUserModal function, ensuring it's on the window object
    if (typeof window.openEditUserModal === 'function') {
      // Pass user data to the modal, including screen permissions
      window.openEditUserModal(user.id, user.username, user.auth_threshold_band ?? "", screenPermissions);
    } else {
      console.error("openEditUserModal function is not defined globally.");
      displayMessage("Error: Edit modal function not available.", "error");
    }
  });
  td.appendChild(editBtn);

  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "Delete";
  deleteBtn.style.marginLeft = "8px";
  deleteBtn.addEventListener("click", () => deleteUser(user.id));
  td.appendChild(deleteBtn);

  return td;
}

async function addOrUpdateUser() {
  const id = document.getElementById("user-id")?.value;
  const username = document.getElementById("user-username")?.value.trim();
  const password = document.getElementById("user-password")?.value;
  const bandRaw = document.getElementById("user-auth-threshold-band")?.value;
  const auth_threshold_band = bandRaw === "" ? null : parseInt(bandRaw, 10);

  if (!username) {
    displayMessage("Username is required.", "error");
    return;
  }

  if (!id && !password) {
    displayMessage("Password is required when adding a new user.", "error");
    return;
  }

  const payload = {
    username,
    rights: "edit", // hardcoded for now
    auth_threshold_band
  };

  if (!id || password) {
    payload.password = password;
  }

  const url = id ? `/lookups/users/${id}` : "/lookups/users";
  const method = id ? "PUT" : "POST";

  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "Unknown error");
    }

    // After adding/updating, refresh the list
    window.fetchUsers();
    cancelUserEdit();
    displayMessage("User saved successfully.", "success");
  } catch (err) {
    console.error("Failed to save user:", err);
    displayMessage("Failed to save user. " + err.message, "error");
  }
}

// This function is no longer needed for populating the main form when editing.
// It was replaced by calling openEditUserModal directly.
// Keeping it for reference, but it won't be called for 'Edit' button clicks.
function populateUserForm(user) {
  console.log("populateUserForm called (old logic, should not be for modal):", user);
  const idField = document.getElementById("user-id");
  const usernameField = document.getElementById("user-username");
  const passwordField = document.getElementById("user-password");
  const bandField = document.getElementById("user-auth-threshold-band");

  if (idField) idField.value = user.id;
  if (usernameField) usernameField.value = user.username;
  if (passwordField) passwordField.value = ""; // Clear password field for security
  if (bandField) bandField.value = user.auth_threshold_band ?? "";

  const cancelBtn = document.getElementById("cancel-user-edit");
  const submitBtn = document.querySelector("#users button[type='submit']");

  if (cancelBtn) cancelBtn.style.display = "inline";
  if (submitBtn) submitBtn.textContent = "Update User";
}

function cancelUserEdit() {
  document.getElementById("user-id").value = "";
  document.getElementById("user-username").value = "";
  document.getElementById("user-password").value = "";
  document.getElementById("user-auth-threshold-band").value = "";

  document.getElementById("cancel-user-edit").style.display = "none";
  document.querySelector("#users button[type='submit']").textContent = "Add User";
}

async function deleteUser(id) {
  // Replaced confirm with a custom modal or message box for confirmation
  if (!await confirmAction("Are you sure you want to delete this user?")) return;

  try {
    const res = await fetch(`/lookups/users/${id}`, { method: "DELETE" });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Delete failed");
    }

    window.fetchUsers(); // Refresh the list after deletion
    displayMessage("User deleted.", "success");
  } catch (err) {
    console.error("Failed to delete user:", err);
    displayMessage("Failed to delete user. " + err.message, "error");
  }
}

// --- Custom Message Box Functions (replacing alert/confirm) ---
// These are exposed globally for use by other scripts (like the modal's save logic)
window.displayMessage = function(message, type = "info") {
  // For simplicity, using console.log. In a real app,
  // you'd render this message in a dedicated UI element (e.g., a custom modal/toast).
  console.log(`[${type.toUpperCase()}] ${message}`);
  // Example:
  // const messageBox = document.getElementById('message-box');
  // messageBox.textContent = message;
  // messageBox.className = `message-box ${type}`;
  // messageBox.style.display = 'block';
  // setTimeout(() => messageBox.style.display = 'none', 3000);
}

window.confirmAction = function(message) {
  // For simplicity, using window.confirm for now.
  // In a real app, this would be a custom confirmation modal
  // that returns a Promise resolving to true/false.
  return Promise.resolve(window.confirm(message));
}
