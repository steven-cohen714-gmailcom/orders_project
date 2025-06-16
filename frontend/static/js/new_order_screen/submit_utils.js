// frontend/static/js/new_order_screen/submit_utils.js

export async function submitOrder({
  currentOrderNumber,
  authThresholds,        // [thr1, thr2, thr3, thr4]
  itemsList,
  updateGrandTotal,
  incrementOrderNumber,
  logToServer,
  setCurrentOrderId,
  setCurrentOrderNumber,
  paymentTerms,          // passed in but still read from DOM for now
  orderType,             // "Normal" | "Draft"
  isDraft                // boolean
}) {
  console.log("submitOrder triggered");
  await logToServer("INFO", "submitOrder started", { orderType });

  // --- Basic required fields ----------------------------------------------
  const requesterId   = document.getElementById("requester_id").value;
  const supplierId    = document.getElementById("supplier_id").value;
  const noteToSupplier = document.getElementById("note_to_supplier").value;
  const payTermsDom    = document.getElementById("payment_terms").value;
  const payTerms       = payTermsDom || paymentTerms || "On account";

  if (!requesterId || !supplierId) {
    await logToServer("ERROR", "Missing requester or supplier", { requesterId, supplierId });
    alert("Please fill in Requester and Supplier");
    return;
  }

  // --- Line-items collection ----------------------------------------------
  let items;
  try {
    items = Array.from(document.querySelectorAll("#items-body tr")).map((row) => {
      const itemCode   = row.querySelector(".item-code")?.value;
      const itemDesc   = itemsList.find((i) => i.item_code === itemCode)?.item_description || "";
      const project    = row.querySelector(".project")?.value;
      const qtyOrdered = parseFloat(row.querySelector(".qty-ordered")?.value) || 0;
      const price      = parseFloat(row.querySelector(".price")?.value) || 0;

      // Relaxed validation for drafts
      if (!itemCode || !project || (!isDraft && (qtyOrdered <= 0 || price <= 0))) {
        throw new Error("Each item needs item, project, qty>0 & price>0 (unless Draft)");
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
    alert(`❌ ${e.message}`);
    await logToServer("ERROR", "Item validation failed", { err: e.message });
    return;
  }

  // --- Totals & status -----------------------------------------------------
  const total = updateGrandTotal();

  let status = "Pending";
  let authBandRequired = null;

  if (isDraft) {
    status = "Draft";
  } else {
    // Determine authorisation band only for non-drafts
    for (let i = 0; i < authThresholds.length; i++) {
      if (total > authThresholds[i]) {
        status = "Awaiting Authorisation";
        authBandRequired = i + 1;
      } else {
        break;
      }
    }
  }

  // --- Payload -------------------------------------------------------------
  const orderData = {
    order_number: currentOrderNumber,
    total,
    order_note: document.getElementById("order_note").value,
    note_to_supplier: noteToSupplier,
    payment_terms: payTerms,
    requester_id: parseInt(requesterId),
    supplier_id: parseInt(supplierId),
    status,
    ...(authBandRequired && !isDraft ? { auth_band_required: authBandRequired } : {}),
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
      await logToServer("ERROR", "Failed to submit order", { status: res.status, errorText });
      throw new Error(`Failed: ${res.status} – ${errorText}`);
    }

    const data = await res.json();
    if (data.message !== "Order created successfully") {
      throw new Error(`Unexpected response: ${data.message}`);
    }

    // --- Success handling --------------------------------------------------
    setCurrentOrderId(data.order_id);

    if (!isDraft) {
      const newOrderNumber = await incrementOrderNumber(currentOrderNumber);
      setCurrentOrderNumber(newOrderNumber);
      document.getElementById("order-number").textContent = newOrderNumber;

      await logToServer("INFO", "Order submitted & number incremented", {
        orderNumber: newOrderNumber,
        orderId: data.order_id,
      });
    } else {
      await logToServer("INFO", "Draft order submitted (no number increment)", {
        orderNumber: currentOrderNumber,
        orderId: data.order_id,
      });
    }

    alert("✅ Order submitted successfully!");

    // Clear form (minimal — adjust as needed)
    document.getElementById("requester_id").value = "";
    document.getElementById("supplier_id").value  = "";
    document.getElementById("note_to_supplier").value = "";
    document.getElementById("items-body").innerHTML = "";

  } catch (error) {
    console.error("Order submission failed:", error.message);
    await logToServer("ERROR", "Order submission failed", { err: error.message });
    alert(`❌ Order submission failed: ${error.message}`);
  }
}
