// File: frontend/static/js/components/pdf_modal.js

// ---------- helpers ----------
function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64data = reader.result.split(",")[1]; // strip data: prefix
      resolve(base64data);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

// Prompt for email & send. Receives a cleanup() callback to close/revoke the viewer on success.
async function promptForEmailAndSend(orderId, orderNumber, pdfBlob, initialEmail = "", cleanup = null) {
  const emailPromptModal = document.createElement("div");
  emailPromptModal.style.position = "fixed";
  emailPromptModal.style.top = "0";
  emailPromptModal.style.left = "0";
  emailPromptModal.style.width = "100vw";
  emailPromptModal.style.height = "100vh";
  emailPromptModal.style.backgroundColor = "rgba(0,0,0,0.7)";
  emailPromptModal.style.display = "flex";
  emailPromptModal.style.alignItems = "center";
  emailPromptModal.style.justifyContent = "center";
  emailPromptModal.style.zIndex = 10001; // above the PDF modal

  emailPromptModal.innerHTML = `
    <div style="background:white; padding:2rem; border-radius:8px; box-shadow:0 0 15px rgba(0,0,0,0.3); text-align:center; max-width: 520px; width: 92vw;">
      <h3 style="margin-top:0;">Email Purchase Order ${orderNumber || ""}</h3>
      <p>Please confirm or enter the recipient's email address:</p>
      <input type="email" id="manual-supplier-email" placeholder="supplier@example.com"
             style="width:100%; padding:0.5rem; margin-bottom:1rem; border:1px solid #ccc; border-radius:4px;">
      <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap;">
        <button id="send-manual-email-btn" style="background:#28a745; color:white; padding:8px 15px; border:none; border-radius:4px; cursor:pointer;">
          Send Email
        </button>
        <button id="cancel-manual-email-btn" style="background:#ccc; color:black; padding:8px 15px; border:none; border-radius:4px; cursor:pointer;">
          Cancel
        </button>
      </div>
      <div style="margin-top:10px; text-align:left;">
        <label style="user-select:none; cursor:pointer;">
          <input type="checkbox" id="save-email-checkbox"> Save email to supplier record (if order is saved)
        </label>
      </div>
    </div>
  `;
  document.body.appendChild(emailPromptModal);

  const manualEmailInput = document.getElementById("manual-supplier-email");
  manualEmailInput.value = initialEmail || "";
  const sendManualEmailBtn = document.getElementById("send-manual-email-btn");
  const cancelManualEmailBtn = document.getElementById("cancel-manual-email-btn");
  const saveEmailCheckbox = document.getElementById("save-email-checkbox");

  if (!orderId) {
    saveEmailCheckbox.disabled = true;
    saveEmailCheckbox.checked = false;
    saveEmailCheckbox.parentNode.style.opacity = "0.5";
    saveEmailCheckbox.parentNode.title = "Saving email to supplier is only available for saved orders.";
  }

  cancelManualEmailBtn.onclick = () => emailPromptModal.remove();

  sendManualEmailBtn.onclick = async () => {
    const email = (manualEmailInput.value || "").trim();
    if (!email || !email.includes("@") || !email.includes(".")) {
      alert("Please enter a valid email address.");
      return;
    }

    try {
      const pdfBase64 = await blobToBase64(pdfBlob);

      const payload = {
        pdf_base64: pdfBase64,
        order_number: orderNumber,
        recipient_email: email,
        order_id: orderId, // null for preview-only
        save_email_to_supplier: saveEmailCheckbox.checked && !!orderId,
      };

      const response = await fetch(`/email/send_pdf`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to send email.");
      }

      const result = await response.json();
      alert("✅ Purchase order emailed successfully!");
      emailPromptModal.remove();

      if (result.update_order_note && typeof window.updateOrderNoteForEmail === "function") {
        window.updateOrderNoteForEmail(email, orderNumber);
      }

      // Close the main viewer & revoke the object URL
      if (typeof cleanup === "function") cleanup();
    } catch (err) {
      console.error("Email failed:", err);
      alert(`❌ Failed to send email: ${err.message}`);
    }
  };
}

