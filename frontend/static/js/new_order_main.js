// frontend/static/js/new_order_main.js

// Utility functions (inlined since new_order_utils.js is not provided)
let itemsList = [];
let projectsList = [];
let rowCount = 0;
let currentOrderNumber = "URC1000";

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
       const suppliersData = await fetchData("/lookups/suppliers");
       populateDropdown("supplier_id", suppliersData?.suppliers, "name");
       const itemsData = await fetchData("/lookups/items");
       itemsList = itemsData?.items || [];
       const projectsData = await fetchData("/lookups/projects");
       projectsList = projectsData?.projects || [];
   } catch (error) {
       console.error("Error loading dropdowns:", error);
       throw error;
   }
}

// Load order number
async function loadOrderNumber() {
   try {
       const settingsData = await fetchData("/lookups/settings");
       currentOrderNumber = settingsData.order_number_start || "URC1000";
       document.getElementById("order-number").textContent = currentOrderNumber;
   } catch (error) {
       console.error("Error loading order number:", error);
       document.getElementById("order-number").textContent = "URC1000"; // Fallback
   }
}

// Add a row to the table
function addRow() {
   // Check if itemsList and projectsList are populated
   if (itemsList.length === 0 || projectsList.length === 0) {
       alert('Cannot add items: Failed to load items or projects. Please refresh the page.');
       return;
   }

   const tbody = document.getElementById("items-body");
   const row = document.createElement("tr");
   row.id = `row_${rowCount++}`;

   // Item Code dropdown (show code + description)
   const itemCell = document.createElement("td");
   const itemSelect = document.createElement("select");
   itemSelect.className = "item-code";
   itemSelect.id = `item_code_${rowCount}`;
   itemSelect.innerHTML = '<option value="">Select Item</option>';
   itemsList.forEach(item => {
       const option = document.createElement("option");
       option.value = item.item_code;
       option.textContent = `${item.item_code} - ${item.item_description}`; // Display code and description
       option.dataset.description = item.item_description;
       itemSelect.appendChild(option);
   });
   itemCell.appendChild(itemSelect);
   row.appendChild(itemCell);

   // Project dropdown (show code + name)
   const projectCell = document.createElement("td");
   const projectSelect = document.createElement("select");
   projectSelect.className = "project";
   projectSelect.id = `project_${rowCount}`;
   projectSelect.innerHTML = '<option value="">Select Project</option>';
   projectsList.forEach(project => {
       const option = document.createElement("option");
       option.value = project.project_code;
       option.textContent = `${project.project_code} - ${project.project_name}`; // Display code and name
       projectSelect.appendChild(option);
   });
   projectCell.appendChild(projectSelect);
   row.appendChild(projectCell);

   // Quantity input
   const qtyCell = document.createElement("td");
   const qtyInput = document.createElement("input");
   qtyInput.type = "number";
   qtyInput.className = "qty-ordered";
   qtyInput.id = `qty_${rowCount}`;
   qtyInput.value = "1";
   qtyInput.min = "1";
   qtyCell.appendChild(qtyInput);
   row.appendChild(qtyCell);

   // Price input (placeholder; assuming no price data in itemsList)
   const priceCell = document.createElement("td");
   const priceInput = document.createElement("input");
   priceInput.type = "number";
   priceInput.className = "price";
   priceInput.id = `price_${rowCount}`;
   priceInput.value = "0.00";
   priceInput.step = "0.01";
   priceCell.appendChild(priceInput);
   row.appendChild(priceCell);

   // Total (read-only)
   const totalCell = document.createElement("td");
   const totalInput = document.createElement("input");
   totalInput.type = "text";
   totalInput.className = "total";
   totalInput.id = `total_${rowCount}`;
   totalInput.value = "0.00";
   totalInput.readOnly = true;
   totalCell.appendChild(totalInput);
   row.appendChild(totalCell);

   // Actions (delete button)
   const actionsCell = document.createElement("td");
   const deleteBtn = document.createElement("button");
   deleteBtn.textContent = "Delete";
   deleteBtn.onclick = () => deleteRow(row.id);
   actionsCell.appendChild(deleteBtn);
   row.appendChild(actionsCell);

   tbody.appendChild(row);
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

   return { container, inner };
}

