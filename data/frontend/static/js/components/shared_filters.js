// File: frontend/static/js/components/shared_filters.js

export async function loadRequesters(selectId) {
  try {
    const res = await fetch("/lookups/requesters");
    const data = await res.json();
    const select = document.getElementById(selectId);
    if (!select) return;

    select.innerHTML = '<option value="All">All</option>';
    data.requesters.forEach(r => {
      const opt = document.createElement("option");
      opt.value = r.name;
      opt.textContent = r.name;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error(`❌ Failed to load requesters for ${selectId}:`, err);
  }
}

export async function loadSuppliers(selectId) {
  try {
    const res = await fetch("/lookups/suppliers");
    const data = await res.json();
    const select = document.getElementById(selectId);
    if (!select) return;

    select.innerHTML = '<option value="All">All</option>';
    data.suppliers.forEach(s => {
      const opt = document.createElement("option");
      opt.value = s.name;
      opt.textContent = s.name;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error(`❌ Failed to load suppliers for ${selectId}:`, err);
  }
}

export async function loadRequisitioners(selectId) {
  try {
    const res = await fetch("/lookups/requisitioners");
    // Capture the JSON response once.
    const data = await res.json();

    if (!res.ok) {
      // Use the already parsed 'data' for error details if response was not ok.
      console.error(`❌ Backend error fetching requisitioners (HTTP ${res.status}):`, data);
      throw new Error(JSON.stringify(data.detail || data.message || "Unknown error from server."));
    }
    
    const select = document.getElementById(selectId);
    if (!select) return;

    select.innerHTML = '<option value="All">All</option>';
    // The backend's /lookups/requisitioners GET endpoint should now return a list directly.
    if (Array.isArray(data)) { // Check if data is an array before forEach
      data.forEach(r => {
        const opt = document.createElement("option");
        opt.value = r.id; // Use r.id as value if the backend is returning Requisitioner objects
        opt.textContent = r.name;
        select.appendChild(opt);
      });
    } else {
      console.error("❌ Expected an array of requisitioners, but received:", data);
      throw new Error("Invalid data format from server for requisitioners.");
    }

  } catch (err) {
    console.error(`❌ Failed to load requisitioners for ${selectId}:`, err);
    alert(`❌ Failed to load requisitioners for filter-requisitioner: ${err.message}`);
  }
}