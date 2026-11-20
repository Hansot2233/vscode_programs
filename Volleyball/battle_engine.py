import random
from player_database import PLAYER_DATABASE
from player import Player
from copy import deepcopy

POSITION_WEIGHTS = {
    "LS": 1.0,
    "MB": 1.0,
    "RS": 1.1,
    "S": 1.15,
    "L": 0.9
}

RARITY_FALLBACKS = {
    "Legendary": ["Legendary", "Epic", "Rare", "Common", "Starter"],
    "Epic": ["Epic", "Rare", "Common", "Starter"],
    "Rare": ["Rare", "Common", "Starter"],
    "Common": ["Common", "Starter"],
    "Starter": ["Starter"]
}



def build_player(data, rarity):

    return Player(
        data["name"],
        data["position"],
        rarity,
        data["attack"],
        data["block"],
        data["receive"],
        data["setting"],
        data["serve"]
    )

def calculate_team_stats(players):

    attack = 0
    block = 0
    receive = 0
    setting = 0
    serve = 0

    for player in players:

        attack += player.attack
        block += player.block
        receive += player.receive
        setting += player.setting
        serve += player.serve

    count = len(players)

    return {
        "attack": attack / count,
        "block": block / count,
        "receive": receive / count,
        "setting": setting / count,
        "serve": serve / count
    }

def rally_power(players):

    attack = 0
    block = 0
    receive = 0
    setting = 0
    serve = 0

    total_weight = 0

    for player in players:

        weight = POSITION_WEIGHTS[
            player.position
        ]

        attack += player.attack * weight
        block += player.block * weight
        receive += player.receive * weight
        setting += player.setting * weight
        serve += player.serve * weight

        total_weight += weight

    attack /= total_weight
    block /= total_weight
    receive /= total_weight
    setting /= total_weight
    serve /= total_weight

    return (
        attack * 0.35 +
        block * 0.15 +
        receive * 0.20 +
        setting * 0.20 +
        serve * 0.10
    )

def play_rally(player_team,enemy_team):

    player_power = (
        rally_power(player_team)
        *
        random.uniform(
            0.95,
            1.05
        )
    )

    enemy_power = (
        rally_power(enemy_team)
        *
        random.uniform(
            0.95,
            1.05
        )
    )

    difference = (
        player_power -
        enemy_power
    )
    win_chance = (
        0.5 +
        difference / 250
    )
    win_chance = max(0.10,min(0.90,win_chance))

    return (random.random() < win_chance)

def play_set(player_team,enemy_team):

    player_score = 0
    enemy_score = 0

    while True:

        if play_rally(
            player_team,
            enemy_team
        ):

            player_score += 1

        else:

            enemy_score += 1

        if (

            player_score >= 25
            or
            enemy_score >= 25

        ) and (

            abs(
                player_score -
                enemy_score
            ) >= 2

        ):

            return (
                player_score,
                enemy_score
            )
        
def simulate(player_lineup,game):
        
    player_team = [p for p in player_lineup.values() if p is not None]

    enemy_team, league = (game.get_current_enemy())

    player_sets = 0
    enemy_sets = 0

    set_scores = []

    while (player_sets < 3 and enemy_sets < 3):

        p,e = play_set(
            player_team,
            enemy_team
        )

        set_scores.append(
            f"{p}-{e}"
        )

        if p > e:

            player_sets += 1

        else:

            enemy_sets += 1

    winner = (player_sets > enemy_sets)
    return (
        winner,
        set_scores,
        league
    )


def get_player_for_position(position, rarity):

    for tier in RARITY_FALLBACKS[rarity]:

        candidates = [

            p

            for p in PLAYER_DATABASE[tier]

            if p["position"] == position

        ]

        if candidates:

            player_data = random.choice(candidates)

            return build_player(
                player_data,
                tier
            )

    return None

