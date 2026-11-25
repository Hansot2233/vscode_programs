import random
from player import Player

from league_constants import (
    TEAM_ROSTERS,
    PLAYER_LOOKUP,
    LEAGUE_TEAM_NAMES
)

def create_player(name):

    data = PLAYER_LOOKUP[name]

    return Player(

        data["name"],

        data["position"],

        data["rarity"],

        data["attack"],
        data["block"],
        data["receive"],
        data["setting"],
        data["serve"]

    )

def scale_player(player, target_strength):

    current_strength = player.strength

    if current_strength <= 0:
        return player

    # Calculate how much the player's stats need to increase.
    multiplier = target_strength / current_strength

    # Scale the actual player stats.
    player.attack = max(1, round(player.attack * multiplier))
    player.block = max(1, round(player.block * multiplier))
    player.receive = max(1, round(player.receive * multiplier))
    player.setting = max(1, round(player.setting * multiplier))
    player.serve = max(1, round(player.serve * multiplier))

    return player

def generate_league_team(team_name, target_strength):

    roster = TEAM_ROSTERS[team_name]

    lineup = {}

    for position, player_name in roster.items():

        player = create_player(player_name)

        scale_player(player, target_strength)

        lineup[position] = player

    return lineup


def generate_league_teams(
    league_number,
    player_strength,
    minimum_percentage=None,
    rng=None
):

    if rng is None:
        rng = random

    if minimum_percentage is None:
        minimum_percentage = min(
            15 + ((league_number - 1) * 5),
            90
        )

    maximum_percentage = 105
    teams = []

    for name in LEAGUE_TEAM_NAMES:

        percentage = rng.uniform(
            minimum_percentage,
            maximum_percentage
        )

        target_strength = (
            player_strength * percentage / 100
        )

        teams.append({
            "name": name,
            "wins": 0,
            "losses": 0,
            "played": 0,
            "lineup": generate_league_team(
                name,
                target_strength
            )
        })

    return teams