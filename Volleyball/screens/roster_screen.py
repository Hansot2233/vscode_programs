from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget

class RosterScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.list = QListWidget()

        layout.addWidget(self.list)

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        self.list.clear()

        for player in sorted(
            self.game.roster,
            key=lambda p: p.strength,
            reverse=True
        ):

            self.list.addItem(
                f"{player.name} | "
                f"{player.position} | "
                f"{player.rarity} | "
                f"STR {player.strength}"
            )
