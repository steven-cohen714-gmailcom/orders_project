export async function showMobilePDFModal(orderId) {
  // Remove existing modal if it exists
  const existing = document.getElementById("pdf-modal");
  if (existing) existing.remove();

  const modal = document.createElement("div");
  modal.id = "pdf-modal";
  modal.style.position = "fixed";
  modal.style.top = 0;
  modal.style.left = 0;
  modal.style.width = "100vw";
  modal.style.height = "100vh";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.85)";
  modal.style.zIndex = 9999;
  modal.style.display = "flex";
  modal.style.flexDirection = "column";

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "✖ Close";
  closeBtn.style.padding = "0.6rem 1.2rem";
  closeBtn.style.alignSelf = "flex-end";
  closeBtn.style.margin = "1rem";
  closeBtn.style.backgroundColor = "#ffffff";
  closeBtn.style.color = "#000";
  closeBtn.style.border = "none";
  closeBtn.style.borderRadius = "6px";
  closeBtn.style.fontSize = "1rem";
  closeBtn.style.cursor = "pointer";
  closeBtn.onclick = () => modal.remove();

  const iframe = document.createElement("iframe");
  iframe.style.flex = 1;
  iframe.style.width = "100%";
  iframe.style.border = "none";
  iframe.style.background = "white";

  try {
    const res = await fetch(`/orders/api/generate_pdf_for_order/${orderId}`);
    if (!res.ok) throw new Error("PDF fetch failed");
    const blob = await res.blob();
    const blobUrl = URL.createObjectURL(blob);
    iframe.src = blobUrl;
  } catch (err) {
    iframe.srcdoc = `<p style="color:white;text-align:center;margin-top:2rem;">❌ Failed to load PDF</p>`;
    console.error("❌ Error loading PDF:", err);
  }

  modal.appendChild(closeBtn);
  modal.appendChild(iframe);
  document.body.appendChild(modal);
}