// Core functionality
let businessDetails = null;

async function fetchData(endpoint) {
   try {
       const response = await fetch(`http://localhost:8004${endpoint}`, {
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
           dropdown.appendChild(option);
       });
   }
}

async function previewOrder() {
    console.log('previewOrder called');
    const orderNumber = document.getElementById('order-number').textContent;
    const supplierId = document.getElementById('supplier_id').value;
    const noteToSupplier = document.getElementById('note_to_supplier').value;
    const date = new Date().toISOString().split('T')[0]; // Add current date
    console.log('Collected data:', { orderNumber, supplierId, noteToSupplier, date });

    if (!orderNumber || !supplierId) {
        alert('Please fill in all required fields (Order Number, Supplier)');
        return;
    }

    const items = Array.from(document.querySelectorAll('#items-body tr')).map(row => {
        const itemCode = row.querySelector('.item-code')?.value;
        const itemDescription = itemsList.find(i => i.item_code === itemCode)?.item_description || '';
        const project = row.querySelector('.project')?.value;
        const qtyOrdered = parseFloat(row.querySelector('.qty-ordered')?.value) || 0;
        const price = parseFloat(row.querySelector('.price')?.value) || 0;
        if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {
            throw new Error('All items must have a valid item code, project, quantity, and price');
        }
        return { item_code: itemCode, item_description: itemDescription, project, qty_ordered: qtyOrdered, price };
    });

    console.log('Items:', items);
    if (items.length === 0) {
        alert('Please add at least one item to the order');
        return;
    }

    const total = items.reduce((sum, item) => sum + (item.qty_ordered * item.price), 0);
    if (!businessDetails || !businessDetails.company_name) {
        console.error('No business details available');
        alert('Error: No business details found');
        return;
    }

    const payload = {
        order_number: orderNumber,
        date: date,
        supplier_id: parseInt(supplierId),
        note_to_supplier: noteToSupplier,
        items,
        total,
        business_details: businessDetails
    };

    console.log('Sending payload:', payload);
    try {
        const res = await fetch('/orders/generate_pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        console.log(`Response status: ${res.status}`);
        if (!res.ok) {
            const errorText = await res.text();
            console.error('Error response:', errorText);
            throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);
        }

        const contentType = res.headers.get('content-type');
        console.log('Content-Type:', contentType);
        if (contentType && contentType.includes('application/pdf')) {
            const blob = await res.blob();
            console.log('Blob size:', blob.size);
            if (blob.size === 0) {
                throw new Error('Received empty PDF file');
            }

            const modal = document.createElement('div');
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100vw';
            modal.style.height = '100vh';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            modal.style.zIndex = '9999';

            const inner = document.createElement('div');
            inner.style.backgroundColor = 'white';
            inner.style.padding = '1rem';
            inner.style.borderRadius = '8px';
            inner.style.width = '90%';
            inner.style.maxWidth = '800px';
            inner.style.height = '80vh';
            inner.style.display = 'flex';
            inner.style.flexDirection = 'column';

            const iframe = document.createElement('iframe');
            iframe.src = URL.createObjectURL(blob);
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.border = 'none';
            inner.appendChild(iframe);

            const closeBtn = document.createElement('button');
            closeBtn.textContent = 'Close';
            closeBtn.style.marginTop = '1rem';
            closeBtn.style.padding = '0.5rem 1rem';
            closeBtn.style.cursor = 'pointer';
            closeBtn.style.alignSelf = 'center';
            closeBtn.onclick = () => document.body.removeChild(modal);
            inner.appendChild(closeBtn);

            modal.appendChild(inner);
            document.body.appendChild(modal);
            console.log('PDF displayed in modal');
        } else {
            const data = await res.json();
            throw new Error(`Unexpected response: ${JSON.stringify(data)}`);
        }
    } catch (error) {
        console.error('Error generating PDF:', error);
        alert(`Error generating PDF: ${error.message}`);
    }
}

