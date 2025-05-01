document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value.trim().toLowerCase();

  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });

  if (res.ok) {
    window.location.href = "/home";
  } else {
    const msg = await res.text();
    document.getElementById("login-error").textContent = msg || "Login failed";
  }
});
