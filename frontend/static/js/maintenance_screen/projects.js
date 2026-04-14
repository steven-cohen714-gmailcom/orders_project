// File: /frontend/static/js/maintenance_screen/projects.js

export function initProjects() {
  console.log("✅ initProjects loaded");

  fetchProjects();

  const addBtn = document.getElementById("save-project-button");
  const cancelBtn = document.getElementById("cancel-project-edit");

  if (addBtn) addBtn.addEventListener("click", saveProject);
  if (cancelBtn) cancelBtn.addEventListener("click", clearForm);
}

async function fetchProjects() {
  try {
    const res = await fetch("/lookups/projects");
    const data = await res.json();

    const tbody = document.getElementById("projects-table");
    if (!tbody) return;
    tbody.innerHTML = "";

    data.projects.forEach(project => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${project.project_code}</td>
        <td>${project.project_name}</td>
        <td><button onclick="deleteProject(${project.id})">Delete</button></td>
      `;

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("❌ Failed to load projects", err);
    alert("❌ Failed to load projects");
  }
}

async function saveProject() {
  const code = document.getElementById("project-code")?.value.trim();
  const name = document.getElementById("project-name")?.value.trim();

  const errorDiv = document.getElementById("project-form-error");
  if (!code || !name) {
    if (errorDiv) errorDiv.style.display = "block";
    return;
  } else {
    if (errorDiv) errorDiv.style.display = "none";
  }

  try {
    const res = await fetch("/lookups/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_code: code, project_name: name }),
    });

    if (res.ok) {
      clearForm();
      fetchProjects();
      alert("✅ Project added");
    } else {
      const msg = await res.text();
      alert(`❌ ${msg}`);
    }
  } catch (err) {
    console.error("❌ Network/server error", err);
    alert("❌ Network/server error");
  }
}

window.deleteProject = async function (id) {
  try {
    const res = await fetch(`/lookups/projects/${id}`, { method: "DELETE" });
    if (res.ok) {
      fetchProjects();
      alert("🗑️ Project deleted");
    } else {
      const msg = await res.text();
      alert(`❌ ${msg}`);
    }
  } catch (err) {
    console.error("❌ Network/server error", err);
    alert("❌ Network/server error");
  }
};

function clearForm() {
  document.getElementById("project-id").value = "";
  document.getElementById("project-code").value = "";
  document.getElementById("project-name").value = "";
  const err = document.getElementById("project-form-error");
  if (err) err.style.display = "none";
}
