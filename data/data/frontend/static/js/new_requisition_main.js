// File: frontend/static/js/new_requisition_main.js
import { logToServer, populateDropdown } from "./components/utils.js";

let rowCount = 0;
let currentRequisitionId = null;
let currentRequisitionNumber = null;

document.addEventListener("DOMContentLoaded", async () => {
  await populateDropdown("/lookups/requisitioners", "requisitioner");
  addLineItem();

  try {
    const settings = await fetch("/lookups/settings").then(res => res.json());
    const nextReqNum = settings.requisition_number_start || "REQ1000";
    const today = new Date().toISOString().split("T")[0];

    currentRequisitionNumber = nextReqNum;
    document.getElementById("requisition-number").value = nextReqNum;
    document.getElementById("requisition-date").value = today;
  } catch (err) {
    console.error("❌ Failed to load settings:", err);
  }

  document.getElementById("add-line").addEventListener("click", addLineItem);
  document.getElementById("submit-requisition").addEventListener("click", submitRequisition);
});

function addLineItem() {
  const tbody = document.getElementById("line-items-body");
  const row = document.createElement("tr");
  row.dataset.row = rowCount;

  row.innerHTML = `
    <td><input type="text" class="description" required placeholder="Enter item description"></td>
    <td><input type="number" class="quantity" required min="0" step="1" value="1"></td>
    <td><button type="button" onclick="this.closest('tr').remove()">🗑️</button></td>
  `;

  tbody.appendChild(row);
  rowCount++;
}

async function submitRequisition() {
  const log = document.getElementById("requisition-log");
  log.textContent = "";

  const requisitionerId = document.getElementById("requisitioner").value;
  const note = document.getElementById("requisition-note").value;
  const date = document.getElementById("requisition-date").value;

  if (!requisitionerId) {
    log.textContent = "⚠️ Please select a requisitioner.";
    alert("⚠️ Please select a requisitioner."); // Added alert 
    return;
  }

  const items = [];
  document.querySelectorAll("#line-items-body tr").forEach(row => {
    const desc = row.querySelector(".description").value.trim();
    const qty = parseFloat(row.querySelector(".quantity").value);

    if (desc && qty > 0) {
      items.push({ description: desc, quantity: qty });
    }
  });

  if (items.length === 0) {
    log.textContent = "⚠️ Please add at least one valid line item.";
    alert("⚠️ Please add at least one valid line item."); // Added alert 
    return;
  }

  try {
    const payload = {
      requisition_number: currentRequisitionNumber,
      requisitioner_id: parseInt(requisitionerId),
      requisition_note: note,
      requisition_date: date,
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
      alert(`✅ Requisition ${currentRequisitionNumber} submitted successfully!`); // Added prominent alert 
      currentRequisitionId = data.requisition_id;
      // Optional: Clear form after successful submission
      document.getElementById("requisitioner").value = "";
      document.getElementById("requisition-note").value = "";
      document.getElementById("line-items-body").innerHTML = ""; // Clear line items
      addLineItem(); // Add one empty line item for next requisition
      // Reload order number (if it increments on backend)
      const settings = await fetch("/lookups/settings").then(res => res.json()); // Fetch updated settings
      const nextReqNum = settings.requisition_number_start; // Use updated number from settings 
      currentRequisitionNumber = nextReqNum;
      document.getElementById("requisition-number").value = nextReqNum;
    } else {
      log.textContent = `❌ Submission failed: ${data.detail}`;
      alert(`❌ Submission failed: ${data.detail}`); // Added alert 
    }

  } catch (err) {
    log.textContent = `❌ Error: ${err.message}`;
    alert(`❌ Error: ${err.message}`); // Added alert 
  }
}

function previewPDF() {
  alert("📄 PDF preview not yet implemented.");
}