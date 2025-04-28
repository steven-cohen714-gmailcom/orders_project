import { expandLineItems } from "/static/js/components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "/static/js/components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "/static/js/components/order_note_modal.js";
import { loadRequesters, loadSuppliers } from "/static/js/components/shared_filters.js";

async function populateDropdown(dropdownId, items, key) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = '<option value="">All</option>';
    if (items && Array.isArray(items)) {
        items.forEach(item => {
            const option = document.createElement("option");
            option.value = item[key];
            option.textContent = item[key];
            dropdown.appendChild(option);
        });
    }
}

function escapeHTML(str) {
    if (!str) return "";
    return str.replace(/'/g, "\\'").replace(/"/g, "\\\"").replace(/</g, "<").replace(/>/g, ">").replace(/\n/g, " ").replace(/\r/g, "");
}

async function fetchData(endpoint) {
    try {
        const response = await fetch(`http://localhost:8004${endpoint}`, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch ${endpoint}: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        return null;
    }
}

async function loadFiltersAndOrders() {
    try {
        const requestersData = await fetchData("/lookups/requesters");
        const suppliersData = await fetchData("/lookups/suppliers");

        await populateDropdown("filter-requester", requestersData?.requesters, "name");
        await populateDropdown("filter-supplier", suppliersData?.suppliers, "name");

        await loadOrders();
    } catch (error) {
        console.error("Failed to load filters:", error);
        await loadOrders();
    }
}

async function loadOrders() {
    try {
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;
        const requester = document.getElementById("filter-requester").value;
        const supplier = document.getElementById("filter-supplier").value;
        const status = document.getElementById("filter-status").value;

        const params = new URLSearchParams();
        if (startDate) params.append("start_date", startDate);
        if (endDate) params.append("end_date", endDate);
        if (requester) params.append("requester", requester);
        if (supplier) params.append("supplier", supplier);
        if (status && status !== "All") params.append("status", status);

        const response = await fetch(`/orders/api/received_orders?${params.toString()}`, {
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch received orders Error: HTTP ${response.status}: ${await response.text()}`);
        }
        const data = await response.json();
        const tbody = document.getElementById("received-body");
        tbody.innerHTML = "";

        if (data.orders && data.orders.length > 0) {
            data.orders.forEach(order => {
                const row = document.createElement("tr");
                const sanitizedOrderNote = escapeHTML(order.order_note || "");
                const sanitizedSupplierNote = escapeHTML(order.note_to_supplier || "");
                const sanitizedOrderNumber = escapeHTML(order.order_number);
                const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
                const sanitizedRequester = escapeHTML(order.requester);
                row.innerHTML = `
                    <td>${order.created_date}</td>
                    <td>${sanitizedOrderNumber}</td>
                    <td>${sanitizedRequester}</td>
                    <td>${sanitizedSupplier}</td>
                    <td>R${order.total.toFixed(2)}</td>
                    <td><span class="status">${order.status}</span></td>
                    <td>
                        <span class="expand-icon" onclick="window.expandLineItems(${order.id}, this)">⬇️</span>
                        <span class="clip-icon" title="View/Upload Attachments" onclick="window.checkAttachments(${order.id}).then(has => has ? window.showViewAttachmentsModal(${order.id}, '${sanitizedOrderNumber}') : window.showUploadAttachmentsModal(${order.id}, '${sanitizedOrderNumber}', () => window.checkAttachments(${order.id}).then(has => this.classList.toggle('eye-icon', has))))">📎</span>
                        <span class="note-icon" title="Edit Order Note" onclick="window.showOrderNoteModal('${sanitizedOrderNote}', ${order.id})">📝</span>
                        <span class="supplier-note-icon" title="View Note to Supplier" onclick="try { window.showSupplierNoteModal('${sanitizedSupplierNote}'); } catch (e) { console.error('Failed to show supplier note for order ${order.order_number}:', e); alert('Error displaying supplier note: ' + e.message); }}">📦</span>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="7">No received orders found.</td></tr>';
        }
    } catch (error) {
        console.error("Error loading orders:", error);
        document.getElementById("received-body").innerHTML = '<tr><td colspan="7">Error loading orders.</td></tr>';
    }
}

function clearFilters() {
    document.getElementById("start-date").value = "";
    document.getElementById("end-date").value = "";
    document.getElementById("filter-requester").value = "";
    document.getElementById("filter-supplier").value = "";
    document.getElementById("filter-status").value = "All";
    loadOrders();
}

// Event listeners
document.getElementById("run-btn").addEventListener("click", loadOrders);
document.getElementById("clear-btn").addEventListener("click", clearFilters);

// Initial load
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);

// Expose functions to global scope for onclick handlers
window.expandLineItems = expandLineItems;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;
window.showOrderNoteModal = showOrderNoteModal;
window.showSupplierNoteModal = showSupplierNoteModal;