// ---------- main modal ----------
export function showPDFModal(blob, orderId = null, orderNumber = null, initialSupplierEmail = "") {
  // Remove any existing modal to avoid duplicates
  const existing = document.getElementById("pdf-modal");
  if (existing) existing.remove();

  const modal = document.createElement("div");
  modal.id = "pdf-modal";
  modal.style.position = "fixed";
  modal.style.inset = "0";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
  modal.style.display = "flex";
  modal.style.alignItems = "center";
  modal.style.justifyContent = "center";
  modal.style.zIndex = 10000;

  const contentWrapper = document.createElement("div");
  contentWrapper.style.width = "min(1200px, 90vw)";
  contentWrapper.style.height = "min(95vh, 90vh)";
  contentWrapper.style.display = "flex";
  contentWrapper.style.flexDirection = "column";
  contentWrapper.style.backgroundColor = "white";
  contentWrapper.style.borderRadius = "10px";
  contentWrapper.style.boxShadow = "0 10px 30px rgba(0,0,0,0.35)";
  contentWrapper.style.overflow = "hidden"; // header hidden; viewer handles own scroll

  // Header bar
  const headerBar = document.createElement("div");
  headerBar.style.display = "flex";
  headerBar.style.justifyContent = "space-between";
  headerBar.style.alignItems = "center";
  headerBar.style.backgroundColor = "#f0f0f0";
  headerBar.style.padding = "8px 12px";
  headerBar.style.flex = "0 0 auto";

  const leftTitle = document.createElement("div");
  leftTitle.textContent = `Purchase Order ${orderNumber ?? orderId ?? ""}`;
  leftTitle.style.fontWeight = "600";

  const rightButtons = document.createElement("div");
  rightButtons.style.display = "flex";
  rightButtons.style.alignItems = "center";
  rightButtons.style.gap = "10px";

  const pdfURL = URL.createObjectURL(blob);

  // Email button (always available when we have an order number for display)
  const emailBtn = document.createElement("button");
  emailBtn.textContent = "📧 Email PDF";
  emailBtn.style.background = "#28a745";
  emailBtn.style.color = "#fff";
  emailBtn.style.border = "none";
  emailBtn.style.padding = "6px 12px";
  emailBtn.style.borderRadius = "6px";
  emailBtn.style.cursor = "pointer";
  if (orderNumber) {
    emailBtn.disabled = false;
    emailBtn.onclick = () => {
      // pass cleanup so we close + revoke on success
      promptForEmailAndSend(orderId, orderNumber, blob, initialSupplierEmail, cleanup);
    };
  } else {
    emailBtn.disabled = true;
    emailBtn.title = "Emailing is only available for purchase orders.";
    emailBtn.style.opacity = "0.5";
    emailBtn.style.cursor = "not-allowed";
  }

  // Download button
  const downloadBtn = document.createElement("button");
  downloadBtn.textContent = "Download PDF";
  downloadBtn.style.background = "#007bff";
  downloadBtn.style.color = "#fff";
  downloadBtn.style.border = "none";
  downloadBtn.style.padding = "6px 12px";
  downloadBtn.style.borderRadius = "6px";
  downloadBtn.style.cursor = "pointer";
  downloadBtn.onclick = () => {
    const link = document.createElement("a");
    link.href = pdfURL;
    link.download = orderNumber ? `PurchaseOrder_${orderNumber}.pdf` : "PurchaseOrder.pdf";
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  // Close (X)
  const closeBtn = document.createElement("button");
  closeBtn.textContent = "✖";
  closeBtn.style.background = "transparent";
  closeBtn.style.border = "none";
  closeBtn.style.color = "#333";
  closeBtn.style.fontSize = "20px";
  closeBtn.style.cursor = "pointer";
  closeBtn.title = "Close (Esc)";
  closeBtn.onclick = () => cleanup();

  rightButtons.appendChild(emailBtn);
  rightButtons.appendChild(downloadBtn);
  rightButtons.appendChild(closeBtn);

  headerBar.appendChild(leftTitle);
  headerBar.appendChild(rightButtons);

  // Viewer wrapper (prevents right-edge clipping; provides scrolling instead)
  const viewerWrap = document.createElement("div");
  viewerWrap.style.flex = "1 1 auto";
  viewerWrap.style.minHeight = "0";           // CRITICAL for flex children sizing
  viewerWrap.style.overflow = "auto";         // scroll, don't clip
  viewerWrap.style.background = "#fff";

  const iframe = document.createElement("iframe");
  iframe.src = pdfURL;
  iframe.type = "application/pdf";
  iframe.title = "PDF preview";
  iframe.style.width = "100%";
  iframe.style.height = "100%";
  iframe.style.border = "none";
  iframe.style.display = "block";             // avoid inline-gap quirks

  viewerWrap.appendChild(iframe);

  // Assemble
  contentWrapper.appendChild(headerBar);
  contentWrapper.appendChild(viewerWrap);
  modal.appendChild(contentWrapper);
  document.body.appendChild(modal);

  // Close when clicking outside content
  modal.addEventListener("click", (e) => {
    if (e.target === modal) cleanup();
  });

  // Esc to close
  const onKey = (e) => {
    if (e.key === "Escape") cleanup();
  };
  document.addEventListener("keydown", onKey);

  // Unified cleanup (removes modal and revokes object URL)
  function cleanup() {
    document.removeEventListener("keydown", onKey);
    if (document.body.contains(modal)) document.body.removeChild(modal);
    try {
      URL.revokeObjectURL(pdfURL);
    } catch (_) {} // ignore
  }
}
