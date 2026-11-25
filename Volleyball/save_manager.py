import json
import os

from player import Player


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

        "league_teams": [

            {
                "name": team["name"],

                "wins": team["wins"],

                "losses": team["losses"],

                "played": team["played"],

                "battle_level": team["battle_level"],

                "lineup": [

                    player.to_dict()

                    for player in team["lineup"]

                ]
            }

            for team in game.league_teams

        ],
        "league_week": game.league_week,
        "league_schedule": game.league_schedule,
        "league_top4_finishes": game.league_top4_finishes,
        "league_number": game.league_number,
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

        game.league_teams = []

        for team in data.get(
            "league_teams",
            []
        ):

            game.league_teams.append({

                "name": team["name"],

                "wins": team["wins"],

                "losses": team["losses"],

                "played": team["played"],

                "battle_level": team["battle_level"],

                "lineup": [

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

                    for p in team["lineup"]

                ]

            })

        game.completed_league_matches = set(data.get("completed_league_matches", []))
        game.league_week = data.get("league_week", 0)
        game.league_schedule = data.get("league_schedule", [])
        game.league_top4_finishes = data.get("league_top4_finishes", 0)
        game.league_number = data.get("league_number", 1)
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

