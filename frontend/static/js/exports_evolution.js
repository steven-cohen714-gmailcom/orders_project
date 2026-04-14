// File: frontend/static/js/exports_evolution.js
(function () {
  const $  = (id) => document.getElementById(id);
  const tbody = $("staging-body");

  const state = { rows: [], selected: new Set() };

  document.addEventListener("DOMContentLoaded", init);

  function ymd(d) { return new Date(d).toISOString().slice(0,10); }

  async function init() {
    // Sensible defaults (don’t override if the page already set them)
    if (!$("from-date").value) $("from-date").value = "2020-01-01";
    if (!$("to-date").value)   $("to-date").value   = ymd(new Date());

    $("btn-refresh").onclick = loadStaging;
    $("btn-export").onclick  = exportSelected;
    $("chk-all").onchange = (e) => {
      state.selected.clear();
      if (e.target.checked) state.rows.forEach(r => state.selected.add(r.order_item_id));
      render();
    };

    await loadStaging();
    await loadBatches();
  }

  async function loadStaging() {
    state.selected.clear();

    const params = new URLSearchParams();
    const v = (id) => $(id).value.trim();
    if (v("from-date"))        params.set("from_date", v("from-date"));
    if (v("to-date"))          params.set("to_date",   v("to-date"));
    if (v("filter-supplier"))  params.set("supplier",  v("filter-supplier"));
    if (v("filter-project"))   params.set("project",   v("filter-project"));
    if (v("filter-q"))         params.set("q",         v("filter-q"));
    params.set("limit", "1000");

    const res = await fetch("/evo/staging?" + params.toString());
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    state.rows = data.rows || [];
    render();
  }

  function render() {
    tbody.innerHTML = "";
    state.rows.forEach((r, idx) => {
      const checked = state.selected.has(r.order_item_id) ? "checked" : "";
      const tr = document.createElement("tr");
      tr.dataset.id = r.order_item_id;

      tr.innerHTML = `
        <td><input type="checkbox" class="row-cb" ${checked}></td>
        <td>${esc(r.item_code)}</td>
        <td>${inp(r.warehouse_code)}</td>
        <td>${inp(r.date, "text", 'pattern="\\d{4}/\\d{2}/\\d{2}"')}</td>
        <td>${inp(r.reference)}</td>
        <td>${inp(r.description)}</td>
        <td>${inp(num(r.qty_in), "number", 'step="0.01"')}</td>
        <td>${inp(num(r.qty_out), "number", 'step="0.01"')}</td>
        <td>${inp(r.transaction_code)}</td>
        <td>${inp(r.gl_contra_account)}</td>
        <td>${esc(r.project || "")}</td>
        <td>${esc(r.order_number || "")}</td>
        <td>${esc(r.supplier_name || "")}</td>
        <td><button class="row-del" title="remove from selection">✕</button></td>
      `;

      // selection toggle
      tr.querySelector(".row-cb").onchange = (e) => {
        if (e.target.checked) state.selected.add(r.order_item_id);
        else state.selected.delete(r.order_item_id);
      };

      // delete from current grid view
      tr.querySelector(".row-del").onclick = () => {
        state.rows.splice(idx, 1);
        state.selected.delete(r.order_item_id);
        render();
      };

      // bind edits
      const inputs = tr.querySelectorAll('input[type="text"], input[type="number"]');
      inputs[0].oninput = (e)=> r.warehouse_code    = e.target.value;
      inputs[1].oninput = (e)=> r.date              = e.target.value;
      inputs[2].oninput = (e)=> r.reference         = e.target.value;
      inputs[3].oninput = (e)=> r.description       = e.target.value;
      inputs[4].oninput = (e)=> r.qty_in            = parseFloat(e.target.value || 0);
      inputs[5].oninput = (e)=> r.qty_out           = parseFloat(e.target.value || 0);
      inputs[6].oninput = (e)=> r.transaction_code  = e.target.value;
      inputs[7].oninput = (e)=> r.gl_contra_account = e.target.value;

      tbody.appendChild(tr);
    });

    // reflect master checkbox
    $("chk-all").checked = state.rows.length > 0 && state.selected.size === state.rows.length;
  }

  async function exportSelected() {
    const chosen = state.selected.size
      ? state.rows.filter(r => state.selected.has(r.order_item_id))
      : state.rows.slice();

    if (!chosen.length) { alert("Nothing to export."); return; }

    // Validate required fields + In/Out rule
    const err = validate(chosen);
    if (err) { alert("Fix before export:\n" + err); return; }

    if (!confirm(`Export ${chosen.length} line(s) to Evolution?\n\nThis will FLAG those lines as exported.`)) return;

    const notes = $("export-notes") ? $("export-notes").value : "";

    const btn = $("btn-export");
    btn.disabled = true;
    const oldTxt = btn.textContent;
    btn.textContent = "Exporting…";

    try {
      const res = await fetch("/evo/export", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ rows: chosen, notes })
      });
      if (!res.ok) {
        const txt = await res.text();
        alert("Export failed: " + txt);
        return;
      }
      const payload = await res.json();
      alert(`Exported batch ${payload.batch_id} (${payload.row_count} rows)`);
      if (payload.download_url) window.location = payload.download_url;
      await loadStaging();
      await loadBatches();
    } finally {
      btn.disabled = false;
      btn.textContent = oldTxt;
    }
  }

  function validate(rows) {
    const problems = [];
    for (const r of rows) {
      const id = r.order_number || r.order_item_id;
      if (!r.item_code)           problems.push(`#${id}: missing Item Code`);
      if (!r.warehouse_code)      problems.push(`#${id}: missing Warehouse`);
      if (!r.date)                problems.push(`#${id}: missing Date (YYYY/MM/DD)`);
      if (!r.transaction_code)    problems.push(`#${id}: missing Txn Code`);
      if (!r.gl_contra_account)   problems.push(`#${id}: missing GL Contra`);
      const qi = Number(r.qty_in || 0), qo = Number(r.qty_out || 0);
      if ((qi > 0 && qo > 0) || (qi <= 0 && qo <= 0)) {
        problems.push(`#${id}: use either Qty In OR Qty Out (>0), not both/none`);
      }
    }
    return problems.length ? problems.join("\n") : "";
  }

  async function loadBatches() {
    const r = await fetch("/evo/batches?limit=10");
    if (!r.ok) return;
    const data = await r.json();
    const host = $("batches");
    host.innerHTML = `
      <table class="table">
        <thead><tr><th>Batch</th><th>Created</th><th>By</th><th>File</th><th>Rows</th><th></th></tr></thead>
        <tbody>
          ${(data.batches || []).map(b => `
            <tr>
              <td>${b.id}</td>
              <td>${esc(b.created_at || '')}</td>
              <td>${esc(b.created_by || '')}</td>
              <td>${esc(b.filename || '')}</td>
              <td style="text-align:right">${b.row_count || 0}</td>
              <td>${b.filename ? `<a href="/evo/batches/${b.id}/download">Download</a>` : ''}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>`;
  }

  // helpers
  function esc(s){ return (s ?? "").toString().replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
  function num(v){ const n = Number(v); return Number.isFinite(n) ? String(n) : ""; }
  function inp(val, type="text", attrs=""){ const safe = (val==null?"":String(val)).replaceAll('"',"&quot;"); return `<input type="${type}" value="${safe}" ${attrs}>`; }
})();
