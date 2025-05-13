// File: frontend/static/js/components/pdf_modal.js

export function showPDFModal(blob) {
    const modal = document.createElement("div");
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
    emailBtn.onclick = async () => {
        const orderId = window.currentOrderIdForPDF;
        if (!orderId) return alert("Order ID not available");

        try {
            const response = await fetch(`/orders/email_purchase_order/${orderId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include"
            });

            if (!response.ok) {
                const error = await response.text();
                throw new Error(error);
            }

            alert("✅ Purchase order emailed successfully.");
        } catch (err) {
            console.error("Email failed:", err);
            alert("❌ Failed to send email. See console for details.");
        }
    };

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
        const filename = window.currentOrderNumberForPDF || "PurchaseOrder.pdf";
        link.download = filename;
        link.click();
    };

    const buttonGroup = document.createElement("div");
    buttonGroup.style.display = "flex";
    buttonGroup.style.alignItems = "center";
    buttonGroup.style.gap = "10px"; // ← KEY: adds spacing between buttons

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
        document.body.removeChild(modal);
        URL.revokeObjectURL(pdfURL);
    };

    headerBar.appendChild(buttonGroup);
    headerBar.appendChild(closeBtn);

    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
            URL.revokeObjectURL(pdfURL);
        }
    });

    contentWrapper.appendChild(headerBar);
    contentWrapper.appendChild(iframe);
    modal.appendChild(contentWrapper);
    document.body.appendChild(modal);
}
