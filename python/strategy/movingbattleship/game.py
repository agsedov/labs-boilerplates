from common import Game, GameState, Bot
from typing import Any, List, Dict
#Диспетчер для игры

class MovingBattleshipGameState(GameState):
    def __init__(self):
        super().__init__()
        self.historyA = []  # История ходов, как её видит первый игрок
        self.historyB = []  # История ходов, как её видит второй игрок
        self.positions = [None,None,None,None,None,None]
        self.N = 0 # Номер текущего хода
        self.winner = None
        self.game_over = False
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'historyA': self.historyA,
        })
        return base_dict

modulegameclass = "MovingBattleshipGame"

class MovingBattleshipGame(Game):
    def __init__(self):
        super().__init__()
        self.state = MovingBattleshipGameState()

    def get_player_state(self, player_id: int) -> Any:
        if player_id == 0:
            return {'history':self.state.historyB,
                    'ship1':self.state.positions[0],
                    'ship2':self.state.positions[2],
                    'ship3':self.state.positions[4],
                    'N':self.state.N
                    }
        else:
            return {'history':self.state.historyA,
                    'ship1':self.state.positions[1],
                    'ship2':self.state.positions[3],
                    'ship3':self.state.positions[5],
                    'N':self.state.N
                    }

    def initialize_game(self, num_players):
        self.state = MovingBattleshipGameState()
        return

    def is_valid_move(self, player_id, move):
        return True

    def _parseposition(self, s: str):
        valid = (len(s) == 3 and s[0] in '0123456789' and s[1] == '_' and s[2] in '0123456789')
        if not valid:
            raise Exception("Invalid position "+s)
        return [int(s[0]),int(s[2])]

    def _check_collision(self, ship1, ship2, ship3):
        if (ship1 == None) or (ship2==None) or ((ship1[0] == ship2[0]) and (ship1[1] == ship2[1])):
            return True
        if (ship3 == None) or ((ship1[0] == ship3[0]) and (ship1[1] == ship3[1])):
            return True
        if (ship2[0] == ship3[0]) and (ship2[1] == ship3[1]):
            return True
        return False

    def _make_reveal(self, player_id, ship_n, probability):
        pass

    def _make_blast(self, player_id, position):
        pass
    def _check_hit(self, ship_n, position):
        if self.state.positions[ship_n] == None:
            return False
        pos = self.state.positions[ship_n]
        if (pos[0] == position[0]) and (pos[1] == position[1]):
            self.state.positions[ship_n] = None
            return True

    def _change_pos(self, move, position):
        if position == None:
            raise Exception("sunk ship is trying to move")

        if move == "move_r":
            position[0] = position[0] + 1
            if position[0] > 9:
                raise Exception("ship is trying to flee")
        if move == "move_l":
            position[0] = position[0] - 1
            if position[0] < 0:
                raise Exception("ship is trying to flee")
        if move == "move_d":
            position[1] = position[1] + 1
            if position[1] > 9:
                raise Exception("ship is trying to flee")
        if move == "move_u":
            position[1] = position[1] - 1
            if position[1] < 0:
                raise Exception("ship is trying to flee")
        return position


    def apply_move(self, player_id: int, move: str) -> bool:
        if self.state.N<6:
            command,_,position_string = move.partition('_')
            if command != 'place':
                raise Exception("First six moves are for ship placing")
            self.state.positions[self.state.N] = self._parseposition(position_string)

            if self.state.N == 4:
                ship1 = self.state.positions[0]
                ship2 = self.state.positions[2]
                ship3 = self.state.positions[4]
                if self._check_collision(ship1,ship2,ship3):
                    raise Exception("Two ships are in the same square")
            if self.state.N == 5:
                ship1 = self.state.positions[1]
                ship2 = self.state.positions[3]
                ship3 = self.state.positions[5]
                if self._check_collision(ship1,ship2,ship3):
                    raise Exception("Two ships are in the same square")

            self.state.N = self.state.N + 1
            return

        ship_n = self.state.N%6
        if self.state.positions[ship_n] == None:
            raise Exception("sunk ship gives commands")

        if move == "wait":
            _make_reveal(player_id,ship_n, 0.1)
            self.state.N = self.state.N + 1
            return

        if move in ["move_r", "move_l", "move_u", "move_d"]:
            self.state.positions[ship_n] = _change_pos(move, self.state.positions[ship_n])

            if N % 2 == 0:
                ship1 = self.state.positions[0]
                ship2 = self.state.positions[2]
                ship3 = self.state.positions[4]
                if self._check_collision(ship1,ship2,ship3):
                    raise Exception("Two ships are in the same square")
            else:
                ship1 = self.state.positions[1]
                ship2 = self.state.positions[3]
                ship3 = self.state.positions[5]
                if self._check_collision(ship1,ship2,ship3):
                    raise Exception("Two ships are in the same square")

            self.state.N = self.state.N + 1
            self._make_reveal(player_id,ship_n, 0.1)
            return

        command,_,position_string = move.partition('_')
        if command == 'shoot':
            position = self._parseposition(position_string)
            self._make_blast(player_id, position)
            if self.state.N % 2 == 0:
                self._check_hit(1, position)
                self._check_hit(3, position)
                self._check_hit(5, position)
            else:
                self._check_hit(0, position)
                self._check_hit(2, position)
                self._check_hit(4, position)

            self.state.N = self.state.N + 1
            self._make_reveal(player_id,ship_n,1.0)
            return
        raise Exception("unknown command from bot:"+move)


    def check_game_over(self) -> bool:
        if self.state.N < 6:
            return False

        if (self.state.positions[0] is None) and\
        (self.state.positions[2] is None) and\
        (self.state.positions[4] is None):
            self.state.game_over = True
            self.state.winner = 1
            return True

        if (self.state.positions[1] is None) and\
        (self.state.positions[3] is None) and\
        (self.state.positions[5] is None):
            self.state.game_over = True
            self.state.winner = 0
            return True

        return False

    def get_available_moves(self):
        return ["rock","paper","scissors"]
    # ... implement other abstract methods
