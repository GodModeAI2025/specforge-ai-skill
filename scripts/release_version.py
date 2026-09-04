#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liest die Versionsquelle des Repos aus CHANGELOG.md.

Die Version stand an mehreren Stellen: README, Landingpage, Changelog. Wer
eine davon vergisst, merkt es nicht, und beim ersten Release faellt es
gleichzeitig an drei Stellen auf. Deshalb gibt es genau eine gepflegte
Stelle, den Abschnitt "Aktuelles Release" in CHANGELOG.md, und alles andere
liest sie oder wird von der CI dagegen geprueft.

Gelesen wird die erste Datenzeile der Tabelle in diesem Abschnitt:

    | Tag      | Skill-Version | Artefakt              |
    |----------|---------------|-----------------------|
    | `v3.2.0` | 3.2           | `specforge-skill.zip` |

Neuestes Release steht oben. Der Tag traegt eine Stelle mehr als die
Skill-Version, die Patch-Stelle zaehlt Korrekturen ohne Funktionsaenderung.

Dieses Modul wird von package-skill.py, check-package.py und
check-version.py importiert, damit die Zeile nur an einer Stelle geparst
wird. Direkt aufgerufen gibt es die Werte auf der Standardausgabe aus.

Nur Standardbibliothek.
"""

import os
import re
import sys

HEADING = "## Aktuelles Release"
COLUMNS = ("Tag", "Skill-Version", "Artefakt")

TAG_RE = re.compile(r"^v(\d+\.\d+)\.(\d+)$")
SKILL_RE = re.compile(r"^\d+\.\d+$")
ARTIFACT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.zip$")
SEPARATOR_RE = re.compile(r"^[:\- ]+$")


class VersionsquelleFehler(Exception):
    """Der Abschnitt fehlt, ist leer oder haelt sich nicht an das Format."""


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def changelog_path(root=None):
    return os.path.join(root or repo_root(), "CHANGELOG.md")


def _cells(line):
    """Tabellenzeile in Zellen zerlegen, Backticks und Leerraum weg."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    parts = stripped.strip("|").split("|")
    return [part.strip().strip("`").strip() for part in parts]


def _section_rows(text):
    """Gibt (ueberschrift_gefunden, tabellenzeilen) zurueck.

    Gelesen wird nur der Abschnitt unter HEADING, bis zur naechsten
    Ueberschrift derselben Ebene.
    """
    rows = []
    found = False
    inside = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            if inside:
                break
            inside = stripped == HEADING
            found = found or inside
            continue
        if not inside:
            continue
        cells = _cells(line)
        if cells:
            rows.append(cells)
    return found, rows


def read_release(root=None):
    """Gibt {tag, version, skill_version, artifact} aus CHANGELOG.md zurueck."""
    path = changelog_path(root)
    if not os.path.isfile(path):
        raise VersionsquelleFehler("CHANGELOG.md fehlt: %s" % path)
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    seen, rows = _section_rows(text)
    if not seen:
        raise VersionsquelleFehler(
            "CHANGELOG.md hat keinen Abschnitt '%s'" % HEADING)

    data = [row for row in rows
            if not all(SEPARATOR_RE.match(cell or "-") for cell in row)]
    if not data:
        raise VersionsquelleFehler(
            "Abschnitt '%s' enthaelt keine Tabellenzeile" % HEADING)

    header = data[0]
    if tuple(header[:3]) != COLUMNS:
        raise VersionsquelleFehler(
            "Kopfzeile der Release-Tabelle lautet %s, erwartet %s"
            % (tuple(header[:3]), COLUMNS))
    if len(data) < 2:
        raise VersionsquelleFehler(
            "Abschnitt '%s' hat eine Kopfzeile, aber keine Datenzeile"
            % HEADING)

    row = data[1]
    if len(row) < 3:
        raise VersionsquelleFehler(
            "Erste Datenzeile hat %d Spalten, erwartet 3" % len(row))
    tag, skill_version, artifact = row[0], row[1], row[2]

    match = TAG_RE.match(tag)
    if not match:
        raise VersionsquelleFehler(
            "Tag '%s' entspricht nicht dem Muster v{MAJOR}.{MINOR}.{PATCH}"
            % tag)
    if not SKILL_RE.match(skill_version):
        raise VersionsquelleFehler(
            "Skill-Version '%s' entspricht nicht dem Muster MAJOR.MINOR"
            % skill_version)
    if match.group(1) != skill_version:
        raise VersionsquelleFehler(
            "Tag '%s' und Skill-Version '%s' passen nicht zusammen"
            % (tag, skill_version))
    if not ARTIFACT_RE.match(artifact):
        raise VersionsquelleFehler(
            "Artefaktname '%s' ist kein einfacher Dateiname mit Endung .zip"
            % artifact)

    return {
        "tag": tag,
        "version": tag[1:],
        "skill_version": skill_version,
        "artifact": artifact,
    }


def main():
    try:
        release = read_release()
    except VersionsquelleFehler as error:
        print("FEHLER: %s" % error)
        return 1
    print("Tag:                     %s" % release["tag"])
    print("Version:                 %s" % release["version"])
    print("Skill-Version:           %s" % release["skill_version"])
    print("Artefakt:                %s" % release["artifact"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
