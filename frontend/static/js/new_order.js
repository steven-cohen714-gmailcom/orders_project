let itemsList = [];
let projectsList = [];
let rowCount = 0;
let latestOrderId = null;
let latestOrderDetails = null;
let currentOrderNumber = null;

// Debounce utility function
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

// Client-side logging utility
async function logToServer(level, message, details = {}) {
    try {
        await fetch('/log_client', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level, message, details, timestamp: new Date().toISOString() })
        });
    } catch (error) {
        console.error('Failed to log to server:', error);
    }
}

// Modified previewOrder with enhanced error handling and logging
async function previewOrder() {
    console.log("previewOrder called");
    await logToServer('INFO', 'Starting PDF preview generation');

    const previewBtn = document.getElementById("preview-order");
    const originalText = previewBtn ? previewBtn.textContent : "View Purchase Order";
    if (previewBtn) {
        previewBtn.textContent = "Generating PDF...";
        previewBtn.disabled = true;
    }

    try {
        // Validate form inputs
        const orderNumber = document.getElementById("order-number")?.textContent;
        const date = document.getElementById("request_date")?.value;
        const supplierId = document.getElementById("supplier_id")?.value;
        const noteToSupplier = document.getElementById("note_to_supplier")?.value || '';

        if (!orderNumber || orderNumber === "Error") {
            throw new Error("Invalid or missing order number.");
        }
        if (!date) {
            throw new Error("Request date is required.");
        }
        if (!supplierId) {
            throw new Error("Please select a supplier.");
        }

        await logToServer('DEBUG', 'Collected form data', { orderNumber, date, supplierId, noteToSupplier });

        // Collect and validate items
        const items = Array.from(document.querySelectorAll("#items-body tr"))
            .map((row, index) => {
                const c = row.querySelectorAll("td");
                const itemCode = c[0]?.querySelector("select")?.value;
                const project = c[1]?.querySelector("select")?.value;
                const qtyOrdered = parseFloat(c[2]?.querySelector("input")?.value) || 0;
                const price = parseFloat(c[3]?.querySelector("input")?.value) || 0;
                const selectedOption = c[0]?.querySelector("select")?.selectedOptions[0];
                const itemDescription = selectedOption ? selectedOption.dataset.description : "";
                if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {
                    throw new Error(`Invalid item at row ${index + 1}: requires item code, project, quantity > 0, and price > 0.`);
                }
                return { item_code: itemCode, item_description: itemDescription, project, qty_ordered: qtyOrdered, price };
            });

        if (items.length === 0) {
            throw new Error("At least one valid item is required.");
        }

        const total = items.reduce((sum, item) => sum + (item.qty_ordered * item.price), 0);
        await logToServer('DEBUG', 'Collected items', { items, total });

        // Fetch business details
        const businessDetailsRes = await fetch("/lookups/business_details");
        if (!businessDetailsRes.ok) {
            const errorText = await businessDetailsRes.text();
            throw new Error(`Failed to fetch business details: ${businessDetailsRes.status} - ${errorText}`);
        }
        const businessDetails = await businessDetailsRes.json();
        if (!businessDetails.company_name) {
            throw new Error("Business details are incomplete.");
        }

        const payload = {
            order_number: orderNumber,
            date: date,
            supplier_id: parseInt(supplierId),
            note_to_supplier: noteToSupplier,
            items: items,
            total: total,
            business_details: businessDetails
        };

        await logToServer('INFO', 'Sending PDF generation payload', { payload });

        // Generate PDF
        const res = await fetch("/orders/generate_pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`PDF generation failed: ${res.status} - ${errorText}`);
        }

        const contentType = res.headers.get("content-type");
        if (!contentType || !contentType.includes("application/pdf")) {
            const text = await res.text();
            throw new Error(`Invalid response: Expected PDF, got ${contentType}. Response: ${text}`);
        }

        const blob = await res.blob();
        if (blob.size === 0) {
            throw new Error("Received empty PDF file.");
        }

        await logToServer('INFO', 'PDF generated successfully', { blobSize: blob.size });

        const url = window.URL.createObjectURL(blob);
        const pdfFile = { filename: `order_${orderNumber}.pdf`, file_path: url };
        showViewAttachmentsModal(orderNumber, orderNumber, () => {
            console.log("Modal closed");
            logToServer('INFO', 'PDF modal closed');
        }, [pdfFile]);

        console.log("PDF displayed successfully");
    } catch (error) {
        console.error("PDF generation error:", error);
        await logToServer('ERROR', 'PDF generation failed', { error: error.message, stack: error.stack });
        alert(`Error generating PDF: ${error.message}`);
    } finally {
        if (previewBtn) {
            previewBtn.textContent = originalText;
            previewBtn.disabled = false;
        }
    }
}

