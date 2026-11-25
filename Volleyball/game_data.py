import random
from player import Player
from player_database import PLAYER_DATABASE

class GameData:

    def __init__(self):

        self.level = 1
        self.battle_level = 1
        self.coins = 100
        self.gems = 50
        self.highest_team_rating = 15

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
        self.league_teams = []

        # Regular season progress
        self.league_results = {}
        self.completed_league_matches = set()
        self.league_schedule = []
        self.league_week = 0

        # Values used to regenerate the same opponents when loading a save
        self.league_seed = None
        self.league_generation_strength = None
        self.league_minimum_percentage = 15

        # Long-term league progression
        self.league_top4_finishes = 0
        self.league_number = 1

        # Saved playoff progress
        self.playoff_active = False
        self.playoff_teams = []
        self.playoff_matchups = []
        self.playoff_history = []
        self.playoff_round = 0

        # Standings snapshot; contains numbers, not team objects
        self.league_standings = {}

        self.playoff_active = False
        self.playoff_teams = []
        self.playoff_matchups = []
        self.playoff_history = []
        self.playoff_round = 0

        self.battle_wins = 0
        self.highest_stage = 0
        self.total_upgrades = 0
        self.league_seasons_completed = 0
        self.league_championships = 0
        self.highest_player_level_ever = 0
        self.total_prestiges = 0
        self.claimed_achievements = []
        self.claimed_milestones = []

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
    def update_highest_team_rating(self):

        players = [
            player
            for player in self.lineup.values()
            if player is not None
        ]

        if not players:
            return

        current_rating = sum(
            player.strength for player in players
        ) / len(players)

        self.highest_team_rating = max(
            self.highest_team_rating,
            current_rating
        )