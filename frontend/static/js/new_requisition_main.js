// File: frontend/static/js/new_requisition_main.js

import { logToServer, populateDropdown } from "./components/utils.js";

let rowCount = 0;

// Load requisitioners and projects on page load
document.addEventListener("DOMContentLoaded", async () => {
  await populateDropdown("/lookups/requisitioners", "requisitioner");
  await populateDropdown("/lookups/projects", "project-template", true); // hidden <select> for cloning
  addLineItem(); // Start with one row

  document.getElementById("add-line").addEventListener("click", addLineItem);
  document.getElementById("submit-requisition").addEventListener("click", submitRequisition);
  document.getElementById("preview-pdf").addEventListener("click", previewPDF); // placeholder
});

function addLineItem() {
  const tbody = document.getElementById("line-items-body");
  const row = document.createElement("tr");
  row.dataset.row = rowCount;

  row.innerHTML = `
    <td><input type="text" class="description" required placeholder="Enter item description"></td>
    <td>${getProjectDropdown()}</td>
    <td><input type="number" class="quantity" required min="0" step="1" value="1"></td>
    <td><button type="button" onclick="this.closest('tr').remove()">🗑️</button></td>
  `;

  tbody.appendChild(row);
  rowCount++;
}

function getProjectDropdown() {
  const template = document.getElementById("project-template");
  if (!template) return '<input type="text" placeholder="Missing project list">';
  return template.outerHTML.replace('id="project-template"', '').replace("display:none;", "");
}

async function submitRequisition() {
  const log = document.getElementById("requisition-log");
  log.textContent = "";

  const requisitionerId = document.getElementById("requisitioner").value;
  const note = document.getElementById("requisition-note").value;
  if (!requisitionerId) {
    log.textContent = "⚠️ Please select a requisitioner.";
    return;
  }

  const items = [];
  document.querySelectorAll("#line-items-body tr").forEach(row => {
    const desc = row.querySelector(".description").value.trim();
    const qty = parseFloat(row.querySelector(".quantity").value);
    const project = row.querySelector("select")?.value || "";

    if (desc && qty > 0) {
      items.push({ description: desc, project, quantity: qty });
    }
  });

  if (items.length === 0) {
    log.textContent = "⚠️ Please add at least one valid line item.";
    return;
  }

  try {
    const settings = await fetch("/lookups/settings").then(res => res.json());
    const nextReqNum = settings.requisition_number_start || "REQ1000";

    const payload = {
      requisition_number: nextReqNum,
      requisitioner_id: parseInt(requisitionerId),
      requisition_note: note,
      items
    };

    const res = await fetch("/requisitions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
      log.textContent = `✅ Requisition submitted (ID: ${data.requisition_id})`;
    } else {
      log.textContent = `❌ Submission failed: ${data.detail}`;
    }

  } catch (err) {
    log.textContent = `❌ Error: ${err.message}`;
  }
}

function previewPDF() {
  alert("📄 PDF preview not yet implemented."); // will hook into WeasyPrint route later
}
