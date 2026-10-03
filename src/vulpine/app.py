import sys

import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class VulpineShell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vulpine Shell")
        self.resize(1280, 720)

        self.title = QLabel("VULPINE")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stats = QLabel()
        self.stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.stats)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #080c10;
            }

            QLabel {
                color: #d7e2e8;
                font-family: "Segoe UI";
            }
            """
        )

        self.title.setStyleSheet(
            """
            font-size: 32px;
            color: #4dc3ff;
            """
        )

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