function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = inputField.value.trim();
    if (!message) return;

    // Add user message
    const userMessage = document.createElement("div");
    userMessage.className = "chat-message user-message";
    userMessage.textContent = message;
    chatBox.appendChild(userMessage);

    inputField.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Add loading animation
    const loadingMessage = document.createElement("div");
    loadingMessage.className = "chat-message bot-message loading";
    loadingMessage.textContent = ".";
    chatBox.appendChild(loadingMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Simulate bot response after delay
    setTimeout(() => {
        chatBox.removeChild(loadingMessage); // Remove loading animation

        const botMessage = document.createElement("div");
        botMessage.className = "chat-message bot-message";
        botMessage.textContent = "This is a fixed response.";
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 2000); // Delay for effect
}

// Press "Enter" to send message
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
