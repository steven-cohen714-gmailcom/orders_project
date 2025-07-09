// /frontend/static/js/cod_orders.js

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { expandLineItems } from "./components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "./components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "./components/order_note_modal.js";
import { showPDFModal } from "./components/pdf_modal.js";
import { showCodPaymentModal } from "./components/payments_modal.js"; // ✅ REQUIRED

// New function to format currency with thousand separators and 2 decimal places
function formatCurrency(amount) {
  if (amount == null) return "R0.00";
  return `R${parseFloat(amount).toLocaleString('en-ZA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

console.log("✅ cod_orders.js loaded");

async function loadFiltersAndOrders() {
  try {
    await Promise.all([
      loadRequesters("filter-requester"),
      loadSuppliers("filter-supplier")
    ]);
    await loadOrders();
  } catch (err) {
    console.error("❌ Error loading filters:", err);
    document.getElementById("cod-body").innerHTML = `<tr><td colspan="7">Error loading filters: ${err.message}</td></tr>`;
  }
}

async function loadOrders() {
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;
  const requester = document.getElementById("filter-requester").value;
  const supplier = document.getElementById("filter-supplier").value;
  const status = document.getElementById("filter-status").value;

  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);
  if (requester && requester !== "All") params.append("requester", requester);
  if (supplier && supplier !== "All") params.append("supplier", supplier);
  if (status && status !== "All") params.append("status", status);

  try {
    const res = await fetch(`/orders/api/cod_orders?${params.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();

    const tbody = document.getElementById("cod-body");
    tbody.innerHTML = "";

    if (Array.isArray(data.orders) && data.orders.length > 0) {
      data.orders.forEach((order, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${escapeHTML(order.created_date || "")}</td>
          <td>${escapeHTML(order.order_number || "")}</td>
          <td>${escapeHTML(order.requester || "")}</td>
          <td>${escapeHTML(order.supplier || "")}</td>
          <td>${formatCurrency(order.total)}</td>
          <td>${escapeHTML(order.status || "")}</td>
          <td>
            <span class="expand-icon" data-order-id="${order.id}">⬇️</span>
            <span class="clip-icon" data-order-id="${order.id}" data-order-number="${order.order_number}">📎</span>
            <span class="note-icon" data-order-id="${order.id}" data-order-note="${escapeHTML(order.order_note || "")}">📝</span>
            <span class="supplier-note-icon" data-note="${escapeHTML(order.note_to_supplier || "")}">📦</span>
            <span 
              class="receive-icon" 
              style="color: green; cursor: pointer;" 
              title="Mark COD as Paid" 
              data-order-id="${order.id}" 
              data-order-number="${escapeHTML(order.order_number || "")}"
            >✅</span>
            <span class="pdf-icon" data-order-id="${order.id}">📄</span>

          </td>
        `;

        tbody.appendChild(row);

        row.querySelector(".expand-icon").addEventListener("click", (e) =>
          expandLineItems(order.id, e.target)
        );

        row.querySelector(".clip-icon").addEventListener("click", async (e) => {
          const has = await checkAttachments(order.id);
          if (has) {
            showViewAttachmentsModal(order.id, order.order_number);
          } else {
            showUploadAttachmentsModal(order.id, order.order_number);
          }
        });

        row.querySelector(".note-icon").addEventListener("click", (e) => {
          const el = e.target;
          showOrderNoteModal(el.getAttribute("data-order-note"), order.id, (newNote) => {
            el.setAttribute("data-order-note", escapeHTML(newNote));
          });
        });

        row.querySelector(".supplier-note-icon").addEventListener("click", (e) => {
          const note = e.target.getAttribute("data-note");
          showSupplierNoteModal(note);
        });

        row.querySelector(".receive-icon").addEventListener("click", () => {
          showCodPaymentModal(order.id, parseFloat(order.total || 0), new Date().toISOString().split("T")[0]);
        });

        row.querySelector(".pdf-icon").addEventListener("click", async () => {
          try {
            const res = await fetch(`/orders/api/generate_pdf_for_order/${order.id}`);
            if (!res.ok) throw new Error(`PDF failed (${res.status})`);
            const blob = await res.blob();
            if (!blob.size) throw new Error("Empty PDF");
            showPDFModal(blob);
          } catch (err) {
            alert("❌ Could not generate PDF");
            console.error(err);
          }
        });
      });
    } else {
      tbody.innerHTML = "<tr><td colspan='7'>No COD orders found.</td></tr>";
    }
  } catch (err) {
    console.error("❌ Error loading orders:", err);
    document.getElementById("cod-body").innerHTML = `<tr><td colspan="7">Error loading orders: ${err.message}</td></tr>`;
  }
}

function clearFilters() {
  document.getElementById("start-date").value = "";
  document.getElementById("end-date").value = "";
  document.getElementById("filter-requester").value = "All";
  document.getElementById("filter-supplier").value = "All";
  document.getElementById("filter-status").value = "All";
  loadOrders();
}

function escapeHTML(str) {
  return (str || "").replace(/&/g, "&amp;")
                   .replace(/</g, "&lt;")
                   .replace(/>/g, "&gt;")
                   .replace(/"/g, "&quot;")
                   .replace(/'/g, "&#39;");
}

document.getElementById("run-btn").addEventListener("click", loadOrders);
document.getElementById("clear-btn").addEventListener("click", clearFilters);
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);
