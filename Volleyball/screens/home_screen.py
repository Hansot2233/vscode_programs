from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class HomeScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        self.layout = QVBoxLayout()

        self.info = QLabel()

        self.layout.addWidget(self.info)

        self.setLayout(self.layout)

        self.refresh()

    def refresh(self):

        self.info.setText(
            f"""
Level: {self.game.level}

Coins: {self.game.coins}

Spins: {self.game.spins}

Team Rating: {self.game.team_rating()}
"""
        )
