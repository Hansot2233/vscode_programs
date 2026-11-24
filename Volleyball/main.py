import sys, os
from PyQt6.QtWidgets import *
from game_data import GameData
from battle_engine import simulate, get_enemy_team, play_rally
from save_manager import save_game,load_game
from screens.team_screen import TeamScreen
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QTimer
from screens.team_screen import TeamScreen
from screens.player_upgrade_screen import PlayerUpgradeScreen
from screens.gacha_screen import GachaScreen
from screens.battle_screen import BattleScreen
from screens.league_screen import LeagueScreen
from league_engine import create_league, simulate_other_matches, get_current_match

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
        ('League', self.show_league_screen),
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
    self.league_screen = LeagueScreen(self.g)

    self.upgrade_screen = PlayerUpgradeScreen(self.g)
    self.team_screen.open_upgrade_requested.connect(self.show_upgrade_screen)
    self.battle_screen.start_button.clicked.connect(self.battle)
    self.league_screen.play_button.clicked.connect(self.league_battle)
    self.league_screen.reset_button.clicked.connect(self.reset_league)

    back_button = QPushButton("Back")
    back_button.clicked.connect(self.show_home_screen)
    back_to_home = QPushButton("Back")
    back_to_home.clicked.connect(self.show_home_screen)
    battle_back = QPushButton("Back")
    battle_back.clicked.connect(self.show_home_screen)
    league_back = QPushButton("Back")
    league_back.clicked.connect(self.show_home_screen)

    self.battle_screen.layout.addWidget(battle_back)
    self.gacha_screen.layout().addWidget(back_to_home)
    self.team_screen.layout().addWidget(back_button)
    self.league_screen.layout().addWidget(league_back)    

    self.stack.addWidget(self.home_widget)
    self.stack.addWidget(self.team_screen)
    self.stack.addWidget(self.upgrade_screen)
    self.stack.addWidget(self.gacha_screen)
    self.stack.addWidget(self.battle_screen)
    self.stack.addWidget(self.league_screen)

    back_to_team = QPushButton("Back")
    back_to_team.clicked.connect(self.show_team_screen)
    self.upgrade_screen.layout.addWidget(back_to_team)

    self.setCentralWidget(self.stack)

    self.refresh()
    
    self.autosave_timer = QTimer(self)
    self.autosave_timer.timeout.connect(self.save)
    self.autosave_timer.start(30000)

  def refresh(self):

    self.info.setText(
        f"Lv {self.g.level} | "
        f"Stage {self.g.battle_level} | "
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

    self.battle_screen.start_button.setEnabled(False)

    self.stage = self.g.battle_level

    self.player_team = [
        p for p in self.g.lineup.values()
        if p is not None
    ]

    self.enemy_team, self.enemy_league = (
        self.g.get_current_enemy()
    )

    self.player_sets = 0
    self.enemy_sets = 0

    self.player_points = 0
    self.enemy_points = 0

    self.set_scores = []

    self.battle_screen.score_label.setText(
        "Set 1\n\n0 - 0\n\nSets: 0 - 0"
    )

    self.play_next_rally()

  def play_next_rally(self):

    # Simulate one rally
    if play_rally(
        self.player_team,
        self.enemy_team
    ):

        self.player_points += 1

    else:

        self.enemy_points += 1

    # Update live scoreboard
    self.battle_screen.score_label.setText(
        f"Set {len(self.set_scores) + 1}\n\n"
        f"{self.player_points} - {self.enemy_points}\n\n"
        f"Sets: {self.player_sets} - {self.enemy_sets}\n\n"
        f"Completed Sets: "
        f"{' | '.join(self.set_scores)}"
    )

    # Check whether the set has ended
    set_finished = (
        (self.player_points >= 25 or
         self.enemy_points >= 25)
        and
        abs(
            self.player_points -
            self.enemy_points
        ) >= 2
    )

    if set_finished:

        self.set_scores.append(
            f"{self.player_points}-{self.enemy_points}"
        )

        if self.player_points > self.enemy_points:
            self.player_sets += 1
        else:
            self.enemy_sets += 1

        self.battle_screen.score_label.setText(
            f"Set {len(self.set_scores)} Complete!\n\n"
            f"{self.player_points} - {self.enemy_points}\n\n"
            f"Sets: {self.player_sets} - {self.enemy_sets}\n\n"
            f"Completed Sets: "
            f"{' | '.join(self.set_scores)}"
        )

        # Check whether the match has ended
        if self.player_sets == 3 or self.enemy_sets == 3:

            QTimer.singleShot(
                500,
                self.finish_battle
            )

            return

        # Prepare next set
        self.player_points = 0
        self.enemy_points = 0

    # Wait 0.5 seconds before the next rally
    QTimer.singleShot(
        100,
        self.play_next_rally
    )

  def finish_battle(self):

        winner = self.player_sets > self.enemy_sets

        stage = self.stage

        reward = 0
        gems = 0

        if winner:

            self.g.level += 1
            self.g.battle_level += 1

            self.g.current_enemy_team = None
            self.g.current_enemy_league = None

            reward = int(
                (5001 ** (self.g.battle_level / 100)) * 0.15
            ) + 1000

            gems = max(
                1,
                int(1 + (self.g.battle_level ** 2) / 250)
            )

            self.g.coins += reward
            self.g.gems += gems

        result_text = (
            f"{'WIN' if winner else 'LOSS'}\n\n"
            f"Stage: {stage}\n\n"
            f"Set Scores:\n"
        )

        for score in self.set_scores:
            result_text += score + "\n"

        if winner:

            result_text += (
                f"\nRewards:\n"
                f"Coins: {reward}\n"
                f"Gems: {gems}\n"
                f""
            )

        # Result popup
        popup = QDialog(self)

        popup.setWindowTitle("Match Result")

        screen_geometry = self.screen().availableGeometry()

        popup_width = int(
            screen_geometry.width() * 0.33
        )

        popup_height = int(
            screen_geometry.height() * 0.4
        )

        popup.setFixedSize(
            popup_width,
            popup_height
        )

        popup.move(
            screen_geometry.center().x() - popup_width // 2,
            screen_geometry.center().y() - popup_height // 2
        )

        layout = QVBoxLayout(popup)

        result_label = QLabel(result_text)

        result_label.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        result_label.setWordWrap(True)

        result_label.setStyleSheet(
            "font-size: 16px;"
        )

        layout.addWidget(result_label, 1)

        ok_button = QPushButton("OK")

        ok_button.clicked.connect(popup.accept)

        layout.addWidget(ok_button)

        popup.exec()

        self.battle_screen.start_button.setEnabled(True)

        self.battle_screen.refresh()
        self.refresh()

  def league_battle(self):

    if self.g.playoff_active:

      if (
          not self.g.playoff_teams
          or
          not self.g.playoff_matchups
      ):

          msg = QMessageBox(self)

          msg.setWindowTitle(
              "Playoffs Reset"
          )

          msg.setText(
              "Playoff data was incomplete.\n"
              "A new league has been generated."
          )

          msg.setIcon(
              QMessageBox.Icon.NoIcon
          )

          msg.exec()

          self.g.playoff_active = False

          create_league(
              self.g
          )

          self.league_screen.refresh()

          return

      self.playoff_battle()

      return

    your_team = next(

        t

        for t in self.g.league_teams

        if t["name"] == "Your Team"

    )

    your_team["lineup"] = [

        p

        for p in self.g.lineup.values()

        if p is not None

    ]

    opponent_name = (
        get_current_match(
            self.g
        )
    )

    if opponent_name is None:

        QMessageBox.information(
            self,
            "Season Complete",
            "Start a new season."
        )

        return

    team = next(

        t

        for t in self.g.league_teams

        if t["name"] == opponent_name

    )

    from battle_engine import (
        simulate_match
    )

    winner, scores = simulate_match(

        [

            p

            for p in self.g.lineup.values()

            if p is not None

        ],

        team["lineup"]

    )

    if winner:

        self.g.coins += 50

        your_team["wins"] += 1
        team["losses"] += 1

        reward_text = (
            "\n\nReward:\n"
            "50 Coins"
        )

    else:

        your_team["losses"] += 1
        team["wins"] += 1

        reward_text = ""

    your_team["played"] += 1
    team["played"] += 1

    week = self.g.league_schedule[
    self.g.league_week
    ]

    for team_a_name, team_b_name in week:

      if "Your Team" in [
          team_a_name,
          team_b_name
      ]:
          continue

      team_a = next(

          t

          for t in self.g.league_teams

          if t["name"] == team_a_name

      )

      team_b = next(

          t

          for t in self.g.league_teams

          if t["name"] == team_b_name

      )

      ai_winner, _ = simulate_match(

          team_a["lineup"],
          team_b["lineup"]

      )

      if ai_winner:

          team_a["wins"] += 1
          team_b["losses"] += 1

      else:

          team_b["wins"] += 1
          team_a["losses"] += 1

      team_a["played"] += 1
      team_b["played"] += 1

    self.g.league_week += 1

    result_text = (
        f"{'WIN' if winner else 'LOSS'}\n\n"
        f"Your Team vs "
        f"{opponent_name}\n\n"
        f"Sets:\n"
    )

    for score in scores:

      if isinstance(
          score,
          tuple
      ):

          result_text += (
              f"{score[0]}"
              f"-"
              f"{score[1]}\n"
          )

      else:

          result_text += (
              str(score)
              +
              "\n"
          )

    result_text += reward_text

    msg = QMessageBox(self)

    msg.setWindowTitle(
        "League Match"
    )

    msg.setText(
        result_text
    )

    msg.setIcon(
        QMessageBox.Icon.NoIcon
    )

    msg.exec()

    self.league_screen.refresh()
    self.refresh()

    if (self.g.league_week >= len(self.g.league_schedule)):

      standings = sorted(

          self.g.league_teams,

          key=lambda t: (
              t["wins"],
              -t["losses"]
          ),

          reverse=True

      )

      placement = next(

          (
              i + 1

              for i, team in enumerate(
                  standings
              )

              if team["name"] == "Your Team"
          ),

          16

      )

      if placement == 1:

          gems = 500

      elif placement <= 4:

          gems = 250

      elif placement <= 8:

          gems = 100

      else:

          gems = 50

      self.g.gems += gems

      msg = QMessageBox(self)

      msg.setWindowTitle(
          "Season Complete"
      )

      msg.setText(
          f"You finished "
          f"#{placement}\n\n"
          f"Reward:\n"
          f"{gems} Gems"
      )

      msg.setIcon(
          QMessageBox.Icon.NoIcon
      )

      msg.exec()
      
      if placement <= 4:
        self.g.league_top4_finishes += 1

      self.start_playoffs()
      
      self.league_screen.refresh()

  def start_playoffs(self):

    self.g.playoff_history = []
    self.g.playoff_teams = []

    standings = sorted(
    
      self.g.league_teams,
    
      key=lambda t: (
          t["wins"],
          -t["losses"]
      ),
      reverse=True
    )

    for seed, team in enumerate(
        standings,
        start=1
    ):

        team["seed"] = seed

        self.g.playoff_teams.append(
            team
        )

    self.g.playoff_teams = standings

    self.g.playoff_matchups = []
    
    seed_map = {

      team["seed"]: team

      for team in self.g.playoff_teams

    }

    self.g.playoff_matchups = [

        (
            seed_map[1]["name"],
            seed_map[16]["name"]
        ),

        (
            seed_map[2]["name"],
            seed_map[15]["name"]
        ),

        (
            seed_map[3]["name"],
            seed_map[14]["name"]
        ),

        (
            seed_map[4]["name"],
            seed_map[13]["name"]
        ),

        (
            seed_map[5]["name"],
            seed_map[12]["name"]
        ),

        (
            seed_map[6]["name"],
            seed_map[11]["name"]
        ),

        (
            seed_map[7]["name"],
            seed_map[10]["name"]
        ),

        (
            seed_map[8]["name"],
            seed_map[9]["name"]
        )

    ]  

    self.g.playoff_active = True

    self.g.playoff_round = 1

    QMessageBox(
        QMessageBox.Icon.NoIcon,
        "Playoffs",
        "Playoffs have begun!"
    ).exec()

  def get_playoff_opponent(self):

    standings = self.g.playoff_teams

    your_index = next(

        i

        for i, team in enumerate(
            standings
        )

        if team["name"] == "Your Team"

    )

    opponent_index = (
        len(standings)
        - 1
        - your_index
    )

    if opponent_index == your_index:

        return None

    return standings[
        opponent_index
    ]

  def playoff_battle(self):

    opponent = (
        self.get_playoff_opponent()
    )

    from battle_engine import (
        simulate_match
    )

    winner, scores = simulate_match(

        [
            p
            for p in self.g.lineup.values()
            if p is not None
        ],

        opponent["lineup"]

    )

    result_text = (
      f"PLAYOFFS\n\n"
      f"Round "
      f"{self.g.playoff_round}\n\n"
      f"Your Team vs "
      f"{opponent['name']}\n\n"
    )

    for score in scores:

      if isinstance(score, tuple):

          result_text += (
              f"{score[0]}-{score[1]}\n"
          )

      else:

          result_text += (
              str(score) + "\n"
          )

    if winner:

      self.g.coins += 2500

      result_text += (
        "\nReward:\n"
        "2500 Coins"
      )

      msg = QMessageBox(self)

      msg.setWindowTitle(
          "Playoff Victory"
      )

      msg.setText(
          result_text
      )

      msg.setIcon(
          QMessageBox.Icon.NoIcon
      )

      msg.exec()

      self.g.playoff_teams.remove(
          opponent
      )

      survivors = []

      # Keep Your Team alive since it already won

      your_team_entry = next(

          team

          for team in self.g.playoff_teams

          if team["name"] == "Your Team"

      )

      survivors.append(
          your_team_entry
      )

      # Remove Your Team from AI simulation

      teams = [

          team

          for team in self.g.playoff_teams

          if team["name"] != "Your Team"

      ]

      while len(teams) >= 2:

          high = teams.pop(0)

          low = teams.pop(-1)

          ai_winner, _ = simulate_match(

              high["lineup"],
              low["lineup"]

          )

          survivors.append(

              high

              if ai_winner

              else low

          )

      self.g.playoff_teams = survivors

      self.g.playoff_history.append(

        {
            "round": self.g.playoff_round,
            "teams": [

                team["name"]

                for team in survivors

            ]
          }
      )

      self.g.playoff_matchups = []
      winners = [

          team["name"]

          for team in survivors

      ]

      if self.g.playoff_round == 1:

        self.g.playoff_matchups = [

            (
                winners[0],
                winners[7]
            ),

            (
                winners[1],
                winners[6]
            ),

            (
                winners[2],
                winners[5]
            ),

            (
                winners[3],
                winners[4]
            )

        ]

      elif self.g.playoff_round == 2:

        self.g.playoff_matchups = [

            (
                winners[0],
                winners[3]
            ),

            (
                winners[1],
                winners[2]
            )

        ]

      elif self.g.playoff_round == 3:

        self.g.playoff_matchups = [

            (
                winners[0],
                winners[1]
            )

        ]

      self.g.playoff_round += 1

      if (
          self.g.playoff_round == 3
          and
          not getattr(
              self.g,
              "league_incremented",
              False
          )
      ):

          self.g.league_number += 1

          self.g.league_incremented = True

      if len(self.g.playoff_teams) == 1:
         
         champion = (self.g.playoff_teams[0])

         if champion["name"] == "Your Team":
            
            self.g.coins += 10000

            QMessageBox(
                QMessageBox.Icon.NoIcon,
                "Champion",
                "You won the league!\n\n"
                "Reward:\n"
                "10,000 Coins"
            ).exec()

            self.g.playoff_active = False

            create_league(self.g)

    if not winner:

        self.g.playoff_active = False

        msg = QMessageBox(self)

        msg.setWindowTitle(
            "Playoffs Eliminated"
        )

        msg.setText(
            result_text +
            "\n\nYour playoff run has ended."
        )

        msg.setIcon(
            QMessageBox.Icon.NoIcon
        )

        msg.exec()

        create_league(
            self.g
        )

        self.league_screen.refresh()

        self.refresh()

        self.stack.setCurrentWidget(
            self.league_screen
        )

        return

    self.league_screen.refresh()
    self.refresh()

  def reset_league(self):

    reply = QMessageBox.question(

        self,

        "Reset League",

        "Reset the current league and playoffs?\n\n"
        "All standings and playoff progress will be lost.",

        QMessageBox.StandardButton.Yes
        |
        QMessageBox.StandardButton.No

    )

    if (
        reply
        !=
        QMessageBox.StandardButton.Yes
    ):
        return

    create_league(
        self.g
    )

    self.league_screen.refresh()

    self.refresh()
  
  def save(self):
    save_game(self.g, SAVE_FILE)

  def closeEvent(self, event):
    self.save()     
    event.accept()

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

  def show_league_screen(self):

    if not self.g.league_teams:

        create_league(
            self.g
        )

    if (
      self.g.playoff_active
      and
      (
          not self.g.playoff_teams
          or
          not self.g.playoff_matchups
      )
    ):

      self.g.playoff_active = False

      create_league(
          self.g
      )

    your_team = next(

        (

            t

            for t in self.g.league_teams

            if t["name"] == "Your Team"

        ),

        None

    )

    if your_team:

        your_team["lineup"] = [

            p

            for p in self.g.lineup.values()

            if p is not None

        ]

    self.league_screen.refresh()

    self.stack.setCurrentWidget(
        self.league_screen
    )



app=QApplication(sys.argv)
m=Main()
m.show()
app.exec()
