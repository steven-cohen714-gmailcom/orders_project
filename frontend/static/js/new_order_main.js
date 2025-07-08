// File: frontend/static/js/new_order_main.js

import { previewOrder } from "./new_order_screen/pdf_utils.js";
import { submitOrder } from "./new_order_screen/submit_utils.js";
import { logToServer } from "./components/utils.js";
import { createFuzzyDropdown } from "./components/fuzzy_dropdown.js"; // UNCOMMENTED

let itemsList = [];
let projectsList = [];
let rowCount = 0;
let currentOrderNumber = "URC1000";
let authThreshold = 0; // Added for authorization threshold
let currentOrderId = null; // Added to store order ID after submission

// Debounce function
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
      const later = () => {
          clearTimeout(timeout);
          func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
  };
}

// Load dropdowns
async function loadDropdowns() {
  try {
      const requestersData = await fetchData("/lookups/requesters");
      populateDropdown("requester_id", requestersData?.requesters, "name");
      
      // UNCOMMENTED: Re-enable fuzzy dropdown calls
      await createFuzzyDropdown("supplier_id", "/lookups/suppliers");

      const itemsData = await fetchData("/lookups/items");
      itemsList = itemsData?.items || [];
      await createFuzzyDropdown("item-template", "/lookups/items"); // Use item-template for fuzzy search

      const projectsData = await fetchData("/lookups/projects");
      projectsList = projectsData?.projects || [];
      await createFuzzyDropdown("project-template", "/lookups/projects"); // Use project-template for fuzzy search

      // REMOVED: Old temporary populateDropdown fallbacks
      // const suppliersData = await fetchData("/lookups/suppliers");
      // populateDropdown("supplier_id", suppliersData?.suppliers, "name");
      // populateDropdown("item-template", itemsList, "item_description", "item_code");
      // populateDropdown("project-template", projectsList, "project_name", "project_code");

  } catch (error) {
      console.error("Error loading dropdowns:", error);
      throw error;
  }
}

// Load order number and authorization threshold
async function loadOrderNumber() {
  try {
      const settingsData = await fetchData("/lookups/settings");
      currentOrderNumber = settingsData.order_number_start || "URC1000";
      authThreshold = [
        parseFloat(settingsData.auth_threshold_1 || 0),
        parseFloat(settingsData.auth_threshold_2 || 0),
        parseFloat(settingsData.auth_threshold_3 || 0),
        parseFloat(settingsData.auth_threshold_4 || 0)
      ];
      
      document.getElementById("order-number").textContent = currentOrderNumber;
  } catch (error) {
      console.error("Error loading order number:", error);
      document.getElementById("order-number").textContent = "URC1000"; // Fallback
  }
}

// Added: Function to increment and update order number
async function incrementOrderNumber(currentOrderNumber) {
  const current = currentOrderNumber.match(/\d+$/);
  const prefix = currentOrderNumber.replace(/\d+$/, "");
  const nextNum = current ? String(parseInt(current[0]) + 1).padStart(4, "0") : "1001";
  const newOrderNumber = `${prefix}${nextNum}`;

  try {
      const res = await fetch('/lookups/order_number', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ order_number_start: newOrderNumber })
      });

      if (!res.ok) {
          const errorText = await res.text();
          console.error("Failed to update order number:", errorText);
      }

      return newOrderNumber;
  } catch (err) {
      console.error("Exception during order number update:", err.message);
      return currentOrderNumber;  // fallback
  }
}

