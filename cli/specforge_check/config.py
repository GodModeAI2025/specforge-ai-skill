# -*- coding: utf-8 -*-
"""Liest specforge.json und loest F-Stufen je Pruefpunkt auf.

Die Aufloesung folgt enforcement-engine.md, Abschnitt "Perspektivenabhaengige
F-Stufen": Perspektive aus specforge.json lesen, im severity-Objekt
nachschlagen, bei Fehltreffer _default, ohne _default F3 als Fallback.

Fehlt severity_model, ist das Projekt eine Altkonfiguration. Dann greift der
Legacy-Uebersetzer aus severity.py — einmal beim Einlesen. Danach rechnet der
Checker ausschliesslich mit F-Stufen.
"""

import json
import os

from . import severity

FALLBACK = "F3"


class Config(object):
    def __init__(self, data=None, path=None):
        self.data = data or {}
        self.path = path

    @property
    def profile(self):
        value = self.data.get("profile")
        return value.lower() if isinstance(value, str) else None

    @property
    def perspective(self):
        value = self.data.get("perspective")
        return value if isinstance(value, str) else None

    @property
    def legacy(self):
        """True, wenn die Datei noch kein severity_model fuehrt."""
        return bool(self.data) and "severity_model" not in self.data

    def _entry(self, check):
        for gate in self.data.get("checks_config", {}).values():
            if isinstance(gate, dict) and check in gate:
                return gate[check]
        return None

    def severity_for(self, check, default):
        """F-Stufe eines Pruefpunkts: Konfiguration schlaegt Default."""
        entry = self._entry(check)
        if not isinstance(entry, dict):
            return default

        if "severity" in entry:
            value = entry["severity"]
            if isinstance(value, dict):
                if self.perspective and self.perspective in value:
                    resolved = severity.normalise(value[self.perspective])
                    if resolved:
                        return resolved
                if "_default" in value:
                    resolved = severity.normalise(value["_default"])
                    if resolved:
                        return resolved
                return FALLBACK
            resolved = severity.normalise(value)
            if resolved:
                return resolved

        # Altkonfiguration ohne severity: Boolean-Logik uebersetzen.
        if "required" in entry:
            if entry["required"]:
                return "F4"
            if entry.get("skip_reason_required"):
                return "F3"
            return "F1"
        return default


def load(path):
    """Laedt eine specforge.json. Fehlt sie, gilt die leere Konfiguration."""
    if not path or not os.path.isfile(path):
        return Config()
    with open(path, encoding="utf-8") as handle:
        return Config(json.load(handle), path)


def find(start):
    """Sucht specforge.json neben der Spec und in den Elternverzeichnissen."""
    directory = os.path.abspath(start if os.path.isdir(start)
                                else os.path.dirname(start))
    while True:
        candidate = os.path.join(directory, "specforge.json")
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent
