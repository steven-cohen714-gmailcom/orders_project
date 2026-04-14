// /frontend/static/js/maintenance_screen/business_details.js

export function initBusinessDetails() {
  console.log("initBusinessDetails loaded");

  fetchBusinessDetails();

  const updateBtn = document.getElementById("update-business-details-button");
  if (updateBtn) {
    updateBtn.addEventListener("click", updateBusinessDetails);
  }

  async function fetchBusinessDetails() {
    try {
      const res = await fetch("/lookups/business_details");
      const data = await res.json();

      setValue("company-name", data.company_name);
      setValue("address-line1", data.address_line1);
      setValue("address-line2", data.address_line2);
      setValue("city", data.city);
      setValue("province", data.province);
      setValue("postal-code", data.postal_code);
      setValue("telephone", data.telephone);
      setValue("vat-number", data.vat_number);
    } catch (err) {
      console.error("Failed to fetch business details:", err);
    }
  }

  async function updateBusinessDetails() {
    const payload = {
      company_name: getValue("company-name"),
      address_line1: getValue("address-line1"),
      address_line2: getValue("address-line2"),
      city: getValue("city"),
      province: getValue("province"),
      postal_code: getValue("postal-code"),
      telephone: getValue("telephone"),
      vat_number: getValue("vat-number")
    };

    try {
      const res = await fetch("/lookups/business_details", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        fetchBusinessDetails();
        alert("✅ Business details updated successfully.");
      }

    } catch (err) {
      console.error("Failed to update business details:", err);
    }
  }

  function setValue(id, value) {
    const el = document.getElementById(id);
    if (el) el.value = value || "";
  }

  function getValue(id) {
    const el = document.getElementById(id);
    return el ? el.value : "";
  }
}
