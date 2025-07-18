// File: frontend/static/js/new_order_screen/submit_utils.js

export async function submitOrder({
  currentOrderNumber, // The order number of the order being submitted
  authThresholds,     // Authorization thresholds
  itemsList,          // List of items for description lookup
  updateGrandTotal,   // Function to get the current total
  logToServer,        // Logging utility
  setCurrentOrderId,  // Function to set the ID of the newly created final order
  paymentTerms,       // Payment terms for the order
  draftId             // Optional: ID of the draft order if finalizing a draft
}) {
  console.log("submitOrder triggered (finalizing order)");
  await logToServer("INFO", "submitOrder started (finalizing order)", { orderNumber: currentOrderNumber, draftId: draftId });

  // --- Basic required fields (read directly from DOM) ----------------------------------------------
  const requesterId = document.getElementById("requester_id").value;
  const supplierId = document.getElementById("supplier_id").value;
  const noteToSupplier = document.getElementById("note_to_supplier").value;
  const orderNote = document.getElementById("order_note").value;
  const payTerms = document.getElementById("payment_terms").value || paymentTerms || "On account";
  const requestDate = document.getElementById("request_date").value;

  if (!requesterId || !supplierId) {
    await logToServer("ERROR", "Missing requester or supplier for final order", { requesterId, supplierId });
    alert("Please fill in Requester and Supplier");
    return false; // Return false on validation failure
  }
  if (!requestDate) {
    alert("Please select a Request Date for the order.");
    await logToServer("WARNING", "Missing request date for final order");
    return false; // Return false on validation failure
  }

  // --- Line-items collection ----------------------------------------------
  let items;
  try {
    items = Array.from(document.querySelectorAll("#items-body tr")).map((row) => {
      const itemCode = row.querySelector(".item-code")?.value;
      const itemDesc = itemsList.find((i) => i.item_code === itemCode)?.item_description || "";
      const project = row.querySelector(".project")?.value;
      const qtyOrdered = parseFloat(row.querySelector(".qty-ordered")?.value) || 0;
      const price = parseFloat(row.querySelector(".price")?.value) || 0;

      // Strict validation for final orders
      if (!itemCode || !project || qtyOrdered <= 0 || price <= 0) {
        throw new Error("Each item needs item, project, quantity > 0 & price > 0 for a final order.");
      }

      return {
        item_code: itemCode,
        item_description: itemDesc,
        project,
        qty_ordered: qtyOrdered,
        price,
      };
    });
  } catch (e) {
    alert(`❌ Item validation failed for final order: ${e.message}`);
    await logToServer("ERROR", "Item validation failed for final order", { err: e.message });
    return false; // Return false on validation failure
  }

  if (items.length === 0) {
    alert("Please add at least one item to the order.");
    await logToServer("WARNING", "No items added to final order");
    return false; // Return false on validation failure
  }

  // --- Totals & status -----------------------------------------------------
  const total = updateGrandTotal();

  let status = "Pending";
  let authBandRequired = null;

  if (authThresholds.length !== 5) {
    await logToServer("ERROR", "Invalid authThresholds array length", { length: authThresholds.length });
    alert("Configuration error: authorization thresholds missing."); // Added alert for config error
    return false;
  }

  if (total > authThresholds[4]) {
    status = "Awaiting Authorisation";
    authBandRequired = 5;
  } else if (total > authThresholds[3]) { // No upper bound needed here, previous if handles it implicitly
    status = "Awaiting Authorisation";
    authBandRequired = 4;
  } else if (total > authThresholds[2]) {
    status = "Awaiting Authorisation";
    authBandRequired = 3;
  } else if (total > authThresholds[1]) {
    status = "Awaiting Authorisation";
    authBandRequired = 2;
  } else if (total > authThresholds[0]) {
    status = "Awaiting Authorisation";
    authBandRequired = 1;
  }

  // --- Payload -------------------------------------------------------------
  const orderData = {
    order_number: currentOrderNumber,
    total,
    order_note: orderNote,
    note_to_supplier: noteToSupplier,
    payment_terms: payTerms,
    requester_id: parseInt(requesterId),
    supplier_id: parseInt(supplierId),
    status,
    created_date: requestDate,
    ...(authBandRequired !== null ? { auth_band_required: authBandRequired } : {}),
    items,
  };

  // --- POST to backend -----------------------------------------------------
  try {
    const res = await fetch("/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(orderData),
    });

    if (!res.ok) {
      const errorText = await res.text();
      await logToServer("ERROR", "Failed to submit final order", { status: res.status, errorText });
      throw new Error(`Failed: ${res.status} – ${errorText}`);
    }

    const data = await res.json();
    if (data.message !== "Order created successfully") {
      throw new Error(`Unexpected response: ${data.message}`);
    }

    // --- Success handling ---
    setCurrentOrderId(data.order_id);

    // If this order originated from a draft, delete the draft entry
    if (draftId) {
        try {
            const deleteDraftRes = await fetch(`/draft_orders/${draftId}`, { method: "DELETE" });
            if (!deleteDraftRes.ok) {
                const deleteErrorText = await deleteDraftRes.text();
                console.error(`Failed to delete original draft order ${draftId}: ${deleteErrorText}`);
                await logToServer("WARNING", `Failed to delete original draft after final submission`, { draftId: draftId, finalOrderId: data.order_id, error: deleteErrorText });
            } else {
                console.log(`Original draft order ${draftId} deleted successfully after final submission.`);
                await logToServer("INFO", `Original draft deleted after final submission`, { draftId: draftId, finalOrderId: data.order_id });
            }
        } catch (deleteErr) {
            console.error(`Exception while deleting draft ${draftId}:`, deleteErr.message);
            await logToServer("ERROR", `Exception deleting original draft`, { draftId: draftId, finalOrderId: data.order_id, exception: deleteErr.message });
        }
    }
    
    await logToServer("INFO", "Order submitted successfully", {
      orderNumber: currentOrderNumber,
      orderId: data.order_id,
      status: status,
    });

    alert("✅ Order submitted successfully!");
    return true; // Return true on success

  } catch (error) {
    console.error("Order submission failed:", error.message);
    await logToServer("ERROR", "Order submission failed", { err: error.message });
    alert(`❌ Order submission failed: ${error.message}`);
    return false; // Return false on failure
  }
}