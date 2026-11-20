import sys, os
from PyQt6.QtWidgets import *
from game_data import GameData
from battle_engine import simulate
from save_manager import save_game,load_game
from screens.team_screen import TeamScreen
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor
from screens.team_screen import TeamScreen
from screens.player_upgrade_screen import PlayerUpgradeScreen
from screens.gacha_screen import GachaScreen
from screens.battle_screen import BattleScreen

SAVE_FILE = os.path.join(
    os.path.dirname(__file__),
    "saves",
    "save.json"
)

class Main(QMainWindow):
  def __init__(self):
    super().__init__()

    self.resize(1400, 800)

    self.g=GameData()
    load_game(self.g, SAVE_FILE)

    self.stack = QStackedWidget()

    self.home_widget = QWidget()

    main_layout = QHBoxLayout()

    left_layout = QVBoxLayout()

    self.info = QLabel()
    self.list = QListWidget()

    left_layout.addWidget(self.info)
    left_layout.addWidget(self.list)

    button_layout = QVBoxLayout()

    for t, f in [
        ('Recruit Players', self.show_gacha_screen),
        ('Battle', self.show_battle_screen),
        ('Save', self.save)
    ]:
        b = QPushButton(t)
        b.clicked.connect(f)
        button_layout.addWidget(b)

    team_button = QPushButton("Team Manager")
    team_button.clicked.connect(self.show_team_screen)
    button_layout.addWidget(team_button)

    button_layout.addStretch()

    main_layout.addLayout(left_layout)
    main_layout.addLayout(button_layout)

    main_layout.setStretch(0, 4)
    main_layout.setStretch(1, 1)

    self.home_widget.setLayout(main_layout)

    self.team_screen = TeamScreen(self.g)
    self.gacha_screen = GachaScreen(self.g)
    self.battle_screen = BattleScreen(self.g)
    

    self.upgrade_screen = PlayerUpgradeScreen(self.g)
    self.team_screen.open_upgrade_requested.connect(self.show_upgrade_screen)
    self.battle_screen.start_button.clicked.connect(self.battle)

    back_button = QPushButton("Back")
    back_button.clicked.connect(self.show_home_screen)
    back_to_home = QPushButton("Back")
    back_to_home.clicked.connect(self.show_home_screen)
    battle_back = QPushButton("Back")
    battle_back.clicked.connect(self.show_home_screen)

    self.battle_screen.layout.addWidget(battle_back)
    self.gacha_screen.layout().addWidget(back_to_home)
    self.team_screen.layout().addWidget(back_button)    

    self.stack.addWidget(self.home_widget)
    self.stack.addWidget(self.team_screen)
    self.stack.addWidget(self.upgrade_screen)
    self.stack.addWidget(self.gacha_screen)
    self.stack.addWidget(self.battle_screen)

    back_to_team = QPushButton("Back")
    back_to_team.clicked.connect(self.show_team_screen)
    self.upgrade_screen.layout.addWidget(back_to_team)

    self.setCentralWidget(self.stack)

    self.refresh()

  def refresh(self):

    self.info.setText(
        f"Lv {self.g.level} | "
        f"Coins {self.g.coins} | "
        f"Gems {self.g.gems} | "
        f"Team Rating {self.g.team_rating()}"
    )

    self.list.clear()

    rarity_colors = {
        "Starter": QColor(150, 150, 150),
        "Common": QColor(0, 200, 0),
        "Rare": QColor(0, 100, 255),
        "Epic": QColor(170, 0, 255),
        "Legendary": QColor(255, 140, 0)
    }

    for slot, player in self.g.lineup.items():

        if player is None:
            self.list.addItem(f"{slot}: Empty")

        else:
            item = QListWidgetItem(
                f"{slot}: "
                f"{player.name} | "
                f"{player.position} | "
                f"{player.rarity} | "
                f"STR {player.strength}"
            )

            item.setForeground(
                rarity_colors.get(
                    player.rarity,
                    QColor("black")
                )
            )

            self.list.addItem(item)

  def spin(self):
    if self.g.gems > 0:
        self.g.gems -= 1
        self.g.roster.append(
            self.g.generate_player()
        )
        self.refresh()

  def upgrade(self):

    if not self.g.roster:
        return

    if self.g.coins < 100:
        return

    best_player = max(
        self.g.roster,
        key=lambda p: p.strength
    )

    best_player.level += 1
    self.g.coins -= 100

    self.refresh()

  def battle(self):

    if not self.g.lineup_complete():

        QMessageBox.information(
            self,
            "Incomplete Team",
            "Fill all 7 lineup positions first."
        )

        return

    winner, set_scores, enemy = simulate(
      self.g.lineup,
      self.g
    )


    if winner:

        self.g.level += 1
        self.g.battle_level += 1

        self.g.current_enemy_team = None
        self.g.current_enemy_league = None

        reward = (
            500 +
            self.g.battle_level * 100
        )

        gems = (
            10 +
            self.g.level // 5
        )

        self.g.coins += reward
        self.g.gems += gems

    result_text = (
      f"{'WIN' if winner else 'LOSS'}\n\n"
      f"Opponent:\n"
      f"{enemy}\n\n"
      f"Set Scores:\n"
    )

    for score in set_scores:
        result_text += score + "\n"

    if winner:
        result_text += (
          f"Rewards:\n"
          f"Coins: {reward}\n"
          f"Gems: {gems}"
        )

    QMessageBox.information(
        self,
        "Match Result",
        result_text
    )

    self.battle_screen.refresh()
    self.refresh()
    
  def save(self): 
    save_game(self.g,SAVE_FILE)

  def show_team_screen(self):
    self.team_screen.refresh()
    self.stack.setCurrentWidget(self.team_screen)

  def show_home_screen(self):
    self.refresh()
    self.stack.setCurrentWidget(self.home_widget)

  def show_upgrade_screen(self, player):
    self.upgrade_screen.set_player(player)
    self.stack.setCurrentWidget(self.upgrade_screen)

  def show_gacha_screen(self):

    self.gacha_screen.refresh()

    self.stack.setCurrentWidget(
        self.gacha_screen
    )

  def show_battle_screen(self):

    self.battle_screen.refresh()

    self.stack.setCurrentWidget(
        self.battle_screen
    )

app=QApplication(sys.argv)
m=Main()
m.show()
app.exec()
