// File: frontend/static/js/audit_trail_expand.js
// Relative Path: frontend/static/js/audit_trail_expand.js

export async function expandAuditTrailDetails(orderId, iconElement, detailContainer) {
  console.log(`Expanding Audit Trail details for order ID: ${orderId}`);

  if (!detailContainer) {
    console.error("expandAuditTrailDetails: detailContainer is undefined. Cannot proceed.");
    return;
  }

  // Toggle open/close
  const opening = detailContainer.style.display === "" || detailContainer.style.display === "none";
  detailContainer.style.display = opening ? "block" : "none";
  iconElement.textContent = opening ? "⬆️" : "⬇️";
  if (!opening) return;

  // If already loaded once, don't refetch
  if (detailContainer.dataset.loaded === "1") return;

  try {
    // ── Fetch all necessary data in parallel ───────────────────────────────
    const [itemsRes, logsRes, orderDetailsRes, auditHistoryRes] = await Promise.all([
      fetch(`/orders/api/order_items/${orderId}`),
      fetch(`/orders/api/receipt_logs/${orderId}`),
      fetch(`/orders/api/order_details_for_audit/${orderId}`),
      fetch(`/orders/api/order_audit_history/${orderId}`)
    ]);

    if (!itemsRes.ok || !logsRes.ok || !orderDetailsRes.ok || !auditHistoryRes.ok) {
      const itemsErr        = itemsRes.ok        ? "" : await itemsRes.text();
      const logsErr         = logsRes.ok         ? "" : await logsRes.text();
      const orderDetailsErr = orderDetailsRes.ok ? "" : await orderDetailsRes.text();
      const auditHistoryErr = auditHistoryRes.ok ? "" : await auditHistoryRes.text();
      throw new Error(
        `Fetch error: items ${itemsRes.status} (${itemsErr}), ` +
        `logs ${logsRes.status} (${logsErr}), ` +
        `order details ${orderDetailsRes.status} (${orderDetailsErr}), ` +
        `audit history ${auditHistoryRes.status} (${auditHistoryErr})`
      );
    }

    const items       = await itemsRes.json();
    const logsData    = await logsRes.json();
    const orderData   = await orderDetailsRes.json();
    let auditHistory  = await auditHistoryRes.json(); // Use let as we'll filter it
    const receiptLogs = logsData.logs || [];

    // --- Filtering out unwanted audit trail entries ---
    auditHistory = auditHistory.filter(entry => {
      // Exclude "Viewed PDF" unless it's related to emailing (email activity is captured by 'Emailed')
      if (entry.action === "Viewed PDF" && !(entry.details || "").toLowerCase().includes("emailed")) {
        return false;
      }
      // Exclude "Note Updated"
      if (entry.action === "Note Updated") {
        return false;
      }
      return true;
    });
    // ----------------------------------------------------

    // Map of receipt logs per order_item_id (kept if needed later)
    const logMap = {};
    for (const log of receiptLogs) {
      if (!log.order_item_id) continue;
      if (!logMap[log.order_item_id]) logMap[log.order_item_id] = [];
      logMap[log.order_item_id].push(log);
    }

    // Helper to render ZA date/time safely
    const formatDateTimeZA = (isoLike) => {
      if (!isoLike) return "N/A";
      const d = new Date(isoLike);
      if (isNaN(d.getTime())) return "N/A";
      return d.toLocaleString("en-ZA", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
      });
    };

    // Compute Created / Edited strings
    const createdStr = formatDateTimeZA(orderData?.created_date);

    // Oldest first for an easy "last entry = latest action"
    const sortedHistory = [...auditHistory].sort((a, b) => new Date(a.action_date) - new Date(b.action_date));
    const latestActionDate = sortedHistory.length ? sortedHistory[sortedHistory.length - 1].action_date : orderData?.created_date;
    const editedStr = formatDateTimeZA(latestActionDate);

    // Build HTML with a placeholder for meta (we set its textContent after .innerHTML)
    let contentHTML = `
      <div class="audit-meta" id="audit-meta-${orderId}" style="font-size:0.9rem; color:#555; margin:0.25rem 0 0.5rem;"></div>
      <div class="audit-events" style="margin-bottom: 1rem;">
        <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; table-layout: fixed;">
          <thead>
            <tr style="background:#f0f0f0; font-weight:bold;">
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">Activity</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">Date</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">User</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">Details</td>
            </tr>
          </thead>
          <tbody>
    `;

    if (auditHistory && auditHistory.length > 0) {
      // Sort audit history chronologically (oldest first)
      auditHistory.sort((a, b) => new Date(a.action_date) - new Date(b.action_date));

      auditHistory.forEach(entry => {
        const formattedDate = formatDateTimeZA(entry.action_date);
        const user     = entry.username || "Unknown";
        const activity = entry.action;

        let details = "";

        switch (entry.action) {
          case "Created":
            details = "Order created";
            break;
          case "Created as Draft":
            details = "Order saved as draft";
            break;
          case "Converted from Draft":
            details = `Order converted from draft (Draft ID: ${entry.details})`;
            break;
          case "Draft Updated":
            details = "Draft order updated";
            break;
          case "Authorised":
            details = "Order authorised";
            break;
          case "Reviewed":
            details = entry.details || "Reviewed";
            break;
          case "Received": {
            details = "Order received";
            let receivedItems = [];
            try {
              const detailsContent = (entry.details || "").replace("Order received: ", "");
              receivedItems = detailsContent ? JSON.parse(detailsContent) : [];
            } catch (e) {
              console.error("Error parsing received details:", e);
            }
            if (Array.isArray(receivedItems) && receivedItems.length > 0) {
              details += '<ul style="margin-top: 0.5rem; padding-left: 1.5rem;">';
              receivedItems.forEach(recItem => {
                const itemData  = items.find(i => i.id === recItem.item_id);
                const itemLabel = itemData
                  ? `${itemData.item_code} – ${itemData.item_description || ""}`
                  : "Unknown Item";
                details += `<li>${itemLabel}: ${recItem.received_qty} qty</li>`;
              });
              details += "</ul>";
            }
            break;
          }
          case "COD Payment recorded":
            details = entry.details || "COD payment recorded";
            break;
          case "Emailed": {
            const m = (entry.details || "").match(/emailed to ([\w.@-]+)/i);
            const email = m ? m[1] : "Unknown";
            const num = orderData && orderData.order_number ? orderData.order_number : orderId;
            details = `Purchase order ${num} emailed to ${email}`;
            break;
          }
          case "Deleted":
            details = "Order deleted";
            break;
          case "Viewed PDF":
            details = `PDF viewed: ${entry.details || ""}`;
            break;
          default:
            details = entry.details || "No details";
            break;
        }

        if (details) {
          const rowClass = activity === "Deleted" ? "audit-row-deleted" : "";
          contentHTML += `
            <tr class="${rowClass}">
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${activity}</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${formattedDate}</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${user}</td>
              <td style="text-align:left; padding: 0.5rem; border: 1px solid #ddd;">${details}</td>
            </tr>
          `;
        }
      });
    } else {
      contentHTML += `
        <tr>
          <td colspan="4" style="text-align:center; padding: 0.5rem; border: 1px solid #ddd;">
            No audit trail available for this order.
          </td>
        </tr>
      `;
    }

    contentHTML += `
          </tbody>
        </table>
      </div>
    `;

    // Inject HTML first…
    detailContainer.innerHTML = contentHTML;

    // …then set the meta line via textContent (prevents &#x2F; etc.)
    const metaEl = document.getElementById(`audit-meta-${orderId}`);
    if (metaEl) {
      metaEl.textContent = `Created: ${createdStr} · Edited: ${editedStr}`;
    }

    detailContainer.dataset.loaded = "1";
  } catch (error) {
    console.error("Failed to fetch audit trail details:", error);
    detailContainer.innerHTML = `<p style="color: red;">Error loading audit trail: ${escapeHtml(error.message)}</p>`;
  }
}

// Simple HTML escaper for error text and any dynamic strings we might echo
function escapeHtml(str) {
  if (typeof str !== "string") return String(str || "");
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
