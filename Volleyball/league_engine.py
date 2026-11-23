from battle_engine import get_enemy_team, simulate_match
import random

TEAM_NAMES = [

    "Karasuno",
    "Nekoma",
    "Aoba Johsai",
    "Shiratorizawa",

    "Fukurodani",
    "Date Tech",
    "Inarizaki",
    "Kamomedai",

    "Nohebi",
    "Johzenji",
    "Wakutani",

    "Shinzen",
    "Mujinazaka",
    "Tsubakihara",

    "Ubugawa"
]

def create_league(game):

    game.league_teams = []
    game.completed_league_matches = set()

    game.league_teams.append({

        "name": "Your Team",

        "lineup": [
            p
            for p in game.lineup.values()
            if p is not None
        ],

        "wins": 0,

        "losses": 0,

        "played": 0,

        "battle_level": game.battle_level

    })

    for name in TEAM_NAMES:

        battle_level = max(
            1,
            game.battle_level +
            random.randint(-3, 3)
        )

        lineup, _ = get_enemy_team(
            battle_level
        )

        game.league_teams.append({

            "name": name,

            "lineup": lineup,

            "wins": 0,

            "losses": 0,

            "played": 0,

            "battle_level": battle_level

        })

    create_schedule(game)

def simulate_other_matches(game,excluded_teams=None):

    if excluded_teams is None:
        excluded_teams = set()

    teams = [

        t

        for t in game.league_teams

        if t["name"] not in excluded_teams

    ]

    random.shuffle(teams)

    while len(teams) >= 2:

        team_a = teams.pop()

        team_b = teams.pop()

        winner, _ = simulate_match(
            team_a["lineup"],
            team_b["lineup"]
        )

        if winner:

            team_a["wins"] += 1
            team_b["losses"] += 1

        else:

            team_b["wins"] += 1
            team_a["losses"] += 1

        team_a["played"] += 1
        team_b["played"] += 1

def create_schedule(game):

    teams = [
        team["name"]
        for team in game.league_teams
    ]

    schedule = []

    teams = teams[:]

    for _ in range(len(teams) - 1):

        round_matches = []

        for i in range(len(teams) // 2):

            round_matches.append(
                (
                    teams[i],
                    teams[-(i + 1)]
                )
            )

        schedule.append(
            round_matches
        )

        teams = (
            [teams[0]]
            +
            [teams[-1]]
            +
            teams[1:-1]
        )

    game.league_schedule = schedule
    game.league_week = 0

def get_current_match(game):

    if game.league_week >= len(
        game.league_schedule
    ):
        return None

    week = game.league_schedule[
        game.league_week
    ]

    for team_a, team_b in week:

        if team_a == "Your Team":

            return team_b

        if team_b == "Your Team":

            return team_a

    return None