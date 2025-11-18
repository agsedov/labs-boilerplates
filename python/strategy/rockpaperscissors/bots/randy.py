from common import Bot
import random

class Randy(Bot):
    """Random bot for rock paper scissors"""

    def make_move(self, player_state):
        return random.choice(["rock","paper","scissors"])

    def get_bot_info(self):
        return {
            'name': 'RandomBot',
            'author': 'System',
            'description': 'Makes random valid moves'
        }
