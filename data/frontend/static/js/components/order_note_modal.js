export function showOrderNoteModal(note, orderId, onSaveCallback) {
    const modal = createBaseModal();
    const title = document.createElement("h3");
    title.textContent = "Order Note";
    modal.inner.appendChild(title);
  
    const textarea = document.createElement("textarea");
    textarea.value = note;
    textarea.style.width = "100%";
    textarea.style.height = "150px";
    textarea.style.resize = "vertical";
    modal.inner.appendChild(textarea);
  
    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save";
    saveBtn.style.marginTop = "1rem";
    saveBtn.style.marginRight = "0.5rem";
    saveBtn.style.padding = "0.5rem 1rem";
    saveBtn.style.border = "none";
    saveBtn.style.cursor = "pointer";
    saveBtn.style.background = "#4CAF50";
    saveBtn.style.color = "white";
  
    saveBtn.onclick = async () => {
        const newNote = textarea.value;
        console.log(`Saving order note for order ${orderId}:`, newNote);
        try {
            const res = await fetch(`/orders/save_note/${orderId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ order_note: newNote })
            });

            console.log(`Update order note response status: ${res.status}`);
            if (!res.ok) {
                const errorText = await res.text();
                throw new Error(`Failed to update order note: ${res.status} - ${errorText}`);
            }
            const data = await res.json();
            console.log("Update order note response:", data);
            if (data.message !== "Order note updated successfully") {
                throw new Error(`Unexpected response: ${data.message}`);
            }
            alert("✅ Order note updated!");
            if (onSaveCallback) {
                onSaveCallback(newNote); // Call the callback to update the note in the DOM
            }
            document.body.removeChild(modal.container);
        } catch (err) {
            console.error("Error saving order note:", err.message);
            alert(`❌ Failed to save order note: ${err.message}`);
        }
    };
  
    modal.inner.appendChild(saveBtn);
  
    const closeBtn = document.createElement("button");
    closeBtn.textContent = "Close";
    closeBtn.style.marginTop = "1rem";
    closeBtn.style.padding = "0.5rem 1rem";
    closeBtn.style.border = "none";
    closeBtn.style.cursor = "pointer";
    closeBtn.style.background = "#ccc";
    closeBtn.onclick = () => document.body.removeChild(modal.container);
  
    modal.inner.appendChild(closeBtn);
  
    document.body.appendChild(modal.container);
  }
  
  export function showSupplierNoteModal(note) {
    console.log("Displaying supplier note:", note);
    const modal = createBaseModal();
    const title = document.createElement("h3");
    title.textContent = "Note to Supplier";
    modal.inner.appendChild(title);
  
    const noteDisplay = document.createElement("p");
    // Replace line breaks with <br> for HTML rendering
    const formattedNote = note ? note.replace(/\n/g, '<br>') : "Empty note";
    noteDisplay.innerHTML = formattedNote;
    modal.inner.appendChild(noteDisplay);
  
    const closeBtn = document.createElement("button");
    closeBtn.textContent = "Close";
    closeBtn.style.marginTop = "1rem";
    closeBtn.style.padding = "0.5rem 1rem";
    closeBtn.style.border = "none";
    closeBtn.style.cursor = "pointer";
    closeBtn.style.background = "#ccc";
    closeBtn.onclick = () => document.body.removeChild(modal.container);
  
    modal.inner.appendChild(closeBtn);
  
    document.body.appendChild(modal.container);
  }
  
  function createBaseModal() {
    const container = document.createElement("div");
    container.style.position = "fixed";
    container.style.top = "0";
    container.style.left = "0";
    container.style.width = "100vw";
    container.style.height = "100vh";
    container.style.backgroundColor = "rgba(0,0,0,0.5)";
    container.style.display = "flex";
    container.style.alignItems = "center";
    container.style.justifyContent = "center";
    container.style.zIndex = "9999";
  
    const inner = document.createElement("div");
    inner.style.backgroundColor = "white";
    inner.style.padding = "1.5rem";
    inner.style.borderRadius = "8px";
    inner.style.width = "90%";
    inner.style.maxWidth = "500px";
    inner.style.maxHeight = "80vh";
    inner.style.overflowY = "auto";
    inner.style.fontFamily = "Arial, sans-serif";
    inner.style.position = "relative";
  
    const close = document.createElement("button");
    close.textContent = "✖";
    close.style.position = "absolute";
    close.style.top = "10px";
    close.style.right = "10px";
    close.style.background = "none";
    close.style.border = "none";
    close.style.fontSize = "1.2rem";
    close.style.cursor = "pointer";
    close.onclick = () => document.body.removeChild(container);
  
    inner.appendChild(close);
    container.appendChild(inner);
  
    return { container, inner };
  }