document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value.trim().toLowerCase();
  const password = document.getElementById("password").value;

  if (!username || !password) {
    document.getElementById("login-error").textContent = "Please enter both username and password";
    return;
  }

  try {
    const res = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (res.ok) {
      window.location.href = "/home";
    } else {
      const data = await res.json();
      document.getElementById("login-error").textContent = data.detail || "Login failed";
    }
  } catch (err) {
    document.getElementById("login-error").textContent = "An error occurred. Please try again.";
  }
});