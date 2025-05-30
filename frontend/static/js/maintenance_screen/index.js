import { initUsers } from "./users.js";
import { initRequesters } from "./requesters.js";
import { initItems } from "./items.js";
import { initSuppliers } from "./suppliers.js";
import { initProjects } from "./projects.js";
import { initRequisitioners } from "./requisitioners.js";
import { initSettings } from "./settings.js";
import { initBusinessDetails } from "./business_details.js";

function initTabs() {
  const tabs = document.querySelectorAll(".tab");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const activeId = tab.dataset.tab;
      document.getElementById(activeId).classList.add("active");
    });
  });
}

function handleCsvImport(buttonId, fileInputId, endpoint, label) {
  const button = document.getElementById(buttonId);
  const fileInput = document.getElementById(fileInputId);

  if (!button || !fileInput) return;

  button.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) {
      alert(`Please select a CSV file to import ${label}.`);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(`Server error: ${err}`);
      }

      const result = await response.json();
      alert(`✅ Imported ${result.inserted} ${label} successfully.`);
      location.reload();
    } catch (error) {
      console.error(`❌ Import failed for ${label}:`, error);
      alert(`Import failed. Check console for ${label} details.`);
    }
  });
}

export function initMaintenanceScreen() {
  initTabs();
  initUsers();
  initRequesters();
  initItems();
  initSuppliers();
  initProjects();
  initSettings();
  initBusinessDetails();
  initRequisitioners();

  // ✅ CSV import handlers
  handleCsvImport("import-items-button", "items-csv-upload", "/maintenance/import_items_csv", "items");
  handleCsvImport("import-suppliers-button", "suppliers-csv-upload", "/maintenance/import_suppliers_csv", "suppliers");
  handleCsvImport("import-projects-button", "projects-csv-upload", "/maintenance/import_projects_csv", "projects");
}
