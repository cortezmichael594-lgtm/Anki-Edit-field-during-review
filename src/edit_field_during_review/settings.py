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

from aqt import mw

from . import constants


def _read_meta() -> dict[str, object]:
    config = mw.addonManager.getConfig(constants.PACKAGE) or {}
    meta = config.get(constants.CONFIG_KEY_META)
    return meta if isinstance(meta, dict) else {}


def is_welcome_shown() -> bool:
    return bool(_read_meta().get(constants.META_KEY_WELCOME_SHOWN, False))


def mark_welcome_shown() -> None:
    # Start from the config Anki already has so unrelated keys are never lost.
    config = mw.addonManager.getConfig(constants.PACKAGE) or {}
    meta = config.get(constants.CONFIG_KEY_META)
    if not isinstance(meta, dict):
        meta = {}
    meta[constants.META_KEY_WELCOME_SHOWN] = True
    config[constants.CONFIG_KEY_META] = meta
    mw.addonManager.writeConfig(constants.PACKAGE, config)
