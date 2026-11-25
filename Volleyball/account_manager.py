import json, uuid, os, shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_ACCOUNTS_DIR = os.path.join(BASE_DIR,"accounts")
ACCOUNTS_FILE = os.path.join(BASE_ACCOUNTS_DIR, "accounts.json")

def load_accounts():

    os.makedirs(

        BASE_ACCOUNTS_DIR,

        exist_ok=True

    )

    if not os.path.exists(
        ACCOUNTS_FILE
    ):
        return []

    with open(
        ACCOUNTS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def save_accounts(accounts):

    os.makedirs(
        BASE_ACCOUNTS_DIR,
        exist_ok=True
    )

    with open(
        ACCOUNTS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            accounts,
            f,
            indent=2
        )

def create_account(
    username
):

    accounts = load_accounts()

    user = {

        "id": str(
            uuid.uuid4()
        ),

        "username": username

    }

    accounts.append(
        user
    )

    save_accounts(
        accounts
    )

    #
    # create account folder
    #

    user_folder = os.path.join(

        BASE_ACCOUNTS_DIR,

        user["id"]

    )

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    for filename in ["settings.json","stats.json","achievements.json"]:

        filepath = os.path.join(user_folder,filename)

        if not os.path.exists(filepath):

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as f:

                f.write("{}")


    return user

def delete_account(user_id):

    accounts = load_accounts()

    accounts = [

        account

        for account in accounts

        if account["id"] != user_id

    ]

    save_accounts(
        accounts
    )

    user_folder = os.path.join(

        BASE_ACCOUNTS_DIR,

        user_id

    )

    if os.path.exists(
        user_folder
    ):

        shutil.rmtree(
            user_folder
        )