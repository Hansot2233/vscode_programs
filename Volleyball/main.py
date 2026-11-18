import sys, os
from PyQt6.QtWidgets import *
from game_data import GameData
from battle_engine import simulate
from save_manager import save_game,load_game
from screens.team_screen import TeamScreen

SAVE_FILE = os.path.join(
    os.path.dirname(__file__),
    "saves",
    "save.json"
)

class Main(QMainWindow):
  def __init__(self):
    super().__init__()
    self.g=GameData()
    load_game(self.g, SAVE_FILE)
    w=QWidget(); l=QVBoxLayout()
    self.info=QLabel()
    self.list=QListWidget()
    l.addWidget(self.info)
    l.addWidget(self.list)
    for t,f in [
      ('Spin', self.spin),
      ('Upgrade', self.upgrade),
      ('Battle', self.battle),
      ('Save', self.save)
    ]:
      b=QPushButton(t); b.clicked.connect(f); l.addWidget(b)
    team_button = QPushButton("Team Manager")
    team_button.clicked.connect(self.open_team_manager)
    l.addWidget(team_button)
    w.setLayout(l); self.setCentralWidget(w); self.refresh()
  def refresh(self):
    self.info.setText(
      f"Lv {self.g.level} | "
      f"Coins {self.g.coins} | "
      f"Spins {self.g.spins} | "
      f"Team Rating {self.g.team_rating()}"
    )
    self.list.clear()
    [self.list.addItem(f'{p.name} {p.position} {p.rarity} STR {p.strength}') for p in self.g.roster]
  def spin(self):
    if self.g.spins>0: 
      self.g.spins-=1
      self.g.roster.append(self.g.generate_player())
      self.refresh()
  def upgrade(self):
    if self.g.roster and self.g.coins>=100: 
      max(self.g.roster,key=lambda p:p.strength).level+=1; self.g.coins-=100
      self.refresh()
  def battle(self):

    if not self.g.lineup_complete():

      QMessageBox.information(
          self,
          "Incomplete Team",
          "Fill all 7 lineup positions first."
      )

      return
    
    w,e=simulate(self.g.team_rating(),self.g.level)
    if w: 
      self.g.level+=1
      self.g.coins+=200
      self.g.spins+=1
    QMessageBox.information(self,'Result',('Win' if w else 'Loss')+f' vs {e}'); self.refresh()
  def save(self): 
    save_game(self.g,SAVE_FILE)
  def open_team_manager(self):
    self.team_window = TeamScreen(self.g)
    self.team_window.show()
app=QApplication(sys.argv); m=Main(); m.show(); app.exec()
