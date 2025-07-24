// File: frontend/static/js/admin/edit_order_main.js

import { createFuzzyDropdown } from "../components/fuzzy_dropdown.js";
import { logToServer } from "../components/utils.js";

let rowCount = 0; // Global counter for new rows
let itemsList = []; // To store all available items for description lookup
let projectsList = []; // To store all available projects

// Debounce function to limit how often a function is called
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

// Function to format currency with thousand separators and 2 decimal places
function formatCurrency(amount) {
    if (amount == null) return "R0.00";
    return `R${parseFloat(amount).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Fetch data from a given endpoint
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

// Add a new row to the items table
function addRow(itemData = {}) {
    const tbody = document.getElementById("items-body");
    const row = document.createElement("tr");
    const currentRowCount = rowCount++; // Increment global counter for unique row IDs
    row.id = `row_${currentRowCount}`;

    // Get templates for dropdowns from hidden select elements
    const itemTemplateOptions = document.getElementById("item-template").innerHTML;
    const projectTemplateOptions = document.getElementById("project-template").innerHTML;

    row.innerHTML = `
        <td>
            <select class="item-code wide-select" id="item_code_${currentRowCount}">
                ${itemTemplateOptions}
            </select>
        </td>
        <td>
            <select class="project wide-select" id="project_${currentRowCount}">
                ${projectTemplateOptions}
            </select>
        </td>
        <td><input type="number" class="qty-ordered narrow-input" value="${itemData.qty_ordered || '1'}" min="0" step="1"></td>
        <td><input type="number" class="price narrow-input" value="${itemData.price != null ? itemData.price.toFixed(2) : '0.00'}" step="0.01"></td>
        <td><input type="text" class="total medium-input" value="${itemData.total != null ? itemData.total.toFixed(2) : '0.00'}" readonly></td>
        <td><button type="button" onclick="deleteRow('row_${currentRowCount}')">Delete</button></td>
    `;
    tbody.appendChild(row);

    // Initialize TomSelect for the new row's dropdowns
    const itemSelect = document.getElementById(`item_code_${currentRowCount}`);
    const projectSelect = document.getElementById(`project_${currentRowCount}`);

    // Store TomSelect instances to allow setting values
    let itemTomSelect;
    let projectTomSelect;

    createFuzzyDropdown(itemSelect.id, "/lookups/items").then(ts => {
        itemTomSelect = ts;
        if (itemData.item_code) {
            itemTomSelect.setValue(itemData.item_code);
        }
        updateTotal(itemSelect); // Update total after item is set
    }).catch(err => console.error("Error initializing item dropdown:", err));

    createFuzzyDropdown(projectSelect.id, "/lookups/projects").then(ts => {
        projectTomSelect = ts;
        if (itemData.project) {
            projectTomSelect.setValue(itemData.project);
        }
    }).catch(err => console.error("Error initializing project dropdown:", err));

    updateGrandTotal(); // Update grand total after adding a new row
}

// Delete a row from the table
window.deleteRow = function(rowId) {
    const row = document.getElementById(rowId);
    if (row) {
        row.remove();
        updateGrandTotal();
    }
};

// Update the total for a single line item
function updateTotal(elementInRow) {
    const row = elementInRow.closest("tr");
    const qtyInput = row.querySelector(".qty-ordered");
    const priceInput = row.querySelector(".price");
    const totalInput = row.querySelector(".total");

    const qty = parseFloat(qtyInput.value) || 0;
    const price = parseFloat(priceInput.value) || 0;
    const total = qty * price;
    totalInput.value = total.toFixed(2);
    updateGrandTotal();
}

// Update the grand total of all line items
function updateGrandTotal() {
    const totals = Array.from(document.querySelectorAll("#items-body .total")).map(input => parseFloat(input.value) || 0);
    const grandTotal = totals.reduce((sum, val) => sum + val, 0);
    document.getElementById("grand-total").textContent = grandTotal.toFixed(2);
    return grandTotal;
}

// Handle form submission
document.getElementById("save-changes").addEventListener("click", debounce(async () => {
    const orderId = document.getElementById("order-id").value;
    const requesterId = document.getElementById("requester_id").value;
    const supplierId = document.getElementById("supplier_id").value;
    const paymentTerms = document.getElementById("payment_terms").value;
    const orderNote = document.getElementById("order_note").value;
    const noteToSupplier = document.getElementById("note_to_supplier").value;

    if (!requesterId || !supplierId || !paymentTerms) {
        alert("Please fill in Requester, Supplier, and Payment Terms.");
        return;
    }

    const items = [];
    try {
        Array.from(document.querySelectorAll("#items-body tr")).forEach(row => {
            const itemCode = row.querySelector(".item-code")?.value;
            const project = row.querySelector(".project")?.value;
            const qtyOrdered = parseFloat(row.querySelector(".qty-ordered")?.value) || 0;
            const price = parseFloat(row.querySelector(".price")?.value) || 0;

            if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {
                throw new Error("Each item needs item code, project, quantity > 0 and price > 0.");
            }

            // Find item description from the pre-loaded itemsList
            const itemDetails = itemsList.find(i => i.item_code === itemCode);
            const itemDescription = itemDetails ? itemDetails.item_description : "";

            items.push({
                item_code: itemCode,
                item_description: itemDescription,
                project: project,
                qty_ordered: qtyOrdered,
                price: price
            });
        });
    } catch (e) {
        alert(`❌ Item validation failed: ${e.message}`);
        return;
    }

    if (items.length === 0) {
        alert("Please add at least one item to the order.");
        return;
    }

    const payload = {
        supplier_id: parseInt(supplierId),
        requester_id: parseInt(requesterId),
        payment_terms: paymentTerms,
        order_note: orderNote,
        note_to_supplier: noteToSupplier,
        items: items
    };

    try {
        const response = await fetch(`/admin/edit_order/${orderId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to save changes.");
        }

        alert("✅ Order updated successfully!");
        logToServer("INFO", `Order ${orderId} updated successfully via admin edit.`, { orderId, payload });
        window.location.href = `/orders/audit_trail`; // Redirect to audit trail or pending orders
    } catch (error) {
        console.error("Error saving changes:", error);
        alert(`❌ Error saving changes: ${error.message}`);
        logToServer("ERROR", `Failed to update order ${orderId} via admin edit.`, { orderId, payload, error: error.message });
    }
}, 500)); // Debounce to prevent multiple rapid submissions

