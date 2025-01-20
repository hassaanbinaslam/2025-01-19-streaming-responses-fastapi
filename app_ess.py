from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sse_starlette.sse import EventSourceResponse
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
    " through FastAPI SSE.",
    " Here's the final",
    " chunk!",
]


@app.get("/")
async def get_html_page(request: Request):
    return templates.TemplateResponse("ess.html", {"request": request})


async def event_generator():
    for message in MESSAGES:
        yield {"data": message}
        await asyncio.sleep(1)  # Simulate an async delay


@app.get("/stream")
async def stream_response():
    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
