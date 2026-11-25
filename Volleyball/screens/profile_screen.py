from PyQt6.QtWidgets import *
from account_manager import load_accounts, create_account, delete_account

class ProfileScreen(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        title = QLabel(
            "Select Profile"
        )

        self.list = QListWidget()

        self.new_button = QPushButton("Create Profile")
        self.delete_button = QPushButton("Delete Profile")
        self.play_button = QPushButton("Play")

        layout.addWidget(title)
        layout.addWidget(self.list)

        layout.addWidget(self.new_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.play_button)

        self.setLayout(layout)

        self.new_button.clicked.connect(self.create_profile)
        self.delete_button.clicked.connect(self.delete_profile)

        self.refresh()

    def refresh(self):

        self.list.clear()

        for account in load_accounts():

            self.list.addItem(
                account["username"]
            )

    def create_profile(self):

        username, ok = (
            QInputDialog.getText(
                self,
                "Create Profile",
                "Username"
            )
        )

        if not ok:
            return

        username = username.strip()

        if not username:
            return

        create_account(
            username
        )

        self.refresh()

    def delete_profile(self):

        row = self.list.currentRow()

        if row < 0:
            return

        accounts = load_accounts()

        account = accounts[row]

        reply = QMessageBox.question(

            self,

            "Delete Profile",

            f"Delete profile "
            f"'{account['username']}'?\n\n"
            f"This cannot be undone.",

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

        delete_account(
            account["id"]
        )

        self.refresh()