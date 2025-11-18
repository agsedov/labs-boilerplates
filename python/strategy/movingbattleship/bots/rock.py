from common import Bot
import random

class Rock(Bot):
    def make_move(self, player_state):
        if(player_state['N']<6):#Просто ставим корабли куда-то на диагональ
            return "place_"+str(player_state['N'])+"_"+str(player_state['N'])
        else:
            n = (player_state['N'] - player_state['N']%2)>>1

            #стреляем по всем клеткам 1 по 100
            return "shoot_"+str(n%10)+"_"+str(int(((n-n%10)%100)/10))

    def get_bot_info(self):
        return {
            'name': 'Admiral Rock',
            'author': 'System',
            'description': 'dumb as rock'
        }
