// File: /frontend/static/js/maintenance_screen/index.js

import { initUsers } from "./users.js";
import { initRequesters } from "./requesters.js";
import { initItems } from "./items.js";
import { initSuppliers } from "./suppliers.js";
import { initProjects } from "./projects.js";
import { initRequisitioners } from "./requisitioners.js";
import { initSettings } from "./settings.js";
import { initBusinessDetails } from "./business_details.js";

const initFunctions = {
  users: initUsers,
  requesters: initRequesters,
  items: initItems,
  suppliers: initSuppliers,
  projects: initProjects,
  requisitioners: initRequisitioners,
  settings: initSettings,
  business_details: initBusinessDetails
};

function initTabs() {
  const tabs = document.querySelectorAll(".tab");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const activeId = tab.dataset.tab;
      const contentEl = document.getElementById(activeId);
      if (contentEl) contentEl.classList.add("active");

      // Lazy-load init function only once per tab
      if (!tab.dataset.initialized && initFunctions[activeId]) {
        initFunctions[activeId]();
        tab.dataset.initialized = "true";
      }
    });
  });

  // Immediately init the default active tab (e.g. Users)
  const defaultTab = document.querySelector(".tab.active");
  if (defaultTab) {
    const defaultId = defaultTab.dataset.tab;
    if (initFunctions[defaultId]) {
      initFunctions[defaultId]();
      defaultTab.dataset.initialized = "true";
    }
  }
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

  // Bind CSV import buttons globally
  handleCsvImport("import-items-button", "items-csv-upload", "/maintenance/import_items_csv", "items");
  handleCsvImport("import-suppliers-button", "suppliers-csv-upload", "/maintenance/import_suppliers_csv", "suppliers");
  handleCsvImport("import-projects-button", "projects-csv-upload", "/maintenance/import_projects_csv", "projects");
}