// Add a row to the table
function addRow() {
  const tbody = document.getElementById("items-body");
  const row = document.createElement("tr");
  row.id = `row_${rowCount++}`;

  // Item Code dropdown
  const itemCell = document.createElement("td");
  const itemSelect = document.createElement("select");
  itemSelect.className = "item-code wide-select";
  itemSelect.id = `item_code_${rowCount}`;
  itemSelect.innerHTML = '<option value="">Select Item</option>';
  // MODIFIED: No direct population here, TomSelect will handle it
  itemCell.appendChild(itemSelect);
  row.appendChild(itemCell);

  // Project dropdown
  const projectCell = document.createElement("td");
  const projectSelect = document.createElement("select");
  projectSelect.className = "project wide-select";
  projectSelect.id = `project_${rowCount}`;
  projectSelect.innerHTML = '<option value="">Select Project</option>';
  // MODIFIED: No direct population here, TomSelect will handle it
  projectCell.appendChild(projectSelect);
  row.appendChild(projectCell);

// Quantity input
  const qtyCell = document.createElement("td");
  const qtyInput = document.createElement("input");
  qtyInput.type = "number";
  qtyInput.className = "qty-ordered narrow-input";
  qtyInput.id = `qty_${rowCount}`;
  qtyInput.value = "1";
  qtyInput.min = "1";
  qtyCell.appendChild(qtyInput);
  row.appendChild(qtyCell);

// Price input
  const priceCell = document.createElement("td");
  const priceInput = document.createElement("input");
  priceInput.type = "number";
  priceInput.className = "price narrow-input";
  priceInput.id = `price_${rowCount}`;
  priceInput.value = "0.00";
  priceInput.step = "0.01";
  priceCell.appendChild(priceInput);
  row.appendChild(priceCell);

// Total
  const totalCell = document.createElement("td");
  const totalInput = document.createElement("input");
  totalInput.type = "text";
  totalInput.className = "total medium-input";
  totalInput.id = `total_${rowCount}`;
  totalInput.value = "0.00";
  totalInput.readOnly = true;
  totalCell.appendChild(totalInput);
  row.appendChild(totalCell);

// Actions
  const actionsCell = document.createElement("td");
  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "Delete";
  deleteBtn.onclick = () => deleteRow(row.id);
  actionsCell.appendChild(deleteBtn);
  row.appendChild(actionsCell);

  tbody.appendChild(row);

  // UNCOMMENTED: Re-enable fuzzy dropdown calls for dynamically added rows
  createFuzzyDropdown(itemSelect.id, "/lookups/items");
  createFuzzyDropdown(projectSelect.id, "/lookups/projects");

  // REMOVED: Old temporary populateDropdown fallbacks
  // populateDropdown(`/lookups/items`, itemSelect.id, "item_description", "item_code");
  // populateDropdown(`/lookups/projects`, projectSelect.id, "project_name", "project_code");

  updateTotal(itemSelect);
}

// Update row total
function updateTotal(itemSelect) {
    const row = itemSelect.closest("tr");
    const qty = parseFloat(row.querySelector(".qty-ordered").value) || 0;
    const price = parseFloat(row.querySelector(".price").value) || 0;
    const total = qty * price;
    row.querySelector(".total").value = total.toFixed(2);
    updateGrandTotal();
  }
  
  // Update grand total
  function updateGrandTotal() {
    const totals = Array.from(document.querySelectorAll(".total")).map(input => parseFloat(input.value) || 0);
    const grandTotal = totals.reduce((sum, val) => sum + val, 0);
    document.getElementById("grand-total").textContent = grandTotal.toFixed(2);
    return grandTotal; // Added return for use in submitOrder
  }
  
  // Delete a row
  function deleteRow(rowId) {
    const row = document.getElementById(rowId);
    if (row) {
        row.remove();
        updateGrandTotal();
    }
  }
  
  // Modal functions (inlined since new_order_modals.js is not provided)
  function showOrderNoteModal(note, callback) {
    const modal = createBaseModal();
    const title = document.createElement("h3");
    title.textContent = "Order Note";
    modal.inner.appendChild(title);
  
    const textarea = document.createElement("textarea");
    textarea.value = note || "";
    textarea.style.width = "100%";
    textarea.style.height = "150px";
    modal.inner.appendChild(textarea);
  
    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save";
    saveBtn.style.marginTop = "1rem";
    saveBtn.onclick = () => {
        callback(textarea.value);
        document.body.removeChild(modal.container);
    };
    modal.inner.appendChild(saveBtn);
  
    const closeBtn = document.createElement("button");
    closeBtn.textContent = "Close";
    closeBtn.style.marginTop = "1rem";
    closeBtn.style.marginLeft = "1rem";
    closeBtn.onclick = () => document.body.removeChild(modal.container);
    modal.inner.appendChild(closeBtn);
  
    document.body.appendChild(modal.container);
  }
  
  function showSupplierNoteModal(note) {
    const modal = createBaseModal();
    const title = document.createElement("h3");
    title.textContent = "Note to Supplier";
    modal.inner.appendChild(title);
  
    const p = document.createElement("p");
    p.textContent = note || "No note provided";
    modal.inner.appendChild(p);
  
    const closeBtn = document.createElement("button");
    closeBtn.textContent = "Close";
    closeBtn.style.marginTop = "1rem";
    closeBtn.onclick = () => document.body.removeChild(modal.container);
    modal.inner.appendChild(closeBtn);
  
    document.body.appendChild(modal.container);
  }
  
  function createBaseModal() {
    const container = document.createElement("div");
    container.style.position = "fixed";
    container.style.top = "0";
    container.style.left = "0";
    container.style.width = "100vw";
    container.style.height = "100vh";
    container.style.backgroundColor = "rgba(0,0,0,0.5)";
    container.style.display = "flex";
    container.style.alignItems = "center";
    container.style.justifyContent = "center";
    container.style.zIndex = "9999";
  
    const inner = document.createElement("div");
    inner.style.backgroundColor = "white";
    inner.style.padding = "1.5rem";
    inner.style.borderRadius = "8px";
    inner.style.width = "90%";
    inner.style.maxWidth = "500px";
    inner.style.maxHeight = "80vh";
    inner.style.overflowY = "auto";
    container.appendChild(inner);
  
    const close = document.createElement("button");
    close.textContent = "✖";
    close.style.position = "absolute";
    close.style.top = "10px";
    close.style.right = "10px";
    close.style.background = "none";
    close.style.border = "none";
    close.style.fontSize = "1.2rem";
    close.style.cursor = "pointer";
    close.onclick = () => document.body.removeChild(container);
  
    inner.appendChild(close);
    container.appendChild(inner);
  
    return { container, inner };
  }
  
  // Core functionality
  let businessDetails = null;
  
  async function fetchData(endpoint) {
    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch ${endpoint}: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        throw error;
    }
  }
  
  function populateDropdown(dropdownId, items, key, idKey = "id") {
    const dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = '<option value="">Select ' + dropdownId.replace('_id', '') + '</option>';

    if (items && Array.isArray(items)) {
      items.forEach(item => {
        const option = document.createElement("option");
        option.value = item[idKey];
        option.textContent = item[key];

        // ✨ Description used for fuzzy filtering
        option.dataset.description = item[key]?.toLowerCase() || "";

        dropdown.appendChild(option);
      });
    }
}
  
  // Added: Function to send email
  async function sendEmail(orderId) {
      try {
          const response = await fetch(`/orders/email_purchase_order/${orderId}`, {
              method: 'POST',
              credentials: 'include'
          });
          if (!response.ok) throw new Error('Failed to send email');
          await logToServer('INFO', 'Email sent successfully', { orderId });
          alert('Email sent successfully');
      } catch (error) {
          await logToServer('ERROR', 'Failed to send email', { orderId, error: error.message });
          alert('Failed to send email: ' + error.message);
      }
  }

