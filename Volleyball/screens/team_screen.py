from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
)


class TeamScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QHBoxLayout()

        self.roster_list = QListWidget()

        self.lineup_list = QListWidget()

        button_layout = QVBoxLayout()

        positions = [
            "LS1",
            "LS2",
            "MB1",
            "MB2",
            "S",
            "RS",
            "L"
        ]

        for pos in positions:

            button = QPushButton(
                f"Assign to {pos}"
            )

            button.clicked.connect(
                lambda checked,
                p=pos: self.assign_player(p)
            )

            button_layout.addWidget(button)

        layout.addWidget(self.roster_list)
        layout.addLayout(button_layout)
        layout.addWidget(self.lineup_list)

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        self.roster_list.clear()
        self.lineup_list.clear()

        for player in self.game.roster:

            self.roster_list.addItem(
                f"{player.name} "
                f"{player.position} "
                f"STR {player.strength}"
            )

        for slot, player in self.game.lineup.items():

            if player:

                self.lineup_list.addItem(
                    f"{slot}: "
                    f"{player.name}"
                )

            else:

                self.lineup_list.addItem(
                    f"{slot}: Empty"
                )

    def assign_player(self, slot):

        index = self.roster_list.currentRow()

        if index < 0:
            return

        player = self.game.roster[index]

        position_map = {
            "LS1": "LS",
            "LS2": "LS",
            "MB1": "MB",
            "MB2": "MB",
            "S": "S",
            "RS": "RS",
            "L": "L"
        }

        required = position_map[slot]

        if player.position != required:
            return

        for current_slot, current_player in self.game.lineup.items():

            if current_player == player:
                return

        self.game.lineup[slot] = player

        self.refresh()