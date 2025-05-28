console.log("✅ cod_payments_screen.js loaded");
import { loadRequesters, loadSuppliers } from './components/shared_filters.js';
import { expandLineItems } from './components/expand_line_items.js';
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from './components/attachment_modal.js';
import { showOrderNoteModal, showSupplierNoteModal } from './components/order_note_modal.js';
import { showPDFModal } from './components/pdf_modal.js';
import { showCodPaymentModal } from './components/payment_modal.js'; // 🔔 New import

console.log("🔁 Loading cod_payments_screen.js");

async function loadFiltersAndOrders() {
    try {
        await Promise.all([
            loadRequesters("filter-requester"),
            loadSuppliers("filter-supplier")
        ]);
        await loadOrders();
    } catch (error) {
        console.error("Error loading filters or orders:", error);
        document.getElementById("payments-body").innerHTML = '<tr><td colspan="7">Error loading filters: ' + escapeHTML(error.message) + '</td></tr>';
    }
}

function escapeHTML(str) {
    if (typeof str !== 'string') return '';
    return str
        .replace(/&/g, '&')
        .replace(/</g, '<')
        .replace(/>/g, '>')
        .replace(/"/g, '"')
        .replace(/'/g, '');
}

async function loadOrders() {
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const requester = document.getElementById("filter-requester").value;
    const supplier = document.getElementById("filter-supplier").value;

    const params = new URLSearchParams();
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);
    if (requester && requester !== "All") params.append("requester", requester);
    if (supplier && supplier !== "All") params.append("supplier", supplier);

    try {
        const res = await fetch(`/orders/api/cod_orders?${params.toString()}`);
        if (!res.ok) throw new Error(`Failed to fetch COD orders: ${res.status}`);
        const data = await res.json();

        const tbody = document.getElementById("payments-body");
        tbody.innerHTML = "";

        if (!data.orders || data.orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8">No COD orders found.</td></tr>';
            return;
        }

        data.orders.forEach((order, index) => {
            console.log("🧾 COD Order:", order);
            const row = document.createElement("tr");
            const sanitizedOrderNumber = escapeHTML(order.order_number || "");
            const sanitizedSupplier = escapeHTML(order.supplier || "N/A");
            const sanitizedDate = escapeHTML(order.created_date || "");
            const sanitizedTotal = order.total != null ? `R${parseFloat(order.total).toFixed(2)}` : "R0.00";
            const sanitizedTerms = escapeHTML(order.payment_terms || "COD");
            const paymentDate = escapeHTML(order.payment_date || "—");
            const amountPaid = order.amount_paid ? `R${parseFloat(order.amount_paid).toFixed(2)}` : "—";

            row.innerHTML = `
                <td>${sanitizedOrderNumber}</td>
                <td>${sanitizedSupplier}</td>
                <td>${sanitizedDate}</td>
                <td>${sanitizedTotal}</td>
                <td>${sanitizedTerms}</td>
                <td>${paymentDate}</td>
                <td>${amountPaid}</td>
                <td>
                    <span class="expand-icon" data-order-id="${order.id}">⬇️</span>
                    <span class="clip-icon" data-order-id="${order.id}" data-order-number="${sanitizedOrderNumber}">📎</span>
                    <span class="note-icon" data-order-id="${order.id}" id="note-${index}">📝</span>
                    <span class="cod-pay-icon" data-order-id="${order.id}" data-order-number="${sanitizedOrderNumber}">✅</span>
                    <span class="pdf-icon" data-order-id="${order.id}" data-order-number="${sanitizedOrderNumber}">📄</span>
                </td>
            `;
            tbody.appendChild(row);

            row.querySelector(".expand-icon").addEventListener("click", e => {
                expandLineItems(order.id, e.target);
            });

            row.querySelector(".clip-icon").addEventListener("click", e => {
                const target = e.target;
                checkAttachments(order.id).then(has => {
                    if (has) {
                        showViewAttachmentsModal(order.id, sanitizedOrderNumber);
                    } else {
                        showUploadAttachmentsModal(order.id, sanitizedOrderNumber, () => {
                            checkAttachments(order.id).then(has => target.classList.toggle('eye-icon', has));
                        });
                    }
                });
            });

            row.querySelector(`#note-${index}`).addEventListener("click", () => {
                showOrderNoteModal(order.order_note || "", order.id, updatedNote => {
                    document.querySelector(`#note-${index}`).title = "Edit Order Note\n" + updatedNote;
                });
            });

            row.querySelector(".cod-pay-icon").addEventListener("click", () => {
                showCodPaymentModal(order.id, sanitizedOrderNumber);
            });

            row.querySelector(".pdf-icon").addEventListener("click", async () => {
                try {
                    const response = await fetch(`/orders/api/generate_pdf_for_order/${order.id}`);
                    if (!response.ok) throw new Error(`PDF generation failed: ${response.status}`);
                    const blob = await response.blob();
                    if (blob.size === 0) throw new Error('Empty PDF');
                    showPDFModal(blob);
                } catch (err) {
                    alert("❌ Could not generate PDF");
                    console.error(err);
                }
            });
        });
    } catch (error) {
        console.error("Error loading COD orders:", error);
        document.getElementById("payments-body").innerHTML = '<tr><td colspan="8">Error loading orders: ' + escapeHTML(error.message) + '</td></tr>';
    }
}

function clearFilters() {
    document.getElementById("start-date").value = "";
    document.getElementById("end-date").value = "";
    document.getElementById("filter-requester").value = "All";
    document.getElementById("filter-supplier").value = "All";
    loadOrders();
}

document.getElementById("filter-btn").addEventListener("click", loadOrders);
document.getElementById("clear-btn").addEventListener("click", clearFilters);
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);
