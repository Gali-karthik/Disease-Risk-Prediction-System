const API_BASE = "http://127.0.0.1:5000";

async function sendJson(url, body) {
  const response = await fetch(`${API_BASE}${url}`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  const data = await response.json();
  return { response, data };
}

const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const error = document.getElementById("error");
    error.textContent = "";

    try {
      const { response, data } = await sendJson("/login", {
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value
      });

      if (!response.ok || !data.success) {
        throw new Error(data.message || "Login failed.");
      }

      window.location.href = "index.html";
    } catch (err) {
      error.textContent = err.message;
    }
  });
}

const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const error = document.getElementById("error");
    error.textContent = "";

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
      error.textContent = "Passwords do not match.";
      return;
    }

    try {
      const { response, data } = await sendJson("/register", {
        name: document.getElementById("name").value.trim(),
        email: document.getElementById("email").value.trim(),
        password
      });

      if (!response.ok || !data.success) {
        throw new Error(data.message || "Registration failed.");
      }

      window.location.href = "index.html";
    } catch (err) {
      error.textContent = err.message;
    }
  });
}