def get_enemy_team(level):

    progression = [

        (5,  "Starter",    0),

        (10, "Common",     2),
        (15, "Common",     4),
        (20, "Common",     7),

        (25, "Rare",       2),
        (30, "Rare",       4),
        (35, "Rare",       7),

        (40, "Epic",       2),
        (45, "Epic",       4),
        (50, "Epic",       7),

        (55, "Legendary",  1),
        (60, "Legendary",  2),
        (65, "Legendary",  2)
    ]

    target_rarity = "Starter"
    target_count = 0

    for max_level, rarity, count in progression:

        if level <= max_level:

            target_rarity = rarity
            target_count = count

            break

    else:

        target_rarity = "Legendary"
        target_count = 7

    display_count = target_count

    previous_tier = {
        "Starter": "Starter",
        "Common": "Starter",
        "Rare": "Common",
        "Epic": "Rare",
        "Legendary": "Epic"
    }

    fallback_rarity = previous_tier[
        target_rarity
    ]

    required_positions = [
        "LS",
        "LS",
        "MB",
        "MB",
        "S",
        "RS",
        "L"
    ]

    enemy_players = [None] * 7

    #
    # LEGENDARY SPECIAL HANDLING
    #

    if target_rarity == "Legendary":

        # Level 51-55:
        # no guaranteed legendary yet

        if level <= 55:

            legendary_slots = []

        # Level 56-60:
        # guarantee either Gojo OR Yujiro

        elif level <= 60:

            legendary_slots = random.sample(
                [4, 5],  # S or RS
                1
            )

        # Level 61+:
        # guarantee both

        else:

            legendary_slots = [4, 5]

        for slot in legendary_slots:

            # Gojo
            if slot == 4:

                enemy_players[slot] = build_player(
                    PLAYER_DATABASE["Legendary"][1],
                    "Legendary"
                )

            # Yujiro
            elif slot == 5:

                enemy_players[slot] = build_player(
                    PLAYER_DATABASE["Legendary"][0],
                    "Legendary"
                )

        target_count -= len(
            legendary_slots
        )

    #
    # PICK RANDOM UPGRADED POSITIONS
    #

    available_slots = [

        i

        for i in range(7)

        if enemy_players[i] is None

    ]

    upgraded_slots = set(

        random.sample(
            available_slots,
            min(
                target_count,
                len(available_slots)
            )
        )

    )

    #
    # BUILD LINEUP
    #

    for index, position in enumerate(
        required_positions
    ):

        if enemy_players[index] is not None:
            continue

        if index in upgraded_slots:

            rarity_used = target_rarity

        else:

            rarity_used = fallback_rarity

        enemy_players[index] = (
            get_player_for_position(
                position,
                rarity_used
            )
        )

    if level <= 5:
        multiplier = 1.00 + ((level - 1) * 0.03)

    elif level <= 10:
        multiplier = 1.00 + ((level - 6) * 0.03)

    elif level <= 15:
        multiplier = 1.00 + ((level - 11) * 0.03)

    elif level <= 20:
        multiplier = 1.00 + ((level - 16) * 0.03)

    elif level <= 25:
        multiplier = 1.00 + ((level - 21) * 0.03)

    elif level <= 30:
        multiplier = 1.00 + ((level - 26) * 0.03)

    elif level <= 35:
        multiplier = 1.00 + ((level - 31) * 0.03)

    elif level <= 40:
        multiplier = 1.00 + ((level - 36) * 0.03)

    elif level <= 45:
        multiplier = 1.00 + ((level - 41) * 0.03)

    elif level <= 50:
        multiplier = 1.00 + ((level - 46) * 0.03)

    elif level <= 55:
        multiplier = 1.00 + ((level - 51) * 0.03)

    elif level <= 60:
        multiplier = 1.00 + ((level - 56) * 0.03)

    elif level <= 65:
        multiplier = 1.00 + ((level - 61) * 0.03)

    else:
        multiplier = 1.15 + ((level - 65) * 0.02)

    enemy_players = apply_multiplier(
        enemy_players,
        multiplier
    )


    league = (
        f"{target_rarity} Tier "
        f"({display_count}/7)"
        f" | {multiplier:.2f}x"
    )


    return (
        enemy_players,
        league
    )

def apply_multiplier(players, multiplier):

    for player in players:

        player.attack = int(
            player.attack * multiplier
        )

        player.block = int(
            player.block * multiplier
        )

        player.receive = int(
            player.receive * multiplier
        )

        player.setting = int(
            player.setting * multiplier
        )

        player.serve = int(
            player.serve * multiplier
        )

    return players