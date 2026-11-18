from PyQt6.QtWidgets import *
from battle_engine import simulate

class BattleScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.result = QLabel()

        self.button = QPushButton(
            "Battle"
        )

        self.button.clicked.connect(
            self.battle
        )

        layout.addWidget(self.result)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def battle(self):

        if not self.game.lineup_complete():

            self.result.setText(
                "Complete lineup first"
            )

            return

        win, enemy = simulate(
            self.game.team_rating(),
            self.game.level
        )

        if win:

            self.game.level += 1
            self.game.coins += 200
            self.game.spins += 1

            self.result.setText(
                f"Win vs {enemy}"
            )

        else:

            self.result.setText(
                f"Lost vs {enemy}"
            )
