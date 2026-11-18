from PyQt6.QtWidgets import *

class UpgradeScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.button = QPushButton(
            "Upgrade Strongest Player"
        )

        self.button.clicked.connect(
            self.upgrade
        )

        self.message = QLabel()

        layout.addWidget(self.button)
        layout.addWidget(self.message)

        self.setLayout(layout)

    def upgrade(self):

        if self.game.coins < 100:

            self.message.setText(
                "Not enough coins"
            )

            return

        player = max(
            self.game.roster,
            key=lambda p: p.strength
        )

        player.level += 1

        self.game.coins -= 100

        self.message.setText(
            f"Upgraded {player.name}"
        )
