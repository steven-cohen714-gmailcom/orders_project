// /frontend/static/js/maintenance_screen/projects.js
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
    const project_code = document.getElementById("project-code")?.value;
    const project_name = document.getElementById("project-name")?.value;

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
}
