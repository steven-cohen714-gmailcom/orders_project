export function later(func, wait) {
    return setTimeout(func, wait);
}

export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const delayed = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(delayed, wait);
    };
}

export function updateGrandTotal() {
    let sum = 0;
    document.querySelectorAll("#items-table tbody tr").forEach(row => {
        const totalField = row.querySelector("td:nth-child(5) input");
        if (totalField) {
            sum += parseFloat(totalField.value) || 0;
        }
    });
    document.getElementById("grand-total").textContent = `R${sum.toFixed(2)}`;
}

export function updateTotal(input) {
    const row = input.closest("tr");
    const qty = parseFloat(row.cells[2].querySelector("input").value) || 0;
    const price = parseFloat(row.cells[3].querySelector("input").value) || 0;
    row.cells[4].querySelector("input").value = (qty * price).toFixed(2);
    updateGrandTotal();
}

export function deleteRow(btn) {
    if (rowCount > 1) {
        btn.closest("tr").remove();
        rowCount--;
        updateGrandTotal();
    }
}

export let itemsList = [];
export let projectsList = [];
export let rowCount = 0;
export let currentOrderNumber = null;

export function addRow() {
    const tbody = document.getElementById("items-body");
    const row = tbody.insertRow();

    const itemOpts = itemsList.map(i =>
        `<option value="${i.item_code}" data-description="${i.item_description}">${i.item_code} — ${i.item_description}</option>`
    ).join("");

    const projOpts = projectsList.map(p =>
        `<option value="${p.project_code}">${p.project_code} — ${p.project_name}</option>`
    ).join("");

    row.innerHTML = `
        <td>
            <select name="items[${rowCount}][item_code]" id="item_code_${rowCount}">
                <option value="">Select Item</option>
                ${itemOpts}
            </select>
        </td>
        <td>
            <select name="items[${rowCount}][project]" id="project_${rowCount}">
                <option value="">Select Project</option>
                ${projOpts}
            </select>
        </td>
        <td><input type="number" name="items[${rowCount}][qty_ordered]" id="qty_ordered_${rowCount}" step="1" min="1" value="1"></td>
        <td><input type="number" name="items[${rowCount}][price]" id="price_${rowCount}" step="0.01" min="0" value="1"></td>
        <td><input type="text" name="items[${rowCount}][total]" id="total_${rowCount}" readonly value="1.00"></td>
        <td><button type="button" id="remove_${rowCount}">Remove</button></td>
    `;

    // Auto-select the first project if available
    const projectSelect = row.querySelector(`#project_${rowCount}`);
    if (projectSelect.options.length > 1) {
        projectSelect.value = projectSelect.options[1].value;
    }

    // Attach event listeners after the row is added to the DOM
    const qtyInput = row.querySelector(`#qty_ordered_${rowCount}`);
    const priceInput = row.querySelector(`#price_${rowCount}`);
    const removeBtn = row.querySelector(`#remove_${rowCount}`);
    qtyInput.addEventListener("change", () => updateTotal(qtyInput));
    priceInput.addEventListener("change", () => updateTotal(priceInput));
    removeBtn.addEventListener("click", () => deleteRow(removeBtn));

    rowCount++;
    updateGrandTotal();
}

export async function loadOrderNumber() {
    try {
        const settingsRes = await fetch("/lookups/settings");
        const settings = await settingsRes.json();
        const orderNumber = settings.order_number_start || "URC1000";
        document.getElementById("order-number").textContent = orderNumber;
        return orderNumber;
    } catch (error) {
        console.error("Error fetching order number:", error);
        document.getElementById("order-number").textContent = "Error";
        return "Error";
    }
}

export async function loadDropdowns() {
    try {
        const fetchWithErrorHandling = async (url, name) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error(`Error response body for ${name}:`, errorText);
                    throw new Error(`Failed to fetch ${name}: HTTP ${response.status} - ${response.statusText}`);
                }
                const data = await response.json();
                if (!data[name.toLowerCase()]) {
                    throw new Error(`Response for ${name} is missing expected data`);
                }
                return data;
            } catch (err) {
                console.error(`Error fetching ${name}:`, err.message);
                throw new Error(`Failed to load ${name}: ${err.message}`);
            }
        };

        const [supR, reqR, itmR, prjR] = await Promise.all([
            fetchWithErrorHandling("/lookups/suppliers", "suppliers"),
            fetchWithErrorHandling("/lookups/requesters", "requesters"),
            fetchWithErrorHandling("/lookups/items", "items"),
            fetchWithErrorHandling("/lookups/projects", "projects")
        ]);

        const supplierDropdown = document.getElementById("supplier_id");
        supplierDropdown.innerHTML = '<option value="">Select Supplier</option>';
        supR.suppliers.forEach(s => {
            const opt = document.createElement("option");
            opt.value = s.id;
            opt.textContent = s.name;
            supplierDropdown.appendChild(opt);
        });

        const requesterDropdown = document.getElementById("requester_id");
        requesterDropdown.innerHTML = '<option value="">Select Requester</option>';
        reqR.requesters.forEach(r => {
            const opt = document.createElement("option");
            opt.value = r.id;
            opt.textContent = r.name;
            requesterDropdown.appendChild(opt);
        });

        itemsList = itmR.items || [];
        projectsList = prjR.projects || [];

        // Load the order number
        currentOrderNumber = await loadOrderNumber();

        // Add initial row
        addRow();
    } catch (err) {
        console.error("Lookup loading failed:", err.message);
        alert(`⚠️ Failed to load dropdowns: ${err.message}. Check server or database.`);
        throw err;
    }
}