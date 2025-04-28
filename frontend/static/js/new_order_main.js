import { debounce, later, loadDropdowns, loadOrderNumber, addRow, updateTotal, updateGrandTotal, deleteRow, itemsList, projectsList, rowCount, currentOrderNumber } from '/static/js/new_order_utils.js';   
import { showOrderNoteModal, showSupplierNoteModal } from '/static/js/new_order_modals.js';

async function previewOrder() {   
  console.log('previewOrder called');   
  const orderNumber = document.getElementById('order-number').textContent;   
  const supplierId = document.getElementById('supplier_id').value;   
  const noteToSupplier = document.getElementById('note_to_supplier').value;

  console.log('Collected data:', { orderNumber, supplierId, noteToSupplier });

  if (!orderNumber || !supplierId) {   
      alert('Please fill in all required fields (Order Number, Supplier)');   
      return;   
  }

  const items = Array.from(document.querySelectorAll('#items-body tr')).map(row => {   
      const itemCode = row.querySelector('.item-code')?.value || row.cells[0].querySelector('select')?.value;   
      const itemDescription = itemsList.find(i => i.item_code === itemCode)?.item_description || '';   
      const project = row.querySelector('.project')?.value || row.cells[1].querySelector('select')?.value;   
      const qtyOrdered = parseFloat(row.querySelector('.qty-ordered')?.value || row.cells[2].querySelector('input')?.value) || 0;   
      const price = parseFloat(row.querySelector('.price')?.value || row.cells[3].querySelector('input')?.value) || 0;

      if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {   
          throw new Error('All items must have a valid item code, project, quantity, and price');   
      }

      return { item_code: itemCode, item_description: itemDescription, project, qty_ordered: qtyOrdered, price };   
  });

  console.log('Items:', items);

  if (items.length === 0) {   
      alert('Please add at least one item to the order');   
      return;   
  }

  const total = items.reduce((sum, item) => sum + (item.qty_ordered * item.price), 0);

  const payload = {   
      order_number: orderNumber,   
      supplier_id: parseInt(supplierId),   
      note_to_supplier: noteToSupplier,   
      items,   
      total,   
      business_details: {   
          company_name: "Universal Recycling Company Pty Ltd",   
          address_line1: "123 Industrial Road",   
          address_line2: "Unit 4",   
          city: "Cape Town",   
          province: "Western Cape",   
          postal_code: "8001",   
          telephone: "+27 21 555 1234",   
          vat_number: "VAT123456789"   
      }   
  };

  console.log('Sending payload:', payload);

  try {   
      const res = await fetch('/orders/generate_pdf', {   
          method: 'POST',   
          headers: { 'Content-Type': 'application/json' },   
          body: JSON.stringify(payload)   
      });

      console.log(`Response status: ${res.status}`);

      if (!res.ok) {   
          const errorText = await res.text();   
          throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);   
      }

      const contentType = res.headers.get('content-type');   
      console.log('Content-Type:', contentType);

      if (contentType && contentType.includes('application/pdf')) {   
          const blob = await res.blob();   
          console.log('Blob size:', blob.size);

          const modal = document.createElement('div');   
          modal.style.position = 'fixed';   
          modal.style.top = '0';   
          modal.style.left = '0';   
          modal.style.width = '100vw';   
          modal.style.height = '100vh';   
          modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';   
          modal.style.display = 'flex';   
          modal.style.alignItems = 'center';   
          modal.style.justifyContent = 'center';   
          modal.style.zIndex = '9999';

          const inner = document.createElement('div');   
          inner.style.backgroundColor = 'white';   
          inner.style.padding = '1rem';   
          inner.style.borderRadius = '8px';   
          inner.style.width = '90%';   
          inner.style.maxWidth = '800px';   
          inner.style.height = '80vh';   
          inner.style.display = 'flex';   
          inner.style.flexDirection = 'column';

          const iframe = document.createElement('iframe');   
          iframe.src = URL.createObjectURL(blob);   
          iframe.style.width = '100%';   
          iframe.style.height = '100%';   
          iframe.style.border = 'none';   
          inner.appendChild(iframe);

          const closeBtn = document.createElement('button');   
          closeBtn.textContent = 'Close';   
          closeBtn.style.marginTop = '1rem';   
          closeBtn.style.padding = '0.5rem 1rem';   
          closeBtn.style.cursor = 'pointer';   
          closeBtn.style.alignSelf = 'center';   
          closeBtn.onclick = () => document.body.removeChild(modal);   
          inner.appendChild(closeBtn);

          modal.appendChild(inner);   
          document.body.appendChild(modal);

          console.log('PDF displayed in modal');   
      } else {   
          const data = await res.json();   
          alert(`Unexpected response: ${JSON.stringify(data)}`);   
      }   
  } catch (error) {   
      console.error('Error generating PDF:', error);   
      alert(`Error generating PDF: ${error.message}`);   
  }   
}

