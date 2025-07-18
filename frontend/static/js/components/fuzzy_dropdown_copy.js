// File: frontend/static/js/components/fuzzy_dropdown.js

/**
 * Create a fuzzy searchable dropdown using a single <select> tag and Tom Select.
 * Supports item_code/item_description, project_code/project_name, or name fallback.
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
    select.innerHTML = "";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select...";
    select.appendChild(defaultOption);

    items.forEach((item) => {
      let label = "(no label)";
      let value = item.id;

      if ("item_code" in item && "item_description" in item) {
        label = `${item.item_code} - ${item.item_description}`;
        value = item.item_code;
      } else if ("project_code" in item && "project_name" in item) {
        label = `${item.project_code} - ${item.project_name}`;
        value = item.project_code;
      } else if ("name" in item) {
        label = item.name;
        value = item.id;
      }

      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      select.appendChild(option);
    });

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
