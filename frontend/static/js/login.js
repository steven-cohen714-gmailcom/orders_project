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
        const data = await response.json();

        if (data.success && data.authorized_screens && data.authorized_screens.length > 0) {
          const firstAuthorizedScreenCode = data.authorized_screens[0];

          // --- MODIFIED: Corrected screenToPathMap with lowercase, underscore-separated codes ---
          const screenToPathMap = {
            "new_requisition": "/requisitions/new",
            "pending_requisitions": "/requisitions/pending_requisitions",
            "new_order": "/orders/new",
            "pending_orders": "/orders/pending_orders",
            "received_orders": "/orders/received_orders",
            "partially_delivered_orders": "/orders/partially_delivered",
            "audit_trail": "/orders/audit_trail",
            "my_authorisations": "/orders/authorisations_per_user",
            "cod_orders": "/orders/cod_orders",
            "maintenance": "/maintenance",
            // Add any other screens if you have them and their corresponding paths
          };

          let redirectPath = "/"; // Default to home if no specific mapping found

          if (screenToPathMap[firstAuthorizedScreenCode]) {
              redirectPath = screenToPathMap[firstAuthorizedScreenCode];
          } else {
              console.warn(`No direct mapping found for screen_code: ${firstAuthorizedScreenCode}. Redirecting to home.`);
              // If the first authorized screen doesn't have a specific mapping,
              // or if you prefer a generic dashboard for all users, you can redirect to /home
              redirectPath = "/home"; // Redirect to a safe default like /home
          }

          window.location.href = redirectPath; // Redirect to the first authorized screen
        } else {
          // If login is successful but no authorized screens (e.g., a new user with no permissions yet)
          errorBox.textContent = "Login successful, but no accessible screens found. Please contact support or log in as an administrator.";
          console.error("Login successful but no authorized screens received or list is empty:", data);
          // Redirect to a neutral page, like a generic home or an access denied page, not back to login.
          window.location.href = "/home"; // Or "/access_denied" if you have one
        }

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
