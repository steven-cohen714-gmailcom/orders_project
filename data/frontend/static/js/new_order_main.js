/* File: /Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/js/new_order_main.js */

import { previewOrder } from "./new_order_screen/pdf_utils.js";
import { submitOrder } from "./new_order_screen/submit_utils.js";
import { saveDraftOrder } from "./new_order_screen/submit_draft_order_utils.js";
import { logToServer } from "./components/utils.js";
import { createFuzzyDropdown } from "./components/fuzzy_dropdown.js";

let itemsList = [];
let projectsList = [];
let rowCount = 0;
let currentOrderNumber = "URC1000"; // Holds the currently displayed order number
let authThresholds = [0, 0, 0, 0, 0];
let currentOrderId = null; // Stores the ID of the final order if submitted
let currentDraftOrderId = null; // Stores the ID of the draft order if editing/creating a draft

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
    
    await createFuzzyDropdown("supplier_id", "/lookups/suppliers");

    const itemsData = await fetchData("/lookups/items");
    itemsList = itemsData?.items || [];
    await createFuzzyDropdown("item-template", "/lookups/items");

    const projectsData = await fetchData("/lookups/projects");
    projectsList = projectsData?.projects || [];
    await createFuzzyDropdown("project-template", "/lookups/projects");
  } catch (error) {
    console.error("Error loading dropdowns:", error);
    throw error;
  }
}

// Load current order number and authorization thresholds from settings
async function loadOrderNumber() {
  try {
    const settingsData = await fetchData("/lookups/settings");
    currentOrderNumber = settingsData.order_number_start || "URC1000";
    authThresholds = [
      parseFloat(settingsData.auth_threshold_1 || 0),
      parseFloat(settingsData.auth_threshold_2 || 0),
      parseFloat(settingsData.auth_threshold_3 || 0),
      parseFloat(settingsData.auth_threshold_4 || 0),
      parseFloat(settingsData.auth_threshold_5 || 0)
    ];
    console.log("Loaded thresholds:", authThresholds);
    document.getElementById("order-number").textContent = currentOrderNumber;
  } catch (error) {
    console.error("Error loading order number or thresholds:", error);
    document.getElementById("order-number").textContent = "URC1000";
  }
}

// Function to increment order number in backend settings
async function incrementOrderNumber(orderNumberToIncrement) {
  const current = orderNumberToIncrement.match(/\d+$/);
  const prefix = orderNumberToIncrement.replace(/\d+$/, "");
  const nextNum = current ? String(parseInt(current[0]) + 1).padStart(4, "0") : "1000";
  const newOrderNumber = `${prefix}${nextNum}`;

  try {
    const res = await fetch('/lookups/order_number', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_number_start: newOrderNumber })
    });
    if (!res.ok) {
      const errorText = await res.text();
      console.error("Failed to update order number in backend settings:", errorText);
      await logToServer('ERROR', 'Failed to update order number on backend settings', { oldNum: orderNumberToIncrement, newNum: newOrderNumber, error: errorText });
      throw new Error(`Failed to update order number: ${errorText}`);
    } else {
      await logToServer('INFO', 'Order number incremented in backend settings', { oldNum: orderNumberToIncrement, newNum: newOrderNumber });
    }
    return newOrderNumber;
  } catch (err) {
    console.error("Exception during order number update in backend settings:", err.message);
    await logToServer('ERROR', 'Exception during order number update in backend settings', { oldNum: orderNumberToIncrement, error: err.message });
    throw err;
  }
}

