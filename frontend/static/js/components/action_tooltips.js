// File: frontend/static/js/components/action_tooltips.js

// Map CSS selectors to human-readable tooltips.
// Extend this list over time as you spot other icons.
const TOOLTIP_MAP = {
  ".view-btn":        "View order",
  ".note-icon":       "Edit order note",
  ".pdf-icon":        "View PDF",
  ".review-icon":     "Approve (set Pending)",
  ".hold-icon":       "Put On Hold",

  // Row expand / collapse (use any one of these selectors in your HTML)
  ".expand-icon":           "Expand order details",
  ".row-toggle":            "Expand order details",
  ".toggle-details":        "Expand order details",
  "button[data-action='expand']": "Expand order details",
  "span[data-action='expand']":   "Expand order details",

  ".attach-icon":     "Attachments",
  ".receive-icon":    "Receive items",
  ".authorise-icon":  "Authorise order",
  ".pay-icon":        "Mark as Paid",
  ".delete-icon":     "Delete",
  ".edit-user-icon":  "Edit user",
  ".save-user-icon":  "Save user",
};

function applyActionTooltips(root = document) {
  for (const [selector, text] of Object.entries(TOOLTIP_MAP)) {
    root.querySelectorAll(selector).forEach(el => {
      if (!el.getAttribute("title")) el.setAttribute("title", text);
    });
  }
}

// Initial run
document.addEventListener("DOMContentLoaded", () => applyActionTooltips());

// Keep tooltips applied for dynamically inserted rows (tables built by JS)
const mo = new MutationObserver(mutations => {
  for (const m of mutations) {
    for (const n of m.addedNodes) {
      if (n && n.nodeType === 1) applyActionTooltips(n); // ELEMENT_NODE
    }
  }
});
mo.observe(document.documentElement, { childList: true, subtree: true });

// Optional: expose for manual calls if needed
window.applyActionTooltips = applyActionTooltips;
