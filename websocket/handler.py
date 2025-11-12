import json
from fastapi import WebSocket
from datetime import datetime
from game.state import ROUND_END_TIME, get_leaderboard, ROUND_EMOJIS, LOCKED_EMOJIS
from game.analytics import track_event

active_players = set()


async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_players.add(ws)

    # broadcast updated connection count
    await broadcast_connection_count()

    try:
        await send_full_state(ws)
        track_event("system", "player connected", {"timestamp": datetime.utcnow().isoformat()})
        while True:
            await ws.receive_text()
    except:
        pass
    finally:
        active_players.discard(ws)
        await broadcast_connection_count()


async def send_full_state(ws: WebSocket):
    if ROUND_END_TIME:
        remaining = max(0, int((ROUND_END_TIME - datetime.utcnow()).total_seconds()))
        status = "running" if remaining > 0 else "ended"
    else:
        remaining = 0
        status = "idle"

    state = {
        "type": "full_state",
        "time_remaining": remaining,
        "status": status,
        "leaderboard": get_leaderboard(),
        "emojis": [{"emoji": e, "locked_by": LOCKED_EMOJIS.get(e)} for e in ROUND_EMOJIS],
        "active_players": len(connected_websockets),
    }
    await ws.send_json(state)


async def broadcast_connection_count():
    payload = {"type": "active_players", "count": len(connected_websockets)}
    for ws in list(connected_websockets):
        try:
            await ws.send_json(payload)
        except:
            connected_websockets.discard(ws)


async def redis_pubsub_forwarder(redis_client):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("photoscavenger_countdown", "photoscavenger_events")

    async for msg in pubsub.listen():
        if not msg or msg.get("type") != "message":
            continue
        data = msg["data"]
        try:
            payload = json.loads(data)
        except:
            payload = {"type": "raw", "data": data}
        for ws in list(connected_websockets):
            try:
                await ws.send_json(payload)
            except:
                connected_websockets.discard(ws)
