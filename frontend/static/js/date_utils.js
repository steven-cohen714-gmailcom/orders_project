export function setDateInputFormat(inputId) {
  const display = document.getElementById(`${inputId}-display`);
  const hidden = document.getElementById(inputId);

  if (!display || !hidden) return;

  display.addEventListener("click", () => hidden.showPicker());

  hidden.addEventListener("change", () => {
    const date = new Date(hidden.value);
    if (!isNaN(date)) {
      const formatted = date.toLocaleDateString("en-GB");
      display.value = formatted;
    } else {
      display.value = "";
    }
  });

  // Init with current value if present
  if (hidden.value) {
    const date = new Date(hidden.value);
    if (!isNaN(date)) {
      display.value = date.toLocaleDateString("en-GB");
    }
  }
}
