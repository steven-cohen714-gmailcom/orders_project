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

    // Create the iframe to display PDF
    const iframe = document.createElement("iframe");
    iframe.src = URL.createObjectURL(blob);
    iframe.style.width = "80%";
    iframe.style.height = "80%";
    iframe.style.border = "none";
    iframe.style.backgroundColor = "white";
    iframe.style.boxShadow = "0 0 10px #fff";
    iframe.style.borderRadius = "8px";

    // Close modal on click outside iframe
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
            URL.revokeObjectURL(iframe.src);
        }
    });

    modal.appendChild(iframe);
    document.body.appendChild(modal);
}
