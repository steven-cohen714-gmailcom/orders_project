import { loadRequisitioners } from "./components/shared_filters.js";
import { showUploadAttachmentsModal, showViewAttachmentsModal, checkAttachments } from "./components/requisitions_attachment_modal.js";
import { showOrderNoteModal } from "./components/order_note_modal.js";
import { showPDFModal } from "./components/pdf_modal.js";

console.log("📦 pending_requisitions.js loaded");

async function loadFiltersAndRequisitions() {
  try {
    await loadRequisitioners("filter-requisitioner");
    await loadRequisitions();
  } catch (err) {
    console.error("❌ Error loading filters:", err);
    document.getElementById("pending-requisition-body").innerHTML = `<tr><td colspan="7">Error loading filters: ${err.message}</td></tr>`;
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

        const formattedDate = new Date(req.requisition_date).toLocaleDateString("en-ZA");
        const sanitizedNote = escapeHTML(req.requisition_note || "");
        const converted = req.converted_order_id ? "✅" : "";

        row.innerHTML = `
          <td>${formattedDate}</td>
          <td>${escapeHTML(req.requisition_number)}</td>
          <td>${escapeHTML(req.requisitioner)}</td>
          <td>${escapeHTML(req.project || "")}</td>
          <td>${escapeHTML(req.total_quantity || "")}</td>
          <td>${escapeHTML(req.description || "")}</td>
          <td>
            ${converted}
            <span class="pdf-icon" title="View PDF" data-id="${req.id}">📄</span>
            <span class="note-icon" title="Edit Note" data-id="${req.id}" data-note="${sanitizedNote}" id="note-${index}">📝</span>
            <span class="clip-icon" title="View/Upload Attachments" data-id="${req.id}" data-number="${req.requisition_number}">📎</span>
          </td>
        `;

        tbody.appendChild(row);

        row.querySelector(`#note-${index}`).addEventListener("click", (e) => {
          const target = e.target;
          showOrderNoteModal(sanitizedNote, req.id, (newNote) => {
            target.setAttribute("data-note", escapeHTML(newNote));
          });
        });

        row.querySelector(".clip-icon").addEventListener("click", async (e) => {
          const target = e.target;
          const id = target.getAttribute("data-id");
          const number = target.getAttribute("data-number");

          const has = await checkAttachments(number, "requisition"); // ✅ FIXED LINE

          if (has) {
            showViewAttachmentsModal(id, number, null, null, "requisition");
          } else {
            showUploadAttachmentsModal(id, number, () => {}, "requisition");
          }
        });

        row.querySelector(".pdf-icon").addEventListener("click", async () => {
          try {
            const response = await fetch(`/requisitions/api/generate_pdf/${req.id}`);
            if (!response.ok) throw new Error(`PDF generation failed with status ${response.status}`);
            const blob = await response.blob();
            showPDFModal(blob);
          } catch (err) {
            alert("❌ Could not generate PDF");
            console.error(err);
          }
        });
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="7">No requisitions found.</td></tr>`;
    }
  } catch (err) {
    console.error("❌ Error loading requisitions:", err);
    document.getElementById("pending-requisition-body").innerHTML = `<tr><td colspan="7">Error loading requisitions: ${err.message}</td></tr>`;
  }
}

function escapeHTML(str) {
  if (typeof str !== "string") return "";
  return str.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
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
window.showPDFModal = showPDFModal;
