import random
import math
from enum import Enum

class Attack(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class WeightedRandy:
    def __init__(self, p):
        self.p = p
        assert( math.isclose(p[0]+p[1]+p[2], 1.) )

    def chooseAttack(self):
        x = random.random()
        if(x<self.p[0]):
            return Attack.ROCK
        if(x<self.p[0]+self.p[1]):
            return Attack.PAPER
        return Attack.SCISSORS

class BotGame:
    def __init__(self, N, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.N = N
        self.scores = [0,0]
        self.player1payoffs = [3, 4, 5]
        self.player2payoffs = [3, 3, 6]

    def whoWins(self, attack1, attack2):
        if attack1 == attack2:
            return 0 #draw
        if (attack1.value+1) % 3 == attack2.value:
            return 1 #player2 wins
        return -1 #player1 wins

    def gameRound(self):
        a1 = self.player1.chooseAttack()
        a2 = self.player2.chooseAttack()
        result = self.whoWins(a1,a2)
        if (result == 1):
            self.scores[1] += self.player2payoffs[a2.value]
        if (result == -1):
            self.scores[0] += self.player1payoffs[a1.value]

    def fullGame(self):
        for i in range(0,self.N):
            self.gameRound()


def printWinStats(bot1, bot2):
    wins = [0,0]
    for i in range(0,10000):
        game = BotGame(100, bot1, bot2)
        game.fullGame()
        if game.scores[0] > game.scores[1]:
            wins[0] += 1
        if game.scores[0] < game.scores[1]:
            wins[1] += 1
    print(wins)

printWinStats(WeightedRandy([1/3,1/3,1/3]), WeightedRandy([1/3, 1/3, 1/3]))
printWinStats(WeightedRandy([1/3,1/3,1/3]), WeightedRandy([1/6, 1/6, 4/6]))
printWinStats(WeightedRandy([4/6,1/6,1/6]), WeightedRandy([1/6, 1/6, 4/6]))
printWinStats(WeightedRandy([1,0,0]),       WeightedRandy([1/3, 1/3, 1/3]))
