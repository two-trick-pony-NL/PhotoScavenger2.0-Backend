from fastapi import APIRouter, Query, UploadFile, File, HTTPException
import asyncio
from game.state import is_locked, try_lock_emoji, award_points, get_leaderboard, start_upload, finish_upload
from game.detection import detect_match
from game.events import publish_event
from game.countdown import pre_round_countdown
from game import state
from game.analytics import track_event

UPLOAD_LIMIT_PER_EMOJI = 10
POINTS_PER_EMOJI = 10

api_router = APIRouter()

# in your endpoint
@api_router.post("/start_round/")
async def start_round_endpoint():
    if state.ROUND_LOCKED:
        raise HTTPException(status_code=400, detail="round_already_active_or_countdown")
    
    state.ROUND_LOCKED = True
    asyncio.create_task(pre_round_countdown())
    track_event("system", "pre_round_started")
    return {"status": "pre_round_started"}

@api_router.post("/upload/")
async def upload_photo(player_id: str = Query(...), emoji: str = Query(...), file: UploadFile = File(...)):
    if not state.ROUND_ACTIVE: 
        track_event(player_id, "image uploaded", {"player_id": player_id, "emoji": emoji, "status": "round_not_active"})
        raise HTTPException(status_code=400, detail="round_not_active")

    if not start_upload(emoji, UPLOAD_LIMIT_PER_EMOJI):
        track_event(player_id, "image uploaded", {"player_id": player_id, "emoji": emoji, "status": "too_many_uploads"})
        raise HTTPException(status_code=429, detail="too_many_uploads")
    try:
        contents = await file.read()
        await publish_event({"type": "photo_uploading", "player_id": player_id, "emoji": emoji})
        if is_locked(emoji):
            await publish_event({"type": "photo_processed", "player_id": player_id, "emoji": emoji, "status": "too_late"})
            track_event(player_id, "image uploaded", {"player_id": player_id, "emoji": emoji, "status": "too_late"})
            return {"status": "too_late"}
        matched = detect_match(contents, emoji, player_id)
        if not matched:
            await publish_event({"type": "photo_processed", "player_id": player_id, "emoji": emoji, "status": "wrong"})
            track_event(player_id, "image uploaded", {"player_id": player_id, "emoji": emoji, "status": "not_matched"})
            return {"status": "wrong"}
        if not try_lock_emoji(emoji, player_id):
            await publish_event({"type": "photo_processed", "player_id": player_id, "emoji": emoji, "status": "too_late"})
            return {"status": "too_late"}
        award_points(player_id, POINTS_PER_EMOJI)
        await publish_event({
            "type": "emoji_locked",
            "emoji": emoji,
            "winner": player_id,
            "points": POINTS_PER_EMOJI,
            "leaderboard": get_leaderboard()
        })
        track_event(player_id, "image uploaded", {"player_id": player_id, "emoji": emoji, "status": "matched"})
        return {"status": "success"}
    finally:
        finish_upload(emoji)
