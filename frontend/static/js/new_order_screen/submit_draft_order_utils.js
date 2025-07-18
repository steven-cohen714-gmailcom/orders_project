// File: frontend/static/js/new_order_screen/submit_draft_order_utils.js

import { logToServer } from "../components/utils.js";

/**
 * Handles saving an order as a draft.
 * @param {object} params - Parameters needed for draft submission.
 * @param {string} params.currentOrderNumber - The current order number displayed.
 * @param {Array<object>} params.itemsList - The list of available items for description lookup.
 * @param {function(): number} params.updateGrandTotal - Function to calculate the current grand total.
 * @param {function(string): Promise<string>} params.incrementOrderNumber - Function to increment the order number on the backend.
 * @param {function(number): void} params.setCurrentOrderId - Function to set the current order ID.
 * @param {function(string): void} params.setCurrentOrderNumber - Function to set the current order number.
 */
export async function saveDraftOrder({
  currentOrderNumber,
  itemsList,
  updateGrandTotal,
  incrementOrderNumber,
  logToServer,
  setCurrentOrderId, // Will actually set draft_order_id
  setCurrentOrderNumber, // This is needed to update the UI after a new draft is saved
}) {
  console.log("saveDraftOrder triggered (saving as draft)");
  await logToServer("INFO", "saveDraftOrder started (saving as draft)", { orderNumber: currentOrderNumber });

  // --- Basic required fields for a draft ----------------------------------
  const requesterId = document.getElementById("requester_id")?.value;
  const supplierId = document.getElementById("supplier_id")?.value;
  const noteToSupplier = document.getElementById("note_to_supplier")?.value;
  const orderNote = document.getElementById("order_note")?.value; // Added orderNote from DOM
  const paymentTerms = document.getElementById("payment_terms")?.value || "On account";
  const requestDate = document.getElementById("request_date")?.value;
  const draftOrderId = document.getElementById("draft-order-id")?.value; // Get hidden draft ID if editing

  if (!requesterId || !supplierId) {
    alert("Please select Requester and Supplier for the draft.");
    await logToServer("WARNING", "Missing requester or supplier for draft", { requesterId, supplierId });
    return false; // Return false on validation failure
  }
  if (!requestDate) {
    alert("Please select a Request Date for the draft.");
    await logToServer("WARNING", "Missing request date for draft");
    return false; // Return false on validation failure
  }

  // --- Line-items collection (more lenient for drafts) --------------------
  let items;
  try {
    items = Array.from(document.querySelectorAll("#items-body tr")).map((row) => {
      const itemCode = row.querySelector(".item-code")?.value;
      const itemDesc = itemsList.find((i) => i.item_code === itemCode)?.item_description || "";
      const project = row.querySelector(".project")?.value;
      const qtyOrdered = parseFloat(row.querySelector(".qty-ordered")?.value) || 0;
      const price = parseFloat(row.querySelector(".price")?.value) || 0;

      if (!itemCode || !project) {
        throw new Error("Each item needs an item code and project, even for drafts.");
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
    alert(`❌ Invalid item: ${e.message}`);
    await logToServer("ERROR", "Item validation failed for draft", { err: e.message });
    return false; // Return false on validation failure
  }

  if (items.length === 0) {
    alert("Please add at least one item to the draft order.");
    await logToServer("WARNING", "No items added to draft order");
    return false; // Return false on validation failure
  }

  // --- Calculate total (even for drafts, to store it) ----------------------
  const total = updateGrandTotal();

  // --- Payload -------------------------------------------------------------
  const draftOrderData = {
    order_number: currentOrderNumber, // Use the current number on the screen
    total: total,
    order_note: orderNote,
    note_to_supplier: noteToSupplier,
    payment_terms: paymentTerms,
    requester_id: parseInt(requesterId),
    supplier_id: parseInt(supplierId),
    items: items,
  };

  // --- POST/PUT to backend -------------------------------------------------
  try {
    let res;
    let method;
    let url;

    if (draftOrderId) { // If editing an existing draft
      method = "PUT";
      url = `/draft_orders/${draftOrderId}`;
      res = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(draftOrderData),
      });
    } else { // If creating a new draft
      method = "POST";
      url = "/draft_orders";
      res = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(draftOrderData),
      });
    }

    if (!res.ok) {
      const errorText = await res.text();
      await logToServer("ERROR", `Failed to ${method === 'POST' ? 'create' : 'update'} draft order`, { status: res.status, errorText });
      throw new Error(`Failed: ${res.status} – ${errorText}`);
    }

    const data = await res.json();
    if (data.message) {
      console.log(data.message);
    }

    // --- Success handling for draft saving ---
    if (!draftOrderId) { // If it was a NEW draft creation
      setCurrentOrderId(data.draft_id); // Set the new draft_id returned by the backend
      // Crucially, increment the order number only ONCE when a NEW draft is created
      const newOrderNumber = await incrementOrderNumber(currentOrderNumber); // Call increment function
      setCurrentOrderNumber(newOrderNumber); // Update the displayed order number for the next new entry
    }
    // If it was an update (draftOrderId exists), currentOrderNumber doesn't change, no increment needed.

    alert(`✅ Draft order ${currentOrderNumber} saved successfully!`);
    await logToServer("INFO", `Draft order ${method === 'POST' ? 'created' : 'updated'} successfully`, { orderNumber: currentOrderNumber, draftId: draftOrderId || data.draft_id });

    return true; // Return true on success

  } catch (error) {
    console.error(`Draft order ${draftOrderId ? 'update' : 'creation'} failed:`, error.message);
    await logToServer("ERROR", `Draft order ${draftOrderId ? 'update' : 'creation'} failed`, { err: error.message });
    alert(`❌ Draft order ${draftOrderId ? 'update' : 'creation'} failed: ${error.message}`);
    return false; // Return false on failure
  }
}