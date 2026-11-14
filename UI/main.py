import os
import sys

# let python find the UI package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout,
                               QLabel, QMainWindow, QPushButton,
                               QStackedWidget, QVBoxLayout, QWidget)

from UI import styles
from UI.createPreset import CreatePresetPage
from UI.icons import get_icon
from UI.settings import SettingsPage
from UI.styles import apply_icon
from UI.yourPresets import YourPresetsPage


# fonts
def load_fonts():
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    for name in ["Inter-Regular.otf", "Inter-Bold.otf"]:
        QFontDatabase.addApplicationFont(os.path.join(folder, name))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Presetly")
        self.resize(1100, 700)
        self.setMinimumSize(980, 640)

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(16, 22, 16, 16)
        side_layout.setSpacing(6)

        logo_row = QHBoxLayout()
        logo_row.setContentsMargins(6, 0, 0, 0)
        logo_row.setSpacing(10)
        self.logo_icon = QLabel()
        logo_text = QLabel("Presetly")
        logo_text.setObjectName("logo")
        logo_row.addWidget(self.logo_icon)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()
        side_layout.addLayout(logo_row)
        side_layout.addSpacing(22)

        # pages
        self.stack = QStackedWidget()
        self.stack.setObjectName("content")
        self.create_page = CreatePresetPage()
        self.presets_page = YourPresetsPage(go_create=lambda: self.go(0))
        self.settings_page = SettingsPage(on_change=self.apply_theme)
        self.pages = [self.create_page, self.presets_page, self.settings_page]
        for page in self.pages:
            self.stack.addWidget(page)

        # nav buttons
        self.nav_buttons = []
        self.nav_icons = ["plus", "list", "settings"]
        group = QButtonGroup(self)
        group.setExclusive(True)
        for number, text in enumerate([" Create Preset", " Your Presets", " Settings"]):
            button = QPushButton(text)
            button.setObjectName("nav")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda checked=False, i=number: self.go(i))
            group.addButton(button)
            side_layout.addWidget(button)
            self.nav_buttons.append(button)
        side_layout.addStretch()

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.stack, 1)

        self.apply_theme()
        self.go(0)

    def go(self, number):
        self.stack.setCurrentIndex(number)
        self.nav_buttons[number].setChecked(True)
        self.update_nav_icons()

    def update_nav_icons(self):
        for number, button in enumerate(self.nav_buttons):
            colorkey = "onaccent" if button.isChecked() else "text"
            apply_icon(button, self.nav_icons[number], colorkey, 20)

    def apply_theme(self):
        QApplication.instance().setStyleSheet(styles.build_stylesheet())
        apply_icon(self.logo_icon, "layers", "accent", 36)
        self.setWindowIcon(get_icon("layers", styles.palette()["accent"], 64))
        for page in self.pages:
            page.refresh()
        self.update_nav_icons()


def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    load_fonts()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()