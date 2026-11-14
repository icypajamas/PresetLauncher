import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QFileDialog, QFrame, QHBoxLayout,
                               QInputDialog, QLabel, QLineEdit, QPushButton,
                               QScrollArea, QSizePolicy, QStackedWidget,
                               QVBoxLayout, QWidget)
from shiboken6 import isValid

from UI.styles import Page

# icons and names for each item type
type_icons = {"app": "laptop", "folder": "folder", "file": "file", "url": "link"}
type_names = {"app": "App", "folder": "Folder", "file": "File", "url": "Website"}

# plain scroll area with a thin scrollbar
scroll_style = """
QScrollArea { background: transparent; border: none; }
#itemlist { background: transparent; }
QScrollBar:vertical { background: transparent; width: 10px; margin: 6px 2px; }
QScrollBar::handle:vertical { background: rgba(128, 128, 128, 90); border-radius: 3px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
"""


def shorten(text, limit):
    if len(text) <= limit:
        return text
    return text[:limit - 3] + "..."


def item_title(kind, value):
    if kind == "url":
        return value.split("://", 1)[-1]
    if kind == "app":
        return os.path.splitext(os.path.basename(value))[0] or value
    return os.path.basename(value) or value


def item_detail(kind, value):
    if kind == "url":
        return type_names[kind]
    return value


class CreatePresetPage(Page):
    # sends the finished preset as a dictionary when Save is pressed
    saved = Signal(dict)

    def __init__(self):
        super().__init__()
        self.items = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(0)

        # heading
        title = QLabel("Create Preset")
        title.setObjectName("title")
        subtitle = QLabel("Build a custom preset by adding your apps, folders, files and URLs.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addSpacing(4)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        # preset name
        name_label = QLabel("Preset Name")
        name_label.setObjectName("sectionlabel")
        self.name_box = QLineEdit()
        self.name_box.setPlaceholderText("Enter preset name")
        layout.addWidget(name_label)
        layout.addSpacing(8)
        layout.addWidget(self.name_box)
        layout.addSpacing(22)

        # add items buttons
        add_label = QLabel("Add Items")
        add_label.setObjectName("sectionlabel")
        layout.addWidget(add_label)
        layout.addSpacing(8)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)
        buttons = [
            (" Add App", "laptop", self.add_app),
            (" Add Folder", "folder", self.add_folder),
            (" Add File", "file", self.add_file),
            (" Add URL", "link", self.add_url),
        ]
        for text, icon, action in buttons:
            button = QPushButton(text)
            button.setObjectName("outline")
            button.setMinimumHeight(46)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.clicked.connect(action)
            self.put_icon(button, icon, "text", 20)
            button_row.addWidget(button)
        layout.addLayout(button_row)
        layout.addSpacing(22)

        # preset items box
        items_label = QLabel("Preset Items")
        items_label.setObjectName("sectionlabel")
        layout.addWidget(items_label)
        layout.addSpacing(8)

        items_box = QFrame()
        items_box.setObjectName("card")
        box_layout = QVBoxLayout(items_box)
        box_layout.setContentsMargins(4, 4, 4, 4)

        self.views = QStackedWidget()
        self.views.addWidget(self.build_empty())
        self.views.addWidget(self.build_list())
        box_layout.addWidget(self.views)
        layout.addWidget(items_box, 1)
        layout.addSpacing(16)

        # bottom buttons
        bottom = QHBoxLayout()
        bottom.addStretch()
        cancel = QPushButton("Cancel")
        cancel.setObjectName("outline")
        cancel.setMinimumSize(120, 42)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.clear_form)
        save = QPushButton("Save Preset")
        save.setObjectName("primary")
        save.setMinimumSize(150, 42)
        save.setCursor(Qt.CursorShape.PointingHandCursor)
        save.clicked.connect(self.save_preset)
        bottom.addWidget(cancel)
        bottom.addWidget(save)
        layout.addLayout(bottom)

    # empty view
    def build_empty(self):
        empty = QWidget()
        empty_layout = QVBoxLayout(empty)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.setSpacing(10)

        empty_icon = QLabel()
        empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.put_icon(empty_icon, "list", "muted", 34)
        empty_text = QLabel("No items added yet.")
        empty_text.setObjectName("muted")
        empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(empty_text)
        return empty

    # list view
    def build_list(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(scroll_style)
        scroll.viewport().setAutoFillBackground(False)

        holder = QWidget()
        holder.setObjectName("itemlist")
        self.list_layout = QVBoxLayout(holder)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(0)
        scroll.setWidget(holder)
        return scroll

    # add items
    def add_app(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose an app", "", "Apps (*.exe *.lnk *.bat);;All files (*)")
        if path:
            self.add_item("app", path)

    def add_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Choose a folder")
        if path:
            self.add_item("folder", path)

    def add_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose a file")
        if path:
            self.add_item("file", path)

    def add_url(self):
        text, ok = QInputDialog.getText(self, "Add URL", "Enter the website address:")
        text = text.strip()
        if ok and text:
            if not text.startswith(("http://", "https://")):
                text = "https://" + text
            self.add_item("url", text)

    def add_item(self, kind, value):
        if kind != "url":
            value = os.path.normpath(value)
        entry = {"type": kind, "value": value}
        if entry in self.items:
            return
        self.items.append(entry)
        self.render_items()

    def remove_item(self, number):
        del self.items[number]
        self.render_items()

    # draw the list again
    def render_items(self):
        self.icon_list = [i for i in self.icon_list if isValid(i[0])]
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for number, data in enumerate(self.items):
            self.list_layout.addWidget(self.build_row(number, data))
            if number < len(self.items) - 1:
                line = QFrame()
                line.setObjectName("sep")
                line.setFixedHeight(1)
                self.list_layout.addWidget(line)
        self.list_layout.addStretch()
        self.views.setCurrentIndex(1 if self.items else 0)

    # one item row
    def build_row(self, number, data):
        kind = data["type"]
        value = data["value"]

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(16, 10, 10, 10)
        row_layout.setSpacing(14)

        icon = QLabel()
        self.put_icon(icon, type_icons[kind], "accent", 24)

        text_box = QVBoxLayout()
        text_box.setSpacing(0)
        title = QLabel(shorten(item_title(kind, value), 50))
        title.setObjectName("sectionlabel")
        detail = QLabel(shorten(item_detail(kind, value), 70))
        detail.setObjectName("muted")
        text_box.addWidget(title)
        text_box.addWidget(detail)

        remove = QPushButton()
        remove.setObjectName("flat")
        remove.setFixedSize(34, 34)
        remove.setToolTip("Remove")
        remove.setCursor(Qt.CursorShape.PointingHandCursor)
        remove.clicked.connect(lambda checked=False, n=number: self.remove_item(n))
        self.put_icon(remove, "trash", "muted", 18)

        row_layout.addWidget(icon)
        row_layout.addLayout(text_box, 1)
        row_layout.addWidget(remove)
        return row

    # form actions
    def get_preset(self):
        return {
            "name": self.name_box.text().strip(),
            "items": [dict(i) for i in self.items],
        }

    def clear_form(self):
        self.name_box.clear()
        self.items = []
        self.render_items()

    def save_preset(self):
        if not self.name_box.text().strip():
            self.name_box.setFocus()
            return
        if not self.items:
            return
        self.saved.emit(self.get_preset())