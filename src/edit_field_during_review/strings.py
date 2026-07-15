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

DEFAULT_LANGUAGE: str = "es"

STRINGS: dict[str, dict[str, str]] = {
    "es": {
        # --- Review errors ---
        "save_failed": "No se pudo guardar el cambio: {error}",
        "field_missing": "El campo «{field}» ya no existe en esta nota. El cambio no se ha guardado.",
        "note_missing": "La nota ya no existe. El cambio no se ha guardado.",
        "bad_message": "El editor envió una orden que no se entiende. El cambio no se ha guardado.",
        "render_failed": "El cambio se ha guardado, pero no se pudo redibujar la tarjeta.",
        # --- Branding / welcome ---
        "version_line": "{name} v{version}",
        "welcome_title": "{name} v{version}",
        "kofi_button": "☕ Ko-fi",
        "kofi_tooltip": "Invítame a un café en Ko-fi",
        "patreon_button": "♥ Patreon",
        "rate_button": "👍 Valorar",
        "report_button": "Reportar un problema",
        "welcome_close": "Cerrar",
        "welcome_body": (
            "<b>{name}</b> te permite editar cualquier campo de una nota "
            "directamente durante el repaso, sin salir de la pantalla.\n\n"
            "Haz clic sobre el texto que quieras cambiar: aparece un cuadro azul. "
            "Escribe, borra o corrige. Al salir del cuadro (o al pulsar Enter), "
            "el cambio se guarda automáticamente y puedes deshacerlo con Ctrl+Z."
        ),
        "welcome_support_note": (
            "Este complemento es gratuito y de código abierto (AGPLv3). "
            "Si te resulta útil, considera apoyar su desarrollo."
        ),
    },
    "en": {
        # --- Review errors ---
        "save_failed": "Could not save the change: {error}",
        "field_missing": "Field '{field}' no longer exists in this note. The change was not saved.",
        "note_missing": "The note no longer exists. The change was not saved.",
        "bad_message": "The editor sent an unrecognised command. The change was not saved.",
        "render_failed": "The change was saved, but the card could not be redrawn.",
        # --- Branding / welcome ---
        "version_line": "{name} v{version}",
        "welcome_title": "{name} v{version}",
        "kofi_button": "☕ Buy me a coffee",
        "kofi_tooltip": "Support development on Ko-fi",
        "patreon_button": "♥ Patreon",
        "rate_button": "👍 Rate this add-on",
        "report_button": "Report a bug",
        "welcome_close": "Close",
        "welcome_body": (
            "<b>{name}</b> lets you edit any field of a note directly "
            "during review — no extra screens, no interruptions.\n\n"
            "Click on any text: a blue outline appears. Type, delete, or fix it. "
            "When you click away (or press Enter), the change is saved "
            "automatically and you can undo it with Ctrl+Z."
        ),
        "welcome_support_note": (
            "This add-on is free and open source (AGPLv3). "
            "If it saves you time, consider supporting its development."
        ),
    },
}


def tr(key: str, **values: str) -> str:
    table = STRINGS.get(DEFAULT_LANGUAGE, {})
    text = table.get(key) or STRINGS.get("en", {}).get(key, key)
    if not values:
        return text
    try:
        return text.format(**values)
    except (KeyError, IndexError):
        return text
