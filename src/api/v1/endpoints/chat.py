import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_message(self, message: str, session_id: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/stream/{session_id}")
async def websocket_chat_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Here you would typically process the message with Groq / OpenAI
            # For demonstration, we simulate a streaming response
            user_text = message_data.get("content", "")
            
            response_chunks = f"AI processing: {user_text}".split(" ")
            
            for chunk in response_chunks:
                await manager.send_message(json.dumps({"type": "chunk", "content": chunk + " "}), session_id)
                await asyncio.sleep(0.1) # Simulate token streaming delay
                
            await manager.send_message(json.dumps({"type": "done"}), session_id)
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)
