export function showOrderNoteModal(noteText, orderId) {
  const modal = document.createElement("div");
  modal.className = "note-modal";
  modal.style = `
    position: fixed;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background: white;
    border: 1px solid #ccc;
    padding: 2rem;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    z-index: 9999;
    font-family: Arial, sans-serif;
  `;

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "Close";
  closeBtn.style = "float:right; font-weight:bold; cursor:pointer;";
  closeBtn.onclick = () => document.body.removeChild(modal);

  const title = document.createElement("h3");
  title.textContent = "Order Note";

  const noteBox = document.createElement("div");
  noteBox.contentEditable = true;
  noteBox.textContent = noteText || "(No note)";
  noteBox.style = `
    margin-top: 1rem;
    white-space: pre-wrap;
    border: 1px solid #ddd;
    padding: 1rem;
    background: #f9f9f9;
    min-height: 100px;
  `;

  const saveBtn = document.createElement("button");
  saveBtn.textContent = "Save";
  saveBtn.style = "margin-top: 1rem; padding: 0.5rem 1rem; cursor: pointer;";
  saveBtn.onclick = async () => {
    const updatedNote = noteBox.textContent;
    try {
      const res = await fetch(`/orders/save_note/${orderId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_note: updatedNote })
      });
      if (!res.ok) throw new Error("Failed to save order note");
      alert("✅ Order note updated!");
      document.body.removeChild(modal);
    } catch (err) {
      console.error(err);
      alert("❌ Failed to update order note");
    }
  };

  modal.appendChild(closeBtn);
  modal.appendChild(title);
  modal.appendChild(noteBox);
  modal.appendChild(saveBtn);
  document.body.appendChild(modal);
}

export function showSupplierNoteModal(noteText) {
  const modal = document.createElement("div");
  modal.className = "note-modal";
  modal.style = `
    position: fixed;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background: white;
    border: 1px solid #ccc;
    padding: 2rem;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    z-index: 9999;
    font-family: Arial, sans-serif;
  `;

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "Close";
  closeBtn.style = "float:right; font-weight:bold; cursor:pointer;";
  closeBtn.onclick = () => document.body.removeChild(modal);

  const title = document.createElement("h3");
  title.textContent = "Note to Supplier";

  const noteBox = document.createElement("div");
  noteBox.textContent = noteText || "(No note)";
  noteBox.style = `
    margin-top: 1rem;
    white-space: pre-wrap;
    border: 1px solid #ddd;
    padding: 1rem;
    background: #f9f9f9;
    min-height: 100px;
  `;

  modal.appendChild(closeBtn);
  modal.appendChild(title);
  modal.appendChild(noteBox);
  document.body.appendChild(modal);
}