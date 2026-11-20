from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton
)

class BattleScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        self.layout = QVBoxLayout()

        self.title = QLabel()

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

        enemy_players, league = (
            self.game.get_current_enemy()
        )

        self.enemy_players = enemy_players

        self.title.setText(
            f"Opponent: {league}"
        )

        player_total = 0

        for slot, player in (
            self.game.lineup.items()
        ):

            if player:

                self.user_team.addItem(
                    f"{slot} | "
                    f"{player.name} | "
                    f"{player.strength}"
                )

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

            self.enemy_team.addItem(
                f"{slot} | "
                f"{player.name} | "
                f"{player.strength}"
            )

            enemy_total += (
                player.strength
            )

        self.summary.setText(
            f"Your Rating: "
            f"{player_total // 7}\n\n"
            f"Enemy Rating: "
            f"{enemy_total // 7}"
        )