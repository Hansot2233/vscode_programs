import random
from player import Player
from player_database import PLAYER_DATABASE

class GameData:

    def __init__(self):

        self.level = 1
        self.battle_level = 1
        self.coins = 1000
        self.gems = 100

        # All owned players
        self.roster = []

        for data in PLAYER_DATABASE["Starter"]:

            self.roster.append(
                Player(
                    data["name"],
                    data["position"],
                    "Starter",
                    data["attack"],
                    data["block"],
                    data["receive"],
                    data["setting"],
                    data["serve"]
                )
            )

        # Active team
        self.lineup = {
            "LS1": self.roster[0],
            "LS2": self.roster[1],
            "MB1": self.roster[2],
            "MB2": self.roster[3],
            "S": self.roster[5],
            "RS": self.roster[4],
            "L": self.roster[6]
        }

        self.current_enemy_team = None
        self.current_enemy_league = None

    def generate_player(self):

        r = random.random()

        if r < 0.70:
            rarity = "Common"

        elif r < 0.90:
            rarity = "Rare"

        elif r < 0.98:
            rarity = "Epic"

        else:
            rarity = "Legendary"

        data = random.choice(
            PLAYER_DATABASE[rarity]
        )

        return Player(
            name=data["name"],
            position=data["position"],
            rarity=rarity,

            attack=data["attack"],
            block=data["block"],
            receive=data["receive"],
            setting=data["setting"],
            serve=data["serve"]
        )

    def team_rating(self):

        players = [
            p
            for p in self.lineup.values()
            if p is not None
        ]

        if not players:
            return 0

        return int(
            sum(p.strength for p in players)
            / len(players)
        )

    def lineup_complete(self):

        return all(
            player is not None
            for player in self.lineup.values()
        )

    def generate_player_of_rarity(self, rarity):

        data = random.choice(
            PLAYER_DATABASE[rarity]
        )

        return Player(
            name=data["name"],
            position=data["position"],
            rarity=rarity,
            attack=data["attack"],
            block=data["block"],
            receive=data["receive"],
            setting=data["setting"],
            serve=data["serve"]
        )

    def get_current_enemy(self):

        if self.current_enemy_team is None:

            from battle_engine import get_enemy_team

            self.current_enemy_team, self.current_enemy_league = (
                get_enemy_team(
                    self.battle_level
                )
            )

        return (
            self.current_enemy_team,
            self.current_enemy_league
        )
