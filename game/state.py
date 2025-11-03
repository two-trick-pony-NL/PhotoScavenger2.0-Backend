from datetime import datetime, timedelta

ROUND_DURATION = 60
ROUND_ACTIVE = False
ROUND_LOCKED = False      # True during pre-round countdown or active round
ROUND_END_TIME = None
ROUND_EMOJIS = []
LOCKED_EMOJIS = {}
UPLOAD_COUNTER = {}
LEADERBOARD = {}
EMOJIS = ["🍎", "🍌", "🍇"]

def init_round(emojis=None):
    global ROUND_EMOJIS, LOCKED_EMOJIS, UPLOAD_COUNTER, ROUND_END_TIME
    ROUND_EMOJIS = emojis.copy() if emojis else EMOJIS.copy()
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
