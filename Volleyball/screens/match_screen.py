from PyQt6.QtWidgets import (QWidget,QLabel,QVBoxLayout)
from PyQt6.QtCore import QTimer
import random

class MatchScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout()

        self.status = QLabel(
            "Waiting..."
        )

        self.layout.addWidget(
            self.status
        )

        self.setLayout(
            self.layout
        )

    def start_match(self,player_rating,enemy_rating):

        self.player_rating = player_rating
        self.enemy_rating = enemy_rating

        self.player_sets = 0
        self.enemy_sets = 0

        self.current_set = 1

        self.status.setText(
            "MATCH STARTED"
        )

        QTimer.singleShot(
            3000,
            self.play_next_set
        )

    def play_next_set(self):

        if (
            self.player_sets >= 3
            or
            self.enemy_sets >= 3
        ):

            self.match_finished()

            return

        player_score = (
            self.player_rating *
            random.uniform(0.85, 1.15)
        )

        enemy_score = (
            self.enemy_rating *
            random.uniform(0.85, 1.15)
        )
