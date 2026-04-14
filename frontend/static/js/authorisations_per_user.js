import { escapeHTML, formatCurrency, formatYMD } from './components/utils.js';
// File: frontend/static/js/authorisations_per_user.js
'use strict';

import { loadRequesters, loadSuppliers } from "./components/shared_filters.js";
import { expandLineItemsWithReceipts } from "./components/expand_line_items.js";
import { showPDFModal } from "./components/pdf_modal.js";

// ---------- utils ----------



function numericOrder(orderNumber) {
  const m = String(orderNumber || "").match(/\d+/g);
  return m ? Number(m.join("")) : -Infinity;
}

// ---------- main ----------
export async function setupAuthorisationUI({
  user,
  mountPointId,
  onAuthorised = () => {},
  onError = () => {}
}) {
  const tableBody = document.getElementById(mountPointId);
  if (!tableBody) {
    console.error(`Mount point '${mountPointId}' not found.`);
    return;
  }

  try {
    await Promise.all([
      loadRequesters("filter-requester"),
      loadSuppliers("filter-supplier"),
    ]);
  } catch (e) {
    console.error("Failed to load filters", e);
    tableBody.innerHTML = `<tr><td colspan="7">Error loading filters.</td></tr>`;
    return;
  }

  // initial load + buttons
  await loadOrdersForUser(user);
  document.getElementById("run-btn")?.addEventListener("click", () => loadOrdersForUser(user));
  document.getElementById("clear-btn")?.addEventListener("click", () => {
    document.getElementById("start-date").value = "";
    document.getElementById("end-date").value = "";
    document.getElementById("filter-requester").value = "All";
    document.getElementById("filter-supplier").value = "All";
    loadOrdersForUser(user);
  });

  async function loadOrdersForUser(currentUser) {
    tableBody.innerHTML = "<tr><td colspan='7'>Loading orders…</td></tr>";

    // collect filters
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
      const res = await fetch(`/orders/api/awaiting_authorisation?${params.toString()}`, { credentials: "same-origin" });
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
      const orders = await res.json();
      const userBand = Number(currentUser.auth_threshold_band);
      const eligible = orders.filter((o) => {
        if (o.status !== "Awaiting Authorisation") return false;
        const band = (o.required_auth_band == null) ? null : Number(o.required_auth_band);
        // Treat NULL/0 as Band 1; otherwise allow any order with required_band <= userBand
        if (band == null || band === 0) return userBand >= 1;    // visible to any authoriser
        return band <= userBand;
      });

      eligible.sort((a, b) => {
        const nb = numericOrder(b.order_number);
        const na = numericOrder(a.order_number);
        if (nb !== na) return nb - na;
        return String(b.created_date).localeCompare(String(a.created_date));
      });

      if (eligible.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='7'>✅ No orders awaiting your authorisation.</td></tr>";
        return;
      }

      tableBody.innerHTML = "";
      for (const order of eligible) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${escapeHTML(formatYMD(order.created_date))}</td>
          <td>${escapeHTML(order.order_number)}</td>
          <td>${escapeHTML(order.requester_name)}</td>
          <td>${escapeHTML(order.supplier_name)}</td>
          <td>${formatCurrency(order.total)}</td>
          <td>${escapeHTML(order.status)}</td>
          <td>
            <button class="expand-btn" data-id="${order.id}" title="View Line Items">⬇️</button>
            <button class="view-btn" data-id="${order.id}" data-number="${escapeHTML(order.order_number)}">View</button>
            <button class="auth-btn" data-id="${order.id}" data-number="${escapeHTML(order.order_number)}">Authorise</button>
          </td>
        `;
        tableBody.appendChild(tr);

        const detailRow = document.createElement("tr");
        detailRow.className = "expanded-details-row";
        const detailCell = document.createElement("td");
        detailCell.colSpan = 7;
        const detailContainer = document.createElement("div");
        detailContainer.id = `detail-container-${order.id}`;
        detailContainer.style.display = "none";
        detailCell.appendChild(detailContainer);
        detailRow.appendChild(detailCell);
        tableBody.appendChild(detailRow);

        tr.querySelector(".expand-btn").addEventListener("click", (e) => {
          expandLineItemsWithReceipts(order.id, e.currentTarget, detailContainer, order);
        });

        tr.querySelector(".view-btn").addEventListener("click", async (e) => {
          try {
            const id = e.currentTarget.getAttribute("data-id");
            const num = e.currentTarget.getAttribute("data-number");
            const r = await fetch(`/orders/api/generate_pdf_with_projects/${id}`, { credentials: "same-origin" });
            if (!r.ok) throw new Error(`PDF HTTP ${r.status}`);
            const blob = await r.blob();
            showPDFModal(blob, id, num);
          } catch (err) {
            console.error(err);
            onError("Could not open PDF preview.");
          }
        });

        // --- Spinner + double-click guard on Authorise ---
        tr.querySelector(".auth-btn").addEventListener("click", async (e) => {
          const btn = e.currentTarget;
          if (btn.disabled) return; // guard against double clicks

          // show spinner + disable
          const originalHTML = btn.innerHTML;
          btn.disabled = true;
          btn.setAttribute("aria-busy", "true");
          btn.innerHTML = "⏳ Authorising…";

          // let the spinner render before the network call
          await new Promise((resolve) => {
            requestAnimationFrame(() => requestAnimationFrame(resolve));
          });

          const id = btn.getAttribute("data-id");
          const num = btn.getAttribute("data-number");

          // timeout safety so we always restore the button
          const controller = new AbortController();
          const timeout = setTimeout(() => controller.abort(), 20000);

          try {
            const res = await fetch(`/orders/api/authorise_order/${encodeURIComponent(id)}`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              credentials: "same-origin",
              signal: controller.signal,
            });

            clearTimeout(timeout);

            // robust body parsing
            let body = null;
            const text = await res.text();
            try { body = text ? JSON.parse(text) : null; } catch {}

            if (res.ok && (body?.message === "Order authorised" || /authoris/i.test(String(body?.message)))) {
              alert(`✅ Order ${num} authorised.`);
              onAuthorised({ id, order_number: num });
              await loadOrdersForUser(currentUser); // refresh removes the row
              return; // no restore needed; row is gone
            }

            const msg = body?.detail || body?.message || text || `HTTP ${res.status}`;
            throw new Error(msg);

          } catch (err) {
            console.error(err);
            onError(err?.message || "Authorisation failed.");
          } finally {
            clearTimeout(timeout);
            // restore button so the user can retry (if the row still exists)
            if (document.body.contains(btn)) {
              btn.disabled = false;
              btn.removeAttribute("aria-busy");
              btn.innerHTML = originalHTML || "Authorise";
            }
          }
              }); // <-- end .auth-btn click handler
      } // <-- end for (const order of eligible)
    } catch (err) {
      console.error(err);
      tableBody.innerHTML = "<tr><td colspan='7'>❌ Error loading orders.</td></tr>";
      onError("Error loading orders for authorisation.");
    }
  } // <-- end loadOrdersForUser
} // <-- end setupAuthorisationUI

// boot
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/api/me", { credentials: "same-origin" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const user = await res.json();

    const heading = document.getElementById("user-heading");
    if (heading) heading.textContent = `${user.username}, here are your authorisations:`;

    await setupAuthorisationUI({
      user,
      mountPointId: "pending-body",
      onAuthorised: () => {},
      onError: (msg) => alert(msg),
    });
  } catch (e) {
    console.error(e);
    const body = document.getElementById("pending-body");
    if (body) {
      body.innerHTML = "<tr><td colspan='7'>❌ Could not load user session or orders.</td></tr>";
    }
  }
});
