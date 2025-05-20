console.log("📱 Mobile authorisation screen loaded");

function formatDate(dateStr) {
  if (!dateStr) return "—";
  try {
    const date = new Date(dateStr);
    const day = date.getDate().toString().padStart(2, "0");
    const month = date.toLocaleString("default", { month: "short" });
    const year = date.getFullYear().toString().slice(-2);
    return `${day} ${month} ${year}`;
  } catch {
    return "—";
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("order-list");

  // 🔍 Fetch username from session via backend
  try {
    const res = await fetch("/mobile/get_user_info");
    const user = await res.json();
    const username = user.username || "";
    const heading = document.querySelector("h2");
    if (heading) {
      heading.innerHTML = `<span style="font-weight: normal;">${username}</span>, please review the orders below which are waiting for you to authorise:`;
    }
  } catch (err) {
    console.error("❌ Failed to fetch user info:", err);
  }

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

    container.innerHTML = ""; // Clear "Loading orders..."

    data.forEach(order => {
      const item = document.createElement("div");
      item.className = "order-row";

      const dateFormatted = formatDate(order.created_date);

      item.innerHTML = `
        <span>${dateFormatted}</span>
        <span>${order.order_number}</span>
        <span>R${order.total}</span>
        <span class="buttons"></span>
      `;

      const viewBtn = document.createElement("button");
      viewBtn.textContent = "View PDF";
      viewBtn.onclick = () => window.open(`/orders/api/generate_pdf_for_order/${order.id}`, "_blank");

      const authBtn = document.createElement("button");
      authBtn.textContent = "Authorise";
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
            item.style.opacity = 0.6;
          } else {
            alert("❌ Failed to authorise: " + result.message);
          }
        } catch (err) {
          console.error(err);
          alert("❌ Error sending authorisation request.");
        }
      };

      item.querySelector(".buttons").appendChild(viewBtn);
      item.querySelector(".buttons").appendChild(authBtn);
      container.appendChild(item);
    });

  } catch (err) {
    container.textContent = "❌ Failed to load orders.";
    console.error("Fetch error:", err);
  }
});
