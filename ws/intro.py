from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Bookly Realtime</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e1e2f, #2c2c54);
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        .chat-container {
            width: 400px;
            height: 600px;
            background: #111827;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            overflow: hidden;
        }

        .header {
            padding: 15px;
            background: #6366f1;
            font-weight: bold;
            text-align: center;
            font-size: 18px;
        }

        .messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
        }

        .message {
            margin: 8px 0;
            padding: 10px 14px;
            border-radius: 12px;
            max-width: 70%;
            animation: fadeIn 0.3s ease;
        }

        .sent {
            background: #6366f1;
            align-self: flex-end;
        }

        .received {
            background: #374151;
            align-self: flex-start;
        }

        .input-area {
            display: flex;
            padding: 10px;
            background: #1f2937;
        }

        input {
            flex: 1;
            padding: 10px;
            border-radius: 10px;
            border: none;
            outline: none;
        }

        button {
            margin-left: 10px;
            padding: 10px 15px;
            border: none;
            border-radius: 10px;
            background: #6366f1;
            color: white;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            background: #4f46e5;
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(5px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="header">📚 Bookly Realtime Chat</div>

    <div id="messages" class="messages"></div>

    <div class="input-area">
        <input id="messageText" type="text" placeholder="Type a message..." />
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script>
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    const messagesDiv = document.getElementById("messages");

    ws.onmessage = function(event) {
        addMessage(event.data, "received");
    };

    function sendMessage() {
        const input = document.getElementById("messageText");
        if (!input.value.trim()) return;

        ws.send(input.value);
        addMessage(input.value, "sent");
        input.value = "";
    }

    function addMessage(text, type) {
        const msg = document.createElement("div");
        msg.classList.add("message", type);
        msg.textContent = text;
        messagesDiv.appendChild(msg);

        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
</script>

</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)


# -----------------------------------------------------------------------------
# Basic Websocket Endpoint
# Almost all endpoints must follow this flow
# Accept connection -> loop over incoming messages -> handle disconnection
# ------------------------------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket : WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You sent : {data}")
    except WebSocketDisconnect:
        print("Client Disconnected")


