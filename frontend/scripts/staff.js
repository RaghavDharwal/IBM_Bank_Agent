const staffLoginForm = document.getElementById("staffLoginForm");
const loginBtn = document.getElementById("loginBtn");
const errorAlert = document.getElementById("errorAlert");
const successAlert = document.getElementById("successAlert");

function showAlert(message, type) {
  const alert = type === "error" ? errorAlert : successAlert;
  alert.textContent = message;
  alert.style.display = "block";

  // Hide the other alert
  const otherAlert = type === "error" ? successAlert : errorAlert;
  otherAlert.style.display = "none";

  // Auto-hide after 5 seconds
  setTimeout(() => {
    alert.style.display = "none";
  }, 5000);
}

function clearUserSession() {
  // Clear user session when staff logs in
  localStorage.removeItem("currentUser");
  fetch("/user-logout", { method: "POST" }).catch(() => {});
}

function checkConflictingSessions() {
  // Check if user is logged in
  const savedUser = localStorage.getItem("currentUser");
  if (savedUser) {
    const user = JSON.parse(savedUser);
    showAuthWarning(
      `⚠️ User session detected. You are currently logged in as user: ${user.email}`
    );
  }

  // Also check server-side user session
  fetch("/user-auth-status")
    .then((response) => response.json())
    .then((data) => {
      if (data.logged_in) {
        showAuthWarning(
          `⚠️ User session detected. You are currently logged in as user: ${data.email}`
        );
      }
    })
    .catch(() => {});
}

function showAuthWarning(message) {
  document.getElementById("statusText").textContent = message;
  document.getElementById("authStatusBar").classList.add("show");
}

function clearAllSessions() {
  // Clear all sessions and localStorage
  localStorage.clear();
  fetch("/clear-all-sessions", { method: "POST" })
    .then(() => {
      location.reload();
    })
    .catch(() => location.reload());
}

staffLoginForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    showAlert("Please enter both username and password", "error");
    return;
  }

  loginBtn.disabled = true;
  loginBtn.textContent = "Signing in...";

  try {
    const response = await fetch("/staff-login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    const data = await response.json();

    if (data.success) {
      // Clear user session when staff logs in
      clearUserSession();

      showAlert("Login successful! Redirecting to dashboard...", "success");
      setTimeout(() => {
        window.location.href = "/admin-dashboard";
      }, 1500);
    } else {
      showAlert(
        data.error || "Login failed. Please check your credentials.",
        "error"
      );
    }
  } catch (error) {
    showAlert("Network error. Please try again.", "error");
  }

  loginBtn.disabled = false;
  loginBtn.textContent = "Sign In to Dashboard";
});

// Focus on username field when page loads
window.onload = function () {
  document.getElementById("username").focus();

  // Check for conflicting sessions
  checkConflictingSessions();
};

// Handle Enter key in password field
document.getElementById("password").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    staffLoginForm.dispatchEvent(new Event("submit"));
  }
});
