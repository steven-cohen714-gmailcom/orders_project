console.log("📱 Mobile authorisation screen loaded");

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("order-list");

  try {
    const res = await fetch("/orders/api/awaiting_authorisation");
    const data = await res.json();

    if (!Array.isArray(data)) {
      container.textContent = "❌ Invalid response from server.";
      console.error("Expected an array but got:", data);
      return;
    }

    if (data.length === 0) {
      container.textContent = "✅ No orders awaiting your authorisation.";
      return;
    }

    const list = document.createElement("ul");

    data.forEach(order => {
      const item = document.createElement("li");
      item.style.marginBottom = "1rem";

      const heading = document.createElement("div");
      heading.textContent = `Order ${order.order_number} — Total: R${order.total}`;
      heading.style.fontWeight = "bold";

      const viewBtn = document.createElement("button");
      viewBtn.textContent = "View PDF";
      viewBtn.onclick = () => window.open(`/orders/pdf/${order.id}`, "_blank");

      const authBtn = document.createElement("button");
      authBtn.textContent = "Authorise";
      authBtn.style.marginLeft = "1rem";
      authBtn.onclick = async () => {
        try {
          const res = await fetch(`/orders/api/authorise_order/${order.id}`, {
            method: "POST"
          });
          const result = await res.json();
          if (result.status === "success") {
            authBtn.textContent = "✅ Authorised";
            authBtn.disabled = true;
            viewBtn.disabled = true;
            heading.style.color = "green";
          } else {
            alert("❌ Failed to authorise: " + result.message);
          }
        } catch (err) {
          console.error(err);
          alert("❌ Error sending authorisation request.");
        }
      };

      item.appendChild(heading);
      item.appendChild(viewBtn);
      item.appendChild(authBtn);
      list.appendChild(item);
    });

    container.innerHTML = "";
    container.appendChild(list);
  } catch (err) {
    container.textContent = "❌ Failed to load orders.";
    console.error("Fetch error:", err);
  }
});
