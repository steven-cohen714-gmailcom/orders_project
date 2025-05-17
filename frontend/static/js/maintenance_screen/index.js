// /frontend/static/js/maintenance_screen/index.js

import { initUsers } from "./users.js";
import { initRequesters } from "./requesters.js";
import { initItems } from "./items.js";
import { initSuppliers } from "./suppliers.js";
import { initProjects } from "./projects.js";
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

export function initMaintenanceScreen() {
  initTabs(); // 👈 critical
  initUsers();
  initRequesters();
  initItems();
  initSuppliers();
  initProjects();
  initSettings();
  initBusinessDetails();
}
