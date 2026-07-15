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

from anki.hooks import field_filter
from aqt import gui_hooks, mw

from . import constants
from .review import (
    on_card_will_show,
    on_field_filter,
    on_js_message,
    on_webview_will_set_content,
)
from .support import maybe_show_welcome


def _register() -> None:
    mw.addonManager.setWebExports(__name__, constants.WEB_EXPORTS)
    field_filter.append(on_field_filter)
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
    gui_hooks.card_will_show.append(on_card_will_show)
    gui_hooks.webview_did_receive_js_message.append(on_js_message)
    gui_hooks.main_window_did_init.append(maybe_show_welcome)


_register()
