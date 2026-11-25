from battle_engine import simulate_match
import random
from league_factory import generate_league_teams

def get_team_strength(team):

    if not team:
        return 0

    players = (
        team.values()
        if isinstance(team, dict)
        else team
    )

    players = [
        player for player in players
        if player is not None
    ]

    if not players:
        return 0

    return sum(
        player.strength for player in players
    ) / len(players)

def create_league(game, resume=False):

    is_resuming = (
        resume and game.league_seed is not None
    )

    your_lineup = [
        p
        for p in game.lineup.values()
        if p is not None
    ]

    # -------------------------------------------------
    # LOAD EXISTING SEASON SETTINGS
    # -------------------------------------------------

    if is_resuming:

        seed = game.league_seed

        player_strength = game.league_generation_strength

        minimum_percentage = game.league_minimum_percentage

        saved_week = game.league_week

        saved_schedule = game.league_schedule

        saved_standings = game.league_standings

        saved_results = game.league_results

        saved_completed = game.completed_league_matches

        saved_playoff_active = game.playoff_active

        saved_playoff_names = getattr(
            game,
            "playoff_team_names",
            []
        )

        saved_matchups = game.playoff_matchups

        saved_history = game.playoff_history

        saved_round = game.playoff_round

    else:

        # -------------------------------------------------
        # GENERATE A NEW SEASON
        # -------------------------------------------------

        seed = random.randrange(0, 2**32)

        # Update the permanent highest team rating.
        game.update_highest_team_rating()

        # Use the highest rating ever achieved.
        player_strength = game.highest_team_rating

        league_minimum = min(
            15 + ((game.league_number - 1) * 5),
            90
        )

        top4_minimum = min(
            15 + (game.league_top4_finishes * 5),
            90
        )

        minimum_percentage = min(
            max(league_minimum, top4_minimum),
            90
        )

        game.league_week = 0

        game.league_results = {}

        game.completed_league_matches = set()

        game.league_standings = {}

        game.playoff_active = False

        game.playoff_teams = []

        game.playoff_matchups = []

        game.playoff_history = []

        game.playoff_round = 0

    # Store the generation information.
    game.league_seed = seed

    game.league_generation_strength = player_strength

    game.league_minimum_percentage = minimum_percentage

    game.league_teams = []

    # -------------------------------------------------
    # REGENERATE THE SAME OPPONENTS
    # -------------------------------------------------

    rng = random.Random(seed)

    game.league_teams.append({

        "name": "Your Team",

        "lineup": your_lineup,

        "wins": 0,
        "losses": 0,
        "played": 0,

        "battle_level": game.battle_level

    })

    opponents = generate_league_teams(
        game.league_number,
        player_strength,
        minimum_percentage,
        rng
    )

    game.league_teams.extend(opponents)

    # Create the schedule.
    create_schedule(game)

    # -------------------------------------------------
    # RESTORE EXISTING SEASON PROGRESS
    # -------------------------------------------------

    if is_resuming:

        game.league_schedule = saved_schedule

        game.league_week = saved_week

        game.league_results = saved_results

        game.completed_league_matches = set(
            saved_completed
        )

        # Restore standings using team names.
        for team in game.league_teams:

            stats = saved_standings.get(
                team["name"],
                {}
            )

            team["wins"] = stats.get("wins", 0)

            team["losses"] = stats.get("losses", 0)

            team["played"] = stats.get("played", 0)

        # Restore playoff progress.
        team_lookup = {
            team["name"]: team
            for team in game.league_teams
        }

        game.playoff_active = saved_playoff_active

        game.playoff_teams = [
            team_lookup[name]
            for name in saved_playoff_names
            if name in team_lookup
        ]

        game.playoff_matchups = saved_matchups

        game.playoff_history = saved_history

        game.playoff_round = saved_round

    # Store a fresh standings snapshot.
    game.league_standings = {
        team["name"]: {
            "wins": team["wins"],
            "losses": team["losses"],
            "played": team["played"]
        }
        for team in game.league_teams
    }

def simulate_other_matches(game, excluded_teams=None):

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

        schedule.append(round_matches)

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