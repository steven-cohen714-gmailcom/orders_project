// File: frontend/static/js/maintenance_screen/users.js
console.log("💥 users.js has been loaded");

// IMPORTANT: Define window.displayMessage and window.confirmAction here as fallbacks
// or early definitions to ensure they are always available when users.js runs.
// This prevents "window.displayMessage is not a function" if base.html script loads later.
if (typeof window.displayMessage !== 'function') {
  window.displayMessage = function(message, type = "info") {
    if (type === "success") {
      alert("✅ " + message);
    } else if (type === "error") {
      alert("❌ " + message);
    } else {
      alert(message);
    }
    console.log(`[${type.toUpperCase()}] ${message}`);
  };
}

if (typeof window.confirmAction !== 'function') {
  window.confirmAction = function(message) {
    return Promise.resolve(window.confirm(message));
  };
}


export function initUsers() {
  console.log("initUsers loaded");
  window.fetchUsers(); // Call global fetchUsers to populate the table initially

  const cancelBtn = document.getElementById("cancel-user-edit");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", cancelUserEdit);
    cancelBtn.style.display = "none"; // Ensure it's hidden by default on page load
  }

  const form = document.querySelector("#users form");
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      await addOrUpdateUser();
    });
  }

  const submitBtn = document.getElementById("add-user-button-main"); // Correctly target by ID as per maintenance.html
  if (submitBtn) {
    submitBtn.textContent = "Add User"; // Set default text
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

      let userScreenPermissions = [];
      // Backend now sends "roles" as screen_permissions from the 'screen_permissions' table
      if (Array.isArray(user.roles)) { 
        userScreenPermissions = user.roles;
      } else if (typeof user.roles === 'string' && user.roles.trim() !== '') {
        try {
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

      row.appendChild(createCell(user.username));
      row.appendChild(createCell(user.auth_threshold_band ?? "Not Set"));
      row.appendChild(createCell(user.rights)); // 'rights' field is still present
      // Pass the full user object including permissions, email, and payment notifications to the actions cell
      row.appendChild(createActionsCell(user, userScreenPermissions, user.email, user.can_receive_payment_notifications)); 

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Failed to fetch users:", err);
    window.displayMessage("Failed to fetch users: " + err.message, "error");
  }
}

function createCell(content) {
  const td = document.createElement("td");
  td.textContent = content;
  return td;
}

// Modified: accept screenPermissions, email, and canReceivePaymentNotifications for the modal
function createActionsCell(user, screenPermissions, email, canReceivePaymentNotifications) {
  const td = document.createElement("td");

  const editBtn = document.createElement("button");
  editBtn.textContent = "Edit";
  console.log("Attaching edit button for:", user.username);
  editBtn.addEventListener("click", () => {
    // Populate the main form fields with user data for editing
    document.getElementById("user-id").value = user.id;
    document.getElementById("user-username").value = user.username;
    document.getElementById("user-password").value = ""; // Always clear password for security
    document.getElementById("user-auth-threshold-band").value = user.auth_threshold_band ?? "";
    document.getElementById("user-email").value = user.email ?? "";
    document.getElementById("can-receive-payment-notifications").checked = (user.can_receive_payment_notifications === 1);

    // Ensure the edit modal's screen permissions are populated (if applicable, as edit_user_modal is an include)
    if (typeof window.openEditUserModal === 'function') { // Check if the modal's function exists
      window.openEditUserModal(user.id, user.username, user.auth_threshold_band ?? "", screenPermissions, user.email, user.can_receive_payment_notifications); 
    } else {
      console.error("openEditUserModal function is not defined globally.");
      window.displayMessage("Error: Edit modal function not available.", "error");
    }

    // Update button text and show cancel button
    document.getElementById("add-user-button-main").textContent = "Update User";
    document.getElementById("cancel-user-edit").style.display = "inline-block"; // Show cancel button
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
  
  const emailRaw = document.getElementById("user-email")?.value.trim();
  const email = emailRaw === "" ? null : emailRaw; // Send null if empty string

  const can_receive_payment_notifications = document.getElementById("can-receive-payment-notifications")?.checked ? 1 : 0;

  // --- Gather selected screen permissions from modal form ---
  const screenPermissionsCheckboxes = document.querySelectorAll('#edit-user-modal input[name="screens"]:checked'); // Corrected name to 'screens'
  const screen_permissions = Array.from(screenPermissionsCheckboxes).map(cb => cb.value);

  if (!username) {
    window.displayMessage("Username is required.", "error");
    return;
  }

  // Frontend password validation for new users
  if (!id) { // Only validate password min_length if it's a NEW user
    if (!password || password.length < 4) {
      window.displayMessage("Password is required and must be at least 4 characters when adding a new user.", "error");
      return;
    }
  } else if (password && password.length < 4) { // Validate password if provided for existing user
    window.displayMessage("Password must be at least 4 characters if provided for an existing user.", "error");
    return;
  }
  // If password is empty for an existing user (id is present), it's not sent, which is fine for no-change.

  const payload = {
    username,
    rights: "edit", // hardcoded for now
    auth_threshold_band,
    email, 
    can_receive_payment_notifications 
  };
  // Only include password in payload if it's new user or explicitly set for update
  if (!id || (password && password.length >= 4)) { // Ensure password is sent only if new or valid length for update
    payload.password = password;
  }
  
  // --- Add screen_permissions to payload for UPDATE operations ---
  if (id) { // Only send screen_permissions if updating an existing user (PUT request)
      payload.screen_permissions = screen_permissions; 
  }
  // --- END Adding ---

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
      // Throw the actual backend error details for better debugging
      // Prioritize error.detail if it's a string, otherwise stringify the whole object
      throw new Error(typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail) || "Unknown error"); 
    }

    // After adding/updating, refresh the list and reset the form
    window.fetchUsers();
    cancelUserEdit(); // Call cancelUserEdit to clear form and reset buttons
    window.displayMessage("User saved successfully.", "success");
  } catch (err) {
    console.error("Failed to save user:", err);
    window.displayMessage("Failed to save user. " + (err.message || err), "error");
  }
}

