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
        "spins": game.spins,
        "lineup": {
            slot:
            game.roster.index(player)
            if player else None
            for slot, player
            in game.lineup.items()
        }
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_game(game, path):

    if not os.path.exists(path):
        return

    try:
        with open(path, "r") as f:
            d = json.load(f)

        game.level = d["level"]
        game.coins = d["coins"]
        game.spins = d["spins"]

        game.roster = [
            Player(**p)
            for p in d["roster"]
        ]

        game.lineup = {}

        for slot, index in d["lineup"].items():

            if index is None:

                game.lineup[slot] = None

            else:

                game.lineup[slot] = game.roster[index]

    except Exception as e:
        print("Load failed:", e)
