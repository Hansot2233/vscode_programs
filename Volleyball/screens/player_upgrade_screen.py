from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
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

        self.layout.addWidget(self.attack_btn)
        self.layout.addWidget(self.block_btn)
        self.layout.addWidget(self.receive_btn)
        self.layout.addWidget(self.setting_btn)
        self.layout.addWidget(self.serve_btn)

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
            f"| {self.player.attack}\n"

            f"Block Lv {self.player.block_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.block}\n"

            f"Receive Lv {self.player.receive_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.receive}\n"

            f"Setting Lv {self.player.setting_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.setting}\n"

            f"Serve Lv {self.player.serve_level}/{MAX_STAT_LEVEL} "
            f"| {self.player.serve}\n\n"

            f"STR: {self.player.strength}\n"
            f"Coins: {self.game.coins}"
        )

        self.attack_btn.setText(
            f"Attack +{self.get_stat_gain('attack')} ({self.get_upgrade_cost(self.player.attack_level):,} Coins)"
        )

        self.block_btn.setText(
            f"Block +{self.get_stat_gain('block')} ({self.get_upgrade_cost(self.player.block_level):,} Coins)"
        )

        self.receive_btn.setText(
            f"Receive +{self.get_stat_gain('receive')} ({self.get_upgrade_cost(self.player.receive_level):,} Coins)"
        )

        self.setting_btn.setText(
            f"Setting +{self.get_stat_gain('setting')} ({self.get_upgrade_cost(self.player.setting_level):,} Coins)"
        )

        self.serve_btn.setText(
            f"Serve +{self.get_stat_gain('serve')} ({self.get_upgrade_cost(self.player.serve_level):,} Coins)"
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
            self.player.attack += self.get_stat_gain("attack")
            self.player.attack_level += 1

        self.refresh()

    def upgrade_block(self):
        if self.player.block_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.block_level)
        
        if self.spend(cost):
            self.player.block += self.get_stat_gain("block")
            self.player.block_level += 1

        self.refresh()

    def upgrade_receive(self):
        if self.player.receive_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.receive_level)

        if self.spend(cost):
            self.player.receive += self.get_stat_gain("receive")
            self.player.receive_level += 1

        self.refresh()

    def upgrade_setting(self):
        if self.player.setting_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.setting_level)

        if self.spend(cost):
            self.player.setting += self.get_stat_gain("setting")
            self.player.setting_level += 1

        self.refresh()

    def upgrade_serve(self):
        if self.player.serve_level >= MAX_STAT_LEVEL:
            return

        cost = self.get_upgrade_cost(self.player.serve_level)

        if self.spend(cost):
            self.player.serve += self.get_stat_gain("serve")
            self.player.serve_level += 1

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