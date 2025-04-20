export function attachSmartDateInput(id) {
  const input = document.getElementById(id);
  if (!input) return;

  input.setAttribute("type", "text");
  input.setAttribute("placeholder", "dd/mm/yyyy");
  input.setAttribute("maxlength", "10");
  input.setAttribute("inputmode", "numeric");
  input.style.fontFamily = "monospace";

  input.addEventListener("input", () => {
    const cursorPos = input.selectionStart;
    let value = input.value.replace(/\D/g, "").slice(0, 8);
    let formatted = "";

    if (value.length > 2) {
      formatted += value.substr(0, 2) + "/";
      if (value.length > 4) {
        formatted += value.substr(2, 2) + "/";
        formatted += value.substr(4, 4);
      } else {
        formatted += value.substr(2);
      }
    } else {
      formatted = value;
    }

    input.value = formatted;

    // Adjust and restore cursor position
    const slashesBefore = (formatted.slice(0, cursorPos).match(/\//g) || []).length;
    const rawCursorPos = cursorPos - slashesBefore;
    let newCursorPos = rawCursorPos;

    if (rawCursorPos > 1) newCursorPos += 1;
    if (rawCursorPos > 3) newCursorPos += 1;
    input.setSelectionRange(newCursorPos, newCursorPos);
  });

  input.addEventListener("keydown", (e) => {
    const pos = input.selectionStart;
    const val = input.value;

    if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
      e.preventDefault();
      let newPos = pos;

      if (e.key === "ArrowRight") {
        newPos = pos === 2 || pos === 5 ? pos + 2 : pos + 1;
      } else {
        newPos = pos === 3 || pos === 6 ? pos - 2 : pos - 1;
      }

      newPos = Math.max(0, Math.min(newPos, val.length));
      input.setSelectionRange(newPos, newPos);
    }

    const allowed = [
      "Backspace", "Tab", "ArrowLeft", "ArrowRight", "Delete", "Home", "End", "Enter"
    ];
    if (!/^\d$/.test(e.key) && !allowed.includes(e.key)) {
      e.preventDefault();
    }
  });
}
