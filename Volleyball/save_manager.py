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
        }
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
                p.get("serve_level", 0)
            )

            for p in data.get("roster", [])
        ]

        game.lineup = {}

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