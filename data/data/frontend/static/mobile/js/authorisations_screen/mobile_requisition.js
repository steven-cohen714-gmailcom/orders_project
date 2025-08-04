// File: frontend/static/mobile/js/mobile_requisition.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("requisition-form");
  const messageBox = document.getElementById("message");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageBox.textContent = "";

    const description = document.getElementById("description").value.trim();
    const quantity = parseFloat(document.getElementById("quantity").value);
    const note = document.getElementById("note").value.trim();

    if (!description || isNaN(quantity) || quantity <= 0) {
      messageBox.textContent = "Please provide a valid description and quantity.";
      return;
    }

    try {
      const res = await fetch("/mobile_requisition/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ description, quantity, note }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to submit");

      form.reset();
      messageBox.textContent = "✅ Requisition submitted successfully.";
    } catch (err) {
      messageBox.textContent = `❌ ${err.message}`;
    }
  });
});
