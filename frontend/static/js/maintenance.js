// File: /frontend/static/js/maintenance.js

// ----------------- Tab Switching ------------------
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(tab.dataset.tab).classList.add("active");
    });
  });

  fetchUsers();
  fetchRequesters();
  fetchItems();
  fetchSuppliers();
  fetchProjects();
  fetchSettings();
  fetchBusinessDetails();
});

// ----------------- Users ------------------
async function fetchUsers() {
  try {
    const res = await fetch("/users");  // Removed /lookups prefix
    const data = await res.json();
    const tbody = document.getElementById("users-table");
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
      thresholdBandCell.textContent = user.auth_threshold_band || 'Not Set';
      row.appendChild(thresholdBandCell);
      
      const actionsCell = document.createElement("td");
      const editButton = document.createElement("button");
      editButton.textContent = "Edit";
      editButton.onclick = () => editUser(user.id, user.username, user.rights, user.auth_threshold_band);
      actionsCell.appendChild(editButton);
      
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.onclick = () => deleteUser(user.id);
      actionsCell.appendChild(deleteButton);
      
      row.appendChild(actionsCell);
      tbody.appendChild(row);
    });
  } catch (err) { console.error("Failed to fetch users:", err); }
}

async function addUser() {
  const username = document.getElementById("user-username").value;
  const password = document.getElementById("user-password").value;
  const rights = document.getElementById("user-rights").value;
  const auth_threshold_band = document.getElementById("user-auth-threshold-band").value || null;
  try {
    const res = await fetch("/users", {  // Removed /lookups prefix
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, rights, auth_threshold_band })
    });
    if (res.ok) {
      fetchUsers();
      cancelUserEdit();
    }
  } catch (err) { console.error("Failed to add user:", err); }
}

async function editUser(id, username, rights, auth_threshold_band) {
  document.getElementById("user-id").value = id;
  document.getElementById("user-username").value = username;
  document.getElementById("user-rights").value = rights;
  document.getElementById("user-auth-threshold-band").value = auth_threshold_band || '';
  document.getElementById("user-password").value = '';
  document.getElementById("cancel-user-edit").style.display = "inline";
}

function cancelUserEdit() {
  document.getElementById("user-id").value = "";
  document.getElementById("user-username").value = "";
  document.getElementById("user-password").value = "";
  document.getElementById("user-rights").value = "Edit";
  document.getElementById("user-auth-threshold-band").value = "";
  document.getElementById("cancel-user-edit").style.display = "none";
}

async function deleteUser(id) {
  try {
    const res = await fetch(`/users/${id}`, { method: "DELETE" });  // Removed /lookups prefix
    if (res.ok) fetchUsers();
  } catch (err) { console.error("Failed to delete user:", err); }
}

// ----------------- Requesters ------------------
async function fetchRequesters() {
  try {
    const res = await fetch("/lookups/requesters");
    const data = await res.json();
    const tbody = document.getElementById("requesters-table");
    tbody.innerHTML = "";
    data.requesters.forEach(requester => {
      const row = document.createElement("tr");
      
      const nameCell = document.createElement("td");
      nameCell.textContent = requester.name;
      row.appendChild(nameCell);
      
      const actionsCell = document.createElement("td");
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.onclick = () => deleteRequester(requester.id);
      actionsCell.appendChild(deleteButton);
      
      row.appendChild(actionsCell);
      tbody.appendChild(row);
    });
  } catch (err) { console.error("Failed to fetch requesters:", err); }
}

async function addRequester() {
  const name = document.getElementById("requester-name").value;
  try {
    const res = await fetch("/lookups/requesters", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name })
    });
    if (res.ok) fetchRequesters();
  } catch (err) { console.error("Failed to add requester:", err); }
}

async function deleteRequester(id) {
  try {
    const res = await fetch(`/lookups/requesters/${id}`, { method: "DELETE" });
    if (res.ok) fetchRequesters();
  } catch (err) { console.error("Failed to delete requester:", err); }
}

// ----------------- Items ------------------
async function fetchItems() {
  try {
    const res = await fetch("/lookups/items");
    const data = await res.json();
    const tbody = document.getElementById("items-table");
    tbody.innerHTML = "";
    data.items.forEach(item => {
      const row = document.createElement("tr");
      
      const codeCell = document.createElement("td");
      codeCell.textContent = item.item_code;
      row.appendChild(codeCell);
      
      const descCell = document.createElement("td");
      descCell.textContent = item.item_description;
      row.appendChild(descCell);
      
      const actionsCell = document.createElement("td");
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.onclick = () => deleteItem(item.id);
      actionsCell.appendChild(deleteButton);
      
      row.appendChild(actionsCell);
      tbody.appendChild(row);
    });
  } catch (err) { console.error("Failed to fetch items:", err); }
}

async function addItem() {
  const item_code = document.getElementById("item-code").value;
  const item_description = document.getElementById("item-description").value;
  try {
    const res = await fetch("/lookups/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item_code, item_description })
    });
    if (res.ok) fetchItems();
  } catch (err) { console.error("Failed to add item:", err); }
}

async function deleteItem(id) {
  try {
    const res = await fetch(`/lookups/items/${id}`, { method: "DELETE" });
    if (res.ok) fetchItems();
  } catch (err) { console.error("Failed to delete item:", err); }
}

