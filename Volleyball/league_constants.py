from player_database import PLAYER_DATABASE

LEAGUE_TEAM_NAMES = [

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

TEAM_ROSTERS = {

    "Karasuno": {
        "LS1": "Shoyo Hinata",
        "LS2": "Ryunosuke Tanaka",
        "MB1": "Kei Tsukishima",
        "MB2": "Tadashi Yamaguchi",
        "S": "Tobio Kageyama",
        "RS": "Asahi Azumane",
        "L": "Yu Nishinoya"
    },

    "Nekoma": {
        "LS1": "Daniel Riber",
        "LS2": "Xavior Šimić",
        "MB1": "Tetsuro Kuroo",
        "MB2": "Lev Haiba",
        "S": "Kenma Kozume",
        "RS": "Naoki Shimizu",
        "L": "Masato Ono"
    },

    "Aoba Johsai": {
        "LS1": "Hajime Iwaizumi",
        "LS2": "Yuki Mori",
        "MB1": "Daichi Ito",
        "MB2": "Shin Ozaki",
        "S": "Toru Oikawa",
        "RS": "Takumi Abe",
        "L": "Eiji Kondo"
    },

    "Shiratorizawa": {
        "LS1": "Kotaro Bokuto",
        "LS2": "Ryunosuke Tanaka",
        "MB1": "Tetsuro Kuroo",
        "MB2": "Kei Tsukishima",
        "S": "Satoru Gojo",
        "RS": "Wakatoshi Ushijima",
        "L": "Yu Nishinoya"
    },

    "Fukurodani": {
        "LS1": "Kotaro Bokuto",
        "LS2": "Daniel Riber",
        "MB1": "Tadashi Yamaguchi",
        "MB2": "Kenta Hayashi",
        "S": "Akira Nakano",
        "RS": "Asahi Azumane",
        "L": "Hiro Watanabe"
    },

    "Date Tech": {
        "LS1": "Ren Kuroda",
        "LS2": "Yuki Mori",
        "MB1": "Lev Haiba",
        "MB2": "Kei Tsukishima",
        "S": "Koshi Sugawara",
        "RS": "Koki Maeda",
        "L": "Yuji Kano"
    },

    "Inarizaki": {
        "LS1": "Hajime Iwaizumi",
        "LS2": "Kotaro Bokuto",
        "MB1": "Tetsuro Kuroo",
        "MB2": "Lev Haiba",
        "S": "Toru Oikawa",
        "RS": "Yujiro Hanma",
        "L": "Yu Nishinoya"
    },

    "Kamomedai": {
        "LS1": "Shoyo Hinata",
        "LS2": "Xavior Šimić",
        "MB1": "Tetsuro Kuroo",
        "MB2": "Haru Ishikawa",
        "S": "Kenma Kozume",
        "RS": "Asahi Azumane",
        "L": "Masato Ono"
    },

    "Nohebi": {
        "LS1": "Daniel Riber",
        "LS2": "Ryunosuke Tanaka",
        "MB1": "Daichi Ito",
        "MB2": "Shin Ozaki",
        "S": "Riku Endo",
        "RS": "Minato Ueda",
        "L": "Eiji Kondo"
    },

    "Johzenji": {
        "LS1": "Yuki Mori",
        "LS2": "Ren Kuroda",
        "MB1": "Haru Ishikawa",
        "MB2": "Kenta Hayashi",
        "S": "Toma Fujita",
        "RS": "Takumi Abe",
        "L": "Hiro Watanabe"
    },

    "Wakutani": {
        "LS1": "Shoyo Hinata",
        "LS2": "Daniel Riber",
        "MB1": "Lev Haiba",
        "MB2": "Daichi Ito",
        "S": "Koshi Sugawara",
        "RS": "Naoki Shimizu",
        "L": "Yuji Kano"
    },

    "Shinzen": {
        "LS1": "Ryunosuke Tanaka",
        "LS2": "Xavior Šimić",
        "MB1": "Tadashi Yamaguchi",
        "MB2": "Haru Ishikawa",
        "S": "Akira Nakano",
        "RS": "Koki Maeda",
        "L": "Masato Ono"
    },

    "Mujinazaka": {
        "LS1": "Hajime Iwaizumi",
        "LS2": "Shoyo Hinata",
        "MB1": "Tetsuro Kuroo",
        "MB2": "Lev Haiba",
        "S": "Satoru Gojo",
        "RS": "Asahi Azumane",
        "L": "Yu Nishinoya"
    },

    "Tsubakihara": {
        "LS1": "Yuki Mori",
        "LS2": "Daniel Riber",
        "MB1": "Kei Tsukishima",
        "MB2": "Kenta Hayashi",
        "S": "Toma Fujita",
        "RS": "Minato Ueda",
        "L": "Eiji Kondo"
    },

    "Ubugawa": {
        "LS1": "Ren Kuroda",
        "LS2": "Ryunosuke Tanaka",
        "MB1": "Daichi Ito",
        "MB2": "Lev Haiba",
        "S": "Riku Endo",
        "RS": "Takumi Abe",
        "L": "Hiro Watanabe"
    }

}

PLAYER_LOOKUP = {}

for rarity, players in PLAYER_DATABASE.items():

    for player in players:

        PLAYER_LOOKUP[player["name"]] = {

            **player,

            "rarity": rarity

        }

def get_team_template(team_name):

    return TEAM_ROSTERS[team_name]