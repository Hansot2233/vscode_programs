from PyQt6.QtWidgets import *

class LeagueScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.table = QListWidget()

        self.play_button = QPushButton(
            "Play Selected Team"
        )

        layout.addWidget(
            self.table
        )

        layout.addWidget(
            self.play_button
        )

        self.setLayout(layout)

    def refresh(self):

        self.table.clear()

        standings = sorted(

            self.game.league_teams,

            key=lambda team: (
                team["wins"],
                -team["losses"]
            ),

            reverse=True

        )

        rank = 1

        for team in standings:

            self.table.addItem(

                f"{rank}. "
                f"{team['name']} | "
                f"{team['wins']}-{team['losses']}"

            )

            rank += 1