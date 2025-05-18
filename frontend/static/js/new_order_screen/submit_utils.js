export async function submitOrder({
    currentOrderNumber,
    authThresholds, // array: [threshold_1, threshold_2, threshold_3, threshold_4]
    itemsList,
    updateGrandTotal,
    incrementOrderNumber,
    logToServer,
    setCurrentOrderId
}) {
    console.log('submitOrder triggered');
    await logToServer('INFO', 'submitOrder started');

    const requesterId = document.getElementById('requester_id').value;
    const supplierId = document.getElementById('supplier_id').value;
    const noteToSupplier = document.getElementById('note_to_supplier').value;

    if (!requesterId || !supplierId) {
        await logToServer('ERROR', 'Missing required fields', { requesterId, supplierId });
        alert('Please fill in all required fields (Requester, Supplier)');
        return;
    }

    const items = Array.from(document.querySelectorAll('#items-body tr')).map(row => {
        const itemCode = row.querySelector('.item-code')?.value;
        const itemDescription = itemsList.find(i => i.item_code === itemCode)?.item_description || '';
        const project = row.querySelector('.project')?.value;
        const qtyOrdered = parseFloat(row.querySelector('.qty-ordered')?.value) || 0;
        const price = parseFloat(row.querySelector('.price')?.value) || 0;

        if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {
            throw new Error('All items must have a valid item code, project, quantity, and price');
        }

        return {
            item_code: itemCode,
            item_description: itemDescription,
            project,
            qty_ordered: qtyOrdered,
            price
        };
    });

    const total = updateGrandTotal();

    // --- Determine status and band ---
    let status = "Pending";
    let authBandRequired = null;

    for (let i = 0; i < authThresholds.length; i++) {
        if (total > authThresholds[i]) {
            status = "Awaiting Authorisation";
            authBandRequired = i + 1;
        } else {
            break;
        }
    }

    const orderData = {
        order_number: currentOrderNumber,
        total,
        order_note: "",
        note_to_supplier: noteToSupplier,
        requester_id: parseInt(requesterId),
        supplier_id: parseInt(supplierId),
        status,
        ...(authBandRequired ? { auth_band_required: authBandRequired } : {}),
        items
    };

    try {
        const res = await fetch('/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });

        if (!res.ok) {
            const errorText = await res.text();
            await logToServer('ERROR', 'Failed to submit order', { status: res.status, errorText });
            throw new Error(`Failed to submit order: ${res.status} - ${errorText}`);
        }

        const data = await res.json();
        if (data.message === "Order created successfully") {
            setCurrentOrderId(data.order_id);

            const newOrderNumber = await incrementOrderNumber(currentOrderNumber);

            await logToServer('INFO', 'Order submitted and order number incremented', {
                orderNumber: newOrderNumber,
                orderId: data.order_id
            });

            alert('✅ Order submitted successfully!');
            document.getElementById('requester_id').value = '';
            document.getElementById('supplier_id').value = '';
            document.getElementById('note_to_supplier').value = '';
            document.getElementById('items-body').innerHTML = '';
        } else {
            await logToServer('ERROR', 'Unexpected response in submitOrder', { response: data.message });
            throw new Error(`Unexpected response: ${data.message}`);
        }
    } catch (error) {
        console.error('Order submission failed:', error.message);
        await logToServer('ERROR', 'Order submission failed', { error: error.message });
        alert(`❌ Order submission failed: ${error.message}`);
    }
}