// Event listeners for quantity and price input changes (using 'input' event for live update)
document.getElementById('items-body').addEventListener('input', (e) => {
    if (e.target.classList.contains('qty-ordered') || e.target.classList.contains('price')) {
        updateTotal(e.target);
    }
});

// Event listener for item code and project changes to trigger total update (for consistency)
document.getElementById('items-body').addEventListener('change', (e) => {
    if (e.target.classList.contains('item-code') || e.target.classList.contains('project')) {
        updateTotal(e.target); // Recalculate total for the row
    }
});

// Add line item button
document.getElementById("add-line").addEventListener("click", () => addRow());

// Initialize the page
document.addEventListener("DOMContentLoaded", async () => {
    try {
        // Load initial lookup data
        const itemsData = await fetchData("/lookups/items");
        itemsList = itemsData?.items || [];
        const projectsData = await fetchData("/lookups/projects");
        projectsList = projectsData?.projects || [];

        // Initialize TomSelect for existing rows
        const existingRows = document.querySelectorAll("#items-body tr");
        existingRows.forEach(row => {
            const rowIndex = row.id.split('_')[1];
            const itemSelect = row.querySelector(".item-code");
            const projectSelect = row.querySelector(".project");

            // Populate options for existing rows from the pre-fetched data
            const itemTemplateOptions = document.getElementById("item-template").innerHTML;
            const projectTemplateOptions = document.getElementById("project-template").innerHTML;
            itemSelect.innerHTML = itemTemplateOptions;
            projectSelect.innerHTML = projectTemplateOptions;

            // Initialize TomSelect and set values
            createFuzzyDropdown(itemSelect.id, "/lookups/items").then(ts => {
                if (itemSelect.dataset.currentValue) {
                    ts.setValue(itemSelect.dataset.currentValue);
                }
            }).catch(err => console.error("Error initializing existing item dropdown:", err));

            createFuzzyDropdown(projectSelect.id, "/lookups/projects").then(ts => {
                if (projectSelect.dataset.currentValue) {
                    ts.setValue(projectSelect.dataset.currentValue);
                }
            }).catch(err => console.error("Error initializing existing project dropdown:", err));

            // Ensure rowCount is correctly set based on existing rows
            rowCount = Math.max(rowCount, parseInt(rowIndex) + 1);
        });

        // Initialize TomSelect for main supplier dropdown
        // MODIFIED: Read currentSupplierId from the new hidden input
        const currentSupplierId = document.getElementById("current-supplier-id").value; 
        createFuzzyDropdown("supplier_id", "/lookups/suppliers").then(ts => {
            if (currentSupplierId) {
                ts.setValue(currentSupplierId);
            }
        }).catch(err => console.error("Error initializing supplier dropdown:", err));

        // Requester dropdown is a standard select, no fuzzy search needed unless specified.
        // It's already populated by Jinja.

        updateGrandTotal(); // Initial calculation of grand total
    } catch (error) {
        console.error("Page initialization failed:", error);
        alert(`Failed to load page: ${error.message}`);
    }
});
