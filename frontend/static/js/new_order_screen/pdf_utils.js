// frontend/static/js/new_order_screen/pdf_utils.js

import { showPDFModal } from "../components/pdf_modal.js";

export async function previewOrder({ itemsList, updateGrandTotal, logToServer }) {
  console.log('previewOrder called');
  await logToServer('INFO', 'previewOrder started');

  const requesterId = document.getElementById('requester_id').value;
  const supplierId = document.getElementById('supplier_id').value;
  const noteToSupplier = document.getElementById('note_to_supplier').value;
  const orderNumber = document.getElementById('order-number').textContent;
  const createdDate = document.getElementById('request_date').value;
  const total = updateGrandTotal();

  if (!requesterId || !supplierId || !createdDate) {
    alert('Please fill in all required fields (Requester, Supplier, Date)');
    return;
  }

  const items = Array.from(document.querySelectorAll('#items-body tr')).map(row => {
    // MODIFIED: Read value directly from the select element, as TomSelect is temporarily disabled
    const itemCodeElement = row.querySelector('.item-code');
    const itemCode = itemCodeElement ? itemCodeElement.value : '';

    const projectElement = row.querySelector('.project');
    const project = projectElement ? projectElement.value : '';
    
    const qtyOrdered = parseFloat(row.querySelector('.qty-ordered')?.value) || 0;
    const price = parseFloat(row.querySelector('.price')?.value) || 0;
    
    // MODIFIED: Find itemDescription using the itemCode (which is now the value of the select)
    const itemDescription = itemsList.find(i => i.item_code === itemCode)?.item_description || '';

    if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {
      throw new Error('Each item must have a valid code, project, quantity, and price');
    }

    return {
      item_code: itemCode,
      item_description: itemDescription,
      project,
      qty_ordered: qtyOrdered,
      price
    };
  });

  if (!items.length) {
    alert("Please add at least one item to the order");
    return;
  }

  const payload = {
    order_number: orderNumber,
    created_date: createdDate,
    // MODIFIED: Get supplier and requester names from selected option text
    supplier_name: document.getElementById("supplier_id").selectedOptions[0]?.textContent || "",
    requester_name: document.getElementById("requester_id").selectedOptions[0]?.textContent || "",
    total,
    order_note: "",
    note_to_supplier: noteToSupplier,
    requester_id: parseInt(requesterId),
    supplier_id: parseInt(supplierId),
    items
  };

  try {
    const pdfRes = await fetch("/orders/api/preview_pdf_new_order", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!pdfRes.ok || !pdfRes.headers.get("content-type")?.includes("application/pdf")) {
      const err = await pdfRes.text();
      throw new Error(`Failed to generate PDF: ${pdfRes.status} - ${err}`);
    }

    const blob = await pdfRes.blob();
    if (!blob.size) throw new Error("Empty PDF file");

    // MODIFIED: Store the order number for the PDF download filename
    window.currentOrderNumberForPDF = orderNumber; 
    showPDFModal(blob);
    await logToServer('INFO', 'Preview PDF displayed (no DB write)');
  } catch (error) {
    console.error("Preview failed:", error);
    await logToServer('ERROR', 'PreviewOrder failed (no DB write)', { error: error.message });
    alert(`Error: ${error.message}`);
  }
}
