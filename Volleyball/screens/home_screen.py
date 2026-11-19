from email.mime import text

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class HomeScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        self.layout = QVBoxLayout()

        self.info = QLabel()

        self.info.setStyleSheet("""
            color: black;
            font-size: 14px;
        """)

        self.layout.addWidget(self.info)

        self.setLayout(self.layout)

        self.refresh()

    def refresh(self):

        RARITY_COLORS = {
            "Starter": "#808080",
            "Common": "#00CC00",
            "Rare": "#3399FF",
            "Epic": "#AA00FF",
            "Legendary": "#FF9900"
        }

        self.info.setText(
            f"Lv {self.game.level} | "
            f"Coins {self.game.coins} | "
            f"Gems {self.game.gems} | "
            f"Team Rating {self.game.team_rating()}"
        )

        text = f"""
        <b>Level:</b> {self.game.level}
        <b>Coins:</b> {self.game.coins}
        <b>Gems:</b> {self.game.gems}
        <b>Team Rating:</b> {self.game.team_rating()}

        <b>Current Lineup</b>
        """

        for slot, player in self.game.lineup.items():

            if player is None:

                text += f"{slot}: Empty"

            else:

                color = RARITY_COLORS.get(
                    player.rarity,
                    "#FFFFFF"
                )

                text += (
                    f"{slot}: "
                    f"{player.name} | "
                    f"{player.position} | "
                    f"<font color='{color}'>{player.rarity}</font> | "
                f"OVR {player.strength}"
            )

        self.info.setText(text)

