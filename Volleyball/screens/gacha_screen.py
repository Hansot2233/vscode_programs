from PyQt6.QtWidgets import *

class GachaScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.result = QLabel()

        self.button = QPushButton("Lucky Spin")

        self.button.clicked.connect(self.spin)

        layout.addWidget(self.result)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def spin(self):

        if self.game.spins <= 0:
            self.result.setText("No Spins")
            return

        self.game.spins -= 1

        player = self.game.generate_player()

        self.game.roster.append(player)

        self.result.setText(
            f"""
Pulled:

{player.name}

{player.position}

{player.rarity}
"""
        )
