# game/countdown.py
import asyncio
from datetime import datetime, timedelta
from .events import publish_countdown, publish_event
import game.state as state  # <--- import the module itself

PRE_ROUND_COUNTDOWN = 10
ROUND_DURATION = 60

async def pre_round_countdown():
    # Pre-round countdown
    for i in reversed(range(1, PRE_ROUND_COUNTDOWN + 1)):
        await publish_countdown(i, "pre_round")
        await asyncio.sleep(1)

    # Start actual round
    state.init_round()
    state.ROUND_ACTIVE = True
    state.ROUND_END_TIME = datetime.utcnow() + timedelta(seconds=ROUND_DURATION)
    await publish_countdown(ROUND_DURATION, "running")
    await publish_event({"type": "new_round", "emojis": state.ROUND_EMOJIS})

async def broadcast_tick():
    while True:
        if state.ROUND_ACTIVE and state.ROUND_END_TIME:
            remaining = max(0, int((state.ROUND_END_TIME - datetime.utcnow()).total_seconds()))
            status = "running" if remaining > 0 else "ended"

            await publish_countdown(remaining, status)

            if remaining <= 0:
                state.ROUND_ACTIVE = False
                state.ROUND_END_TIME = None  # stop ticking until next round
                state.ROUND_LOCKED = False  # unlock for next round
                await publish_event({"type": "round_ended", "leaderboard": state.get_leaderboard()})
        await asyncio.sleep(1)
