// Load requesters into a given select element
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
  
  // Load suppliers into a given select element
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
  