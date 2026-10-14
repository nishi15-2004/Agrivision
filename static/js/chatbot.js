
function toggleChatbot() {
    const chatbot = document.getElementById("chatbot-container");

    if (chatbot.style.display === "flex") {
        chatbot.style.display = "none";
    } else {
        chatbot.style.display = "flex";

        setTimeout(() => {
            document.getElementById("chatbot-input").focus();
        }, 100);
    }
}


// Voice assistance variables
let recognition = null;
let isListening = false;


document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("chatbot-input");
    const micButton = document.getElementById("chatbot-mic");

    // Enter key se message send hoga
    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendChatMessage();
            }
        });
    }

    // Voice recognition setup
    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (SpeechRecognition) {

        recognition = new SpeechRecognition();

        recognition.lang = "hi-IN";
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function () {
            isListening = true;

            if (micButton) {
                micButton.textContent = "🔴";
                micButton.title = "Stop listening";
            }
        };

        recognition.onresult = function (event) {
            const spokenText =
                event.results[0][0].transcript;

            input.value = spokenText;
            input.focus();
        };

        recognition.onerror = function (event) {
            console.error("Voice recognition error:", event.error);

            if (event.error === "not-allowed") {
                addMessage(
                    "Microphone permission allow karein, phir dobara try karein.",
                    "bot"
                );
            } else if (event.error !== "no-speech") {
                addMessage(
                    "Voice input mein problem aayi. Dobara try karein.",
                    "bot"
                );
            }
        };

        recognition.onend = function () {
            isListening = false;

            if (micButton) {
                micButton.textContent = "🎤";
                micButton.title = "Speak your question";
            }
        };

        // Mic button click
        if (micButton) {
            micButton.addEventListener("click", function () {

                if (isListening) {
                    recognition.stop();
                    return;
                }

                try {
                    recognition.start();
                } catch (error) {
                    console.error("Microphone error:", error);
                }
            });
        }

    } else if (micButton) {

        micButton.addEventListener("click", function () {
            addMessage(
                "Aapka browser voice input support nahi karta. Chrome ke latest version mein try karein.",
                "bot"
            );
        });

    }

});


// Send message to Flask API
async function sendChatMessage() {

    const input = document.getElementById("chatbot-input");
    const message = input.value.trim();

    if (!message || input.disabled) {
        return;
    }

    // Agar mic sun raha hai to stop karein
    if (recognition && isListening) {
        recognition.stop();
    }

    addMessage(message, "user");

    input.value = "";
    input.disabled = true;

    const loadingMessage = addMessage(
        "AgriMitra soch raha hai... 🌾",
        "bot"
    );

    try {

        const response = await fetch("/api/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                language: detectLanguage(message)
            })
        });

        const data = await response.json();

        loadingMessage.remove();

        if (data.success) {
            addMessage(data.reply, "bot");
        } else {
            addMessage(
                "Sorry, abhi response nahi aa raha. Please try again.",
                "bot"
            );

            console.error(data.error);
        }

    } catch (error) {

        loadingMessage.remove();

        addMessage(
            "Server se connection nahi ho pa raha. Please check your Flask server.",
            "bot"
        );

        console.error("Chatbot error:", error);

    } finally {
        input.disabled = false;
        input.focus();
    }

}


// Display chat messages
function addMessage(text, type) {

    const messages = document.getElementById("chatbot-messages");
    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "chat-message",
        type === "user" ? "user-message" : "bot-message"
    );

    // Safe text display with line breaks
    const messageText = document.createElement("span");
    messageText.innerHTML = formatChatText(String(text));

    messageDiv.appendChild(messageText);

    // Bot response ke saath speaker button
    if (type === "bot") {

        const speakButton = document.createElement("button");

        speakButton.type = "button";
        speakButton.textContent = " 🔊";
        speakButton.title = "Listen to this response";
        speakButton.setAttribute(
            "aria-label",
            "Listen to this response"
        );

        speakButton.addEventListener("click", function () {
            speakMessage(String(text));
        });

        messageDiv.appendChild(speakButton);
    }

    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;

    return messageDiv;
}


// Format message safely
function formatChatText(text) {

    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, "<br>");

}


// Speak bot response
function speakMessage(text) {

    if (!("speechSynthesis" in window)) {
        addMessage(
            "Aapka browser voice output support nahi karta.",
            "bot"
        );
        return;
    }

    // Purani speech ko stop karke naya response sunayein
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    const language = detectLanguage(text);

    utterance.lang =
        language === "English" ? "en-IN" : "hi-IN";

    utterance.rate = 0.9;
    utterance.pitch = 1;

    window.speechSynthesis.speak(utterance);
}


// Detect message language
function detectLanguage(text) {

    const hindiCharacters = /[\u0900-\u097F]/;

    if (hindiCharacters.test(text)) {
        return "Hindi";
    }

    const hindiWords = [
        "kya",
        "kaise",
        "kab",
        "meri",
        "mera",
        "fasal",
        "kheti",
        "paudha",
        "paani",
        "barish",
        "keeda",
        "rog",
        "bimari"
    ];

    const lowerText = text.toLowerCase();

    for (const word of hindiWords) {
        if (lowerText.includes(word)) {
            return "Hinglish";
        }
    }

    return "English";
}
