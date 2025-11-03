import os
import dotenv
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis

from websocket.handler import websocket_endpoint, redis_pubsub_forwarder
from api.endpoints import api_router
from game.countdown import broadcast_tick

# --- ENV ---
dotenv.load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# --- REDIS CLIENT ---
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

# --- FASTAPI ---
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router)

# --- WEBSOCKET ---
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket_endpoint(websocket)

# --- STARTUP ---
@app.on_event("startup")
async def startup():
    # Inject redis_client into modules
    from game import events
    events.redis_client = redis_client

    # Start background tasks
    asyncio.create_task(redis_pubsub_forwarder(redis_client))
    asyncio.create_task(broadcast_tick())


@app.get("/")
async def root():
    return {"message": "PhotoScavenger API is running."}