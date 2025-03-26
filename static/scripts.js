
let mediaRecorder;
let audioChunks = [];
let audio = null; // Store the AI speech audio instance globally

// Scenario-based AI greeting messages
let scenarioMessages = {
    "casual": "Hi! Let's have a friendly chat. What’s on your mind today?",
    "interview": "Hello! What job role are you preparing for? Let's do a mock interview!",
    "debate": "Let's have a debate! Here are some topics: 1) AI in Education, 2) Climate Change, 3) Social Media Influence. Choose one!",
    "storytelling": "Tell me a short story idea, and I’ll help you develop it!"
};

// Update AI's initial message based on the selected scenario
function updateScenario() {
    let scenario = document.getElementById("scenario").value;
    document.getElementById("chat-box").innerHTML = `<div class="chat-message ai-message"><strong>AI:</strong> ${scenarioMessages[scenario]}</div>`;
}

// Function to send chat messages
function sendMessage() {
    let userInput = document.getElementById("user_input").value.trim();
    let scenario = document.getElementById("scenario").value;

    if (!userInput) return;

    document.getElementById("chat-box").innerHTML += `<div class="chat-message user-message"><strong>You:</strong> ${userInput}</div>`;
    document.getElementById("user_input").value = "";
    document.getElementById("loading").style.display = "block";

    fetch("/chat", {
        method: "POST",
        body: new URLSearchParams({ user_input: userInput, scenario: scenario })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").style.display = "none";
        displayAIResponse(data);
    })
    .catch(error => {
        document.getElementById("loading").style.display = "none";
        alert("Error processing chat response.");
    });
}

// Function to display AI response and add audio controls
function displayAIResponse(data) {
    let aiMessage = `<div class="chat-message ai-message"><strong>AI:</strong> ${data.response}</div>`;
    let audioButton = `
        <div class="d-flex align-items-center mt-2">
            <button class="btn btn-secondary btn-sm flex-grow-1" onclick="toggleAudio(this)" data-audio-url="${data.speech}">
                🔊 Hear AI
            </button>
            <select class="form-select form-select-sm ms-2 voiceSpeed" onchange="updateAudioSpeed(this)">
                <option value="1">1x</option>
                <option value="1.2">1.2x</option>
                <option value="1.5">1.5x</option>
            </select>
        </div>`;

    document.getElementById("chat-box").innerHTML += aiMessage + audioButton;
    document.getElementById("chat-box").scrollTop = document.getElementById("chat-box").scrollHeight;
}

// Function to handle Enter key press
document.getElementById("user_input").addEventListener("keypress", function(event) {
    if (event.which == 13) { // 13 is the Enter key
        event.preventDefault();
        sendMessage();
    }
});

// Function to play/pause AI speech with speed control
function toggleAudio(button) {
    let audioUrl = button.getAttribute("data-audio-url");
    if (!audioUrl) return;

    let speedSelector = button.nextElementSibling;
    let speed = parseFloat(speedSelector.value);

    if (audio && !audio.paused) {
        audio.pause();
        audio.currentTime = 0;
        button.innerText = "🔊 Hear AI";
    } else {
        audio = new Audio(audioUrl);
        audio.playbackRate = speed; // Apply speed setting
        audio.play();
        button.innerText = "⏹ Stop AI";

        audio.onended = function() {
            button.innerText = "🔊 Hear AI";
        };
    }
}

// Function to update audio speed dynamically
function updateAudioSpeed(select) {
    if (audio) {
        audio.playbackRate = parseFloat(select.value);
    }
}

/* ======================== Voice Recording for Chat Input ======================== */

// Start recording when mic button is clicked
async function startRecording() {
    try {
        let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            let audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            sendVoiceInput(audioBlob);
        };

        mediaRecorder.start();
        document.getElementById("recordButton").classList.add("recording");
    } catch (error) {
        alert("Microphone access denied. Please allow microphone permissions.");
    }
}

// Stop recording when mic button is clicked again
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        document.getElementById("recordButton").classList.remove("recording");
    }
}

// Function to send recorded voice input
async function sendVoiceInput(audioBlob) {
    let formData = new FormData();
    formData.append("audio", audioBlob, "recorded_audio.wav");

    document.getElementById("loading").style.display = "block";

    let response = await fetch("/voice", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    document.getElementById("loading").style.display = "none";

    if (data.transcript) {
        document.getElementById("chat-box").innerHTML += `<div class="chat-message user-message"><strong>You:</strong> ${data.transcript}</div>`;
    }

    displayAIResponse(data);
}
