console.log("💥 users.js has been loaded");

// Safe defaults for messages/confirm
if (typeof window.displayMessage !== 'function') {
  window.displayMessage = function(message, type = "info") {
    if (type === "success") alert("✅ " + message);
    else if (type === "error") alert("❌ " + message);
    else alert(message);
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
  window.fetchUsers();

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

  const submitBtn = document.getElementById("add-user-button-main");
  if (submitBtn) submitBtn.textContent = "Add User";
}

// Exposed globally so modal can refresh after save
window.fetchUsers = async function() {
  try {
    const res = await fetch("/lookups/users");
    if (!res.ok) throw new Error("Failed to fetch users");

    const { users } = await res.json();
    const tbody = document.getElementById("users-table");
    if (!tbody) return;

    tbody.innerHTML = "";
    users.forEach(user => {
      const row = document.createElement("tr");

      let userScreenPermissions = [];
      if (Array.isArray(user.roles)) {
        userScreenPermissions = user.roles;
      } else if (typeof user.roles === 'string' && user.roles.trim() !== '') {
        try {
          const parsed = JSON.parse(user.roles);
          if (Array.isArray(parsed)) userScreenPermissions = parsed;
        } catch (e) {
          console.error(`Error parsing roles for user ${user.username}:`, e, user.roles);
        }
      }

      row.appendChild(createCell(user.username));
      row.appendChild(createCell(user.auth_threshold_band ?? "Not Set"));
      row.appendChild(createCell(user.rights));
      row.appendChild(
        createActionsCell(
          user,
          userScreenPermissions,
          user.email,
          user.can_receive_payment_notifications,
          user.can_receive_review_notifications,
          user.can_delete_transactions,
          user.can_edit_draft_orders // NEW
        )
      );

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

// Accept both notification flags and pass them into the modal (NEW: canEditDraftOrders)
function createActionsCell(user, screenPermissions, email, canReceivePaymentNotifications, canReceiveReviewNotifications, canDeleteTransactions, canEditDraftOrders) {
  const td = document.createElement("td");
  const editBtn = document.createElement("button");
  editBtn.textContent = "Edit";
  editBtn.addEventListener("click", () => {
    // Populate the main inline form (if present)
    document.getElementById("user-id").value = user.id;
    document.getElementById("user-username").value = user.username;
    document.getElementById("user-password").value = "";
    document.getElementById("user-auth-threshold-band").value = user.auth_threshold_band ?? "";
    document.getElementById("user-email").value = email ?? "";
    const payBox = document.getElementById("can-receive-payment-notifications");
    if (payBox) payBox.checked = (canReceivePaymentNotifications === 1);
    const revBox = document.getElementById("can-receive-review-notifications");
    if (revBox) revBox.checked = (canReceiveReviewNotifications === 1);
    // inline form has no "can-edit-draft-orders" checkbox — modal handles it

    // Open modal (the main editor lives there)
    if (typeof window.openEditUserModal === 'function') {
      window.openEditUserModal(
        user.id,
        user.username,
        user.auth_threshold_band ?? "",
        screenPermissions,
        email ?? "",
        canReceivePaymentNotifications,
        canReceiveReviewNotifications,
        canDeleteTransactions ?? 0,
        canEditDraftOrders ?? 0 // NEW
      );
    } else {
      console.error("openEditUserModal function is not defined globally.");
      window.displayMessage("Error: Edit modal function not available.", "error");
    }

    // Button state
    const btn = document.getElementById("add-user-button-main");
    if (btn) btn.textContent = "Update User";
    const cancelBtn = document.getElementById("cancel-user-edit");
    if (cancelBtn) cancelBtn.style.display = "inline-block";
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
  const email = emailRaw === "" ? null : emailRaw;

  const can_receive_payment_notifications =
    document.getElementById("can-receive-payment-notifications")?.checked ? 1 : 0;
  const can_receive_review_notifications =
    document.getElementById("can-receive-review-notifications")?.checked ? 1 : 0;

  // If an inline checkbox for "can-edit-draft-orders" exists, read it; else default 0 (modal covers updates)
  const can_edit_draft_orders =
    document.getElementById("can-edit-draft-orders")?.checked ? 1 : 0;

  // Selected screens (from modal)
  const screenPermissionsCheckboxes =
    document.querySelectorAll('#edit-user-modal input[name="screens"]:checked');
  const screen_permissions = Array.from(screenPermissionsCheckboxes).map(cb => cb.value);

  if (!username) {
    window.displayMessage("Username is required.", "error");
    return;
  }

  if (!id) {
    if (!password || password.length < 4) {
      window.displayMessage("Password is required and must be at least 4 characters when adding a new user.", "error");
      return;
    }
  } else if (password && password.length < 4) {
    window.displayMessage("Password must be at least 4 characters if provided for an existing user.", "error");
    return;
  }

  const payload = {
    username,
    rights: "edit",
    auth_threshold_band,
    email,
    can_receive_payment_notifications,
    can_receive_review_notifications,
    can_edit_draft_orders // NEW
  };
  if (!id || (password && password.length >= 4)) {
    payload.password = password;
  }
  if (id) {
    payload.screen_permissions = screen_permissions;
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
      const error = await res.json().catch(() => ({}));
      throw new Error(typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail) || "Unknown error");
    }

    window.fetchUsers();
    cancelUserEdit();
    window.displayMessage("User saved successfully.", "success");
  } catch (err) {
    console.error("Failed to save user:", err);
    window.displayMessage("Failed to save user. " + (err.message || err), "error");
  }
}

function cancelUserEdit() {
  document.getElementById("user-id").value = "";
  document.getElementById("user-username").value = "";
  document.getElementById("user-password").value = "";
  document.getElementById("user-auth-threshold-band").value = "";
  document.getElementById("user-email").value = "";
  const payBox = document.getElementById("can-receive-payment-notifications");
  if (payBox) payBox.checked = false;
  const revBox = document.getElementById("can-receive-review-notifications");
  if (revBox) revBox.checked = false;
  const ced = document.getElementById("can-edit-draft-orders");
  if (ced) ced.checked = false;

  document.querySelectorAll("#edit-user-modal input[name='screens']").forEach(cb => { cb.checked = false; });

  const cancelBtn = document.getElementById("cancel-user-edit");
  if (cancelBtn) cancelBtn.style.display = "none";
  const btn = document.getElementById("add-user-button-main");
  if (btn) btn.textContent = "Add User";
}

async function deleteUser(id) {
  if (!await window.confirmAction("Are you sure you want to delete this user?")) return;
  try {
    const res = await fetch(`/lookups/users/${id}`, { method: "DELETE" });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Delete failed");
    }
    window.fetchUsers();
    window.displayMessage("User deleted.", "success");
  } catch (err) {
    console.error("Failed to delete user:", err);
    window.displayMessage("Failed to delete user. " + err.message, "error");
  }
}
