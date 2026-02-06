from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"AI: {data}")
