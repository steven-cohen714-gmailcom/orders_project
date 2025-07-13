// File: frontend/static/js/pending_requisitions.js
import { loadRequisitioners } from "./components/shared_filters.js";
import { showUploadAttachmentsModal, showViewAttachmentsModal, checkAttachments } from "./components/requisitions_attachment_modal.js";
import { showOrderNoteModal } from "./components/order_note_modal.js";
import { expandRequisitionItems } from "./components/expand_requisition_items.js";

console.log("📦 pending_requisitions.js loaded (rewritten for direct update)"); // Updated note

async function loadFiltersAndRequisitions() {
  try {
    await loadRequisitioners("filter-requisitioner");
    await loadRequisitions();
  } catch (err) {
    console.error("❌ Error loading filters:", err);
    document.getElementById("pending-requisition-body").innerHTML = `<tr><td colspan="5">Error loading filters: ${err.message}</td></tr>`;
  }
}

// Function to update a single row's status and disable the tick
function updateRequisitionRowStatus(rowElement, newStatus) {
    // Determine display status based on newStatus
    let displayStatus = "";
    if (newStatus === 'submitted') {
        displayStatus = "No Order Yet";
    } else if (newStatus === 'ordered') {
        displayStatus = "Order Placed";
    } else {
        displayStatus = escapeHTML(newStatus || "N/A");
    }

    // Update the status cell (assuming it's the 4th td, index 3)
    const statusCell = rowElement.children[3]; // Requisition Date, Requisition #, Requisitioner, Status (index 3)
    if (statusCell) {
        statusCell.textContent = displayStatus;
    }

    // Disable the green tick icon and update its title
    const convertedIcon = rowElement.querySelector(".converted-icon");
    if (convertedIcon) {
        convertedIcon.classList.add('disabled');
        convertedIcon.style.cursor = 'default';
        convertedIcon.title = 'Already converted';
    }
}


async function loadRequisitions() {
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;
  const requisitioner = document.getElementById("filter-requisitioner").value;
  const status = document.getElementById("filter-status").value;

  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);
  if (requisitioner && requisitioner !== "All") params.append("requisitioner", requisitioner);
  if (status && status !== "All") params.append("status", status);

  try {
    const res = await fetch(`/api/pending_requisitions?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();

    const tbody = document.getElementById("pending-requisition-body");
    tbody.innerHTML = "";

    if (data.requisitions && Array.isArray(data.requisitions) && data.requisitions.length > 0) {
      data.requisitions.forEach((req, index) => {
        const row = document.createElement("tr");
        row.dataset.requisitionId = req.id; // Store ID on the row for easy lookup

        const formattedDate = new Date(req.requisition_date).toLocaleDateString("en-ZA");
        const sanitizedNote = escapeHTML(req.requisition_note || "");

        let displayStatus = "";
        if (req.status === 'submitted') {
            displayStatus = "No Order Yet";
        } else if (req.status === 'ordered') {
            displayStatus = "Order Placed";
        } else {
            displayStatus = escapeHTML(req.status || "N/A");
        }

        const isConverted = req.status === 'ordered';
        const convertedTick = `<span class="converted-icon ${isConverted ? 'disabled' : ''}"
                                  title="${isConverted ? 'Already converted' : 'Mark as Converted'}"
                                  data-id="${req.id}"
                                  data-number="${req.requisition_number}"
                                  style="cursor: ${isConverted ? 'default' : 'pointer'};">✅</span>`;

        row.innerHTML = `
          <td>${formattedDate}</td>
          <td>${escapeHTML(req.requisition_number)}</td>
          <td>${escapeHTML(req.requisitioner)}</td>
          <td>${displayStatus}</td>
          <td>
            <span class="expand-icon" data-id="${req.id}">⬇️</span>
            ${convertedTick}
            <span class="note-icon" title="Edit Note" data-id="${req.id}" data-note="${sanitizedNote}" id="note-${index}">📝</span>
            <span class="clip-icon" title="View/Upload Attachments" data-id="${req.id}" data-number="${req.requisition_number}">📎</span>
          </td>
        `;

        tbody.appendChild(row);

        // Event Listeners
        row.querySelector(`#note-${index}`).addEventListener("click", (e) => {
          const target = e.target;
          showOrderNoteModal(sanitizedNote, req.id, (newNote) => {
            target.setAttribute("data-note", escapeHTML(newNote));
          });
        });

        row.querySelector(".clip-icon").addEventListener("click", async (e) => {
          const target = e.target;
          const id = parseInt(target.getAttribute("data-id"));
          const number = target.getAttribute("data-number");
          const has = await checkAttachments(number, "requisition");

          if (has) {
            showViewAttachmentsModal(id, number, null, null, "requisition");
          } else {
            showUploadAttachmentsModal(id, number, () => {
                checkAttachments(number, "requisition").then(newHas => {
                    if (newHas) target.classList.add("eye-icon");
                });
            }, "requisition");
          }
        });

        row.querySelector(".expand-icon").addEventListener("click", (e) => {
          expandRequisitionItems(row, req.id);
        });

        row.querySelector(".converted-icon").addEventListener("click", async (e) => {
          if (isConverted) return;
          const confirmConvert = confirm(`Convert requisition ${req.requisition_number} to an order?`);
          if (!confirmConvert) return;
          try {
            const res = await fetch(`/requisitions/api/mark_converted/${req.id}`, { method: "PUT" });
            if (!res.ok) {
                const errorText = await res.text();
                throw new Error(`HTTP ${res.status}: ${errorText}`);
            }
            const result = await res.json(); // Get the response from backend
            alert(`Requisition ${req.requisition_number} marked as converted and status updated to "Order Placed".`);

            // NEW: Directly update the row in the DOM instead of full reload
            updateRequisitionRowStatus(row, 'ordered'); // Pass the actual row element and the new status
            
            // If filters are active and this item should now be hidden, remove it from view
            // This is a more complex logic, for now, we only update status.
            // If the user has 'submitted' filter active, the 'ordered' item will still show.
            // A full reload might be desirable if filtering by status 'submitted' and converted items should disappear.
            // For now, let's just make the direct update work.
            if (document.getElementById("filter-status").value === "submitted") {
                 row.remove(); // Remove the row if the filter is "submitted"
            }


          } catch (err) {
            alert(`❌ Failed to convert requisition: ${err.message}`);
            console.error(err);
          }
        });
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="5">No requisitions found.</td></tr>`;
    }
  } catch (err) {
    console.error("❌ Error loading requisitions:", err);
    document.getElementById("pending-requisition-body").innerHTML = `<tr><td colspan="5">Error loading requisitions: ${err.message}</td></tr>`;
  }
}

function escapeHTML(str) {
  if (typeof str !== "string") return "";
  return str.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
}

function clearFilters() {
  document.getElementById("start-date").value = "";
  document.getElementById("end-date").value = "";
  document.getElementById("filter-requisitioner").value = "All";
  document.getElementById("filter-status").value = "All";
  loadRequisitions();
}

document.getElementById("run-btn").addEventListener("click", loadRequisitions);
document.getElementById("clear-btn").addEventListener("click", clearFilters);
document.addEventListener("DOMContentLoaded", loadFiltersAndRequisitions);

window.showOrderNoteModal = showOrderNoteModal;
window.showUploadAttachmentsModal = showUploadAttachmentsModal;
window.checkAttachments = checkAttachments;
window.showViewAttachmentsModal = showViewAttachmentsModal;