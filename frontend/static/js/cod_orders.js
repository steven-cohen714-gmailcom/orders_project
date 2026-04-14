import { escapeHTML, formatCurrency, formatYMD } from './components/utils.js';
// File: frontend/static/js/cod_orders.js

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { expandLineItems } from "./components/expand_line_items.js";
import { showUploadAttachmentsModal, checkAttachments, showViewAttachmentsModal } from "./components/attachment_modal.js";
import { showOrderNoteModal, showSupplierNoteModal } from "./components/order_note_modal.js";
import { showPDFModal } from "./components/pdf_modal.js";
import { showCodPaymentModal } from "./components/payments_modal.js";

console.log("✅ cod_orders.js loaded");

// Currency formatter

// Escape HTML

// Extract trailing digits from order_number for numeric sort (works for "URC1200" or "2407")
function orderNumberKey(orderNumber) {
  const s = String(orderNumber || "");
  const m = s.match(/(\d+)$/);
  if (m) return parseInt(m[1], 10) || 0;
  // fallback: try whole string as int
  const asInt = parseInt(s, 10);
  return Number.isFinite(asInt) ? asInt : 0;
}

async function loadFiltersAndOrders() {
  try {
    await Promise.all([
      loadRequesters("filter-requester"),
      loadSuppliers("filter-supplier"),
    ]);
    await loadOrders();
  } catch (err) {
    console.error("❌ Error loading filters:", err);
    const tbody = document.getElementById("cod-body");
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="7">Error loading filters: ${escapeHTML(err.message)}</td></tr>`;
    }
  }
}

async function loadOrders() {
  const startDate = document.getElementById("start-date")?.value || "";
  const endDate = document.getElementById("end-date")?.value || "";
  const requester = document.getElementById("filter-requester")?.value || "";
  const supplier = document.getElementById("filter-supplier")?.value || "";
  const status = document.getElementById("filter-status")?.value || "";

  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);
  if (requester && requester !== "All") params.append("requester", requester);
  if (supplier && supplier !== "All") params.append("supplier", supplier);
  if (status && status !== "All") params.append("status", status);

  const tbody = document.getElementById("cod-body");
  if (!tbody) return;
  tbody.innerHTML = "<tr><td colspan='7'>Loading…</td></tr>";

  try {
    const res = await fetch(`/orders/api/cod_orders?${params.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();

    const rows = Array.isArray(data.orders) ? data.orders : [];

    // Defensive client-side filter:
    // - Only COD (in case backend hasn’t filtered strictly)
    // - Exclude pre-review / on-hold / deleted / fully paid
    const filtered = rows.filter((o) => {
      const statusUp = String(o.status || "").trim().toUpperCase();
      const termsUp  = String(o.payment_terms || "COD").trim().toUpperCase();

      if (termsUp !== "COD") return false;
      if (statusUp === "DELETED") return false;
      if (statusUp === "PAID" || statusUp === "FULLY PAID") return false;

      // New: keep COD screen clean from pre-review/on-hold leakage
      if (statusUp === "FOR REVIEW" || statusUp === "ON HOLD") return false;

      return true;
    });

    // Sort: numeric order number DESC, then created_date DESC
    filtered.sort((a, b) => {
      const kA = orderNumberKey(a.order_number);
      const kB = orderNumberKey(b.order_number);
      if (kB !== kA) return kB - kA;
      const da = new Date(a.created_date || 0).getTime();
      const db = new Date(b.created_date || 0).getTime();
      return db - da;
    });

    tbody.innerHTML = "";

    if (filtered.length === 0) {
      tbody.innerHTML = "<tr><td colspan='7'>No COD orders found.</td></tr>";
      return;
    }

    filtered.forEach((order) => {
      const tr = document.createElement("tr");

      const rawStatus = String(order.status || "").trim();
      const isAwaitingAuthorisation = rawStatus === "Awaiting Authorisation";

      const receiveIconDisabled = isAwaitingAuthorisation;
      const receiveIconClass = receiveIconDisabled ? "receive-icon disabled" : "receive-icon";
      const receiveIconStyle = receiveIconDisabled ? "color: grey; cursor: not-allowed;" : "color: green; cursor: pointer;";
      const receiveIconTitle = receiveIconDisabled ? "Cannot mark paid until authorised" : "Mark COD as Paid";

      tr.innerHTML = `
        <td>${escapeHTML(order.created_date || "")}</td>
        <td>${escapeHTML(order.order_number || "")}</td>
        <td>${escapeHTML(order.requester || "")}</td>
        <td>${escapeHTML(order.supplier || "")}</td>
        <td>${formatCurrency(order.total)}</td>
        <td>${escapeHTML(order.status || "")}</td>
        <td>
          <span class="expand-icon" data-order-id="${order.id}">⬇️</span>
          <span class="clip-icon" data-order-id="${order.id}" data-order-number="${escapeHTML(order.order_number || "")}">📎</span>
          <span class="note-icon" data-order-id="${order.id}" data-order-note="${escapeHTML(order.order_note || "")}">📝</span>
          <span class="supplier-note-icon" data-note="${escapeHTML(order.note_to_supplier || "")}">📦</span>
          <span
            class="${receiveIconClass}"
            style="${receiveIconStyle}"
            title="${receiveIconTitle}"
            data-order-id="${order.id}"
            data-order-number="${escapeHTML(order.order_number || "")}"
          >✅</span>
          <span class="pdf-icon" data-order-id="${order.id}">📄</span>
        </td>
      `;
      tbody.appendChild(tr);

      // Expanded details row (immediately after main row)
      const detailRow = document.createElement("tr");
      detailRow.className = "expanded-details-row";
      const detailCell = document.createElement("td");
      detailCell.colSpan = 7;
      const detailContainer = document.createElement("div");
      detailContainer.id = `detail-container-${order.id}`;
      detailContainer.style.display = "none";
      detailCell.appendChild(detailContainer);
      detailRow.appendChild(detailCell);
      tbody.appendChild(detailRow);

      // Handlers
      tr.querySelector(".expand-icon")?.addEventListener("click", (e) => {
        expandLineItems(order.id, e.target, detailContainer, order);
      });

      tr.querySelector(".clip-icon")?.addEventListener("click", async () => {
        try {
          const has = await checkAttachments(order.id);
          if (has) {
            showViewAttachmentsModal(order.id, order.order_number);
          } else {
            showUploadAttachmentsModal(order.id, order.order_number);
          }
        } catch (err) {
          console.error("Attachment check failed:", err);
          alert("❌ Could not check attachments.");
        }
      });

      tr.querySelector(".note-icon")?.addEventListener("click", (e) => {
        const el = e.target;
        showOrderNoteModal(el.getAttribute("data-order-note") || "", order.id, (newNote) => {
          el.setAttribute("data-order-note", escapeHTML(newNote || ""));
        });
      });

      tr.querySelector(".supplier-note-icon")?.addEventListener("click", (e) => {
        const note = e.target.getAttribute("data-note") || "";
        showSupplierNoteModal(note);
      });

      const receiveIcon = tr.querySelector(".receive-icon");
      if (receiveIcon && !receiveIcon.classList.contains("disabled")) {
        receiveIcon.addEventListener("click", () => {
          // Modal handles the API call. After it closes/succeeds, we rely on the user flow or modal to refresh.
          // If your modal dispatches a custom event after save, this listener will refresh the list:
          //   window.dispatchEvent(new CustomEvent("cod-payment-updated"));
          showCodPaymentModal(order.id, escapeHTML(order.order_number || ""));
        });
      }

      tr.querySelector(".pdf-icon")?.addEventListener("click", async () => {
        try {
          const r = await fetch(`/orders/api/generate_pdf_with_projects/${order.id}`);
          if (!r.ok) throw new Error(`PDF failed (${r.status})`);
          const blob = await r.blob();
          if (!blob.size) throw new Error("Empty PDF");
          showPDFModal(blob, order.id, order.order_number);
        } catch (err) {
          console.error("❌ PDF error:", err);
          alert("❌ Could not generate PDF.");
        }
      });
    });
  } catch (err) {
    console.error("❌ Error loading orders:", err);
    tbody.innerHTML = `<tr><td colspan="7">Error loading orders: ${escapeHTML(err.message)}</td></tr>`;
  }
}

function clearFilters() {
  const ids = ["start-date", "end-date", "filter-requester", "filter-supplier", "filter-status"];
  ids.forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;
    if (el.tagName === "SELECT") el.value = "All";
    else el.value = "";
  });
  loadOrders();
}

// Optional: auto-refresh when the payment modal completes (if your modal fires this event)
window.addEventListener("cod-payment-updated", () => {
  loadOrders();
});

document.getElementById("run-btn")?.addEventListener("click", loadOrders);
document.getElementById("clear-btn")?.addEventListener("click", clearFilters);
document.addEventListener("DOMContentLoaded", loadFiltersAndOrders);
