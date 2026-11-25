from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QHBoxLayout
)

MAX_STAT_LEVEL = 200

class PlayerUpgradeScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game
        self.player = None

        self.layout = QVBoxLayout()

        self.info = QLabel()

        self.layout.addWidget(self.info)

        self.attack_btn = QPushButton(
            "Attack +1 (100 Coins)"
        )
        self.attack_btn.clicked.connect(
            self.upgrade_attack
        )

        self.block_btn = QPushButton(
            "Block +1 (100 Coins)"
        )
        self.block_btn.clicked.connect(
            self.upgrade_block
        )

        self.receive_btn = QPushButton(
            "Receive +1 (100 Coins)"
        )
        self.receive_btn.clicked.connect(
            self.upgrade_receive
        )

        self.setting_btn = QPushButton(
            "Setting +1 (100 Coins)"
        )
        self.setting_btn.clicked.connect(
            self.upgrade_setting
        )

        self.serve_btn = QPushButton(
            "Serve +1 (100 Coins)"
        )
        self.serve_btn.clicked.connect(
            self.upgrade_serve
        )

        self.attack_10_btn = QPushButton("Attack +10")
        self.attack_10_btn.clicked.connect(
            lambda: self.upgrade_many("attack")
        )

        self.block_10_btn = QPushButton("Block +10")
        self.block_10_btn.clicked.connect(
            lambda: self.upgrade_many("block")
        )

        self.receive_10_btn = QPushButton("Receive +10")
        self.receive_10_btn.clicked.connect(
            lambda: self.upgrade_many("receive")
        )

        self.setting_10_btn = QPushButton("Setting +10")
        self.setting_10_btn.clicked.connect(
            lambda: self.upgrade_many("setting")
        )

        self.serve_10_btn = QPushButton("Serve +10")
        self.serve_10_btn.clicked.connect(
            lambda: self.upgrade_many("serve")
        )

        self.prestige_btn = QPushButton(
            "Prestige Player"
        )

        self.prestige_btn.clicked.connect(
            self.prestige_player
        )

        self.refund_btn = QPushButton(
            "Refund Upgrades"
        )

        self.refund_btn.clicked.connect(
            self.refund_player
        )

        # Attack row
        attack_row = QHBoxLayout()
        attack_row.addWidget(self.attack_btn)
        attack_row.addWidget(self.attack_10_btn)
        self.layout.addLayout(attack_row)

        # Block row
        block_row = QHBoxLayout()
        block_row.addWidget(self.block_btn)
        block_row.addWidget(self.block_10_btn)
        self.layout.addLayout(block_row)

        # Receive row
        receive_row = QHBoxLayout()
        receive_row.addWidget(self.receive_btn)
        receive_row.addWidget(self.receive_10_btn)
        self.layout.addLayout(receive_row)

        # Setting row
        setting_row = QHBoxLayout()
        setting_row.addWidget(self.setting_btn)
        setting_row.addWidget(self.setting_10_btn)
        self.layout.addLayout(setting_row)

        # Serve row
        serve_row = QHBoxLayout()
        serve_row.addWidget(self.serve_btn)
        serve_row.addWidget(self.serve_10_btn)
        self.layout.addLayout(serve_row)

        # Other buttons
        self.layout.addWidget(self.prestige_btn)
        self.layout.addWidget(self.refund_btn)

        self.setLayout(self.layout)

    def set_player(self, player):

        self.player = player
        self.refresh()

    def refresh(self):

        if not self.player:
            return

        self.info.setText(
            f"{self.player.name}\n\n"

            f"Attack Lv {self.player.attack_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.effective_attack}\n"

            f"Block Lv {self.player.block_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.effective_block}\n"

            f"Receive Lv {self.player.receive_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.effective_receive}\n"

            f"Setting Lv {self.player.setting_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.effective_setting}\n"

            f"Serve Lv {self.player.serve_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.effective_serve}\n\n"

            f"Prestige: {self.player.prestige_level}\n"
            f"Permanent Bonus: "
            f"{self.player.prestige_level * 10}%\n\n"

            f"STR: {self.player.strength}\n"
            f"Coins: {self.game.coins}"
        )

        self.attack_btn.setText(
            f"Attack Lv +1 ({self.get_upgrade_cost(self.player.attack_level):,} Coins)"
        )

        self.block_btn.setText(
            f"Block Lv +1 ({self.get_upgrade_cost(self.player.block_level):,} Coins)"
        )

        self.receive_btn.setText(
            f"Receive Lv +1 ({self.get_upgrade_cost(self.player.receive_level):,} Coins)"
        )

        self.setting_btn.setText(
            f"Setting Lv +1 ({self.get_upgrade_cost(self.player.setting_level):,} Coins)"
        )

        self.serve_btn.setText(
            f"Serve Lv +1 ({self.get_upgrade_cost(self.player.serve_level):,} Coins)"
        )

        for stat_name, button in [
            ("attack", self.attack_10_btn),
            ("block", self.block_10_btn),
            ("receive", self.receive_10_btn),
            ("setting", self.setting_10_btn),
            ("serve", self.serve_10_btn)
        ]:

            level = getattr(
                self.player,
                f"{stat_name}_level"
            )

            upgrades = min(
                10,
                MAX_STAT_LEVEL - level
            )

            total_cost = sum(
                self.get_upgrade_cost(level + i)
                for i in range(upgrades)
            )

            button.setText(
                f"{stat_name.capitalize()} +{upgrades} "
                f"({total_cost:,} Coins)"
            )

            button.setEnabled(
                upgrades > 0
            )

        self.attack_btn.setEnabled(
            self.player.attack_level < 200
        )

        self.block_btn.setEnabled(
            self.player.block_level < 200
        )

        self.receive_btn.setEnabled(
            self.player.receive_level < 200
        )

        self.setting_btn.setEnabled(
            self.player.setting_level < 200
        )

        self.serve_btn.setEnabled(
            self.player.serve_level < 200
        )

    def spend(self, cost):

        if self.game.coins < cost:

            QMessageBox.information(
                self,
                "Not Enough Coins",
                f"You need {cost:,} coins."
            )

            return False

        self.game.coins -= cost

        return True

    def upgrade_attack(self):

        if self.player.attack_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.attack_level)

        if self.spend(cost):
            self.game.total_upgrades += 1
            self.player.coins_spent += cost
            self.player.attack += self.get_stat_gain("attack")
            self.player.attack_level += 1

        self.refresh()

    def upgrade_block(self):
        if self.player.block_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.block_level)
        
        if self.spend(cost):
            self.game.total_upgrades += 1
            self.player.coins_spent += cost
            self.player.block += self.get_stat_gain("block")
            self.player.block_level += 1

        self.refresh()

    def upgrade_receive(self):
        if self.player.receive_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.receive_level)

        if self.spend(cost):
            self.game.total_upgrades += 1
            self.player.coins_spent += cost
            self.player.receive += self.get_stat_gain("receive")
            self.player.receive_level += 1

        self.refresh()

    def upgrade_setting(self):
        if self.player.setting_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.setting_level)

        if self.spend(cost):
            self.game.total_upgrades += 1
            self.player.coins_spent += cost
            self.player.setting += self.get_stat_gain("setting")
            self.player.setting_level += 1

        self.refresh()

    def upgrade_serve(self):
        if self.player.serve_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.serve_level)

        if self.spend(cost):
            self.game.total_upgrades += 1
            self.player.coins_spent += cost
            self.player.serve += self.get_stat_gain("serve")
            self.player.serve_level += 1

        self.refresh()

    def upgrade_many(self, stat_name):

        if not self.player:
            return

        level_attr = f"{stat_name}_level"
        stat_level = getattr(self.player, level_attr)

        # Respect maximum upgrade level
        upgrades = min(
            10,
            MAX_STAT_LEVEL - stat_level
        )

        if upgrades <= 0:
            return

        # Calculate the exact cost of each upgrade
        total_cost = sum(
            self.get_upgrade_cost(stat_level + i)
            for i in range(upgrades)
        )

        if not self.spend(total_cost):
            return

        self.game.total_upgrades += upgrades
        
        # Apply the normal position-specific upgrade
        for _ in range(upgrades):

            gain = self.get_stat_gain(stat_name)

            current_stat = getattr(
                self.player,
                stat_name
            )

            setattr(
                self.player,
                stat_name,
                current_stat + gain
            )

            setattr(
                self.player,
                level_attr,
                getattr(self.player, level_attr) + 1
            )

        # Track spending for refunds
        self.player.coins_spent += total_cost

        self.refresh()


    def get_upgrade_cost(self, level):

        return int(round(
            (5001 ** (level / 100))
            + 49
        ))
    def get_stat_gain(self, stat_name):

        position = self.player.position

        gains = {

            "LS": {
                "attack": 3,
                "serve": 3,
                "receive": 2,
                "block": 1,
                "setting": 1
            },

            "RS": {
                "attack": 3,
                "serve": 3,
                "receive": 1,
                "block": 2,
                "setting": 1
            },

            "MB": {
                "attack": 3,
                "block": 3,
                "serve": 2,
                "receive": 1,
                "setting": 1
            },

            "S": {
                "setting": 3,
                "serve": 3,
                "block": 2,
                "attack": 1,
                "receive": 1
            },

            "L": {
                "receive": 4,
                "setting": 3,
                "attack": 1,
                "block": 1,
                "serve": 1
            }
        }

        return gains[position][stat_name]

    def get_duplicates(self):

        return [

            p

            for p in self.game.roster

            if (
                p is not self.player
                and
                p.name == self.player.name
            )

        ]

    def prestige_player(self):

        duplicates = self.get_duplicates()

        if not duplicates:

            self.silent_message(
                "No Duplicate",
                "You need a duplicate copy of this player."
            )

            return

        duplicate = duplicates[0]

        self.game.roster.remove(duplicate)

        self.player.prestige_level += 1

        self.reduce_stat_upgrade(
            "attack"
        )

        self.reduce_stat_upgrade(
            "block"
        )

        self.reduce_stat_upgrade(
            "receive"
        )

        self.reduce_stat_upgrade(
            "setting"
        )

        self.reduce_stat_upgrade(
            "serve"
        )

        self.silent_message(
            "Prestige Success",
            f"{self.player.name}\n"
            f"Prestige "
            f"{self.player.prestige_level}"
        )

        self.refresh()

    def reduce_stat_upgrade(self, stat_name):

        level_attr = f"{stat_name}_level"

        current_level = getattr(
            self.player,
            level_attr
        )

        new_level = current_level // 2

        levels_removed = (
            current_level -
            new_level
        )

        gain_per_level = (
            self.get_stat_gain(
                stat_name
            )
        )

        current_stat = getattr(
            self.player,
            stat_name
        )

        setattr(
            self.player,
            stat_name,
            current_stat -
            (
                levels_removed *
                gain_per_level
            )
        )

        setattr(
            self.player,
            level_attr,
            new_level
        )

    def refund_player(self):

        if (

            self.player.attack_level == 0
            and
            self.player.block_level == 0
            and
            self.player.receive_level == 0
            and
            self.player.setting_level == 0
            and
            self.player.serve_level == 0

        ):
            return

        refund = self.player.coins_spent

        result = QMessageBox.question(
            self,
            "Refund Upgrades",
            f"Refund all upgrades for\n"
            f"{refund:,} coins?"
        )

        if (
            result
            !=
            QMessageBox.StandardButton.Yes
        ):
            return

        for stat_name in [
            "attack",
            "block",
            "receive",
            "setting",
            "serve"
        ]:

            level_attr = (
                f"{stat_name}_level"
            )

            level = getattr(
                self.player,
                level_attr
            )

            gain = self.get_stat_gain(
                stat_name
            )

            current_value = getattr(
                self.player,
                stat_name
            )

            setattr(
                self.player,
                stat_name,
                current_value -
                (
                    level * gain
                )
            )

            setattr(
                self.player,
                level_attr,
                0
            )

        self.game.coins += refund

        self.player.coins_spent = 0

        self.refresh()

    def silent_message(
        self,
        title,
        text
    ):

        msg = QMessageBox(self)

        msg.setWindowTitle(title)
        msg.setText(text)

        msg.setIcon(
            QMessageBox.Icon.NoIcon
        )

        msg.exec()