// File: test_items_dropdown/test_item_dropdown.js

async function loadDropdown() {
  try {
    const res = await fetch("/items");
    if (!res.ok) throw new Error("Failed to fetch items");

    const items = await res.json();
    const select = document.getElementById("item-select");
    select.innerHTML = "";

    const defaultOpt = document.createElement("option");
    defaultOpt.value = "";
    defaultOpt.textContent = "Select...";
    select.appendChild(defaultOpt);

    const options = items.map(i => ({
      value: i.id,
      text: `${i.item_code} - ${i.item_description}`
    }));

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
    console.error("Dropdown failed:", err);
    alert("Failed to load dropdown");
  }
}

document.addEventListener("DOMContentLoaded", loadDropdown);
