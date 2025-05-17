// /frontend/static/js/components/utils.js

export async function logToServer(level, message, details = {}) {
  try {
    await fetch("/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ level, message, details })
    });
  } catch (error) {
    console.error("Failed to log to server:", error);
  }
}
