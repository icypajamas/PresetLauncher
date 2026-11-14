from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QColor, QGuiApplication
from PySide6.QtWidgets import QLabel, QWidget
from shiboken6 import isValid

from UI.icons import get_icon, get_pixmap

# theme colours
light_theme = {
    "bg": "#f6f8fa",
    "sidebar": "#fbfcfd",
    "card": "#ffffff",
    "border": "#e2e6ea",
    "text": "#111418",
    "muted": "#5f6b76",
    "input": "#ffffff",
    "hover": "#eef1f4",
}

dark_theme = {
    "bg": "#14171a",
    "sidebar": "#1a1e22",
    "card": "#1e2328",
    "border": "#2f363d",
    "text": "#f2f4f6",
    "muted": "#9ba6b1",
    "input": "#1e2328",
    "hover": "#272d33",
}

# accent colours, deep enough for white text on top of them
light_accents = {
    "green": "#1a7a3a",
    "brown": "#8b5e47",
    "orange": "#bd5309",
    "pink": "#c2487f",
    "navy": "#294c7a",
    "purple": "#7f4fb8",
}

# dark mode shades are a little lighter so they stand out on dark
dark_accents = {
    "green": "#1c8444",
    "brown": "#9c6a4f",
    "orange": "#bf590c",
    "pink": "#c4447f",
    "navy": "#3b6fb8",
    "purple": "#8c58cf",
}

# current choices (theme can be light, dark or system)
state = {"theme": "light", "accent": "green"}


def is_dark():
    if state["theme"] == "dark":
        return True
    if state["theme"] == "light":
        return False
    try:
        return QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark
    except Exception:
        return False


def accent_list():
    accents = dark_accents if is_dark() else light_accents
    return list(accents.items())


def palette():
    colors = dict(dark_theme if is_dark() else light_theme)
    accents = dict(accent_list())
    accent = accents[state["accent"]]
    colors["accent"] = accent
    colors["accent_hover"] = QColor(accent).darker(112).name()
    # text on top of the accent colour is always white
    colors["onaccent"] = "#ffffff"
    return colors


def apply_icon(widget, name, colorkey, size):
    color = palette()[colorkey]
    if isinstance(widget, QLabel):
        widget.setPixmap(get_pixmap(name, color, size))
    elif isinstance(widget, QAction):
        widget.setIcon(get_icon(name, color, size))
    else:
        widget.setIcon(get_icon(name, color, size))
        widget.setIconSize(QSize(size, size))


# base page that remembers its icons so they can change colour
class Page(QWidget):
    def __init__(self):
        super().__init__()
        self.icon_list = []

    def put_icon(self, widget, name, colorkey="accent", size=20):
        self.icon_list.append((widget, name, colorkey, size))
        apply_icon(widget, name, colorkey, size)

    def refresh(self):
        for widget, name, colorkey, size in self.icon_list:
            if isValid(widget):
                apply_icon(widget, name, colorkey, size)
        self.update()


def build_stylesheet():
    p = palette()
    return f"""
    QWidget {{
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 14px;
        color: {p['text']};
    }}
    QMainWindow, #content {{ background: {p['bg']}; }}
    QLabel {{ background: transparent; }}

    #sidebar {{
        background: {p['sidebar']};
        border-right: 1px solid {p['border']};
    }}
    #logo {{ font-size: 24px; font-weight: 700; }}

    #title {{ font-size: 28px; font-weight: 700; }}
    #subtitle {{ color: {p['muted']}; font-size: 14px; }}
    #muted {{ color: {p['muted']}; }}
    #sectionlabel {{ font-size: 15px; font-weight: 700; }}
    #cardtitle {{ font-size: 19px; font-weight: 700; }}
    #rowtitle {{ font-size: 16px; font-weight: 700; }}
    #statnum {{ font-size: 20px; font-weight: 700; }}
    #bignum {{ font-size: 30px; font-weight: 700; }}
    #emptytitle {{ font-size: 22px; font-weight: 700; }}

    QFrame#card {{
        background: {p['card']};
        border: 1px solid {p['border']};
        border-radius: 12px;
    }}
    QFrame#sep {{ background: {p['border']}; border: none; }}

    QPushButton {{ border: none; }}

    QPushButton#nav {{
        background: transparent;
        border-radius: 8px;
        padding: 11px 14px;
        text-align: left;
        font-size: 14px;
    }}
    QPushButton#nav:hover {{ background: {p['hover']}; }}
    QPushButton#nav:checked {{
        background: {p['accent']};
        color: {p['onaccent']};
        font-weight: 700;
    }}

    QPushButton#primary {{
        background: {p['accent']};
        color: {p['onaccent']};
        border-radius: 8px;
        padding: 9px 18px;
        font-weight: 700;
    }}
    QPushButton#primary:hover {{ background: {p['accent_hover']}; }}

    QPushButton#outline, QPushButton#seg {{
        background: {p['card']};
        border: 1px solid {p['border']};
        border-radius: 8px;
        padding: 9px 14px;
    }}
    QPushButton#outline:hover, QPushButton#seg:hover {{ background: {p['hover']}; }}
    QPushButton#seg:checked {{
        background: {p['accent']};
        color: {p['onaccent']};
        border: 1px solid {p['accent']};
    }}

    QPushButton#flat {{
        background: transparent;
        border-radius: 6px;
    }}
    QPushButton#flat:hover {{ background: {p['hover']}; }}

    QLineEdit {{
        background: {p['input']};
        border: 1px solid {p['border']};
        border-radius: 8px;
        padding: 10px 12px;
        placeholder-text-color: {p['muted']};
    }}
    QLineEdit:focus {{ border: 1px solid {p['accent']}; }}
    QLineEdit#search {{ border-radius: 18px; padding: 8px 14px; }}

    QPushButton#combo {{
        background: {p['input']};
        border: 1px solid {p['border']};
        border-radius: 8px;
        padding: 9px 36px 9px 12px;
        text-align: left;
    }}
    QPushButton#combo:hover {{ border: 1px solid {p['accent']}; }}
    QPushButton#combo[open="true"] {{ border: 1px solid {p['accent']}; }}

    QMenu {{
        background: {p['card']};
        border: 1px solid {p['border']};
        border-radius: 10px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 9px 16px;
        margin: 1px 0px;
        border-radius: 6px;
        color: {p['text']};
        background: transparent;
    }}
    QMenu::item:selected {{
        background: {p['accent']};
        color: {p['onaccent']};
    }}
    """