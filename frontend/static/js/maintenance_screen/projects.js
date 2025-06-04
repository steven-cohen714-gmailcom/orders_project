// File: /frontend/static/js/maintenance_screen/projects.js

export function initProjects() {
  console.log("initProjects loaded");

  fetchProjects();

  const addBtn = document.getElementById("add-project-button");
  if (addBtn) {
    addBtn.addEventListener("click", addProject);
  }

  async function fetchProjects() {
    try {
      const res = await fetch("/lookups/projects");
      const data = await res.json();
      const tbody = document.getElementById("projects-table");
      if (!tbody) return;

      tbody.innerHTML = "";
      data.projects.forEach(project => {
        const row = createRow(project);
        tbody.appendChild(row);
      });
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  }

  async function addProject() {
    const project_code = document.getElementById("project-code")?.value.trim();
    const project_name = document.getElementById("project-name")?.value.trim();

    if (!project_code || !project_name) {
      alert("❌ Please enter both project code and name.");
      return;
    }

    try {
      const res = await fetch("/lookups/projects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_code, project_name })
      });

      if (res.ok) {
        const newProject = await res.json(); // Should return { id, project_code, project_name }
        const row = createRow(newProject);

        const tbody = document.getElementById("projects-table");
        tbody.insertBefore(row, tbody.firstChild); // Add new project at top

        alert("✅ Project added successfully.");

        document.getElementById("project-code").value = "";
        document.getElementById("project-name").value = "";
      } else {
        const errMsg = await res.text();
        alert(`❌ Failed to save project: ${errMsg}`);
      }
    } catch (err) {
      console.error("Failed to add project:", err);
      alert("❌ Network or server error");
    }
  }

  async function deleteProject(id) {
    try {
      const res = await fetch(`/lookups/projects/${id}`, { method: "DELETE" });
      if (res.ok) {
        alert("🗑️ Project deleted");
        fetchProjects();
      } else {
        const errMsg = await res.text();
        alert(`❌ Failed to delete: ${errMsg}`);
      }
    } catch (err) {
      console.error("Failed to delete project:", err);
      alert("❌ Network or server error");
    }
  }

  function createRow(project) {
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
    return row;
  }
}
