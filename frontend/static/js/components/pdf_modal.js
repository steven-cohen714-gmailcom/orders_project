// File: frontend/static/js/components/pdf_modal.js

export function showPDFModal(blob) {
    // Create the modal overlay
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

    // Modal content container
    const contentWrapper = document.createElement("div");
    contentWrapper.style.width = "80%";
    contentWrapper.style.height = "80%";
    contentWrapper.style.display = "flex";
    contentWrapper.style.flexDirection = "column";
    contentWrapper.style.backgroundColor = "white";
    contentWrapper.style.borderRadius = "8px";
    contentWrapper.style.boxShadow = "0 0 10px #fff";
    contentWrapper.style.overflow = "hidden";

    // Header bar for buttons
    const headerBar = document.createElement("div");
    headerBar.style.display = "flex";
    headerBar.style.justifyContent = "space-between";
    headerBar.style.alignItems = "center";
    headerBar.style.backgroundColor = "#f0f0f0";
    headerBar.style.padding = "8px 12px";

    // Create the iframe to display PDF
    const iframe = document.createElement("iframe");
    const pdfURL = URL.createObjectURL(blob);
    iframe.src = pdfURL;
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "none";

    // Download button
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

        // Use dynamic name if set, fallback to "PurchaseOrder.pdf"
        const filename = window.currentOrderNumberForPDF || "PurchaseOrder.pdf";
        link.download = filename;
        link.click();
    };

    // Close button
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

    // Append buttons to header bar
    headerBar.appendChild(downloadBtn);
    headerBar.appendChild(closeBtn);

    // Close modal on background click
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
            URL.revokeObjectURL(pdfURL);
        }
    });

    // Assemble modal
    contentWrapper.appendChild(headerBar);
    contentWrapper.appendChild(iframe);
    modal.appendChild(contentWrapper);
    document.body.appendChild(modal);
}