// Add a row to the table
function addRow(itemData = {}, projectData = {}) {
  const tbody = document.getElementById("items-body");
  const row = document.createElement("tr");
  const currentRowCount = rowCount++;
  row.id = `row_${currentRowCount}`;

  const itemCell = document.createElement("td");
  const itemSelect = document.createElement("select");
  itemSelect.className = "item-code wide-select";
  itemSelect.id = `item_code_${currentRowCount}`;
  itemSelect.innerHTML = '<option value="">Select Item</option>';
  itemCell.appendChild(itemSelect);
  row.appendChild(itemCell);

  const projectCell = document.createElement("td");
  const projectSelect = document.createElement("select");
  projectSelect.className = "project wide-select";
  projectSelect.id = `project_${currentRowCount}`;
  projectSelect.innerHTML = '<option value="">Select Project</option>';
  projectCell.appendChild(projectSelect);
  row.appendChild(projectCell);

  const qtyCell = document.createElement("td");
  const qtyInput = document.createElement("input");
  qtyInput.type = "number";
  qtyInput.className = "qty-ordered narrow-input";
  qtyInput.id = `qty_${currentRowCount}`;
  qtyInput.value = itemData.qty_ordered || "1";
  qtyInput.min = "0";
  qtyInput.step = "1";
  qtyCell.appendChild(qtyInput);
  row.appendChild(qtyCell);

  const priceCell = document.createElement("td");
  const priceInput = document.createElement("input");
  priceInput.type = "number";
  priceInput.className = "price narrow-input";
  priceInput.id = `price_${currentRowCount}`;
  priceInput.value = itemData.price != null ? itemData.price.toFixed(2) : "0.00";
  priceInput.step = "0.01";
  priceCell.appendChild(priceInput);
  row.appendChild(priceCell);

  const totalCell = document.createElement("td");
  const totalInput = document.createElement("input");
  totalInput.type = "text";
  totalInput.className = "total medium-input";
  totalInput.id = `total_${currentRowCount}`;
  totalInput.value = ((itemData.qty_ordered || 0) * (itemData.price || 0)).toFixed(2);
  totalInput.readOnly = true;
  totalCell.appendChild(totalInput);
  row.appendChild(totalCell);

  const actionsCell = document.createElement("td");
  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "Delete";
  deleteBtn.onclick = () => deleteRow(row.id);
  actionsCell.appendChild(deleteBtn);
  row.appendChild(actionsCell);

  tbody.appendChild(row);

  const itemTomSelectPromise = createFuzzyDropdown(itemSelect.id, "/lookups/items");
  const projectTomSelectPromise = createFuzzyDropdown(projectSelect.id, "/lookups/projects");

  if (itemData.item_code) {
    itemTomSelectPromise.then(ts => {
      if (ts) ts.setValue(itemData.item_code);
      updateTotal(itemSelect);
    }).catch(err => console.error("Error setting item code for new row:", err));
  }
  if (projectData.project_code) {
    projectTomSelectPromise.then(ts => {
      if (ts) ts.setValue(projectData.project_code);
    }).catch(err => console.error("Error setting project code for new row:", err));
  }
}

// Update row total
function updateTotal(elementInRow) {
  const row = elementInRow.closest("tr");
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
  return grandTotal;
}

// Delete a row
function deleteRow(rowId) {
  const row = document.getElementById(rowId);
  if (row) {
    row.remove();
    updateGrandTotal();
  }
}

// Modal functions
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
      option.dataset.description = item[key]?.toLowerCase() || "";
      dropdown.appendChild(option);
    });
  }
}

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

// Busy processing indicator
function setProcessingState(isProcessing) {
  const submitBtn = document.getElementById('submit-final-order');
  const saveBtn = document.getElementById('save-draft-order');
  const previewBtn = document.getElementById('preview-order');
  const spinner = '<span style="display:inline-block;width:16px;height:16px;border:2px solid #fff;border-radius:50%;border-top-color:#007bff;animation:spin 1s linear infinite;margin-right:5px;"></span>';
  if (submitBtn) {
    submitBtn.disabled = isProcessing;
    submitBtn.innerHTML = isProcessing ? `${spinner}Submitting...` : 'Submit as Final Order';
    submitBtn.style.opacity = isProcessing ? '0.6' : '1';
  }
  if (saveBtn) {
    saveBtn.disabled = isProcessing;
    saveBtn.innerHTML = isProcessing ? `${spinner}Saving...` : 'Save as Draft Order';
    saveBtn.style.opacity = isProcessing ? '0.6' : '1';
  }
  if (previewBtn) {
    previewBtn.disabled = isProcessing;
    previewBtn.innerHTML = isProcessing ? `${spinner}Previewing...` : 'View Purchase Order';
    previewBtn.style.opacity = isProcessing ? '0.6' : '1';
  }
}

// Animation for spinner
const style = document.createElement('style');
style.innerHTML = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);

