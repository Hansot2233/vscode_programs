import json
import os
from player import Player

def player_from_dict(data):
    return Player(
        data["name"],
        data["position"],
        data["rarity"],
        data["attack"],
        data["block"],
        data["receive"],
        data["setting"],
        data["serve"],
        data.get("level", 1),
        data.get("attack_level", 0),
        data.get("block_level", 0),
        data.get("receive_level", 0),
        data.get("setting_level", 0),
        data.get("serve_level", 0),
        data.get("prestige_level", 0),
        data.get("coins_spent", 0)
    )

def save_game(game, path):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    data = {

        "level": game.level,
        "battle_level": game.battle_level,
        "current_enemy_league": game.current_enemy_league,
        "current_enemy_team": [player.to_dict() for player in game.current_enemy_team] if game.current_enemy_team else None,
        "coins": game.coins,
        "gems": game.gems,
        "highest_team_rating": game.highest_team_rating,
        "highest_player_level_ever": game.highest_player_level_ever,
        "total_prestiges": game.total_prestiges,

        "roster": [
            player.to_dict()
            for player in game.roster
        ],

        "lineup": {
            slot:
            game.roster.index(player)
            if player is not None else None

            for slot, player
            in game.lineup.items()
        },
        # League progression
        "league_week": game.league_week,
        "league_schedule": game.league_schedule,

        "league_number": game.league_number,
        "league_top4_finishes": game.league_top4_finishes,

        # Deterministic league regeneration
        "league_seed": game.league_seed,
        "league_generation_strength": game.league_generation_strength,
        "league_minimum_percentage": game.league_minimum_percentage,

        # Standings only - no team or player objects
        "league_standings": {
            team["name"]: {
                "wins": team["wins"],
                "losses": team["losses"],
                "played": team["played"]
            }
            for team in game.league_teams
        },

        # Match results
        "league_results": game.league_results,
        "completed_league_matches": sorted(
            game.completed_league_matches
        ),

        # Playoff progress - team names only
        "playoff_active": game.playoff_active,

        "playoff_team_names": [
            team["name"]
            for team in game.playoff_teams
        ],

        "playoff_matchups": game.playoff_matchups,

        "playoff_history": game.playoff_history,

        "playoff_round": game.playoff_round,
        "battle_wins": game.battle_wins,
        "highest_stage": game.highest_stage,
        "total_upgrades": game.total_upgrades,
        "league_seasons_completed": game.league_seasons_completed,
        "league_championships": game.league_championships,
        "claimed_achievements": game.claimed_achievements,
        "claimed_milestones": game.claimed_milestones,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def load_game(game, path):

    if not os.path.exists(path):
        return

    try:

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        game.level = data.get("level", 1)
        game.battle_level = data.get("battle_level", 1)
        game.current_enemy_league = data.get("current_enemy_league",None)
        game.coins = data.get("coins", 1000)
        game.gems = data.get("gems", 100)
        game.highest_team_rating = data.get("highest_team_rating", 0)
        game.highest_player_level_ever = data.get("highest_player_level_ever", 0)
        game.total_prestiges = data.get("total_prestiges", 0)

        game.roster = [

            Player(
                p["name"],
                p["position"],
                p["rarity"],
                p["attack"],
                p["block"],
                p["receive"],
                p["setting"],
                p["serve"],
                p.get("level", 1),

                p.get("attack_level", 0),
                p.get("block_level", 0),
                p.get("receive_level", 0),
                p.get("setting_level", 0),
                p.get("serve_level", 0),
                p.get("prestige_level", 0),
                p.get("coins_spent", 0)
            )

            for p in data.get("roster", [])
        ]

        game.lineup = {}

        enemy_data = data.get(
            "current_enemy_team"
        )

        game.current_enemy_team = None

        if enemy_data:

            game.current_enemy_team = [

                Player(
                    p["name"],
                    p["position"],
                    p["rarity"],
                    p["attack"],
                    p["block"],
                    p["receive"],
                    p["setting"],
                    p["serve"],
                    p.get("level", 1),

                    p.get("attack_level", 0),
                    p.get("block_level", 0),
                    p.get("receive_level", 0),
                    p.get("setting_level", 0),
                    p.get("serve_level", 0)
                )

                for p in enemy_data

            ]

        # League progression
        game.league_week = data.get("league_week", 0)

        game.league_schedule = [
            [tuple(match) for match in week]
            for week in data.get("league_schedule", [])
        ]

        game.league_top4_finishes = data.get(
            "league_top4_finishes",
            0
        )

        game.league_number = data.get(
            "league_number",
            1
        )

        # Deterministic league regeneration
        game.league_seed = data.get(
            "league_seed"
        )

        game.league_generation_strength = data.get(
            "league_generation_strength"
        )

        game.league_minimum_percentage = data.get(
            "league_minimum_percentage",
            15
        )

        # Standings
        game.league_standings = data.get(
            "league_standings",
            {}
        )

        # Match results
        game.league_results = data.get(
            "league_results",
            {}
        )

        game.completed_league_matches = set(
            data.get("completed_league_matches", [])
        )

        # Playoff progress
        game.playoff_active = data.get(
            "playoff_active",
            False
        )

        game.playoff_team_names = data.get(
            "playoff_team_names",
            []
        )

        game.playoff_matchups = [
            tuple(matchup)
            for matchup in data.get("playoff_matchups", [])
        ]

        game.playoff_history = data.get(
            "playoff_history",
            []
        )

        game.playoff_round = data.get(
            "playoff_round",
            0
        )

        # Team objects are regenerated after loading.
        game.league_teams = []
        game.playoff_teams = []
        game.battle_wins = data.get("battle_wins", 0)
        game.highest_stage = data.get("highest_stage", 0)
        game.total_upgrades = data.get("total_upgrades", 0)
        game.league_seasons_completed = data.get("league_seasons_completed", 0)
        game.league_championships = data.get("league_championships", 0)
        game.claimed_achievements = data.get("claimed_achievements", [])
        game.claimed_milestones = data.get("claimed_milestones", [])

        for slot, index in data.get(
            "lineup",
            {}
        ).items():

            if index is None:

                game.lineup[slot] = None

            elif 0 <= index < len(game.roster):

                game.lineup[slot] = game.roster[index]

            else:

                game.lineup[slot] = None

    except Exception as e:

        print("Load failed:", e)