// ----------------- Suppliers ------------------
async function fetchSuppliers() {
  try {
    const res = await fetch("/lookups/suppliers");
    const data = await res.json();
    const tbody = document.getElementById("suppliers-table");
    tbody.innerHTML = "";
    data.suppliers.forEach(supplier => {
      const row = document.createElement("tr");
      
      const nameCell = document.createElement("td");
      nameCell.textContent = supplier.name;
      row.appendChild(nameCell);
      
      const actionsCell = document.createElement("td");
      const editButton = document.createElement("button");
      editButton.textContent = "Edit";
      editButton.onclick = () => editSupplier(supplier.id, supplier.name);
      actionsCell.appendChild(editButton);
      
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.onclick = () => deleteSupplier(supplier.id);
      actionsCell.appendChild(deleteButton);
      
      row.appendChild(actionsCell);
      tbody.appendChild(row);
    });
  } catch (err) { console.error("Failed to fetch suppliers:", err); }
}

async function saveSupplier() {
  const id = document.getElementById("supplier-id").value;
  const name = document.getElementById("supplier-name").value;
  try {
    const method = id ? "PUT" : "POST";
    const url = id ? `/lookups/suppliers/${id}` : "/lookups/suppliers";
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name })
    });
    if (res.ok) {
      fetchSuppliers();
      cancelSupplierEdit();
    }
  } catch (err) { console.error("Failed to save supplier:", err); }
}

function editSupplier(id, name) {
  document.getElementById("supplier-id").value = id;
  document.getElementById("supplier-name").value = name;
  document.getElementById("cancel-supplier-edit").style.display = "inline";
}

function cancelSupplierEdit() {
  document.getElementById("supplier-id").value = "";
  document.getElementById("supplier-name").value = "";
  document.getElementById("cancel-supplier-edit").style.display = "none";
}

async function deleteSupplier(id) {
  try {
    const res = await fetch(`/lookups/suppliers/${id}`, { method: "DELETE" });
    if (res.ok) fetchSuppliers();
  } catch (err) { console.error("Failed to delete supplier:", err); }
}

// ----------------- Projects ------------------
async function fetchProjects() {
  try {
    const res = await fetch("/lookups/projects");
    const data = await res.json();
    const tbody = document.getElementById("projects-table");
    tbody.innerHTML = "";
    data.projects.forEach(project => {
      const row = document.createElement("tr");
      
      const codeCell = document.createElement("td");
      codeCell.textContent = project.project_code;
      row.appendChild(codeCell);
      
      const nameCell = document.createElement("td");
      nameCell.textContent = project.project_name;
      row.appendChild(nameCell);
      
      const actionsCell = document.createElement("td");
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.onclick = () => deleteProject(project.id);
      actionsCell.appendChild(deleteButton);
      
      row.appendChild(actionsCell);
      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Failed to fetch projects:", err);
  }
}

async function addProject() {
  const project_code = document.getElementById("project-code").value;
  const project_name = document.getElementById("project-name").value;
  try {
    const res = await fetch("/lookups/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_code, project_name })
    });
    if (res.ok) fetchProjects();
  } catch (err) {
    console.error("Failed to add project:", err);
  }
}

async function deleteProject(id) {
  try {
    const res = await fetch(`/lookups/projects/${id}`, { method: "DELETE" });
    if (res.ok) fetchProjects();
  } catch (err) {
    console.error("Failed to delete project:", err);
  }
}

// ----------------- Settings ------------------
async function fetchSettings() {
  try {
    const res = await fetch("/settings");  // Removed /lookups prefix
    const data = await res.json();
    document.getElementById("order-number-start").value = data.order_number_start || "";
    document.getElementById("auth-threshold-1").value = data.auth_threshold_1 || "";
    document.getElementById("auth-threshold-2").value = data.auth_threshold_2 || "";
    document.getElementById("auth-threshold-3").value = data.auth_threshold_3 || "";
    document.getElementById("auth-threshold-4").value = data.auth_threshold_4 || "";
  } catch (err) {
    console.error("Failed to fetch settings:", err);
  }
}

async function updateSettings() {
  const order_number_start = document.getElementById("order-number-start").value;
  const auth_threshold_1 = document.getElementById("auth-threshold-1").value;
  const auth_threshold_2 = document.getElementById("auth-threshold-2").value;
  const auth_threshold_3 = document.getElementById("auth-threshold-3").value;
  const auth_threshold_4 = document.getElementById("auth-threshold-4").value;
  try {
    const res = await fetch("/settings", {  // Removed /lookups prefix
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ order_number_start, auth_threshold_1, auth_threshold_2, auth_threshold_3, auth_threshold_4 })
    });
    if (res.ok) fetchSettings();
  } catch (err) {
    console.error("Failed to update settings:", err);
  }
}

// ----------------- Business Details ------------------
async function fetchBusinessDetails() {
  try {
    const res = await fetch("/lookups/business_details");
    const data = await res.json();
    document.getElementById("company-name").value = data.company_name || "";
    document.getElementById("address-line1").value = data.address_line1 || "";
    document.getElementById("address-line2").value = data.address_line2 || "";
    document.getElementById("city").value = data.city || "";
    document.getElementById("province").value = data.province || "";
    document.getElementById("postal-code").value = data.postal_code || "";
    document.getElementById("telephone").value = data.telephone || "";
    document.getElementById("vat-number").value = data.vat_number || "";
  } catch (err) {
    console.error("Failed to fetch business details:", err);
  }
}

async function updateBusinessDetails() {
  const company_name = document.getElementById("company-name").value;
  const address_line1 = document.getElementById("address-line1").value;
  const address_line2 = document.getElementById("address-line2").value;
  const city = document.getElementById("city").value;
  const province = document.getElementById("province").value;
  const postal_code = document.getElementById("postal-code").value;
  const telephone = document.getElementById("telephone").value;
  const vat_number = document.getElementById("vat-number").value;

  try {
    const res = await fetch("/lookups/business_details", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        company_name, address_line1, address_line2, city,
        province, postal_code, telephone, vat_number
      })
    });
    if (res.ok) fetchBusinessDetails();
  } catch (err) {
    console.error("Failed to update business details:", err);
  }
}