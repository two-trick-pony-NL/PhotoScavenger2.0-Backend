from datetime import datetime, timedelta
from .emoji import EMOJI_TO_CLASS
import random

ROUND_DURATION = 30
NUM_EMOJIS_PER_ROUND = 16
BASE_POINTS = 10           # max points per emoji
DECAY_RATE = 0.90         # fade leaderboard per round
MAX_LEADERBOARD_SIZE = 50
ROUND_ACTIVE = False
ROUND_LOCKED = False      # True during pre-round countdown or active round
ROUND_END_TIME = None
ROUND_EMOJIS = []
LOCKED_EMOJIS = {}
UPLOAD_COUNTER = {}
LEADERBOARD = {}
EMOJIS = list(EMOJI_TO_CLASS.keys())




def init_round(num_emojis=NUM_EMOJIS_PER_ROUND):
    global ROUND_EMOJIS, LOCKED_EMOJIS, UPLOAD_COUNTER, ROUND_END_TIME, LEADERBOARD
    
    # decay all leaderboard points so top scorers fade over time
    for player in LEADERBOARD:
        LEADERBOARD[player] *= DECAY_RATE
    
    # trim leaderboard to top N players
    top_players = sorted(LEADERBOARD.items(), key=lambda x: -x[1])[:MAX_LEADERBOARD_SIZE]
    LEADERBOARD = dict(top_players)

    # pick `num_emojis` unique emojis for this round
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


def award_points(player_id):
    """Award points proportional to remaining round time"""
    remaining_time = (ROUND_END_TIME - datetime.utcnow()).total_seconds()
    if remaining_time < 0:
        remaining_time = 0
    points = max(int(BASE_POINTS * remaining_time), 1)
    LEADERBOARD[player_id] = LEADERBOARD.get(player_id, 0) + points
    return points


def get_leaderboard(top_n=10):
    return [(user, round(points)) for user, points in sorted(LEADERBOARD.items(), key=lambda x: -x[1])[:top_n]]
