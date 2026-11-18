import random
from player import Player
class GameData:
    def __init__(self):
        self.level=1
        self.coins=1000
        self.spins=10
        self.lineup = {
            "LS1": None,
            "LS2": None,
            "MB1": None,
            "MB2": None,
            "S": None,
            "RS": None,
            "L": None
        }

    def generate_player(self):
        r=random.random()
        rarity,base=('Common',60) if r<.7 else ('Rare',85) if r<.9 else ('Epic',115) if r<.98 else ('Legendary',150)
        return Player(random.choice(['Aoi','Kai','Ren','Mika']),random.choice(['LS','MB','S','RS','L']),rarity,base,base,base,base,base)
    def team_rating(self):

        total = 0
        count = 0

        for player in self.lineup.values():

            if player is not None:
                total += player.strength
                count += 1

        if count == 0:
            return 0

        return int(total / count)

    def lineup_complete(self):

        for player in self.lineup.values():

            if player is None:
                return False

        return True