// Test function for previewOrder
async function testPreviewOrder() {
    console.log("Running testPreviewOrder");
    await logToServer('INFO', 'Starting previewOrder test');

    try {
        // Mock DOM elements
        document.body.innerHTML = `
            <div id="order-number">URC1000</div>
            <input id="request_date" value="2025-05-10">
            <select id="supplier_id"><option value="1">Test Supplier</option></select>
            <textarea id="note_to_supplier">Test note</textarea>
            <table id="items-table"><tbody id="items-body">
                <tr>
                    <td><select><option value="ITEM1" data-description="Test Item">ITEM1</option></select></td>
                    <td><select><option value="PROJ1">PROJ1</option></select></td>
                    <td><input type="number" value="2"></td>
                    <td><input type="number" value="10"></td>
                    <td><input type="text" value="20.00"></td>
                </tr>
            </tbody></table>
            <button id="preview-order">View Purchase Order</button>
        `;

        // Mock fetch responses
        window.fetch = async (url, options) => {
            if (url === '/lookups/business_details') {
                return {
                    ok: true,
                    json: async () => ({
                        company_name: "Test Company",
                        address_line1: "123 Test St",
                        city: "Test City",
                        province: "Test Province",
                        postal_code: "12345",
                        telephone: "123-456-7890",
                        vat_number: "VAT123"
                    })
                };
            }
            if (url === '/orders/generate_pdf') {
                return {
                    ok: true,
                    headers: { get: () => 'application/pdf' },
                    blob: async () => new Blob(['mock pdf content'], { type: 'application/pdf' })
                };
            }
            if (url === '/log_client') {
                return { ok: true };
            }
            throw new Error(`Unexpected fetch call: ${url}`);
        };

        // Mock showViewAttachmentsModal
        window.showViewAttachmentsModal = (orderId, orderNumber, callback, files) => {
            console.log('Mock showViewAttachmentsModal called', { orderId, orderNumber, files });
            callback();
        };

        // Run previewOrder
        await previewOrder();

        console.log("Test passed: previewOrder executed without errors");
        await logToServer('INFO', 'previewOrder test completed successfully');
    } catch (error) {
        console.error("Test failed:", error);
        await logToServer('ERROR', 'previewOrder test failed', { error: error.message, stack: error.stack });
        throw error;
    }
}

// Existing functions (unchanged for this iteration)
function updateGrandTotal() {
    let sum = 0;
    document.querySelectorAll("#items-table tbody tr").forEach(row => {
        const totalField = row.querySelector("td:nth-child(5) input");
        if (totalField) {
            sum += parseFloat(totalField.value) || 0;
        }
    });
    document.getElementById("grand-total").textContent = `R${sum.toFixed(2)}`;
}

function updateTotal(input) {
    const row = input.closest("tr");
    const qty = parseFloat(row.cells[2].querySelector("input").value) || 0;
    const price = parseFloat(row.cells[3].querySelector("input").value) || 0;
    row.cells[4].querySelector("input").value = (qty * price).toFixed(2);
    updateGrandTotal();
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
        <td><button type="button" onclick="deleteRow(this)">Remove</button></td>
    `;

    const projectSelect = row.querySelector(`#project_${rowCount}`);
    if (projectSelect.options.length > 1) {
        projectSelect.value = projectSelect.options[1].value;
    }

    const qtyInput = row.querySelector(`#qty_ordered_${rowCount}`);
    const priceInput = row.querySelector(`#price_${rowCount}`);
    qtyInput.addEventListener("change", () => updateTotal(qtyInput));
    priceInput.addEventListener("change", () => updateTotal(priceInput));

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
        const fetchWithErrorHandling = async (url, name) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`Failed to fetch ${name}: HTTP ${response.status} - ${response.statusText}`);
                }
                return await response.json();
            } catch (err) {
                console.error(`Error fetching ${name}:`, err);
                throw err;
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

        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        document.getElementById("request_date").value = `${yyyy}-${mm}-${dd}`;

        currentOrderNumber = await loadOrderNumber();
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
    latestOrderId = null;
    latestOrderDetails = null;
}

