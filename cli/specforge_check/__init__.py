# -*- coding: utf-8 -*-
"""specforge check — Linter fuer SpecForge-Artefakte.

Der Skill setzt seine Regeln bisher nur in der Claude-Session durch. Dieses
Paket prueft den strukturell entscheidbaren Teil davon ausserhalb: in einer
Pipeline, in einem Pre-Commit-Hook, auf der Kommandozeile.

Geprueft wird gegen dieselben F-Stufen, die enforcement-engine.md fuehrt.
Das Ausgabeformat ist das Gate-Ergebnis-Format aus demselben Dokument.
"""

VERSION = "3.2"

__all__ = ["VERSION"]
