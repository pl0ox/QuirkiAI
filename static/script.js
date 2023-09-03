const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';

    messageDiv.style.transform = 'translateY(100%)';
    messageDiv.style.opacity = '0';

    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    setTimeout(() => {
        messageDiv.style.transform = 'translateY(0)';
        messageDiv.style.opacity = '1';
    }, 0);
}


function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendUserMessage() {
    const message = userInput.value;
    if (message.trim() !== '') {
        userInput.value = '';
        addUserMessage(message);
        fetch('/ask', {
            method: 'POST',
            body: new URLSearchParams({ user_input: message }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
            .then((response) => response.json())
            .then((data) => {
                const botResponse = data.bot_response;
                addBotMessage(botResponse);

           
                setTimeout(() => {
                    const messageDivs = document.querySelectorAll('.message');
                    const latestMessage = messageDivs[messageDivs.length - 1];
                    latestMessage.style.transform = 'translateY(0)';
                    latestMessage.style.opacity = '1';
                }, 300);
            })
            .catch((error) => console.error(error));
    }
}


sendButton.addEventListener('click', sendUserMessage);
userInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        sendUserMessage();
    }
});