async function submitOrder() {   
  console.log('debouncedSubmitOrder triggered');   
  const requesterId = document.getElementById('requester_id').value;   
  const supplierId = document.getElementById('supplier_id').value;   
  const noteToSupplier = document.getElementById('note_to_supplier').value;

  console.log('Submitting order with:', { requester_id: requesterId, supplier_id: supplierId, note_to_supplier: noteToSupplier });

  if (!requesterId || !supplierId) {   
      alert('Please fill in all required fields (Requester, Supplier)');   
      return;   
  }

  const items = Array.from(document.querySelectorAll('#items-body tr')).map(row => {   
      const itemCode = row.querySelector('.item-code')?.value || row.cells[0].querySelector('select')?.value;   
      const itemDescription = itemsList.find(i => i.item_code === itemCode)?.item_description || '';   
      const project = row.querySelector('.project')?.value || row.cells[1].querySelector('select')?.value;   
      const qtyOrdered = parseFloat(row.querySelector('.qty-ordered')?.value || row.cells[2].querySelector('input')?.value) || 0;   
      const price = parseFloat(row.querySelector('.price')?.value || row.cells[3].querySelector('input')?.value) || 0;

      if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {   
          throw new Error('All items must have a valid item code, project, quantity, and price');   
      }

      return { item_code: itemCode, item_description: itemDescription, project, qty_ordered: qtyOrdered, price };   
  });

  console.log('Items:', items);

  if (items.length === 0) {   
      alert('Please add at least one item to the order');   
      return;   
  }

  console.log('Current Order Number:', currentOrderNumber);

  const orderData = {   
      order_number: currentOrderNumber,   
      requester_id: parseInt(requesterId),   
      supplier_id: parseInt(supplierId),   
      note_to_supplier: noteToSupplier,   
      items   
  };

  console.log('Order Data:', orderData);

  try {   
      const res = await fetch('/orders/', {   
          method: 'POST',   
          headers: { 'Content-Type': 'application/json' },   
          body: JSON.stringify(orderData)   
      });

      console.log(`Submit Response Status: ${res.status}`);

      if (!res.ok) {   
          const errorText = await res.text();   
          throw new Error(`Failed to submit order: ${res.status} - ${errorText}`);   
      }

      const data = await res.json();   
      console.log('Submit Response:', data);

      if (data.message === "Order created successfully") {   
          alert('✅ Order submitted successfully!');   
          // Reset the form to allow continued use
          document.getElementById('requester_id').value = '';
          document.getElementById('supplier_id').value = '';
          document.getElementById('note_to_supplier').value = '';
          document.getElementById('items-body').innerHTML = '';
          loadOrderNumber(); // Reload order number for the next order
      } else {   
          throw new Error(`Unexpected response: ${data.message}`);   
      }   
  } catch (error) {   
      console.error('Order submission failed:', error.message);   
      alert(`❌ Order submission failed: ${error.message}`);   
  }   
}

function setupEventListeners() {   
  const submitBtn = document.getElementById('submit-order');   
  if (submitBtn) {   
      console.log('Submit button exists:', !!submitBtn);   
      submitBtn.addEventListener('click', () => {   
          console.log('Submit button clicked');   
          debounce(submitOrder, 500)();   
      });   
  } else {   
      console.error('Submit button not found');   
  }

  document.getElementById('preview-order').addEventListener('click', previewOrder);

  document.getElementById('email-po').addEventListener('click', () => {   
      alert('Email functionality not implemented yet');   
  });

  document.getElementById('cancel-order').addEventListener('click', () => {   
      if (confirm('Are you sure you want to cancel?')) {   
          window.location.href = '/orders/pending_orders';   
      }   
  });

  document.getElementById('add-line').addEventListener('click', () => {   
      addRow();   
  });

  document.querySelectorAll('#items-body').forEach(tbody => {   
      tbody.addEventListener('change', (e) => {   
          if (e.target.matches('select[id^="item_code_"]')) {   
              const row = e.target.closest('tr');   
              const itemCode = e.target.value;   
              const selectedItem = itemsList.find(i => i.item_code === itemCode);   
              updateTotal(e.target);   
          }   
      });   
  });   
}

document.addEventListener('DOMContentLoaded', async () => {   
  console.log('Page loaded');   
  try {   
      await loadDropdowns();   
      console.log('Requester dropdown options:', document.getElementById('requester_id').options.length);   
      console.log('Supplier dropdown options:', document.getElementById('supplier_id').options.length);   
      setupEventListeners();   
  } catch (err) {   
      console.error('Initialization failed:', err.message);   
  }   
});