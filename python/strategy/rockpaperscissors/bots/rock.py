from common import Bot
import random

class Rock(Bot):
    """Bot for rock paper scissors"""

    def make_move(self, player_state):
        return "rock"

    def get_bot_info(self):
        return {
            'name': 'RockBot',
            'author': 'System',
            'description': 'Likes rocks'
        }
