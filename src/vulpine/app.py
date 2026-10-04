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
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class VulpineShell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vulpine Shell")
        self.resize(1280, 720)

        # -------------------------------------------------
        # Root layout
        # -------------------------------------------------

        root = QWidget()

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.setCentralWidget(root)

        # -------------------------------------------------
        # Sidebar
        # -------------------------------------------------

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(110)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 24, 12, 24)
        sidebar_layout.setSpacing(12)

        self.nav_buttons = {}

        page_names = (
            "Home",
            "Games",
            "Code",
            "Files",
            "Terminal",
            "Settings",
        )

        for name in page_names:
            button = QPushButton(name)
            button.setObjectName("navButton")

            button.clicked.connect(
                lambda checked=False, page_name=name:
                    self.show_page(page_name)
            )

            sidebar_layout.addWidget(button)

            self.nav_buttons[name] = button

        sidebar_layout.addStretch()

        # -------------------------------------------------
        # Page stack
        # -------------------------------------------------

        self.stack = QStackedWidget()

        self.pages = {}

        # Home is special, so we build it separately.
        home_page = self.build_home_page()

        self.pages["Home"] = home_page
        self.stack.addWidget(home_page)

        # The other pages can start as placeholders.
        placeholder_pages = {
            "Games": (
                "GAMES",
                "Installed games and launchers will live here.",
            ),
            "Code": (
                "DEVELOPMENT",
                "Projects, editors, tools, and environments will live here.",
            ),
            "Files": (
                "FILES",
                "Vulpine's file browser will live here.",
            ),
            "Terminal": (
                "TERMINAL",
                "Command-line tools and shell access will live here.",
            ),
            "Settings": (
                "SETTINGS",
                "Vulpine configuration will live here.",
            ),
        }

        for page_name, page_info in placeholder_pages.items():
            title, description = page_info

            page = self.build_placeholder_page(
                title,
                description,
            )

            self.pages[page_name] = page
            self.stack.addWidget(page)

        # -------------------------------------------------
        # Add major regions
        # -------------------------------------------------

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.stack)

        # -------------------------------------------------
        # Styling
        # -------------------------------------------------

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

            #navButton[active="true"] {
                color: #45c4ff;

                background: #101a22;

                border-left: 2px solid #45c4ff;
            }

            #title {
                color: #45c4ff;

                font-size: 34px;
                font-weight: 300;
            }

            #subtitle {
                color: #647480;

                font-size: 11px;
            }

            #sectionTitle {
                color: #788995;

                font-size: 12px;
            }

            #pageTitle {
                color: #45c4ff;

                font-size: 28px;
                font-weight: 300;
            }

            #pageDescription {
                color: #758590;

                font-size: 14px;
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

        # -------------------------------------------------
        # Stats timer
        # -------------------------------------------------

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

        self.update_stats()

        # Start on Home.
        self.show_page("Home")

    # -----------------------------------------------------
    # Page creation
    # -----------------------------------------------------

    def build_home_page(self):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(48, 40, 48, 40)

        title = QLabel("VULPINE")
        title.setObjectName("title")

        subtitle = QLabel(
            "PLAY   /   CODE   /   CREATE   /   EXPLORE"
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(50)

        section_title = QLabel("HOME")
        section_title.setObjectName("sectionTitle")

        layout.addWidget(section_title)

        cards = QHBoxLayout()

        games_button = QPushButton("Games")
        games_button.setObjectName("card")

        games_button.clicked.connect(
            lambda:
                self.show_page("Games")
        )

        development_button = QPushButton("Development")
        development_button.setObjectName("card")

        development_button.clicked.connect(
            lambda:
                self.show_page("Code")
        )

        cards.addWidget(games_button)
        cards.addWidget(development_button)

        layout.addLayout(cards)

        layout.addStretch()

        self.stats = QLabel()
        self.stats.setObjectName("stats")
        self.stats.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        layout.addWidget(self.stats)

        return page

    def build_placeholder_page(
        self,
        title_text,
        description_text,
    ):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(48, 40, 48, 40)

        title = QLabel(title_text)
        title.setObjectName("pageTitle")

        description = QLabel(description_text)
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addStretch()

        return page

    # -----------------------------------------------------
    # Navigation
    # -----------------------------------------------------

    def show_page(self, page_name):
        page = self.pages[page_name]

        self.stack.setCurrentWidget(page)

        for name, button in self.nav_buttons.items():
            is_active = name == page_name

            button.setProperty(
                "active",
                is_active,
            )

            button.style().unpolish(button)
            button.style().polish(button)

    # -----------------------------------------------------
    # System monitoring
    # -----------------------------------------------------

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