function setupEventListeners() {
    const submitBtn = document.getElementById('submit-order');
    if (submitBtn) {
      console.log('Submit button exists:', !!submitBtn);
      submitBtn.addEventListener('click', () => {
  console.log('Submit button clicked');
  const orderType = document.getElementById("order_type")?.value;
    if (!orderType) {
      alert("Please select an Order Type: Normal or Draft");
      return;
  }
  const isDraft = orderType === "Draft";
  const paymentTerms = document.getElementById("payment_terms")?.value || "On account";

  debounce(() => submitOrder({
    currentOrderNumber,
    authThresholds: authThreshold,
    itemsList,
    updateGrandTotal,
    incrementOrderNumber,
    logToServer,
    setCurrentOrderId: (id) => currentOrderId = id,
    setCurrentOrderNumber: (newNum) => {
      currentOrderNumber = newNum;
      resetForm();
    },

    paymentTerms,
    orderType: orderType, // "Normal" or "Draft"
    isDraft: isDraft
  }), 500)();

});

    } else {
      console.error('Submit button not found');
    }
  
    const previewBtn = document.getElementById('preview-order');
    if (previewBtn) {
      previewBtn.addEventListener('click', () => {
        previewOrder({
          itemsList, 
          updateGrandTotal, 
          logToServer });
      });
    } else {
      console.error('Preview button not found');
    }

    document.getElementById('add-line').addEventListener('click', () => {
      addRow();
    });
  
    document.getElementById('items-body').addEventListener('change', (e) => {
      if (e.target.classList.contains('item-code')) {
        updateTotal(e.target);
      }
      if (e.target.classList.contains('qty-ordered') || e.target.classList.contains('price')) {
        const itemSelect = e.target.closest('tr').querySelector('.item-code');
        updateTotal(itemSelect);
      }
    });
  }
  
  document.addEventListener('DOMContentLoaded', async () => {
    console.log('Page loaded');
    setupEventListeners();
    try {
      businessDetails = window.businessDetails;
      if (!businessDetails || !businessDetails.company_name) {
        throw new Error('No business details found');
      }
      console.log('Business details loaded:', businessDetails);
      await loadDropdowns();
      console.log('Requester dropdown options:', document.getElementById('requester_id').options.length);
      console.log('Supplier dropdown options:', document.getElementById('supplier_id').options.length);
      await loadOrderNumber();
      const dateField = document.getElementById("request_date");
      if (dateField) {
        const today = new Date().toISOString().split('T')[0];
        dateField.value = today;
      }
    } catch (err) {
      console.error('Initialization failed:', err.message);
      alert(`Error: ${err.message}`);
    }
  });

 function resetForm() {
  document.getElementById("requester_id").value = "";
  document.getElementById("payment_terms").value = "";
  document.getElementById("order_type").value = "";
  document.getElementById("note_to_supplier").value = "";
  document.getElementById("order_note").value = "";

  const supplierDropdown = document.getElementById("supplier_id");
  if (supplierDropdown && supplierDropdown.tomselect) {
    supplierDropdown.tomselect.clear(true); // ✅ Clear TomSelect without touching fuzzy_dropdown.js
  } else {
    supplierDropdown.value = "";
  }

  document.querySelector("#items-body").innerHTML = "";
}
