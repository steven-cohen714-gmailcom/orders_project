let itemsList = [];
let projectsList = [];
let rowCount = 0;
let latestOrderId = null;
let latestOrderDetails = null;

function updateGrandTotal() {
    let sum = 0;
    document.querySelectorAll("#items-table tbody tr").forEach(row => {
        const totalField = row.querySelector("td:nth-child(6) input");
        if (totalField) {
            sum += parseFloat(totalField.value) || 0;
        }
    });
    document.getElementById("grand-total").textContent = `R${sum.toFixed(2)}`;
}

function updateTotal(input) {
    const row = input.closest("tr");
    const index = Array.from(row.parentNode.children).indexOf(row);
    const qty = parseFloat(row.cells[3].querySelector("input").value) || 0;
    const price = parseFloat(row.cells[4].querySelector("input").value) || 0;
    row.cells[5].querySelector("input").value = (qty * price).toFixed(2);
    updateGrandTotal();
}

function autoFillDescription(sel) {
    const desc = sel.selectedOptions[0]?.dataset.description ?? "";
    sel.closest("tr").querySelector("td:nth-child(2) input").value = desc;
}

function deleteRow(btn) {
    if (rowCount > 1) {
        btn.closest("tr").remove();
        rowCount--;
        updateGrandTotal();
    }
}

function addRow() {
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
            <select name="items[${rowCount}][item_code]" id="item_code_${rowCount}" onchange="autoFillDescription(this)">
                <option value="">Select Item</option>
                ${itemOpts}
            </select>
        </td>
        <td><input type="text" name="items[${rowCount}][item_description]" id="item_description_${rowCount}" readonly></td>
        <td>
            <select name="items[${rowCount}][project]" id="project_${rowCount}">
                <option value="">Select Project</option>
                ${projOpts}
            </select>
        </td>
        <td><input type="number" name="items[${rowCount}][qty_ordered]" id="qty_ordered_${rowCount}" step="1" min="1" value="1" onchange="updateTotal(this)"></td>
        <td><input type="number" name="items[${rowCount}][price]" id="price_${rowCount}" step="0.01" min="0" value="0" onchange="updateTotal(this)"></td>
        <td><input type="text" name="items[${rowCount}][total]" id="total_${rowCount}" readonly></td>
        <td><button type="button" onclick="deleteRow(this)">Remove</button></td>
    `;
    rowCount++;
    updateGrandTotal();
}

async function loadOrderNumber() {
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

async function loadDropdowns() {
    try {
        const [supR, reqR, itmR, prjR] = await Promise.all([
            fetch("/lookups/suppliers").then(r => r.json()),
            fetch("/lookups/requesters").then(r => r.json()),
            fetch("/lookups/items").then(r => r.json()),
            fetch("/lookups/projects").then(r => r.json())
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

        // Set the request date
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        document.getElementById("request_date").value = `${yyyy}-${mm}-${dd}`;

        // Load the order number
        await loadOrderNumber();

        // Add initial row
        addRow();
    } catch (err) {
        console.error("Lookup loading failed", err);
        alert("⚠️ Failed to load dropdowns. Check server or database.");
    }
}

function resetForm() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    document.getElementById("request_date").value = `${yyyy}-${mm}-${dd}`;
    document.getElementById("requester_id").value = "";
    document.getElementById("supplier_id").value = "";
    document.getElementById("note_to_supplier").value = "";
    const tbody = document.querySelector("#items-table tbody");
    tbody.innerHTML = "";
    rowCount = 0;
    addRow();
    updateGrandTotal();
}

function previewOrder() {
    const rd = document.getElementById("request_date").value;
    const rq = document.getElementById("requester_id").value;
    const sp = document.getElementById("supplier_id").value;
    const nt = document.getElementById("note_to_supplier").value;

    const items = Array.from(document.querySelectorAll("#items-body tr"))
        .map(row => {
            const c = row.querySelectorAll("td");
            return {
                item_code: c[0].querySelector("select").value,
                item_description: c[1].querySelector("input").value,
                project: c[2].querySelector("select").value,
                qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
                price: parseFloat(c[4].querySelector("input").value) || 0
            };
        })
        .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

    alert("Preview:\n" + JSON.stringify({ request_date: rd, requester_id: rq, supplier_id: sp, note_to_supplier: nt, items }, null, 2));
}

async function viewPurchaseOrder() {
    if (!latestOrderId || !latestOrderDetails) {
        alert("Please submit an order first to view the purchase order.");
        return;
    }
    try {
        const res = await fetch(`/orders/generate_pdf`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(latestOrderDetails)
        });

        if (!res.ok) {
            throw new Error("Failed to generate PDF");
        }

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `order_${latestOrderDetails.order_number}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error("Error generating PDF:", error);
        alert("Failed to generate PDF: " + error.message);
    }
}

