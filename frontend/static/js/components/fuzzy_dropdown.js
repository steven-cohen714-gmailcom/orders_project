// File: frontend/static/js/components/fuzzy_dropdown.js

/**
 * Create a fuzzy searchable dropdown using a single <select> tag and Tom Select.
 * Falls back to `name` if `description` is missing.
 *
 * @param {string} selectId - ID of the <select> element (e.g., "supplier_id")
 * @param {string} endpoint - API endpoint to fetch items (e.g., "/lookups/suppliers")
 */
export async function createFuzzyDropdown(selectId, endpoint) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error(`Failed to fetch from ${endpoint}`);

    const data = await response.json();
    const items = Array.isArray(data) ? data : data[Object.keys(data)[0]];

    console.log(`🔍 Fuzzy dropdown loaded for ${selectId}:`, items.slice(0, 3));

    const select = document.getElementById(selectId);
    if (!select) throw new Error(`Element with ID '${selectId}' not found`);

    // Clear existing options
    select.innerHTML = "";

    // Insert default blank option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select...";
    select.appendChild(defaultOption);

    // Populate options using description fallback
    items.forEach((item) => {
      const label = item.description || item.name || "(no label)";
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = label;
      select.appendChild(option);
    });

    // Initialize Tom Select
    new TomSelect(`#${selectId}`, {
      valueField: "value",
      labelField: "text",
      searchField: ["text"],
      maxOptions: 50,
      create: false,
      sortField: {
        field: "text",
        direction: "asc",
      },
    });
  } catch (err) {
    console.error("Fuzzy dropdown init failed:", err);
    alert(`❌ Could not load ${selectId} dropdown. See console for details.`);
  }
}
