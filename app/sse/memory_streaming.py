from pathlib import Path
from .middleware.token_sse_server import Middleware_Token_SSE_SERVER
from fastapi import FastAPI, Request
from core.lib_fastapi.view_header import *

from core.pubsub.memory_pubsub import MemoryPubSub
from fastapi.responses import StreamingResponse


path = Path(__file__).parent.absolute()
prefix = "/"+path.name
base = 'app.sse'
app = FastAPI()

# Memory
pubsub = MemoryPubSub(time_disable_subscribe=5)


@app.get("/ping")
def ping(request: Request):
    response = pubsub.ping(request)
    return response


@app.get("/publish/")
def pub_send(request: Request, channel: str, message: str = ""):
    response = pubsub.publish(request, channel, message)
    return response


@app.get("/subscribe/")
async def sub_receive(request: Request, channel: str):
    response = StreamingResponse(pubsub.subscribe(
        request, channel), media_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


@app.get("/disable_subscribe/")
def dis_sub(request: Request, channel: str):
    response = pubsub.disable_subscribe(request, channel)
    return response


app.add_middleware(Middleware_Token_SSE_SERVER)
