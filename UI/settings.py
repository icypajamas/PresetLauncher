from PySide6.QtCore import QPoint, QPointF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (QButtonGroup, QCheckBox, QFrame, QGridLayout,
                               QHBoxLayout, QLabel, QMenu, QPushButton,
                               QVBoxLayout, QWidget)

from UI import styles
from UI.icons import get_pixmap
from UI.styles import Page, apply_icon


# toggle switch
class Toggle(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setFixedSize(46, 26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def hitButton(self, pos):
        return self.rect().contains(pos)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        colors = styles.palette()
        track = QColor(colors["accent"]) if self.isChecked() else QColor(colors["border"])
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(track)
        p.drawRoundedRect(0, 0, 46, 26, 13, 13)
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(23 if self.isChecked() else 3, 3, 20, 20)


# dropdown button with our own rounded list
class Combo(QPushButton):
    changed = Signal(str)

    def __init__(self, items):
        super().__init__()
        self.items = items
        self.value = items[0]
        self.setObjectName("combo")
        self.setText(self.value)
        self.setFixedSize(210, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.open_list)

    def current_text(self):
        return self.value

    def set_open(self, is_open):
        self.setProperty("open", is_open)
        self.style().unpolish(self)
        self.style().polish(self)

    def pick(self, text):
        self.value = text
        self.setText(text)
        self.changed.emit(text)

    def open_list(self):
        menu = QMenu(self)
        menu.setWindowFlags(
            menu.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        menu.setMinimumWidth(self.width())

        for text in self.items:
            action = menu.addAction(text)
            if text == self.value:
                font = action.font()
                font.setBold(True)
                action.setFont(font)
            action.triggered.connect(lambda checked=False, t=text: self.pick(t))

        self.set_open(True)
        menu.exec(self.mapToGlobal(QPoint(0, self.height() + 4)))
        self.set_open(False)

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        pixmap = get_pixmap("chevron", styles.palette()["text"], 14)
        p.drawPixmap(self.width() - 28, (self.height() - 14) // 2, pixmap)


# accent colour circle, with one thin ring when selected
class Swatch(QPushButton):
    def __init__(self, key, on_pick):
        super().__init__()
        self.key = key
        self.setFixedSize(40, 40)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda: on_pick(key))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(dict(styles.accent_list())[self.key])
        center = QPointF(20, 20)

        # the colour circle
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color)
        p.drawEllipse(center, 13, 13)

        # ring around the selected colour
        if styles.state["accent"] == self.key:
            p.setPen(QPen(color, 2))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(center, 18, 18)


class SettingsPage(Page):
    def __init__(self, on_change):
        super().__init__()
        self.on_change = on_change
        self.swatches = []
        self.theme_buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(0)

        # heading
        title = QLabel("Settings")
        title.setObjectName("title")
        subtitle = QLabel("Customize Presetly to fit your workflow.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addSpacing(4)
        layout.addWidget(subtitle)
        layout.addSpacing(18)

        # application
        startup = Toggle()
        startup.setChecked(True)
        after = Combo(["Keep Presetly open", "Minimize to tray", "Close Presetly"])
        layout.addWidget(self.build_row(
            "laptop", "Application", "General application preferences.",
            [("Run on system startup", startup, Qt.AlignmentFlag.AlignRight),
             ("After launch", after, Qt.AlignmentFlag.AlignRight)]))
        layout.addSpacing(14)

        # appearance
        theme_box = QWidget()
        theme_layout = QHBoxLayout(theme_box)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_layout.setSpacing(6)
        group = QButtonGroup(self)
        group.setExclusive(True)
        for key, text, icon in [("light", " Light", "sun"),
                                ("dark", " Dark", "moon"),
                                ("system", " System", "monitor")]:
            button = QPushButton(text)
            button.setObjectName("seg")
            button.setCheckable(True)
            button.setMinimumHeight(38)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda checked=False, k=key: self.pick_theme(k))
            group.addButton(button)
            theme_layout.addWidget(button)
            self.theme_buttons[key] = (button, icon)

        accent_box = QWidget()
        accent_layout = QHBoxLayout(accent_box)
        accent_layout.setContentsMargins(0, 0, 0, 0)
        accent_layout.setSpacing(4)
        for key, color in styles.accent_list():
            swatch = Swatch(key, self.pick_accent)
            self.swatches.append(swatch)
            accent_layout.addWidget(swatch)

        layout.addWidget(self.build_row(
            "palette", "Appearance", "Change the look and feel of Presetly.",
            [("Theme", theme_box, Qt.AlignmentFlag.AlignRight),
             ("Accent Colour", accent_box, Qt.AlignmentFlag.AlignRight)]))
        layout.addSpacing(14)

        # presets
        launch_mode = Combo(["All at once", "One by one"])
        layout.addWidget(self.build_row(
            "layers", "Presets", "Default behavior for your presets.",
            [("Default launch mode", launch_mode, Qt.AlignmentFlag.AlignRight)]))
        layout.addSpacing(14)

        # updates
        update_button = QPushButton(" Check for Updates")
        update_button.setObjectName("outline")
        update_button.setMinimumHeight(38)
        update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.put_icon(update_button, "download", "text", 18)
        layout.addWidget(self.build_row(
            "download", "Updates", "Keep Presetly up to date.",
            [("Check for updates", update_button, Qt.AlignmentFlag.AlignRight)]))
        layout.addStretch()

        self.refresh()

    # one settings row
    def build_row(self, icon_name, title, description, controls):
        row = QFrame()
        row.setObjectName("card")
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(22, 16, 22, 16)
        row_layout.setSpacing(18)

        icon = QLabel()
        icon.setFixedWidth(40)
        self.put_icon(icon, icon_name, "accent", 32)

        text_box = QVBoxLayout()
        text_box.setSpacing(2)
        name = QLabel(title)
        name.setObjectName("rowtitle")
        info = QLabel(description)
        info.setObjectName("muted")
        text_box.addWidget(name)
        text_box.addWidget(info)

        grid = QGridLayout()
        grid.setVerticalSpacing(12)
        grid.setHorizontalSpacing(24)
        for number, (label_text, widget, align) in enumerate(controls):
            label = QLabel(label_text)
            grid.addWidget(label, number, 0, Qt.AlignmentFlag.AlignLeft)
            grid.addWidget(widget, number, 1, align)

        row_layout.addWidget(icon)
        row_layout.addLayout(text_box, 1)
        row_layout.addLayout(grid)
        return row

    def pick_theme(self, key):
        styles.state["theme"] = key
        self.on_change()

    def pick_accent(self, key):
        styles.state["accent"] = key
        self.on_change()

    def refresh(self):
        super().refresh()
        for key, (button, icon) in self.theme_buttons.items():
            checked = styles.state["theme"] == key
            button.setChecked(checked)
            apply_icon(button, icon, "onaccent" if checked else "text", 18)
        for swatch in self.swatches:
            swatch.update()
        for widget in self.findChildren(Toggle) + self.findChildren(Combo):
            widget.update()