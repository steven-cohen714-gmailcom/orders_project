// File: test_items_dropdown/test_item_fuzzy_dropdown.js

export async function createFuzzyDropdown(selectId, endpoint) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error(`Failed to fetch from ${endpoint}`);

    const data = await response.json();
    const items = Array.isArray(data) ? data : data.items;

    const select = document.getElementById(selectId);
    if (!select) throw new Error(`Element with ID '${selectId}' not found`);

    // Clear existing options
    select.innerHTML = "";
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select...";
    select.appendChild(defaultOption);

    // Format dropdown options
    const options = items.map(item => {
      const label = `${item.item_code} - ${item.item_description}`;
      return {
        value: item.id,
        text: label,
      };
    });

    // Initialize TomSelect
    new TomSelect(select, {
      options,
      valueField: "value",
      labelField: "text",
      searchField: ["text"],
      maxOptions: 100,
      create: false,
      sortField: {
        field: "text",
        direction: "asc"
      }
    });

  } catch (err) {
    console.error("❌ Dropdown error:", err);
    alert(`Could not load dropdown: ${err.message}`);
  }
}
