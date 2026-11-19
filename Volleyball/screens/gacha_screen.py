from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QMessageBox, 
    QListWidget
)


class GachaScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        self.info = QLabel()
        layout.addWidget(self.info)

        self.result_label = QLabel("No player recruited yet.")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        self.history = QListWidget()
        layout.addWidget(self.history)

        self.wheel1 = QPushButton(
            "Budget Wheel (50 Gems)"
        )

        self.wheel2 = QPushButton(
            "Premium Wheel (150 Gems)"
        )

        self.wheel3 = QPushButton(
            "Legend Wheel (500 Gems)"
        )

        self.wheel1.clicked.connect(
            self.spin_budget
        )

        self.wheel2.clicked.connect(
            self.spin_premium
        )

        self.wheel3.clicked.connect(
            self.spin_legend
        )

        layout.addWidget(self.wheel1)
        layout.addWidget(self.wheel2)
        layout.addWidget(self.wheel3)

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        self.info.setText(
            f"Gems: {self.game.gems}"
        )

    def reward_player(self, rarity_table):

        import random

        if self.game.gems < rarity_table["cost"]:

            self.info.setText(
                f"Not enough gems!\n"
                f"Need {rarity_table['cost']}\n"
                f"Current: {self.game.gems}"
            )
            return

        self.game.gems -= rarity_table["cost"]

        r = random.random()

        cumulative = 0

        for rarity, chance in rarity_table["odds"]:

            cumulative += chance

            if r <= cumulative:

                player = self.game.generate_player_of_rarity(
                    rarity
                )

                self.game.roster.append(player)

                rarity_colors = {
                    "Common": "green",
                    "Rare": "blue",
                    "Epic": "purple",
                    "Legendary": "orange"
                }

                color = rarity_colors.get(
                    player.rarity,
                    "black"
                )

                self.result_label.setText(
                    f"<h2>{player.name}</h2>"
                    f"<b>Position:</b> {player.position}<br>"
                    f"<b>Rarity:</b> "
                    f"<font color='{color}'>{player.rarity}</font><br>"
                    f"<b>STR:</b> {player.strength}"
                )

                self.history.insertItem(
                    0,
                    f"{player.rarity} | "
                    f"{player.name} | "
                    f"{player.position} | "
                    f"STR {player.strength}"
                )

                break

        self.refresh()

    def spin_budget(self):

        self.reward_player({
            "cost": 50,
            "odds": [
                ("Common", 0.80),
                ("Rare", 0.15),
                ("Epic", 0.045),
                ("Legendary", 0.005)
            ]
        })

    def spin_premium(self):

        self.reward_player({
            "cost": 200,
            "odds": [
                ("Common", 0.55),
                ("Rare", 0.30),
                ("Epic", 0.12),
                ("Legendary", 0.03)
            ]
        })

    def spin_legend(self):

        self.reward_player({
            "cost": 600,
            "odds": [
                ("Rare", 0.55),
                ("Epic", 0.36),
                ("Legendary", 0.09)
            ]
        })