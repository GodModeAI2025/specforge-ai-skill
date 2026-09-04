# -*- coding: utf-8 -*-
"""F-Stufen, ihre Gate-Wirkung und der Legacy-Uebersetzer.

Die Tabelle stammt aus references/enforcement/enforcement-engine.md,
Abschnitt I.2. Sie ist hier einmal abgebildet und sonst nirgends, damit ein
geaenderter Wert genau eine Stelle im Code hat.
"""

LEVELS = ("F0", "F1", "F2", "F3", "F4", "F5")

# F-Stufe -> (Gate-Ergebnis, Symbol, Bezeichnung)
GATE = {
    "F4": ("FAIL", "❌", "Schwergewichtiger Mangel"),
    "F3": ("CONDITIONAL", "⚠️", "Gewichtiger Mangel"),
    "F2": ("WARNING", "⚠️", "Mittelschwerer Mangel"),
    "F1": ("INFO", "ℹ️", "Geringfuegiger Mangel"),
    "F0": ("PASS", "✅", "Kein Mangel"),
    "F5": ("SKIP", "⏭️", "Nicht anwendbar"),
}

# Reihenfolge der Ausgabe: schwerster Befund zuerst.
ORDER = ("F4", "F3", "F2", "F1", "F0", "F5")

# Der Eingangs-Uebersetzer fuer alte specforge.json-Dateien ohne
# severity_model. Er gilt beim Einlesen und sonst nirgends; die Regeln des
# Checkers vergeben ausschliesslich F-Stufen.
LEGACY = {
    "BLOCKER": "F4",
    "MAJOR": "F3",
    "MINOR": "F1",
}


def normalise(value):
    """Macht aus einer Konfigurationsangabe eine F-Stufe.

    Akzeptiert 'F4', 'F 4', True/False (Boolean-Logik der Altprojekte) und
    die drei Legacy-Werte. Gibt None zurueck, wenn nichts davon passt.
    """
    if value is True:
        return "F4"
    if value is False:
        return "F1"
    if not isinstance(value, str):
        return None
    text = value.strip().upper().replace(" ", "")
    if text in LEVELS:
        return text
    return LEGACY.get(text)


def rank(level):
    """Sortierschluessel: kleiner heisst schwerer."""
    return ORDER.index(level) if level in ORDER else len(ORDER)


def worst(levels):
    """Schwerste Stufe einer Menge von Befunden."""
    relevant = [level for level in levels if level in ("F4", "F3", "F2", "F1")]
    if not relevant:
        return "F0"
    return sorted(relevant, key=rank)[0]
