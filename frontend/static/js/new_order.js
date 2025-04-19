let itemsList = [];
let projectsList = [];

function updateGrandTotal() {
  let sum = 0;
  document.querySelectorAll(".line-total").forEach(cell => {
    sum += parseFloat(cell.textContent) || 0;
  });
  document.getElementById("grand-total").textContent = `R${sum.toFixed(2)}`;
}

function updateTotal(input) {
  const row = input.closest("tr");
  const qty = parseFloat(row.cells[3].querySelector("input").value) || 0;
  const price = parseFloat(row.cells[4].querySelector("input").value) || 0;
  row.cells[5].textContent = (qty * price).toFixed(2);
  updateGrandTotal();
}

function autoFillDescription(sel) {
  const desc = sel.selectedOptions[0]?.dataset.description ?? "";
  sel.closest("tr").querySelector("td:nth-child(2) input").value = desc;
}

function deleteRow(btn) {
  btn.closest("tr").remove();
  updateGrandTotal();
}

function addRow() {
  const tbody = document.getElementById("items-body");
  const row = tbody.insertRow();

  const itemOpts = itemsList.map(i =>
    `<option value="${i.item_code}" data-description="${i.item_description}">${i.item_code} — ${i.item_description}</option>`
  ).join("");

  const projOpts = projectsList.map(p =>
    `<option value="${p.project_code}">${p.project_code} — ${p.project_name}</option>`
  ).join("");

  row.innerHTML = `
    <td>
      <select onchange="autoFillDescription(this)">
        <option value="">Select</option>
        ${itemOpts}
      </select>
    </td>
    <td><input type="text" placeholder="Description"></td>
    <td>
      <select>
        <option value="">Select</option>
        ${projOpts}
      </select>
    </td>
    <td><input type="number" value="1" min="1" onchange="updateTotal(this)"></td>
    <td><input type="number" value="0" min="0" onchange="updateTotal(this)"></td>
    <td class="line-total">0.00</td>
    <td><button type="button" onclick="deleteRow(this)">❌</button></td>
  `;
  updateGrandTotal();
}

async function loadDropdowns() {
  try {
    const [supR, reqR, itmR, prjR, numR] = await Promise.all([
      fetch("/lookups/suppliers").then(r => r.json()),
      fetch("/lookups/requesters").then(r => r.json()),
      fetch("/lookups/items").then(r => r.json()),
      fetch("/lookups/projects").then(r => r.json()),
      fetch("/orders/next_order_number").then(r => r.json())
    ]);

    const supplierDropdown = document.getElementById("supplier");
    supplierDropdown.innerHTML = '<option value="">Select supplier</option>';
    supR.suppliers.forEach(s => {
      const opt = document.createElement("option");
      opt.value = s.id;
      opt.textContent = `${s.account_number} — ${s.name}`;
      supplierDropdown.appendChild(opt);
    });

    const requesterDropdown = document.getElementById("requester");
    requesterDropdown.innerHTML = '<option value="">Select requester</option>';
    reqR.requesters.forEach(r => {
      const opt = document.createElement("option");
      opt.value = r.id;
      opt.textContent = r.name;
      requesterDropdown.appendChild(opt);
    });

    itemsList = itmR.items || [];
    projectsList = prjR.projects || [];

    document.getElementById("order-number").value = numR.next_order_number || "ORD-????";
    document.getElementById("request-date").valueAsDate = new Date();

    addRow();
  } catch (err) {
    console.error("Lookup loading failed", err);
    alert("⚠️ Failed to load dropdowns. Check server or database.");
  }
}

function previewOrder() {
  const rd = document.getElementById("request-date").value;
  const rq = document.getElementById("requester").value;
  const sp = document.getElementById("supplier").value;
  const nt = document.querySelector("textarea[name='note_to_supplier']").value;

  const items = Array.from(document.querySelectorAll("#items-body tr"))
    .map(row => {
      const c = row.querySelectorAll("td");
      return {
        item_code: c[0].querySelector("select").value,
        item_description: c[1].querySelector("input").value,
        project: c[2].querySelector("select").value,
        qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
        price: parseFloat(c[4].querySelector("input").value) || 0
      };
    })
    .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

  alert("Preview:\n" + JSON.stringify({ request_date: rd, requester_id: rq, supplier_id: sp, note_to_supplier: nt, items }, null, 2));
}

async function submitOrder() {
  const rd = document.getElementById("request-date").value;
  const rqId = document.getElementById("requester").value;
  const spId = document.getElementById("supplier").value;
  const nt = document.querySelector("textarea[name='note_to_supplier']").value;
  const rows = document.querySelectorAll("#items-body tr");

  const items = Array.from(rows)
    .map(row => {
      const c = row.querySelectorAll("td");
      return {
        item_code: c[0].querySelector("select").value,
        item_description: c[1].querySelector("input").value,
        project: c[2].querySelector("select").value,
        qty_ordered: parseFloat(c[3].querySelector("input").value) || 0,
        price: parseFloat(c[4].querySelector("input").value) || 0
      };
    })
    .filter(i => i.item_code && i.item_description && i.project && i.qty_ordered > 0 && i.price > 0);

  if (!rd || !rqId || !spId || items.length === 0) {
    return alert("⚠️ Fill date, requester, supplier & at least one complete line.");
  }

  try {
    const res = await fetch("/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        request_date: rd,
        requester_id: rqId,
        supplier_id: spId,
        note_to_supplier: nt,
        items
      })
    });

    const data = await res.json();

    if (res.ok && data.message === "Order created successfully") {
      const orderNumber = data.order?.order_number || document.getElementById("order-number").value;
      alert(`✅ Order ${orderNumber} created.`);
      location.reload();
    } else {
      const detail = data.detail || data.message || "Unknown error.";
      alert(`❌ ${detail}`);
    }
  } catch (err) {
    console.error("Submit failed", err);
    alert("❌ Submission failed.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadDropdowns();
  document.getElementById("add-line").addEventListener("click", addRow);
  document.getElementById("preview-order").addEventListener("click", previewOrder);
  document.getElementById("submit-order").addEventListener("click", submitOrder);
});
