from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
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
    " through FastAPI StreamingResponse.",
    " Here's the final",
    " chunk!",
]


@app.get("/")
async def get_html_page(request: Request):
    return templates.TemplateResponse("stream.html", {"request": request})


async def stream_generator():
    for message in MESSAGES:
        yield message
        await asyncio.sleep(1)  # Simulate an async delay


@app.get("/stream")
async def stream_response():
    return StreamingResponse(
        stream_generator(),
        media_type="text/plain",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
