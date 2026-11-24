from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class LeagueScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.league_counter = QLabel()

        self.league_counter.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.league_counter.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            padding: 10px;
        """)

        self.table = QListWidget()

        self.play_button = QPushButton(
            "Play Selected Team"
        )

        layout.addWidget(self.league_counter)
        layout.addWidget(self.table)
        layout.addWidget(self.play_button)

        self.setLayout(layout)

    def refresh(self):
        
        self.league_counter.setText(f"LEAGUE #{self.game.league_number}")
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

            # Calculate average team strength
            strength = sum(
                player.strength
                for player in team["lineup"]
            ) // max(len(team["lineup"]), 1)

            self.table.addItem(

                f"{rank}. "
                f"{team['name']} | "
                f"STR {strength} | "
                f"{team['wins']}-{team['losses']}"

            )

            rank += 1