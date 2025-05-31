// Logs messages to the server
export async function logToServer(level, message, details = {}) {
  try {
    await fetch("/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ level, message, details })
    });
  } catch (error) {
    console.error("Failed to log to server:", error);
  }
}

/**
 * Enables fuzzy search on the description part of a select element.
 * Assumes each <option> includes `data-description` for filtering.
 * 
 * @param {string} selectId - The ID of the <select> element.
 */
export function enableFuzzySearch(selectId) {
  const selectEl = document.getElementById(selectId);
  if (!selectEl || selectEl.tagName !== "SELECT") return;

  const originalOptions = Array.from(selectEl.options);

  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Search description...";
  input.style.marginBottom = "0.5rem";
  input.style.width = "100%";
  input.style.padding = "0.25rem";
  input.style.fontSize = "0.9rem";

  selectEl.parentNode.insertBefore(input, selectEl);

  input.addEventListener("input", () => {
    const query = input.value.toLowerCase();
    selectEl.innerHTML = "";

    const matched = originalOptions.filter(opt => {
      const desc = opt.dataset.description || opt.textContent;
      return desc.toLowerCase().includes(query);
    });

    matched.forEach(opt => selectEl.appendChild(opt));
  });

  selectEl.addEventListener("change", () => {
    input.value = "";
    input.dispatchEvent(new Event("input"));
  });
}

export async function populateDropdown(endpoint, selectId, hideDefault = false) {
  try {
    const res = await fetch(endpoint);
    const data = await res.json();
    const select = document.getElementById(selectId);
    if (!select) return;

    if (!hideDefault) {
      select.innerHTML = '<option value="">Select...</option>';
    } else {
      select.innerHTML = "";
    }

    const key = Object.keys(data)[0];
    const items = Array.isArray(data[key]) ? data[key] : data;

    items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item.id;
      opt.textContent = item.name;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error(`❌ Failed to load dropdown from ${endpoint}:`, err);
  }
}

