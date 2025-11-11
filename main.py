import os
import dotenv
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis

from game import events

from websocket.handler import websocket_endpoint, redis_pubsub_forwarder
from api.endpoints import api_router
from game.countdown import broadcast_tick

# --- ENV ---
dotenv.load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# --- REDIS CLIENT ---
redis_client = None


async def wait_for_redis():
    global redis_client
    for _ in range(10):
        try:
            redis_client = aioredis.from_url("redis://localhost:6379")
            await redis_client.ping()
            print("Connected to Redis")
            return
        except aioredis.ConnectionError:
            print("Waiting for Redis...")
            await asyncio.sleep(2)
    raise ConnectionError("Could not connect to Redis")

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
    global redis_client
    redis_client = await wait_for_redis()  # ✅ Wait first

    # Inject into modules
    events.redis_client = redis_client

    # Start background tasks
    asyncio.create_task(redis_pubsub_forwarder(redis_client))
    asyncio.create_task(broadcast_tick())


@app.get("/")
@app.get("/healthcheck")
async def root():
    return {"message": "PhotoScavenger API is running."}