export function escapeHTML(s='') {
  return String(s).replace(/[&<>"'`=\/]/g, c =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;','/':'&#x2F;','`':'&#x60;','=':'&#x3D;'}[c])
  );
}

export function formatCurrency(n) {
  const v = Number(n) || 0;
  return v.toLocaleString('en-ZA', { style: 'currency', currency: 'ZAR', minimumFractionDigits: 2 });
}

export function formatYMD(d) {
  if (!d) return '';
  const x = new Date(d);
  if (Number.isNaN(x.getTime())) return '';
  const y = x.getFullYear();
  const m = String(x.getMonth()+1).padStart(2,'0');
  const day = String(x.getDate()).padStart(2,'0');
  return `${y}-${m}-${day}`;
}

export async function logToServer(message, details = {}, level = 'INFO') {
  try {
    await fetch('/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({ message, details, level })
    });
  } catch (e) {
    // Don't throw from logging; fall back to console
    try { console[level?.toLowerCase?.()]?.('[client-log]', message, details); }
    catch { console.log('[client-log]', message, details); }
  }
}
