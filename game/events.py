import json
from redis.asyncio import Redis

PUBSUB_EVENTS_CHANNEL = "photoscavenger_events"
PUBSUB_COUNTDOWN_CHANNEL = "photoscavenger_countdown"

redis_client: Redis = None  # inject during startup

async def publish_event(payload: dict):
    await redis_client.publish(PUBSUB_EVENTS_CHANNEL, json.dumps(payload))

async def publish_countdown(remaining: int, status: str):
    payload = {"type": "countdown", "time_remaining": remaining, "status": status}
    await redis_client.publish(PUBSUB_COUNTDOWN_CHANNEL, json.dumps(payload))
