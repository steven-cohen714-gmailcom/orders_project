// File: frontend/static/js/components/fuzzy_dropdown.js

export async function createFuzzyDropdown(selectId, endpoint) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error(`Failed to fetch from ${endpoint}`);

    const data = await response.json();
    const items = Array.isArray(data) ? data : data[Object.keys(data)[0]];
    console.log(`[${selectId}] fetched ${items.length} items:`, items);

    const select = document.getElementById(selectId);
    if (!select) throw new Error(`Element with ID '${selectId}' not found`);
    select.innerHTML = "";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select...";
    select.appendChild(defaultOption);

    const options = items.map((item) => {
      let label = "(no label)";
      let value = item.id || "";

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

      return {
        value,
        text: label,
        item_code: item.item_code || "",
        item_description: item.item_description || "",
        project_code: item.project_code || "",
        project_name: item.project_name || "",
        name: item.name || "",
        description: item.description || ""
      };
    });

    new TomSelect(select, {
      options,
      valueField: "value",
      labelField: "text",
      searchField: [
        "text",
        "name",
        "item_code",
        "item_description",
        "project_code",
        "project_name"
      ],
      maxOptions: 50,
      create: false,
      sortField: {
        field: "text",
        direction: "asc"
      }
    });
  } catch (err) {
    console.error(`❌ Fuzzy dropdown failed for ${selectId}:`, err);
    alert(`❌ Could not load ${selectId} dropdown. See console.`);
  }
}
