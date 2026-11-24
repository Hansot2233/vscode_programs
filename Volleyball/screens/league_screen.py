from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from league_engine import get_current_match

class LeagueScreen(QWidget):

    def __init__(self, game):

        super().__init__()

        self.game = game

        layout = QVBoxLayout()

        top_bar = QHBoxLayout()

        top_bar.addStretch()

        self.reset_button = QPushButton(
            "Reset League"
        )

        self.reset_button.setStyleSheet("""
            background-color: #8B0000;
            color: white;
            padding: 6px;
        """)

        top_bar.addWidget(
            self.reset_button
        )

        layout.addLayout(
            top_bar
        )

        self.league_counter = QLabel()

        self.league_counter.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.league_counter.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            padding: 10px;
        """)

        self.table = QListWidget()

        self.bracket_tree = QTreeWidget()

        self.bracket_tree.setHeaderHidden(
            True
        )

        self.bracket_tree.setMinimumHeight(
            100
        )


        self.play_button = QPushButton(
            "Play Selected Team"
        )

        if self.game.playoff_active:

            self.week_label.setText(

                f"PLAYOFFS\n"
                f"Round {self.game.playoff_round}"

            )

            opponent = None

            if self.game.playoff_matchups:

                for matchup in self.game.playoff_matchups:

                    if matchup[0] == "Your Team":

                        opponent = matchup[1]

                        break

                    elif matchup[1] == "Your Team":

                        opponent = matchup[0]

                        break

            if opponent:

                self.play_button.setText(
                    f"Play vs {opponent}"
                )

            else:

                self.play_button.setText(
                    "Playoff Match"
                )

            return

        self.standings_toggle = QPushButton(
            "▼ Regular Season Standings"
        )

        self.bracket_toggle = QPushButton(
            "▼ Playoff Bracket"
        )

        self.standings_toggle.clicked.connect(
            self.toggle_standings
        )

        self.bracket_toggle.clicked.connect(
            self.toggle_bracket
        )

        layout.addWidget(
            self.league_counter
        )

        layout.addWidget(
            self.standings_toggle
        )

        layout.addWidget(
            self.table
        )

        layout.addWidget(
            self.bracket_toggle
        )

        layout.addWidget(
            self.bracket_tree
        )

        layout.addWidget(
            self.play_button
        )

        self.show_standings = True
        self.show_bracket = True

        self.setLayout(layout)

    def refresh(self):

        self.bracket_tree.clear()
        self.league_counter.setText(f"LEAGUE #{self.game.league_number}")
        if self.game.playoff_active:

            self.bracket_tree.show()

            self.bracket_toggle.show()

            self.play_button.setText(
                "Play Playoff Match"
            )

            playoff_root = QTreeWidgetItem(
                [
                    f"PLAYOFFS - Round {self.game.playoff_round}"
                ]
            )

            self.bracket_tree.addTopLevelItem(
                playoff_root
            )

            for matchup in self.game.playoff_matchups:

                match_item = QTreeWidgetItem(
                    [
                        f"{matchup[0]} vs {matchup[1]}"
                    ]
                )

                playoff_root.addChild(
                    match_item
                )

            for round_data in self.game.playoff_history:

                round_item = QTreeWidgetItem(
                    [
                        f"Round {round_data['round']} Winners"
                    ]
                )

                playoff_root.addChild(
                    round_item
                )

                for team_name in round_data["teams"]:

                    round_item.addChild(
                        QTreeWidgetItem(
                            [team_name]
                        )
                    )

            playoff_root.setExpanded(
                False
            )

        else:

            self.bracket_tree.hide()

            self.bracket_toggle.hide()

            opponent = get_current_match(
                self.game
            )

            if opponent:

                self.play_button.setText(
                    f"Play vs {opponent}"
                )

            else:

                self.play_button.setText(
                    "Season Complete"
                )

        self.table.clear()

        standings = sorted(

            self.game.league_teams,

            key=lambda team: (
                team["wins"],
                -team["losses"]
            ),

            reverse=True

        )

        rank = 1

        for team in standings:

            # Calculate average team strength
            strength = sum(
                player.strength
                for player in team["lineup"]
            ) // max(len(team["lineup"]), 1)

            self.table.addItem(

                f"{rank}. "
                f"{team['name']} | "
                f"STR {strength} | "
                f"{team['wins']}-{team['losses']}"

            )

            rank += 1

    def toggle_standings(self):

        self.show_standings = (
            not self.show_standings
        )

        self.table.setVisible(
            self.show_standings
        )

        self.standings_toggle.setText(

            "▼ Regular Season Standings"

            if self.show_standings

            else

            "▶ Regular Season Standings"

        )

    def toggle_bracket(self):

        self.show_bracket = (
            not self.show_bracket
        )

        self.bracket_tree.setVisible(
            self.show_bracket
        )

        self.bracket_toggle.setText(

            "▼ Playoff Bracket"

            if self.show_bracket

            else

            "▶ Playoff Bracket"

        )

    def reset_league(self):

        create_league(
            self.g
        )

        self.league_screen.refresh()

        self.refresh()