async function submitOrder() {
   console.log('debouncedSubmitOrder triggered');
   const requesterId = document.getElementById('requester_id').value;
   const supplierId = document.getElementById('supplier_id').value;
   const noteToSupplier = document.getElementById('note_to_supplier').value;
   console.log('Submitting order with:', { requester_id: requesterId, supplier_id: supplierId, note_to_supplier: noteToSupplier });

   if (!requesterId || !supplierId) {
       alert('Please fill in all required fields (Requester, Supplier)');
       return;
   }

   const items = Array.from(document.querySelectorAll('#items-body tr')).map(row => {
       const itemCode = row.querySelector('.item-code')?.value;
       const itemDescription = itemsList.find(i => i.item_code === itemCode)?.item_description || '';
       const project = row.querySelector('.project')?.value;
       const qtyOrdered = parseFloat(row.querySelector('.qty-ordered')?.value) || 0;
       const price = parseFloat(row.querySelector('.price')?.value) || 0;
       if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {
           throw new Error('All items must have a valid item code, project, quantity, and price');
       }
       return { item_code: itemCode, item_description: itemDescription, project, qty_ordered: qtyOrdered, price };
   });

   console.log('Items:', items);
   if (items.length === 0) {
       alert('Please add at least one item to the order');
       return;
   }

   console.log('Current Order Number:', currentOrderNumber);
   const orderData = {
       order_number: currentOrderNumber,
       status: "Pending",
       total: parseFloat(document.getElementById("grand-total").textContent) || 0,
       order_note: "",
       note_to_supplier: noteToSupplier,
       requester_id: parseInt(requesterId),
       supplier_id: parseInt(supplierId),
       items
   };

   console.log('Order Data:', orderData);
   try {
       const res = await fetch('/orders/', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify(orderData)
       });
       console.log(`Submit Response Status: ${res.status}`);
       if (!res.ok) {
           const errorText = await res.text();
           throw new Error(`Failed to submit order: ${res.status} - ${errorText}`);
       }

       const data = await res.json();
       console.log('Submit Response:', data);
       if (data.message === "Order created successfully") {
           alert('✅ Order submitted successfully!');
           // Reset the form to allow continued use
           document.getElementById('requester_id').value = '';
           document.getElementById('supplier_id').value = '';
           document.getElementById('note_to_supplier').value = '';
           document.getElementById('items-body').innerHTML = '';
           rowCount = 0;
           await loadOrderNumber(); // Reload order number for the next order
       } else {
           throw new Error(`Unexpected response: ${data.message}`);
       }
   } catch (error) {
       console.error('Order submission failed:', error.message);
       alert(`❌ Order submission failed: ${error.message}`);
   }
}

function setupEventListeners() {
   const submitBtn = document.getElementById('submit-order');
   if (submitBtn) {
       console.log('Submit button exists:', !!submitBtn);
       submitBtn.addEventListener('click', () => {
           console.log('Submit button clicked');
           debounce(submitOrder, 500)();
       });
   } else {
       console.error('Submit button not found');
   }

   document.getElementById('preview-order').addEventListener('click', previewOrder);
   document.getElementById('email-po').addEventListener('click', () => {
       alert('Email functionality not implemented yet');
   });
   document.getElementById('cancel-order').addEventListener('click', () => {
       if (confirm('Are you sure you want to cancel?')) {
           window.location.href = '/orders/pending_orders';
       }
   });

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
       // Fetch business details for PDF generation
       const res = await fetch('/lookups/business_details');
       if (!res.ok) {
           throw new Error(`Failed to fetch business details: ${res.status}`);
       }
       businessDetails = await res.json();
       if (!businessDetails || !businessDetails.company_name) {
           throw new Error('No business details found');
       }
       console.log('Business details loaded:', businessDetails);
       await loadDropdowns();
       console.log('Requester dropdown options:', document.getElementById('requester_id').options.length);
       console.log('Supplier dropdown options:', document.getElementById('supplier_id').options.length);
       await loadOrderNumber();
   } catch (err) {
       console.error('Initialization failed:', err.message);
       alert(`Error: ${err.message}`);
   }
});