document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const errorBox = document.getElementById("login-error");

  if (!form || !usernameInput || !passwordInput || !errorBox) {
    console.error("Login form elements not found in the DOM");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = usernameInput.value.trim().toLowerCase();
    const password = passwordInput.value;

    if (!username || !password) {
      errorBox.textContent = "Please enter both username and password";
      return;
    }

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        window.location.href = "/orders/pending_orders";
      } else {
        let errorMessage = "Invalid credentials. Please try again.";
        try {
          const errorData = await response.json();
          errorMessage = errorData?.error || errorData?.detail || errorMessage;
        } catch (parseErr) {
          console.warn("Non-JSON error response:", parseErr);
        }
        errorBox.textContent = errorMessage;
      }
    } catch (err) {
      console.error("Login request failed:", err);
      errorBox.textContent = "Unexpected error occurred. Please try again later.";
    }
  });
});
