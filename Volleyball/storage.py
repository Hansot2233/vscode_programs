import os
from save_manager import save_game,load_game

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_DIR = os.path.join(BASE_DIR,"accounts")

def get_user_folder(
    user_id
):

    folder = os.path.join(

        ACCOUNTS_DIR,

        user_id

    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    return folder

def get_save_path(
    user_id
):

    return os.path.join(

        get_user_folder(
            user_id
        ),

        "save.json"

    )

def get_settings_path(
    user_id
):

    return os.path.join(

        get_user_folder(
            user_id
        ),

        "settings.json"

    )

def get_stats_path(
    user_id
):

    return os.path.join(

        get_user_folder(
            user_id
        ),

        "stats.json"

    )

def save_user_game(
    user_id,
    game
):

    save_game(

        game,

        get_save_path(
            user_id
        )

    )

def load_user_game(
    user_id,
    game
):

    load_game(

        game,

        get_save_path(
            user_id
        )

    )