function setupEventListeners() {
  const submitFinalOrderBtn = document.getElementById('submit-final-order');
  if (submitFinalOrderBtn) {
    submitFinalOrderBtn.addEventListener('click', async () => {
      setProcessingState(true);
      const paymentTerms = document.getElementById("payment_terms")?.value || "On account";
      const draftId = document.getElementById("draft-order-id")?.value;
      debounce(async () => {
        const success = await submitOrder({
          currentOrderNumber: document.getElementById("order-number").textContent,
          authThresholds: authThresholds,
          itemsList,
          updateGrandTotal,
          logToServer,
          setCurrentOrderId: (id) => currentOrderId = id,
          paymentTerms,
          draftId: draftId
        });
        if (success && !draftId) {
          const newOrderNumber = await incrementOrderNumber(currentOrderNumber);
          currentOrderNumber = newOrderNumber;
          document.getElementById("order-number").textContent = newOrderNumber;
        }
        if (success) {
          resetForm();
        }
        setProcessingState(false);
      }, 500)();
    });
  } else {
    console.error('Submit Final Order button not found');
  }

  const saveDraftOrderBtn = document.getElementById('save-draft-order');
  if (saveDraftOrderBtn) {
    saveDraftOrderBtn.addEventListener('click', () => {
      setProcessingState(true);
      debounce(async () => {
        const success = await saveDraftOrder({
          currentOrderNumber: document.getElementById("order-number").textContent,
          itemsList,
          updateGrandTotal,
          incrementOrderNumber,
          logToServer,
          setCurrentOrderId: (id) => currentDraftOrderId = id,
          setCurrentOrderNumber: (newNum) => {
            currentOrderNumber = newNum;
            document.getElementById("order-number").textContent = newNum;
          }
        });
        if (success) {
          const draftOrderId = document.getElementById("draft-order-id")?.value;
          if (!draftOrderId) {
            resetForm();
          }
        }
        setProcessingState(false);
      }, 500)();
    });
  } else {
    console.error('Save Draft Order button not found');
  }

  const previewBtn = document.getElementById('preview-order');
  if (previewBtn) {
    previewBtn.addEventListener('click', () => {
      setProcessingState(true);
      previewOrder({
        itemsList,
        updateGrandTotal,
        logToServer
      }).finally(() => {
        setProcessingState(false);
      });
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

  document.getElementById('items-body').addEventListener('input', (e) => {
    if (e.target.classList.contains('qty-ordered') || e.target.classList.contains('price')) {
      updateTotal(e.target);
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
    
    const urlParams = new URLSearchParams(window.location.search);
    currentDraftOrderId = urlParams.get('draft_id');

    if (currentDraftOrderId) {
      console.log(`Loading draft order ID: ${currentDraftOrderId}`);
      try {
        const draftData = await fetchData(`/draft_orders/${currentDraftOrderId}`);
        if (draftData) {
          document.getElementById("requester_id").value = draftData.requester_id || "";
          const supplierDropdown = document.getElementById("supplier_id");
          if (supplierDropdown && supplierDropdown.tomselect) {
            supplierDropdown.tomselect.setValue(draftData.supplier_id);
          } else {
            supplierDropdown.value = draftData.supplier_id || "";
          }
          document.getElementById("payment_terms").value = draftData.payment_terms || "On account";
          document.getElementById("note_to_supplier").value = draftData.note_to_supplier || "";
          document.getElementById("order_note").value = draftData.order_note || "";
          currentOrderNumber = draftData.order_number;
          document.getElementById("order-number").textContent = currentOrderNumber;
          document.getElementById("order-number").style.pointerEvents = 'none';
          document.getElementById("order-number").style.opacity = '0.7';
          document.getElementById("request_date").value = draftData.created_date ? draftData.created_date.split('T')[0] : new Date().toISOString().split('T')[0];
          document.querySelector("#items-body").innerHTML = "";
          if (draftData.items && draftData.items.length > 0) {
            draftData.items.forEach(item => {
              addRow({
                item_code: item.item_code,
                qty_ordered: item.qty_ordered,
                price: item.price,
                item_description: item.item_description,
              }, {
                project_code: item.project
              });
            });
          } else {
            addRow();
          }
          updateGrandTotal();
          document.getElementById("draft-order-id").value = currentDraftOrderId;
          alert(`Draft Order ${currentOrderNumber} loaded for editing.`);
        } else {
          alert("Could not load draft order. Starting a new order.");
          await loadOrderNumber();
          addRow();
        }
      } catch (err) {
        console.error('Error loading draft order:', err.message);
        alert(`Error loading draft order: ${err.message}. Starting a new order.`);
        await loadOrderNumber();
        addRow();
      }
    } else {
      await loadOrderNumber();
      addRow();
    }

    const dateField = document.getElementById("request_date");
    if (dateField && !dateField.value) {
      const today = new Date().toISOString().split('T')[0];
      dateField.value = today;
    }
  } catch (err) {
    console.error('Initialization failed:', err.message);
    alert(`Error: ${err.message}`);
  }
});

async function resetForm() {
  document.getElementById("requester_id").value = "";
  document.getElementById("payment_terms").value = "";
  document.getElementById("note_to_supplier").value = "";
  document.getElementById("order_note").value = "";
  const supplierDropdown = document.getElementById("supplier_id");
  if (supplierDropdown && supplierDropdown.tomselect) {
    supplierDropdown.tomselect.clear(true);
  } else {
    supplierDropdown.value = "";
  }
  document.querySelector("#items-body").innerHTML = "";
  addRow();
  updateGrandTotal();
  currentDraftOrderId = null;
  document.getElementById("draft-order-id").value = "";
  document.getElementById("order-number").style.pointerEvents = 'auto';
  document.getElementById("order-number").style.opacity = '1';
  await loadOrderNumber(); // Fetch next order number to update UI
}