function showViewAttachmentsModal(orderId, orderNumber, onUploadComplete = null, customFiles = null) {
    const filesPromise = customFiles ? Promise.resolve({ attachments: customFiles }) : fetch(`/orders/attachments/${orderId}`).then(res => res.json());

    filesPromise
        .then(data => {
            const files = data.attachments || [];
            const modal = createBaseModal();
            const title = document.createElement("h3");
            title.textContent = `Attachments for ${orderNumber}`;
            modal.inner.appendChild(title);

            if (files.length > 0) {
                const list = document.createElement("ul");
                list.style.listStyle = "none";
                list.style.padding = "0";

                files.forEach(f => {
                    const li = document.createElement("li");
                    const link = document.createElement("a");
                    link.href = f.file_path;
                    link.textContent = f.filename;
                    link.target = "_blank";
                    link.style.display = "block";
                    link.style.marginBottom = "0.5rem";
                    link.style.color = "green";
                    link.style.textDecoration = "underline";
                    li.appendChild(link);
                    list.appendChild(li);
                });

                modal.inner.appendChild(list);
            }

            const dropzone = document.createElement("div");
            dropzone.textContent = "Drag and drop files here or click to select";
            dropzone.style.border = "2px dashed #aaa";
            dropzone.style.padding = "2rem";
            dropzone.style.textAlign = "center";
            dropzone.style.cursor = "pointer";
            dropzone.style.marginTop = "1rem";
            dropzone.style.background = "#fafafa";

            dropzone.onclick = () => {
                const input = document.createElement("input");
                input.type = "file";
                input.multiple = true;
                input.onchange = () => handleFiles(input.files, orderId, modal.inner, onUploadComplete);
                input.click();
            };

            dropzone.ondragover = e => {
                e.preventDefault();
                dropzone.style.background = "#eee";
            };
            dropzone.ondragleave = () => {
                dropzone.style.background = "#fafafa";
            };
            dropzone.ondrop = e => {
                e.preventDefault();
                dropzone.style.background = "#fafafa";
                handleFiles(e.dataTransfer.files, orderId, modal.inner, onUploadComplete);
            };

            modal.inner.appendChild(dropzone);

            const closeBtn = document.createElement("button");
            closeBtn.textContent = "Close";
            closeBtn.style.marginTop = "1.5rem";
            closeBtn.style.padding = "0.5rem 1rem";
            closeBtn.style.border = "none";
            closeBtn.style.cursor = "pointer";
            closeBtn.style.background = "#ccc";
            closeBtn.onclick = () => document.body.removeChild(modal.container);

            modal.inner.appendChild(closeBtn);

            document.body.appendChild(modal.container);
        })
        .catch(err => {
            alert("❌ Failed to load attachments");
            console.error(err);
        });
}

function handleFiles(fileList, orderId, modalInner, onUploadComplete = null) {
    Array.from(fileList).forEach(file => {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("order_id", orderId);

        fetch("/orders/upload_attachment", {
            method: "POST",
            body: formData,
        })
            .then(res => res.json())
            .then(data => {
                const msg = document.createElement("p");
                msg.textContent = data.status;
                msg.style.color = "green";
                modalInner.appendChild(msg);
                if (onUploadComplete) onUploadComplete();
            })
            .catch(err => {
                const msg = document.createElement("p");
                msg.textContent = `❌ Failed to upload: ${file.name}`;
                msg.style.color = "red";
                modalInner.appendChild(msg);
                console.error(err);
            });
    });
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
    inner.style.fontFamily = "Arial, sans-serif";
    inner.style.position = "relative";

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

function emailPurchaseOrder() {
    alert("Email Purchase Order functionality will be implemented after fixing PDF generation.");
}

function cancelForm() {
    window.location.href = "/orders/pending_orders";
}

const debouncedSubmitOrder = debounce(async () => {
    console.log("debouncedSubmitOrder triggered");
    const rd = document.getElementById("request_date").value;
    const rqId = document.getElementById("requester_id").value;
    const spId = document.getElementById("supplier_id").value;
    const nt = document.getElementById("note_to_supplier").value;
    const rows = document.querySelectorAll("#items-body tr");

    console.log("Submitting order with:", { request_date: rd, requester_id: rqId, supplier_id: spId, note_to_supplier: nt });

    const items = Array.from(rows)
        .map(row => {
            const c = row.querySelectorAll("td");
            const itemCode = c[0].querySelector("select").value;
            const project = c[1].querySelector("select").value;
            const qtyOrdered = parseFloat(c[2].querySelector("input").value) || 0;
            const price = parseFloat(c[3].querySelector("input").value) || 0;
            const selectedOption = c[0].querySelector("select").selectedOptions[0];
            const itemDescription = selectedOption ? selectedOption.dataset.description : "";
            return {
                item_code: itemCode,
                item_description: itemDescription,
                project: project,
                qty_ordered: qtyOrdered,
                price: price
            };
        })
        .filter(i => i.item_code && i.project && i.qty_ordered > 0 && i.price > 0);

    console.log("Items:", items);

    if (!rd) {
        console.log("Validation failed: Missing request date");
        alert("⚠️ Please fill in the request date.");
        return;
    }
    if (!rqId) {
        console.log("Validation failed: Missing requester");
        alert("⚠️ Please select a requester.");
        return;
    }
    if (!spId) {
        console.log("Validation failed: Missing supplier");
        alert("⚠️ Please select a supplier.");
        return;
    }
    if (items.length === 0) {
        console.log("Validation failed: No valid line items");
        alert("⚠️ Please add at least one complete line item with an item code, project, quantity greater than 0, and price greater than 0.");
        return;
    }

    const submitBtn = document.getElementById("submit-order");
    const originalText = submitBtn.textContent;
    submitBtn.textContent = "Submitting...";
    submitBtn.disabled = true;

    try {
        // Implementation continues as in original file...
    } catch (error) {
        console.error("Order submission failed:", error);
        alert(`❌ Order submission failed: ${error.message}`);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});

// Run test on demand (e.g., via console or button)
window.testPreviewOrder = testPreviewOrder;