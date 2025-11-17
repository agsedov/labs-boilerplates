from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
import importlib
import os

class GameState:
    """Base class for game state"""
    def __init__(self):
        self.game_over = False
        self.winner = None
        self.current_player = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            'game_over': self.game_over,
            'winner': self.winner,
            'current_player': self.current_player
        }

class Bot(ABC):
    """Abstract base class for all bots"""

    def __init__(self, bot_id: int):
        self.bot_id = bot_id

    @abstractmethod
    def make_move(self, game_state: GameState, player_state: Any) -> int:
        """
        Make a move in the game

        Args:
            game_state: Current state of the game
            player_state: Bot's private state information

        Returns:
            move_code: Integer representing the chosen move
        """
        pass

    def get_bot_info(self) -> Dict[str, str]:
        """Return bot metadata"""
        return {
            'name': self.__class__.__name__,
            'author': 'Unknown',
            'description': 'No description provided'
        }

class Game(ABC):
    """Abstract base class for all games"""

    def __init__(self):
        self.state = GameState()
        self.players = []
        self.history = []

    @abstractmethod
    def initialize_game(self, num_players: int = 2) -> None:
        """Initialize the game with given number of players"""
        pass

    @abstractmethod
    def get_player_state(self, player_id: int) -> Any:
        """
        Get the state information visible to a specific player

        Args:
            player_id: ID of the player

        Returns:
            Player-specific state information
        """
        pass

    @abstractmethod
    def apply_move(self, player_id: int, move: str) -> bool:
        """
        Apply a move to the game state

        Args:
            player_id: ID of the player making the move
            move: Move code

        Returns:
            success: True if move was valid and applied
        """
        pass

    @abstractmethod
    def is_valid_move(self, player_id: int, move: str) -> bool:
        """Check if a move is valid for the current state"""
        pass

    @abstractmethod
    def get_available_moves(self, player_id: int) -> List[str]:
        """Get list of available moves for a player"""
        pass

    @abstractmethod
    def check_game_over(self) -> bool:
        """Check if the game has ended"""
        pass

    def get_game_info(self) -> Dict[str, Any]:
        """Return game metadata"""
        return {
            'name': self.__class__.__name__,
            'min_players': 2,
            'max_players': 2,
            'description': 'No description provided'
        }

class GameResult:
    """Class to store game results"""
    def __init__(self):
        self.winner = None
        self.scores = {}
        self.moves_played = 0
        self.reason = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'winner': self.winner,
            'scores': self.scores,
            'moves_played': self.moves_played,
            'reason': self.reason
        }

class BotLoader:
    """Utility class to load bots from files"""

    @staticmethod
    def load_bot(game_name: str, bot_name: str, bot_id: int) -> Bot:
        """
        Load a bot from the bots directory

        Args:
            game_name: Name of the game subdirectory
            bot_name: Name of the bot file (without .py)
            bot_id: ID to assign to the bot

        Returns:
            Loaded bot instance
        """
        try:
            module_path = f"{game_name}.bots.{bot_name}"
            module = importlib.import_module(module_path)

            # Find the bot class (assumes class name matches file name in CamelCase)
            class_name = ''.join(word.capitalize() for word in bot_name.split('_'))
            bot_class = getattr(module, class_name)

            return bot_class(bot_id)

        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to load bot {bot_name} for game {game_name}: {e}")

    @staticmethod
    def list_available_bots(game_name: str) -> List[str]:
        """List all available bots for a game"""
        bots_dir = os.path.join(game_name, "bots")
        if not os.path.exists(bots_dir):
            return []

        bots = []
        for file in os.listdir(bots_dir):
            if file.endswith('.py') and not file.startswith('_'):
                bots.append(file[:-3])  # Remove .py extension
        return bots

class GameLoader:
    """Utility class to load games"""

    @staticmethod
    def load_game(game_name: str) -> Game:
        """
        Load a game from the games directory

        Args:
            game_name: Name of the game subdirectory

        Returns:
            Loaded game instance
        """
        try:
            module_path = f"{game_name}.game"
            module = importlib.import_module(module_path)

            game_class_name = getattr(module, "modulegameclass")
            print(game_class_name)
            # Find the game class (assumes class name is Game)
            game_class = getattr(module, game_class_name)

            return game_class()

        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to load game {game_name}: {e}")

    @staticmethod
    def list_available_games() -> List[str]:
        """List all available games"""
        games = []
        for item in os.listdir('.'):
            if os.path.isdir(item) and not item.startswith('_'):
                game_file = os.path.join(item, 'game.py')
                if os.path.exists(game_file):
                    games.append(item)
        return games
