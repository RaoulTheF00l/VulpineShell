import sys

import psutil

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class VulpineShell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vulpine Shell")
        self.resize(1280, 720)

        # -------------------------
        # Sidebar
        # -------------------------

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(110)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 24, 12, 24)
        sidebar_layout.setSpacing(12)

        for name in (
            "Home",
            "Games",
            "Code",
            "Files",
            "Terminal",
            "Settings",
        ):
            button = QPushButton(name)
            button.setObjectName("navButton")
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        # -------------------------
        # Main area
        # -------------------------

        main_panel = QWidget()

        main_layout = QVBoxLayout(main_panel)
        main_layout.setContentsMargins(48, 40, 48, 40)

        title = QLabel("VULPINE")
        title.setObjectName("title")

        subtitle = QLabel("PLAY   /   CODE   /   CREATE   /   EXPLORE")
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(50)

        section_title = QLabel("HOME")
        section_title.setObjectName("sectionTitle")
        main_layout.addWidget(section_title)

        # -------------------------
        # Quick launch cards
        # -------------------------

        cards = QHBoxLayout()

        games_button = QPushButton("Games")
        games_button.setObjectName("card")

        dev_button = QPushButton("Development")
        dev_button.setObjectName("card")

        cards.addWidget(games_button)
        cards.addWidget(dev_button)

        main_layout.addLayout(cards)

        main_layout.addStretch()

        # -------------------------
        # System stats
        # -------------------------

        self.stats = QLabel()
        self.stats.setObjectName("stats")
        self.stats.setAlignment(Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(self.stats)

        # -------------------------
        # Root layout
        # -------------------------

        root = QWidget()

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(main_panel)

        self.setCentralWidget(root)

        # -------------------------
        # Styling
        # -------------------------

        self.setStyleSheet(
            """
            QMainWindow {
                background: #070b0f;
            }

            QWidget {
                background: #070b0f;
                color: #d8e2e8;
                font-family: "Segoe UI";
            }

            #sidebar {
                background: #0b1117;
                border-right: 1px solid #16232d;
            }

            #navButton {
                background: transparent;
                border: none;
                color: #8e9ba5;

                text-align: left;

                padding: 12px;

                font-size: 14px;
            }

            #navButton:hover {
                color: #45c4ff;
                background: #0f1820;
            }

            #title {
                color: #45c4ff;

                font-size: 34px;
                font-weight: 300;
            }

            #subtitle {
                color: #647480;

                font-size: 11px;
                letter-spacing: 2px;
            }

            #sectionTitle {
                color: #788995;

                font-size: 12px;
            }

            #card {
                background: #0b1117;

                border: 1px solid #16232d;
                border-radius: 8px;

                color: #d8e2e8;

                font-size: 18px;

                min-height: 120px;
            }

            #card:hover {
                border: 1px solid #45c4ff;
                background: #0d151c;
            }

            #stats {
                color: #71818c;

                font-size: 13px;
            }
            """
        )

        # -------------------------
        # Stats timer
        # -------------------------

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

        self.update_stats()

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.stats.setText(
            f"CPU  {cpu:.0f}%     RAM  {ram:.0f}%"
        )


def main():
    app = QApplication(sys.argv)

    shell = VulpineShell()
    shell.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()