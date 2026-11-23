from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QMessageBox, 
    QListWidget
)
import random

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
            "Premium Wheel (200 Gems)"
        )

        self.wheel3 = QPushButton(
            "Legend Wheel (600 Gems)"
        )

        self.wheel1_10 = QPushButton(
            "Budget Wheel 10x (500 Gems)"
        )

        self.wheel2_10 = QPushButton(
            "Premium Wheel 10x (2000 Gems)"
        )

        self.wheel3_10 = QPushButton(
            "Legend Wheel 10x (6000 Gems)"
        )

        self.wheel1_10.clicked.connect(
            self.spin_budget_10
        )

        self.wheel2_10.clicked.connect(
            self.spin_premium_10
        )

        self.wheel3_10.clicked.connect(
            self.spin_legend_10
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
        layout.addWidget(self.wheel1_10)

        layout.addWidget(self.wheel2)
        layout.addWidget(self.wheel2_10)

        layout.addWidget(self.wheel3)
        layout.addWidget(self.wheel3_10)

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        self.info.setText(
            f"Gems: {self.game.gems}"
        )

    def reward_player(self, rarity_table, spins=1):

        total_cost = rarity_table["cost"] * spins

        # Check if player can afford all spins
        if self.game.gems < total_cost:

            self.info.setText(
                f"Not enough gems!\n"
                f"Need {total_cost:,}\n"
                f"Current: {self.game.gems:,}"
            )

            return

        # Charge gems
        self.game.gems -= total_cost

        results = []

        rarity_counts = {}

        rarity_colors = {
            "Common": "green",
            "Rare": "blue",
            "Epic": "purple",
            "Legendary": "orange"
        }

        # Perform spins
        for i in range(spins):

            r = random.random()
            cumulative = 0

            for rarity, chance in rarity_table["odds"]:

                cumulative += chance

                if r <= cumulative:

                    player = self.game.generate_player_of_rarity(
                        rarity
                    )

                    self.game.roster.append(player)

                    rarity_counts[rarity] = (
                        rarity_counts.get(rarity, 0) + 1
                    )

                    results.append(
                        f"{player.rarity} | "
                        f"{player.name} | "
                        f"{player.position} | "
                        f"STR {player.strength}"
                    )

                    self.history.insertItem(
                        0,
                        results[-1]
                    )

                    break

        # Display results
        if spins == 1:

            player_text = results[0]

            rarity = player_text.split(" | ")[0]
            color = rarity_colors.get(rarity, "black")

            self.result_label.setText(
                f"<h2>{player_text}</h2>"
                f"<font color='{color}'>{rarity}</font>"
            )

        else:

            summary = "<h2>10x Spin Results</h2>"

            for rarity, count in rarity_counts.items():

                color = rarity_colors.get(
                    rarity,
                    "black"
                )

                summary += (
                    f"<font color='{color}'>"
                    f"{rarity}: {count}"
                    f"</font><br>"
                )

            self.result_label.setText(summary)

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

    # 10x Gacha Spins

    def spin_budget_10(self):

        self.reward_player({
            "cost": 50,
            "odds": [
                ("Common", 0.80),
                ("Rare", 0.15),
                ("Epic", 0.045),
                ("Legendary", 0.005)
            ]
        }, spins=10)


    def spin_premium_10(self):

        self.reward_player({
            "cost": 200,
            "odds": [
                ("Common", 0.55),
                ("Rare", 0.30),
                ("Epic", 0.12),
                ("Legendary", 0.03)
            ]
        }, spins=10)


    def spin_legend_10(self):

        self.reward_player({
            "cost": 600,
            "odds": [
                ("Rare", 0.55),
                ("Epic", 0.36),
                ("Legendary", 0.09)
            ]
        }, spins=10)