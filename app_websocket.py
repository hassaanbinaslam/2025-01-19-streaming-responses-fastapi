from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
import asyncio
import pathlib

app = FastAPI()

# Setup templates
BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Test messages
MESSAGES = [
    "This is",
    " a large",
    " response",
    " being",
    " streamed",
    " through FastAPI WebSocket.",
    " Here's the final",
    " chunk!",
]


@app.get("/")
async def get_html_page(request: Request):
    return templates.TemplateResponse("wsocket.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Send initial messages
        for message in MESSAGES:
            await websocket.send_text(message)
            await asyncio.sleep(1)

        # Keep connection alive and handle incoming messages
        # while True:
        #     data = await websocket.receive_text()
        #     # Echo back the received message
        #     await websocket.send_text(f"Server received: {data}")

        # Set a reasonable timeout
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(), timeout=60  # 60 second timeout
                )
                await websocket.send_text(f"Response: {data}")
            except asyncio.TimeoutError:
                await websocket.close()
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
