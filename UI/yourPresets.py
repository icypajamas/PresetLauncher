from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QStackedWidget,
                               QVBoxLayout, QWidget)

from UI.styles import Page

# change to True to preview the filled layout
show_demo = False

demo_presets = [
    {"name": "Study Setup", "icon": "laptop", "apps": 4, "folders": 2, "files": 1, "urls": 1},
    {"name": "Development", "icon": "code", "apps": 5, "folders": 3, "files": 1, "urls": 2},
    {"name": "Gaming", "icon": "gamepad", "apps": 3, "folders": 1, "files": 1, "urls": 1},
    {"name": "Work", "icon": "briefcase", "apps": 4, "folders": 2, "files": 1, "urls": 2},
]


def count_text(number, word):
    if number == 1:
        return f"{number} {word}"
    return f"{number} {word}s"


class YourPresetsPage(Page):
    def __init__(self, go_create=None):
        super().__init__()
        self.go_create = go_create

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(0)

        # heading and search
        header = QHBoxLayout()
        heading = QVBoxLayout()
        heading.setSpacing(4)
        title = QLabel("Your Presets")
        title.setObjectName("title")
        subtitle = QLabel("Manage and launch your saved presets.")
        subtitle.setObjectName("subtitle")
        heading.addWidget(title)
        heading.addWidget(subtitle)

        self.search_box = QLineEdit()
        self.search_box.setObjectName("search")
        self.search_box.setPlaceholderText("Search presets...")
        self.search_box.setFixedSize(270, 40)
        search_action = self.search_box.addAction(
            self.search_box.style().standardIcon(self.search_box.style().StandardPixmap.SP_FileIcon),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        self.put_icon(search_action, "search", "text", 18)

        header.addLayout(heading, 1)
        header.addWidget(self.search_box, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(header)
        layout.addSpacing(20)

        # two views: empty and list
        self.views = QStackedWidget()
        self.views.addWidget(self.build_empty())
        self.list_view = QWidget()
        self.list_layout = QVBoxLayout(self.list_view)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(16)
        self.views.addWidget(self.list_view)
        layout.addWidget(self.views, 1)

        # start empty unless demo is on
        self.set_presets(demo_presets if show_demo else [])

    # empty view
    def build_empty(self):
        box = QFrame()
        box.setObjectName("card")
        box_layout = QVBoxLayout(box)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.setSpacing(10)

        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.put_icon(icon, "layers", "accent", 64)

        heading = QLabel("Your workspace, ready in one click")
        heading.setObjectName("emptytitle")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text = QLabel("Create your first preset to open your apps, folders and websites together.")
        text.setObjectName("muted")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton(" Create Preset")
        button.setObjectName("primary")
        button.setMinimumSize(170, 42)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.put_icon(button, "plus", "onaccent", 18)
        if self.go_create:
            button.clicked.connect(self.go_create)

        box_layout.addWidget(icon)
        box_layout.addWidget(heading)
        box_layout.addWidget(text)
        box_layout.addSpacing(10)
        box_layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        return box

    # call this later with real presets from the core code
    def set_presets(self, presets):
        # clear old widgets
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not presets:
            self.views.setCurrentIndex(0)
            return

        self.list_layout.addWidget(self.build_stats(presets))

        grid = QGridLayout()
        grid.setSpacing(16)
        for number, data in enumerate(presets):
            grid.addWidget(self.build_card(data), number // 2, number % 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        self.list_layout.addLayout(grid)
        self.list_layout.addStretch()
        self.views.setCurrentIndex(1)

    # stats bar
    def build_stats(self, presets):
        bar = QFrame()
        bar.setObjectName("card")
        row = QHBoxLayout(bar)
        row.setContentsMargins(24, 16, 24, 16)
        row.setSpacing(18)

        total_icon = QLabel()
        self.put_icon(total_icon, "layers", "accent", 46)
        total_box = QVBoxLayout()
        total_box.setSpacing(0)
        total_label = QLabel("Total Presets")
        total_label.setObjectName("rowtitle")
        total_number = QLabel(str(len(presets)))
        total_number.setObjectName("bignum")
        total_box.addWidget(total_label)
        total_box.addWidget(total_number)
        row.addWidget(total_icon)
        row.addLayout(total_box)
        row.addStretch()

        stats = [
            ("laptop", "apps", "Apps"),
            ("folder", "folders", "Folders"),
            ("file", "files", "Files"),
            ("link", "urls", "URLs"),
        ]
        for icon_name, key, label in stats:
            line = QFrame()
            line.setObjectName("sep")
            line.setFixedWidth(1)
            line.setMinimumHeight(48)
            row.addWidget(line)
            row.addStretch()

            icon = QLabel()
            self.put_icon(icon, icon_name, "accent", 32)
            box = QVBoxLayout()
            box.setSpacing(0)
            number = QLabel(str(sum(p[key] for p in presets)))
            number.setObjectName("statnum")
            name = QLabel(label)
            name.setObjectName("muted")
            box.addWidget(number)
            box.addWidget(name)
            row.addWidget(icon)
            row.addLayout(box)
            row.addStretch()
        return bar

    # one preset card
    def build_card(self, data):
        card = QFrame()
        card.setObjectName("card")
        outer = QVBoxLayout(card)
        outer.setContentsMargins(20, 18, 20, 18)
        outer.setSpacing(14)

        top = QHBoxLayout()
        top.setSpacing(14)

        icon = QLabel()
        self.put_icon(icon, data["icon"], "accent", 42)

        info = QVBoxLayout()
        info.setSpacing(6)
        name = QLabel(data["name"])
        name.setObjectName("cardtitle")
        info.addWidget(name)

        meta = QHBoxLayout()
        meta.setSpacing(6)
        items = [
            ("apps", count_text(data["apps"], "App")),
            ("folder", count_text(data["folders"], "Folder")),
            ("link", count_text(data["urls"], "URL")),
        ]
        for number, (icon_name, text) in enumerate(items):
            if number > 0:
                dot = QLabel("\u2022")
                dot.setObjectName("muted")
                meta.addWidget(dot)
            small = QLabel()
            self.put_icon(small, icon_name, "muted", 16)
            label = QLabel(text)
            label.setObjectName("muted")
            meta.addWidget(small)
            meta.addWidget(label)
        meta.addStretch()
        info.addLayout(meta)

        more = QPushButton()
        more.setObjectName("flat")
        more.setFixedSize(34, 30)
        more.setCursor(Qt.CursorShape.PointingHandCursor)
        self.put_icon(more, "more", "muted", 20)

        top.addWidget(icon)
        top.addLayout(info, 1)
        top.addWidget(more, 0, Qt.AlignmentFlag.AlignTop)
        outer.addLayout(top)

        # buttons
        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        launch = QPushButton(" Launch")
        launch.setObjectName("primary")
        launch.setMinimumHeight(40)
        launch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.put_icon(launch, "play", "onaccent", 18)

        edit = QPushButton(" Edit")
        edit.setObjectName("outline")
        edit.setMinimumHeight(40)
        edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.put_icon(edit, "pencil", "text", 18)

        delete = QPushButton()
        delete.setObjectName("outline")
        delete.setFixedSize(46, 40)
        delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.put_icon(delete, "trash", "text", 18)

        buttons.addWidget(launch, 3)
        buttons.addWidget(edit, 2)
        buttons.addWidget(delete)
        outer.addLayout(buttons)
        return card