
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QListWidgetItem,QPushButton
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QColor


class BattleScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        self.layout = QVBoxLayout()

        self.title = QLabel()
        
        self.score_label = QLabel("Ready to battle")

        self.score_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.score_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
        """)

        self.layout.addWidget(self.score_label)

        self.layout.addWidget(
            self.title
        )

        team_layout = QHBoxLayout()

        self.user_team = QListWidget()
        self.enemy_team = QListWidget()

        team_layout.addWidget(
            self.user_team
        )

        team_layout.addWidget(
            self.enemy_team
        )

        self.layout.addLayout(
            team_layout
        )

        self.summary = QLabel()

        self.layout.addWidget(
            self.summary
        )

        self.start_button = QPushButton(
            "Start Match"
        )

        self.layout.addWidget(
            self.start_button
        )

        self.setLayout(
            self.layout
        )

    def refresh(self):

        self.user_team.clear()
        self.enemy_team.clear()

        rarity_colors = {
            "Starter": QColor(150, 150, 150),
            "Common": QColor(0, 200, 0),
            "Rare": QColor(0, 100, 255),
            "Epic": QColor(170, 0, 255),
            "Legendary": QColor(255, 140, 0)
        }

        enemy_players, league = (
            self.game.get_current_enemy()
        )

        self.enemy_players = enemy_players

        self.title.setText(
            f"Stage: {self.game.battle_level}"
        )

        player_total = 0

        for slot, player in (
            self.game.lineup.items()
        ):

            if player:

                item = QListWidgetItem(
                    f"{slot} | "
                    f"{player.name} | "
                    f"{player.strength}"
                )

                item.setForeground(
                    rarity_colors.get(
                        player.rarity,
                        QColor("black")
                    )
                )

                self.user_team.addItem(item)

                player_total += (
                    player.strength
                )

        enemy_total = 0

        positions = [
            "LS1",
            "LS2",
            "MB1",
            "MB2",
            "S",
            "RS",
            "L"
        ]

        for slot, player in zip(
            positions,
            enemy_players
        ):

            item = QListWidgetItem(
                f"{slot} | "
                f"{player.name} | "
                f"{player.strength}"
            )

            item.setForeground(
                rarity_colors.get(
                    player.rarity,
                    QColor("black")
                )
            )

            self.enemy_team.addItem(item)

            enemy_total += (
                player.strength
            )

        self.summary.setText(
            f"Your Rating: "
            f"{player_total // 7}\n\n"
            f"Enemy Rating: "
            f"{enemy_total // 7}"
        )

    def load_match_rosters(self,player_team,enemy_team,title):

        self.user_team.clear()
        self.enemy_team.clear()

        self.title.setText(title)

        rarity_colors = {
            "Starter": QColor(150, 150, 150),
            "Common": QColor(0, 200, 0),
            "Rare": QColor(0, 100, 255),
            "Epic": QColor(170, 0, 255),
            "Legendary": QColor(255, 140, 0)
        }

        positions = [
            "LS1",
            "LS2",
            "MB1",
            "MB2",
            "S",
            "RS",
            "L"
        ]

        player_total = 0

        for slot, player in zip(
            positions,
            player_team
        ):

            item = QListWidgetItem(

                f"{slot} | "
                f"{player.name} | "
                f"{player.strength}"

            )

            item.setForeground(

                rarity_colors.get(
                    player.rarity,
                    QColor("black")
                )

            )

            self.user_team.addItem(item)

            player_total += player.strength

        enemy_total = 0

        for slot, player in zip(
            positions,
            enemy_team
        ):

            item = QListWidgetItem(

                f"{slot} | "
                f"{player.name} | "
                f"{player.strength}"

            )

            item.setForeground(

                rarity_colors.get(
                    player.rarity,
                    QColor("black")
                )

            )

            self.enemy_team.addItem(item)

            enemy_total += player.strength

        self.summary.setText(

            f"Your Rating: "
            f"{player_total // 7}\n\n"

            f"Enemy Rating: "
            f"{enemy_total // 7}"

        )