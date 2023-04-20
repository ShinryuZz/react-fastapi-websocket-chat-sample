from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from ConnectionManager import *
from datetime import datetime
import json

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

manager = ConnectionManager()

@app.get("/")
def home():
    return "Welcome Home"


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket : WebSocket, cliend_id: int):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            message = {"time": current_time, "client_id": cliend_id, "message" : data}
            await manager.broadcast(json.dumps(message))

    except WebSocketDisconnect: 
        manager.disconnect(websocket)
        message = {"time": current_time, "client_id": cliend_id, "message": "Offline"}
        await manager.broadcast(json.dumps(message))





