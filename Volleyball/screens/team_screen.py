from PyQt6.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from screens.player_upgrade_screen import PlayerUpgradeScreen

rarity_colors = {
    "Starter": QColor(150,150,150),
    "Common": QColor(0,200,0),
    "Rare": QColor(0,100,255),
    "Epic": QColor(170,0,255),
    "Legendary": QColor(255,140,0)
}

class TeamScreen(QWidget):

    lineup_changed = pyqtSignal()
    open_upgrade_requested = pyqtSignal(object)

    def __init__(self, game):

        super().__init__()

        self.game = game
        self.selected_player = None
        self.selected_slot = None

        layout = QHBoxLayout()

        self.roster_list = QListWidget()
        self.roster_list.setMinimumWidth(500)
        self.roster_list.itemClicked.connect(self.select_roster_player)

        self.team_strength_label = QLabel()
        self.lineup_list = QListWidget()
        self.lineup_list.setMinimumWidth(250)
        self.lineup_list.itemClicked.connect(self.select_lineup_slot)

        self.roster_list.itemClicked.connect(self.player_selected)
        self.selected_player_swap = None
        self.selected_slot_swap = None

        font = QFont("Consolas", 10)
        self.roster_list.setFont(font)
        self.lineup_list.setFont(font)

        layout.setStretch(0, 3)
        layout.setStretch(1, 1)
        layout.setStretch(2, 2)

        self.resize(1100, 700)

        button_layout = QVBoxLayout()

        swap_button = QPushButton("Swap Player")
        swap_button.clicked.connect(self.swap_player)
        button_layout.addWidget(swap_button)

        upgrade_button = QPushButton("Upgrade Player")
        upgrade_button.clicked.connect(self.open_upgrade)
        button_layout.addWidget(upgrade_button)

        lineup_layout = QVBoxLayout()
        lineup_layout.addWidget(self.team_strength_label)
        lineup_layout.addWidget(self.lineup_list)
        layout.addWidget(self.roster_list)
        layout.addLayout(button_layout)
        layout.addLayout(lineup_layout)

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        self.roster_list.clear()
        self.lineup_list.clear()

        self.team_strength_label.setText(f"Team Rating: {self.game.team_rating()}")

        # Current lineup players
        lineup_players = [
            p for p in self.game.lineup.values()
            if p is not None
        ]

        lineup_ids = {
            id(player)
            for player in lineup_players
        }

        bench_players = [
            p
            for p in self.game.roster
            if id(p) not in lineup_ids
        ]

        rarity_order = {
            "Legendary": 5,
            "Epic": 4,
            "Rare": 3,
            "Common": 2,
            "Starter": 1
        }

        bench_players.sort(
            key=lambda p: (
                -rarity_order.get(p.rarity, 0),
                p.name.lower()
            )
        )

        # Save display order for assignment logic
        self.displayed_players = []

        # First: starters
        for player in lineup_players:

            self.displayed_players.append(player)

            item = QListWidgetItem(
                f"★ {player.name} | "
                f"{player.position} | "
                f"{player.rarity} | "
                f"LV {player.prestige_level} | "
                f"STR {player.strength}"
            )

            item.setForeground(
                rarity_colors.get(
                    player.rarity,
                    QColor("black")
                )
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                player
            )

            self.roster_list.addItem(item)

        for player in bench_players:

            self.displayed_players.append(player)

            item = QListWidgetItem(
                f"{player.name} | "
                f"{player.position} | "
                f"{player.rarity} | "
                f"LV {player.prestige_level} | "
                f"STR {player.strength}"
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                player
            )

            item.setForeground(
                rarity_colors.get(
                player.rarity,
                QColor("black")
                )
            )

            self.roster_list.addItem(item)

        # Current lineup display
        for slot, player in self.game.lineup.items():

            if player:

                item = QListWidgetItem(
                    f"{slot}: {player.name}"
                )

                item.setForeground(
                    rarity_colors.get(
                        player.rarity,
                        QColor("black")
                    )
                )

                self.lineup_list.addItem(item)
            else:
                self.lineup_list.addItem(
                    f"{slot}: Empty"
                )

    def swap_player(self):

        if not self.selected_player:
            return

        if not self.selected_slot:
            return

        position_map = {
            "LS1": "LS",
            "LS2": "LS",
            "MB1": "MB",
            "MB2": "MB",
            "S": "S",
            "RS": "RS",
            "L": "L"
        }

        required_position = position_map[
            self.selected_slot
        ]

        # Prevent duplicate names in the lineup for LS and MB
        if required_position in ("LS", "MB"):

            for slot, player in self.game.lineup.items():

                if (
                    player is not None
                    and slot != self.selected_slot
                    and player.name == self.selected_player.name
                ):

                    QMessageBox.information(
                        self,
                        "Duplicate Player",
                        f"{self.selected_player.name} "
                        f"is already in the lineup at {slot}."
                    )

                    return

        self.game.update_highest_team_rating()

        if self.selected_player.position != required_position:

            QMessageBox.information(
                self,
                "Wrong Position",
                f"{self.selected_player.name} "
                f"cannot play "
                f"{self.selected_slot}"
            )

            return

        destination_player = self.game.lineup[
            self.selected_slot
        ]

        current_slot = None

        # Is selected player already in lineup?
        for slot, player in self.game.lineup.items():

            if player is self.selected_player:

                current_slot = slot
                break

        # Starter -> Starter swap
        if current_slot is not None:

            self.game.lineup[current_slot] = (
                destination_player
            )

        # Put selected player in destination
        self.game.lineup[
            self.selected_slot
        ] = self.selected_player

        self.game.update_highest_team_rating()

        self.refresh()

    def player_selected(self):

        index = self.roster_list.currentRow()

        if index < 0:
            return

        if index >= len(self.displayed_players):
            return

        self.selected_player = self.displayed_players[index]

    def select_roster_player(self):

        item = self.roster_list.currentItem()

        if item is None:
            return

        player = item.data(
            Qt.ItemDataRole.UserRole
        )

        if player is None:
            return

        self.selected_player = player

    def select_lineup_slot(self):

        index = self.lineup_list.currentRow()

        if index < 0:
            return

        self.selected_slot = list(self.game.lineup.keys())[index]

    def open_upgrade(self):

        if not self.selected_player:
            return

        self.open_upgrade_requested.emit(
            self.selected_player
        )