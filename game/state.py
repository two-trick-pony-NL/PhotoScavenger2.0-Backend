from datetime import datetime, timedelta
from .emoji import EMOJI_TO_CLASS
import random
from .analytics import track_event


ROUND_DURATION = 60
NUM_EMOJIS_PER_ROUND = 8
ROUND_ACTIVE = False
ROUND_LOCKED = False      # True during pre-round countdown or active round
ROUND_END_TIME = None
ROUND_EMOJIS = []
LOCKED_EMOJIS = {}
UPLOAD_COUNTER = {}
LEADERBOARD = {}
EMOJIS = list(EMOJI_TO_CLASS.keys())


def init_round(num_emojis=NUM_EMOJIS_PER_ROUND):
    global ROUND_EMOJIS, LOCKED_EMOJIS, UPLOAD_COUNTER, ROUND_END_TIME
    
    # pick `num_emojis` unique emojis from EMOJIS
    ROUND_EMOJIS = random.sample(EMOJIS, k=min(num_emojis, len(EMOJIS)))
    
    LOCKED_EMOJIS = {}
    UPLOAD_COUNTER = {e: 0 for e in ROUND_EMOJIS}
    ROUND_END_TIME = datetime.utcnow() + timedelta(seconds=ROUND_DURATION)

def start_upload(emoji, limit):
    if UPLOAD_COUNTER.get(emoji, 0) >= limit:
        return False
    UPLOAD_COUNTER[emoji] += 1
    return True

def finish_upload(emoji):
    if UPLOAD_COUNTER.get(emoji, 0) > 0:
        UPLOAD_COUNTER[emoji] -= 1

def is_locked(emoji):
    return emoji in LOCKED_EMOJIS

def try_lock_emoji(emoji, player_id):
    if is_locked(emoji):
        return False
    LOCKED_EMOJIS[emoji] = player_id
    return True

def award_points(player_id, points):
    LEADERBOARD[player_id] = LEADERBOARD.get(player_id, 0) + points

def get_leaderboard(top_n=10):
    return sorted(LEADERBOARD.items(), key=lambda x: -x[1])[:top_n]
