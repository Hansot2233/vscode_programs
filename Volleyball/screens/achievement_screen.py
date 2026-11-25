from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton
)
from progression import (
    ACHIEVEMENTS, achievement_progress, claim_achievement
)


class AchievementScreen(QWidget):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.layout = QVBoxLayout(self)

        self.title = QLabel("ACHIEVEMENTS")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title)

        self.list = QListWidget()
        self.list.currentRowChanged.connect(self.show_details)
        self.layout.addWidget(self.list)

        self.details = QLabel("Select an achievement to see its progress.")
        self.details.setWordWrap(True)
        self.layout.addWidget(self.details)

        buttons = QHBoxLayout()
        self.claim_button = QPushButton("Claim Reward")
        self.claim_button.clicked.connect(self.claim_selected)
        self.claim_button.setEnabled(False)
        buttons.addWidget(self.claim_button)
        self.layout.addLayout(buttons)

        self.refresh()

    def refresh(self):
        selected_id = None
        if self.list.currentItem():
            selected_id = self.list.currentItem().data(256)

        self.list.clear()
        claimed = set(getattr(self.game, "claimed_achievements", []))
        self.achievement_by_row = {}

        for achievement in ACHIEVEMENTS:
            progress = achievement_progress(self.game, achievement)
            complete = progress >= achievement["target"]
            is_claimed = achievement["id"] in claimed

            if is_claimed:
                status = "CLAIMED"
            elif complete:
                status = "READY TO CLAIM"
            else:
                status = f"{progress}/{achievement['target']}"

            item = QListWidgetItem(
                f"[{achievement['category']}] {achievement['title']} — {status}"
            )
            item.setData(256, achievement["id"])
            self.list.addItem(item)

        if selected_id:
            for i in range(self.list.count()):
                if self.list.item(i).data(256) == selected_id:
                    self.list.setCurrentRow(i)
                    break
        elif self.list.count():
            self.list.setCurrentRow(0)

        self.show_details(self.list.currentRow())

    def show_details(self, row):
        if row < 0 or row >= self.list.count():
            self.details.setText("Select an achievement to see its progress.")
            self.claim_button.setEnabled(False)
            return

        achievement_id = self.list.item(row).data(256)
        achievement = next(a for a in ACHIEVEMENTS if a["id"] == achievement_id)
        progress = achievement_progress(self.game, achievement)
        claimed = achievement_id in set(getattr(self.game, "claimed_achievements", []))
        complete = progress >= achievement["target"]

        self.details.setText(
            f"{achievement['description']}\n\n"
            f"Progress: {progress}/{achievement['target']}\n"
            f"Reward: {achievement['coins']:,} Coins + {achievement['gems']:,} Gems\n"
            f"Status: {'Claimed' if claimed else 'Ready to claim' if complete else 'In progress'}"
        )
        self.claim_button.setEnabled(complete and not claimed)
        self.claim_button.setText("Claim Reward" if complete and not claimed else "Already Claimed" if claimed else "Not Complete")

    def claim_selected(self):
        item = self.list.currentItem()
        if item is None:
            return
        if claim_achievement(self.game, item.data(256)):
            self.refresh()
