// File: frontend/static/js/components/pdf_modal.js

// Helper function to convert Blob to Base64
function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            // Remove the "data:application/pdf;base64," prefix
            const base64data = reader.result.split(',')[1];
            resolve(base64data);
        };
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

// Helper function to show a prompt for email and then attempt to send
// Now accepts orderId, orderNumber, pdfBlob, and an optional initialEmail
async function promptForEmailAndSend(orderId, orderNumber, pdfBlob, initialEmail = '') {
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
    emailPromptModal.style.zIndex = 10001; // Higher than PDF modal

    emailPromptModal.innerHTML = `
        <div style="background:white; padding:2rem; border-radius:8px; box-shadow:0 0 15px rgba(0,0,0,0.3); text-align:center;">
            <h3>Email Purchase Order ${orderNumber || ''}</h3>
            <p>Please confirm or enter the recipient's email address:</p>
            <input type="email" id="manual-supplier-email" placeholder="supplier@example.com" style="width:80%; padding:0.5rem; margin-bottom:1rem; border:1px solid #ccc; border-radius:4px;">
            <div style="display:flex; justify-content:center; gap:10px;">
                <button id="send-manual-email-btn" style="background:#28a745; color:white; padding:8px 15px; border:none; border-radius:4px; cursor:pointer;">Send Email</button>
                <button id="cancel-manual-email-btn" style="background:#ccc; color:black; padding:8px 15px; border:none; border-radius:4px; cursor:pointer;">Cancel</button>
            </div>
            <div style="margin-top:10px;">
                <input type="checkbox" id="save-email-checkbox">
                <label for="save-email-checkbox">Save email to supplier record (if order is saved)</label>
            </div>
        </div>
    `;
    document.body.appendChild(emailPromptModal);

    const manualEmailInput = document.getElementById("manual-supplier-email");
    manualEmailInput.value = initialEmail; // Pre-populate the email
    const sendManualEmailBtn = document.getElementById("send-manual-email-btn");
    const cancelManualEmailBtn = document.getElementById("cancel-manual-email-btn");
    const saveEmailCheckbox = document.getElementById("save-email-checkbox");

    // Disable "Save email" checkbox if order is not saved (no orderId)
    if (!orderId) {
        saveEmailCheckbox.disabled = true;
        saveEmailCheckbox.checked = false;
        saveEmailCheckbox.parentNode.style.opacity = "0.5";
        saveEmailCheckbox.parentNode.title = "Saving email to supplier is only available for saved orders.";
    }

    cancelManualEmailBtn.onclick = () => emailPromptModal.remove();

    sendManualEmailBtn.onclick = async () => {
        const email = manualEmailInput.value.trim();
        if (!email || !email.includes('@') || !email.includes('.')) {
            alert("Please enter a valid email address.");
            return;
        }

        try {
            const pdfBase64 = await blobToBase64(pdfBlob); // Convert PDF blob to Base64

            const payload = {
                pdf_base64: pdfBase64,
                order_number: orderNumber,
                recipient_email: email,
                order_id: orderId, // Will be null for new order previews
                save_email_to_supplier: saveEmailCheckbox.checked && !!orderId // Only save if orderId exists
            };

            const response = await fetch(`/email/send_pdf`, { // Call the new generic email endpoint
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to send email.");
            }

            const result = await response.json();
            alert("✅ Purchase order emailed successfully!");
            emailPromptModal.remove(); // Close prompt modal

            // Check if backend requested to update order_note (for new order previews)
            if (result.update_order_note && typeof window.updateOrderNoteForEmail === 'function') {
                window.updateOrderNoteForEmail(email, orderNumber);
            }
            
            // Close the main PDF modal and clean up
            const mainPdfModal = document.getElementById("pdf-modal");
            if (mainPdfModal && document.body.contains(mainPdfModal)) {
                document.body.removeChild(mainPdfModal);
            }
            URL.revokeObjectURL(pdfBlob); // Clean up Blob URL

        } catch (err) {
            console.error("Email failed with manual input:", err);
            alert(`❌ Failed to send email: ${err.message}`);
        }
    };
}


// MODIFIED: showPDFModal now accepts orderId and orderNumber (both optional)
// It also takes initialSupplierEmail (optional) to pre-populate the prompt
export function showPDFModal(blob, orderId = null, orderNumber = null, initialSupplierEmail = '') {
    // Remove existing modal if it exists (to prevent duplicates if opened rapidly)
    const existingModal = document.getElementById("pdf-modal");
    if (existingModal) existingModal.remove();

    const modal = document.createElement("div");
    modal.id = "pdf-modal"; // Assign an ID for easier targeting
    modal.style.position = "fixed";
    modal.style.top = 0;
    modal.style.left = 0;
    modal.style.width = "100%";
    modal.style.height = "100%";
    modal.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    modal.style.display = "flex";
    modal.style.alignItems = "center";
    modal.style.justifyContent = "center";
    modal.style.zIndex = 10000;

    const contentWrapper = document.createElement("div");
    contentWrapper.style.width = "80%";
    contentWrapper.style.height = "80%";
    contentWrapper.style.display = "flex";
    contentWrapper.style.flexDirection = "column";
    contentWrapper.style.backgroundColor = "white";
    contentWrapper.style.borderRadius = "8px";
    contentWrapper.style.boxShadow = "0 0 10px #fff";
    contentWrapper.style.overflow = "hidden";

    const headerBar = document.createElement("div");
    headerBar.style.display = "flex";
    headerBar.style.justifyContent = "flex-end";
    headerBar.style.alignItems = "center";
    headerBar.style.backgroundColor = "#f0f0f0";
    headerBar.style.padding = "8px 12px";

    const pdfURL = URL.createObjectURL(blob);
    const iframe = document.createElement("iframe");
    iframe.src = pdfURL;
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "none";

    // === 📧 Email Button ===
    const emailBtn = document.createElement("button");
    emailBtn.textContent = "📧 Email PDF";
    emailBtn.style.background = "#28a745";
    emailBtn.style.color = "#fff";
    emailBtn.style.border = "none";
    emailBtn.style.padding = "6px 12px";
    emailBtn.style.borderRadius = "4px";
    emailBtn.style.cursor = "pointer";
    emailBtn.style.marginRight = "8px";

    // MODIFIED: Email button is always enabled if orderNumber is provided (for display purposes)
    // The prompt will handle missing email addresses
    if (orderNumber) { // Check for orderNumber as it's always available for previews/saved orders
        emailBtn.disabled = false; 
        emailBtn.onclick = async () => {
            // Always prompt for email, pre-populating with initialSupplierEmail
            promptForEmailAndSend(orderId, orderNumber, blob, initialSupplierEmail);
        };
    } else {
        // If no orderNumber (shouldn't happen for POs, but for robustness)
        emailBtn.disabled = true;
        emailBtn.title = "Emailing is only available for purchase orders.";
        emailBtn.style.opacity = "0.5";
        emailBtn.style.cursor = "not-allowed";
    }

    // === Download Button ===
    const downloadBtn = document.createElement("button");
    downloadBtn.textContent = "Download PDF";
    downloadBtn.style.background = "#007bff";
    downloadBtn.style.color = "#fff";
    downloadBtn.style.border = "none";
    downloadBtn.style.padding = "6px 12px";
    downloadBtn.style.borderRadius = "4px";
    downloadBtn.style.cursor = "pointer";
    downloadBtn.onclick = () => {
        const link = document.createElement("a");
        link.href = pdfURL;
        const filename = orderNumber ? `PurchaseOrder_${orderNumber}.pdf` : "PurchaseOrder.pdf";
        link.download = filename;
        link.click();
    };

    const buttonGroup = document.createElement("div");
    buttonGroup.style.display = "flex";
    buttonGroup.style.alignItems = "center";
    buttonGroup.style.gap = "10px"; // adds spacing between buttons

    buttonGroup.appendChild(emailBtn);
    buttonGroup.appendChild(downloadBtn);

    const closeBtn = document.createElement("button");
    closeBtn.textContent = "✖";
    closeBtn.style.background = "transparent";
    closeBtn.style.border = "none";
    closeBtn.style.color = "#333";
    closeBtn.style.fontSize = "20px";
    closeBtn.style.cursor = "pointer";
    closeBtn.onclick = () => {
        if (document.body.contains(modal)) {
            document.body.removeChild(modal);
        }
        URL.revokeObjectURL(pdfURL); // Clean up the Blob URL
    };

    headerBar.appendChild(buttonGroup);
    headerBar.appendChild(closeBtn);

    // Close modal if clicking outside contentWrapper
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            if (document.body.contains(modal)) {
                document.body.removeChild(modal);
            }
            URL.revokeObjectURL(pdfURL);
        }
    });

    contentWrapper.appendChild(headerBar);
    contentWrapper.appendChild(iframe);
    modal.appendChild(contentWrapper);
    document.body.appendChild(modal);
}
