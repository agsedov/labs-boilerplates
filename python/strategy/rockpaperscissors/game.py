from common import Game, GameState, Bot
from typing import Any, List, Dict
#Диспетчер для игры "камень-ножница-бумага"

class RockPaperScissorsGameState(GameState):
    def __init__(self):
        super().__init__()
        self.history = []  # История бросков
        self.N = 0 #Номер текущего "хода". Игроки делают броски по очереди, но проверка проводится после каждого второго хода
        self.firstPlayerMove = ""
        self.secondPlayerMove = ""
        self.winner = None
        self.game_over = False
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'history': self.history,
        })
        return base_dict

modulegameclass = "RockPaperScissorsGame"

class RockPaperScissorsGame(Game):
    def __init__(self):
        super().__init__()
        self.state = RockPaperScissorsGameState()

    def get_player_state(self, player_id: int) -> Any:
        return self.history

    def initialize_game(self, num_players):
        self.state = RockPaperScissorsGameState()
        return

    def is_valid_move(self, player_id, move):
        return True


    def apply_move(self, player_id: int, move: str) -> bool:
        if self.state.N % 2 == 0:
            self.state.firstPlayerMove = move
        else:
            self.state.secondPlayerMove = move
            self.state.history.append([self.state.firstPlayerMove, self.state.secondPlayerMove])
        self.state.N = self.state.N + 1

    def check_game_over(self) -> bool:
        if self.state.N%2 == 1:
            return False
        #print(self.state.firstPlayerMove, self.state.secondPlayerMove)

        if self.state.firstPlayerMove != self.state.secondPlayerMove:
            if self.state.firstPlayerMove == "rock":
                if self.state.secondPlayerMove == "scissors":
                    self.state.winner = 0
                else:
                    self.state.winner = 1
            if self.state.firstPlayerMove == "paper":
                if self.state.secondPlayerMove == "rock":
                    self.state.winner = 0
                else:
                    self.state.winner = 1
            if self.state.firstPlayerMove == "scissors":
                if self.state.secondPlayerMove == "paper":
                    self.state.winner = 0
                else:
                    self.state.winner = 1
            self.state.game_over = True
            return True

        return False

    def get_available_moves(self):
        return ["rock","paper","scissors"]
    # ... implement other abstract methods
