(function() {
    // Styles for the chat panel
    const styles = `
        .ai-chat-panel {
            position: fixed;
            right: -400px;
            top: 0;
            width: 400px;
            height: 100vh;
            background: white;
            box-shadow: -2px 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            z-index: 999999;
            transition: right 0.3s ease;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }

        .ai-chat-panel.open {
            right: 0;
        }

        .ai-chat-toggle {
            position: fixed;
            right: 20px;
            bottom: 20px;
            width: 60px;
            height: 60px;
            border-radius: 30px;
            background: #007AFF;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000000;
        }

        .ai-chat-header {
            padding: 20px;
            background: #007AFF;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .ai-chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .ai-message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 12px;
            line-height: 1.4;
        }

        .ai-user-message {
            background: #007AFF;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }

        .ai-bot-message {
            background: #f0f0f0;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .ai-chat-input {
            padding: 20px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 12px;
        }

        .ai-chat-input input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
        }

        .ai-chat-input input:focus {
            border-color: #007AFF;
        }

        .ai-chat-input button {
            padding: 12px 24px;
            background: #007AFF;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }

        .ai-chat-input button:hover {
            background: #0056b3;
        }

        .ai-chat-input button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .ai-typing-indicator {
            display: none;
            align-self: flex-start;
            padding: 12px 16px;
            background: #f0f0f0;
            border-radius: 12px;
            color: #666;
        }

        .ai-typing-indicator.active {
            display: block;
        }

        .ai-status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }

        .ai-status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4CAF50;
        }

        .ai-status-dot.disconnected {
            background: #f44336;
        }
    `;

    // Create and inject styles
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);

    // Create chat panel HTML
    const chatPanel = document.createElement('div');
    chatPanel.className = 'ai-chat-panel';
    chatPanel.innerHTML = `
        <div class="ai-chat-header">
            <h3>AI Assistant</h3>
            <div class="ai-status-indicator">
                <span class="ai-status-dot"></span>
                <span class="ai-status-text">Connecting...</span>
            </div>
        </div>
        <div class="ai-chat-messages">
            <div class="ai-message ai-bot-message">
                Hello! How can I help you today?
            </div>
            <div class="ai-typing-indicator">
                Assistant is typing...
            </div>
        </div>
        <div class="ai-chat-input">
            <input type="text" placeholder="Type your message..." />
            <button>Send</button>
        </div>
    `;

    // Create toggle button
    const toggleButton = document.createElement('div');
    toggleButton.className = 'ai-chat-toggle';
    toggleButton.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>`;

    // Add elements to page
    document.body.appendChild(chatPanel);
    document.body.appendChild(toggleButton);

    // Chat functionality
    const clientId = 'user_' + Math.random().toString(36).substr(2, 9);
    let ws = null;

    const elements = {
        panel: chatPanel,
        messages: chatPanel.querySelector('.ai-chat-messages'),
        input: chatPanel.querySelector('input'),
        button: chatPanel.querySelector('button'),
        toggle: toggleButton,
        statusDot: chatPanel.querySelector('.ai-status-dot'),
        statusText: chatPanel.querySelector('.ai-status-text'),
        typingIndicator: chatPanel.querySelector('.ai-typing-indicator')
    };

    // Toggle chat panel
    elements.toggle.addEventListener('click', () => {
        elements.panel.classList.toggle('open');
        if (elements.panel.classList.contains('open') && !ws) {
            connectWebSocket();
        }
    });

    // Connect to WebSocket
    function connectWebSocket() {
        ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

        ws.onopen = () => {
            elements.statusDot.classList.remove('disconnected');
            elements.statusText.textContent = 'Connected';
            elements.button.disabled = false;
        };

        ws.onclose = () => {
            elements.statusDot.classList.add('disconnected');
            elements.statusText.textContent = 'Disconnected';
            elements.button.disabled = true;
            ws = null;
        };

        ws.onerror = () => {
            elements.statusDot.classList.add('disconnected');
            elements.statusText.textContent = 'Error';
            elements.button.disabled = true;
        };

        ws.onmessage = (event) => {
            elements.typingIndicator.classList.remove('active');
            addMessage(event.data, 'bot');
        };
    }

    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ai-${sender}-message`;
        messageDiv.textContent = text;
        elements.messages.insertBefore(messageDiv, elements.typingIndicator);
        elements.messages.scrollTop = elements.messages.scrollHeight;
    }

    // Send message
    function sendMessage() {
        const message = elements.input.value.trim();
        if (message && ws && ws.readyState === WebSocket.OPEN) {
            addMessage(message, 'user');
            ws.send(message);
            elements.input.value = '';
            elements.typingIndicator.classList.add('active');
        }
    }

    // Event listeners
    elements.button.addEventListener('click', sendMessage);
    elements.input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
})(); 