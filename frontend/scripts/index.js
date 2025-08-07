const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typingIndicator");

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

function sendQuickMessage(message) {
  messageInput.value = message;
  sendMessage();
}

async function sendMessage() {
  const message = messageInput.value.trim();
  if (!message) return;

  // Add user message
  addMessage(message, "user");
  messageInput.value = "";

  // Disable send button and show typing
  sendBtn.disabled = true;
  showTyping();

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: message }),
    });

    const data = await response.json();

    // Hide typing and add bot response
    hideTyping();
    addMessage(
      data.response || data.error || "Sorry, I encountered an error.",
      "bot"
    );
  } catch (error) {
    hideTyping();
    addMessage(
      "Sorry, I'm having trouble connecting. Please try again.",
      "bot"
    );
  }

  sendBtn.disabled = false;
}

function addMessage(message, type) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}-message`;
  messageDiv.textContent = message;

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
  typingIndicator.style.display = "block";
  chatMessages.appendChild(typingIndicator);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTyping() {
  typingIndicator.style.display = "none";
}

// Focus on input when page loads
window.onload = function () {
  messageInput.focus();

  // Check and clear any conflicting sessions
  checkAndClearSessions();
};

function checkAndClearSessions() {
  // Clear any lingering authentication when on chat page
  localStorage.removeItem("currentUser");
  fetch("/clear-all-sessions", { method: "POST" }).catch(() => {});
}
