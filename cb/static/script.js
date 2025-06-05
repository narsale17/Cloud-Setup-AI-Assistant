let configComplete = false;  

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = inputField.value.trim();
    if (!message) return;

    const userMessage = document.createElement("div");
    userMessage.className = "chat-message user-message";
    userMessage.textContent = message;
    chatBox.appendChild(userMessage);

    inputField.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    const loadingMessage = document.createElement("div");
    loadingMessage.className = "chat-message bot-message loading";
    loadingMessage.textContent = "SIFY is thinking...";
    chatBox.appendChild(loadingMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // 💡 If setup is complete, interpret as final action
        if (configComplete) {
            const response = await fetch("/final_action", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ choice: message })
            });

            const data = await response.json();
            chatBox.removeChild(loadingMessage);

            const botMessage = document.createElement("div");
            botMessage.className = "chat-message bot-message";
            botMessage.innerHTML = `<b>🔧 ${data.type.toUpperCase()} Instructions:</b><br>${data.output.replace(/\n/g, "<br>")}`;
            chatBox.appendChild(botMessage);
            chatBox.scrollTop = chatBox.scrollHeight;

            configComplete = false; // reset after showing instructions
            return;
        }

        // 🚀 Regular message flow
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        chatBox.removeChild(loadingMessage);

        const botMessage = document.createElement("div");
        botMessage.className = "chat-message bot-message";
        botMessage.textContent = data.sify || "Hmm... something went wrong.";
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;

        if (data.complete) {
            configComplete = true; // ✅ enable final step tracking
        }

    } catch (error) {
        console.error("Error talking to SIFY:", error);
        chatBox.removeChild(loadingMessage);
        const errorMessage = document.createElement("div");
        errorMessage.className = "chat-message bot-message";
        errorMessage.textContent = "⚠️ Sorry, I had a problem connecting to the server.";
        chatBox.appendChild(errorMessage);
    }
}


// Press "Enter" to send message
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function submitUserInfo() {
    const name = document.getElementById("user-name").value.trim();
    const experience = document.getElementById("user-experience").value;

    if (!name || !experience) {
        alert("Please fill in both fields!");
        return;
    }

    // 🧹 Clear previous session first
    fetch("/reset_session", { method: "POST" })
    .then(() => {
        return fetch("/store_user_info", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, experience })
        });
    })
    .then(async response => {
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error ${response.status}: ${errorText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("User info stored:", data);
        document.getElementById("user-popup").style.display = "none";
        document.getElementById("chat-container").style.display = "block";
    })
    .catch(error => {
        console.error("Error storing user info:", error);
    });
}

function handleFinalStep(choice) {
    fetch("/final_action", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ choice })
    })
    .then(response => response.json())
    .then(data => {
        const chatBox = document.getElementById("chat-box");
        const botMessage = document.createElement("div");
        botMessage.className = "chat-message bot-message";
        botMessage.innerHTML = `<b>🔧 ${data.type.toUpperCase()} Instructions:</b><br>${data.output.replace(/\\n/g, "<br>")}`;
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error handling final step:", error);
    });
}

