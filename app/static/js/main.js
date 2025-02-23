function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (!userInput) return;

    appendMessage('user', userInput);
    document.getElementById('user-input').value = '';

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.clarification) {
            appendMessage('bot', data.clarification);
        } else {
            document.getElementById('query-box').innerHTML = `<strong>SQL Query:</strong><pre>${data.query}</pre>`;
            document.getElementById('result-box').innerHTML = `<strong>Results:</strong>${data.result}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('bot', 'An error occurred. Please try again.');
    });
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