function emailPurchaseOrder() {
    alert("Email Purchase Order functionality will be implemented after fixing PDF generation.");
}

function cancelForm() {
    window.location.href = "/orders/pending_orders";
}

async function submitOrder() {
    const rd = document.getElementById("request_date").value;
    const rqId = document.getElementById("requester_id").value;
    const spId = document.getElementById("supplier_id").value;
    const nt = document.getElementById("note_to_supplier").value;
    const rows = document.querySelectorAll("#items-body tr");

    const items = Array.from(rows)
        .map(row => {
            const c = row.querySelectorAll("td");
            return {
                item_code: c[0].querySelector("select").value,
                item_description: c[1].querySelector("input").value,
                project: c[2].querySelector("select").value,
                qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
                price: parseFloat(c[4].querySelector("input").value) || 0
            };
        })
        .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

    if (!rd || !rqId || !spId || items.length === 0) {
        return alert("⚠️ Fill date, requester, supplier & at least one complete line.");
    }

    try {
        // Fetch the current order_number_start from settings
        const settingsRes = await fetch("/lookups/settings");
        const settings = await settingsRes.json();
        const currentOrderNumber = settings.order_number_start || "URC1000";

        const res = await fetch("/orders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                order_number: currentOrderNumber,
                request_date: rd,
                requester_id: parseInt(rqId),
                supplier_id: parseInt(spId),
                note_to_supplier: nt,
                items
            })
        });

        const data = await res.json();

        if (res.ok && data.message === "Order created successfully") {
            // Store order details for PDF generation
            latestOrderDetails = {
                order_number: currentOrderNumber,
                date: rd,
                supplier_id: parseInt(spId),
                note_to_supplier: nt,
                items: items,
                total: items.reduce((sum, item) => sum + (item.qty_ordered * item.price), 0),
                business_details: await (await fetch("/lookups/business_details")).json()
            };
            latestOrderId = data.order.id;

            alert(`✅ Order ${currentOrderNumber} created.`);

            // Increment the order number by 1
            const prefix = currentOrderNumber.match(/^URC/) ? "URC" : "";
            const numberPart = parseInt(currentOrderNumber.replace(prefix, ""), 10);
            const nextOrderNumber = `${prefix}${numberPart + 1}`;

            // Update the order_number_start setting
            await fetch("/lookups/settings", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ key: "order_number_start", value: nextOrderNumber })
            });

            resetForm();
            await loadOrderNumber();
        } else {
            const detail = data.detail || data.message || "Unknown error.";
            alert(`❌ ${detail}`);
        }
    } catch (err) {
        console.error("Submit failed", err);
        alert("❌ Submission failed.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("Page loaded");
    console.log("Requester dropdown options:", document.getElementById('requester_id').options.length);
    console.log("Supplier dropdown options:", document.getElementById('supplier_id').options.length);
    loadDropdowns();
    document.getElementById("add-line").addEventListener("click", addRow);
    document.getElementById("preview-order").addEventListener("click", previewOrder);
    document.getElementById("email-po").addEventListener("click", emailPurchaseOrder);
    document.getElementById("submit-order").addEventListener("click", submitOrder);
    document.getElementById("cancel-order").addEventListener("click", cancelForm);
});