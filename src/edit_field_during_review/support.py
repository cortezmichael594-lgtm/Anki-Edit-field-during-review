# Copyright (C) 2026 AnkiCraft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import os

from aqt import mw
from aqt.qt import (
    QDesktopServices,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPixmap,
    QPushButton,
    QSizePolicy,
    Qt,
    QTimer,
    QUrl,
    QVBoxLayout,
    QWidget,
)

from . import constants
from . import settings
from .strings import tr

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _btn_style(bg: str, hover: str) -> str:
    return (
        f"QPushButton {{"
        f"  background-color: {bg};"
        f"  color: white;"
        f"  border: none;"
        f"  border-radius: 6px;"
        f"  padding: 6px 14px;"
        f"  font-weight: 600;"
        f"}}"
        f"QPushButton:hover {{"
        f"  background-color: {hover};"
        f"}}"
        f"QPushButton:pressed {{"
        f"  background-color: {hover};"
        f"}}"
    )


def _open(url: str) -> None:
    QDesktopServices.openUrl(QUrl(url))


# ---------------------------------------------------------------------------
# Welcome dialog
# ---------------------------------------------------------------------------

class WelcomeDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(constants.ADDON_DISPLAY_NAME)
        self.setMinimumWidth(440)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        root = QVBoxLayout(self)
        root.setSpacing(12)
        root.setContentsMargins(24, 24, 24, 20)

        # Logo
        logo_path = os.path.join(
            os.path.dirname(__file__), constants.LOGO_FILENAME
        )
        if os.path.isfile(logo_path):
            logo_lbl = QLabel()
            logo_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            px = QPixmap(logo_path).scaled(
                constants.LOGO_SIZE_PX,
                constants.LOGO_SIZE_PX,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl.setPixmap(px)
            root.addWidget(logo_lbl)

        # Title
        title = QLabel(
            tr("welcome_title",
               name=constants.ADDON_DISPLAY_NAME,
               version=constants.ADDON_VERSION)
        )
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet(
            f"font-size: 15px; font-weight: 700; color: {constants.COLOR_ACCENT};"
        )
        root.addWidget(title)

        # Byline
        byline = QLabel(f"by {constants.AUTHOR_NAME}")
        byline.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        byline.setStyleSheet("font-size: 11px; color: gray;")
        root.addWidget(byline)

        # Body
        body = QLabel(
            tr("welcome_body",
               name=constants.ADDON_NAME,
               version=constants.ADDON_VERSION)
        )
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(body)

        # AGPL note
        note = QLabel(tr("welcome_support_note"))
        note.setWordWrap(True)
        note.setStyleSheet("font-size: 11px; color: gray;")
        root.addWidget(note)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        root.addWidget(line)

        # Support buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        kofi = QPushButton(tr("kofi_button"))
        kofi.setStyleSheet(_btn_style(constants.COLOR_KOFI_BG, constants.COLOR_KOFI_HOVER))
        kofi.setToolTip(tr("kofi_tooltip"))
        kofi.clicked.connect(lambda: _open(constants.URL_KOFI))
        btn_row.addWidget(kofi)

        patreon = QPushButton(tr("patreon_button"))
        patreon.setStyleSheet(_btn_style(constants.COLOR_PATREON_BG, constants.COLOR_PATREON_HOVER))
        patreon.clicked.connect(lambda: _open(constants.URL_PATREON))
        btn_row.addWidget(patreon)

        if constants.ANKIWEB_ID:
            rate = QPushButton(tr("rate_button"))
            rate.setStyleSheet(_btn_style(constants.COLOR_RATE_BG, constants.COLOR_RATE_HOVER))
            rate.clicked.connect(lambda: _open(constants.ANKIWEB_REVIEW_URL))
            btn_row.addWidget(rate)

        root.addLayout(btn_row)

        # Close button (default + focus)
        close_box = QDialogButtonBox()
        close_btn = close_box.addButton(
            tr("welcome_close"), QDialogButtonBox.ButtonRole.AcceptRole
        )
        close_btn.setDefault(True)
        close_box.accepted.connect(self.accept)
        root.addWidget(close_box)

        self.setLayout(root)


def maybe_show_welcome() -> None:
    if settings.is_welcome_shown():
        return
    # Mark BEFORE showing to prevent duplicates if Anki crashes mid-display.
    try:
        settings.mark_welcome_shown()
    except Exception as exc:
        print(f"{constants.LOG_PREFIX} [mark_welcome_shown]: {exc!r}")

    def _show() -> None:
        try:
            dlg = WelcomeDialog(mw)
            dlg.exec()
        except Exception as exc:
            print(f"{constants.LOG_PREFIX} [welcome_dialog]: {exc!r}")

    QTimer.singleShot(constants.WELCOME_DELAY_MS, _show)


# ---------------------------------------------------------------------------
# Sober support footer for any future config dialog
# ---------------------------------------------------------------------------

def build_support_row(parent: QWidget) -> QWidget:
    """Returns a compact widget suitable for the bottom of a config dialog."""
    container = QWidget(parent)
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)

    version_text = tr("version_line",
                      name=constants.ADDON_NAME,
                      version=constants.ADDON_VERSION)
    if constants.ANKIWEB_ID:
        left_lbl = QLabel(
            f'<a href="{constants.URL_REPORT_BUG}" style="text-decoration:none;">'
            f'{version_text} · {tr("report_button")}'
            f"</a>"
        )
    else:
        left_lbl = QLabel(version_text)
    left_lbl.setStyleSheet("font-size: 11px; color: gray;")
    left_lbl.setOpenExternalLinks(True)
    layout.addWidget(left_lbl)
    layout.addStretch()

    for label, url in [
        (tr("kofi_button"), constants.URL_KOFI),
        (tr("patreon_button"), constants.URL_PATREON),
    ]:
        btn = QPushButton(label)
        btn.setFlat(True)
        btn.clicked.connect(lambda _checked=False, u=url: _open(u))
        layout.addWidget(btn)

    if constants.ANKIWEB_ID:
        rate_btn = QPushButton(tr("rate_button"))
        rate_btn.setFlat(True)
        rate_btn.clicked.connect(lambda: _open(constants.ANKIWEB_REVIEW_URL))
        layout.addWidget(rate_btn)

    return container