// The original populateUserForm function is no longer needed as logic is moved to createActionsCell.
// This block ensures it's fully removed to avoid confusion.
// function populateUserForm(user) {
//   console.log("populateUserForm called (old logic, should not be for modal):", user);
//   const idField = document.getElementById("user-id");
//   const usernameField = document.getElementById("user-username");
//   const passwordField = document.getElementById("user-password");
//   const bandField = document.getElementById("user-auth-threshold-band");
//   const emailField = document.getElementById("user-email"); 
//   const canReceivePaymentsCheckbox = document.getElementById("can-receive-payment-notifications"); 
//
//   if (idField) idField.value = user.id;
//   if (usernameField) usernameField.value = user.username;
//   if (passwordField) passwordField.value = ""; // Clear password field for security
//   if (bandField) bandField.value = user.auth_threshold_band ?? "";
//   if (emailField) emailField.value = user.email ?? ""; 
//   if (canReceivePaymentsCheckbox) canReceivePaymentsCheckbox.checked = (user.can_receive_payment_notifications === 1); 
//
//   const cancelBtn = document.getElementById("cancel-user-edit");
//   const submitBtn = document.querySelector("#users button[type='submit']");
//
//   if (cancelBtn) cancelBtn.style.display = "inline";
//   if (submitBtn) submitBtn.textContent = "Update User";
// }


function cancelUserEdit() {
  document.getElementById("user-id").value = "";
  document.getElementById("user-username").value = "";
  document.getElementById("user-password").value = ""; // Clear password field
  document.getElementById("user-auth-threshold-band").value = ""; 
  
  // Clear modal specific fields
  document.getElementById("user-email").value = "";
  document.getElementById("can-receive-payment-notifications").checked = false;

  // Ensure all screen permission checkboxes in the modal are unchecked
  document.querySelectorAll("#edit-user-modal input[name='screens']").forEach(cb => { // Corrected name to 'screens'
    cb.checked = false; // Uncheck all checkboxes
  });

  // Reset button texts and visibility
  document.getElementById("cancel-user-edit").style.display = "none";
  document.getElementById("add-user-button-main").textContent = "Add User";
}

async function deleteUser(id) {
  if (!await window.confirmAction("Are you sure you want to delete this user?")) return;
  try {
    const res = await fetch(`/lookups/users/${id}`, { method: "DELETE" });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Delete failed");
    }

    window.fetchUsers(); // Refresh the list after deletion
    window.displayMessage("User deleted.", "success");
  } catch (err) {
    console.error("Failed to delete user:", err);
    window.displayMessage("Failed to delete user. " + err.message, "error");
  }
}

// --- Custom Message Box Functions (replacing alert/confirm) ---
// These are exposed globally for use by other scripts (like the modal's save logic)
// These functions are now defined in base.html script, so no need to redefine here.
// They are commented out to prevent re-declaration errors if base.html is loaded.
/*
window.displayMessage = function(message, type = "info") {
  console.log(`[${type.toUpperCase()}] ${message}`);
};

window.confirmAction = function(message) {
  return Promise.resolve(window.confirm(message));
};
*/