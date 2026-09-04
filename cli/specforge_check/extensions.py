# -*- coding: utf-8 -*-
"""Liest die F-Stufen-Tabellen der Regulatorik-Extensions.

Jede Extension unter references/custom/@name/ fuehrt in ihrer manifest.md
einen Abschnitt "F-Stufen-Zuordnung": je Kategorie eine Zeile, je Perspektive
eine Spalte, dazu die Pflicht-Spalte _default. Genau das ist die Tabelle, die
in der Session entscheidet, welche F-Stufe eine fehlende Anforderung bekommt.

Der Checker liest sie, statt sie zu wiederholen. Eine Zelle kann mehrere
Stufen nennen ("F4 (TLPT) / F3", "F4 (PII) / F3") — die Bedingung dahinter
ist fachlich, nicht strukturell entscheidbar. Zulaessig sind dann beide
Stufen; falsch ist nur eine Stufe, die in der Zelle gar nicht vorkommt.
"""

import os
import re

TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
BOLD_CODE_RE = re.compile(r"\*\*([A-Z]{2,5})\*\*")
F_LEVEL_RE = re.compile(r"\bF\s?([0-5])\b")
HEADING_RE = re.compile(r"^#+\s*(.*)$")

SECTION = "F-Stufen-Zuordnung"
DEFAULT_COLUMN = "_default"


def split_row(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_manifest(path):
    """Gibt {kategorie: {spalte: {F-Stufen}}} zurueck."""
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")

    start = None
    for index, line in enumerate(lines):
        heading = HEADING_RE.match(line)
        if heading and SECTION in heading.group(1):
            start = index
            break
    if start is None:
        return {}

    header = None
    table = {}
    for line in lines[start:]:
        if HEADING_RE.match(line) and header is not None:
            break
        if not TABLE_ROW_RE.match(line):
            continue
        cells = split_row(line)
        if header is None:
            if cells and cells[0].lower() == "kategorie":
                header = [cell.strip("` ") for cell in cells[1:]]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        code = BOLD_CODE_RE.search(cells[0])
        name = code.group(1) if code else cells[0]
        row = {}
        for position, cell in enumerate(cells[1:]):
            if position >= len(header):
                break
            levels = set("F" + level for level in F_LEVEL_RE.findall(cell))
            if levels:
                row[header[position]] = levels
        if row:
            table[name] = row
    return table


def load(root, names=None):
    """Laedt alle Extension-Pakete unter references/custom/.

    names schraenkt auf die in specforge.json aktivierten Pakete ein.
    """
    base = os.path.join(root, "references", "custom")
    if not os.path.isdir(base):
        return {}
    packages = {}
    for entry in sorted(os.listdir(base)):
        if not entry.startswith("@"):
            continue
        if names and entry not in names and entry.lstrip("@") not in names:
            continue
        manifest = os.path.join(base, entry, "manifest.md")
        if not os.path.isfile(manifest):
            continue
        table = parse_manifest(manifest)
        if table:
            packages[entry] = table
    return packages


def allowed_levels(packages, category, perspective):
    """Zulaessige F-Stufen einer Kategorie fuer eine Perspektive.

    Aufloesung wie in enforcement-engine.md: Perspektive, sonst _default.
    Kennt keine Extension die Kategorie, gibt die Funktion None zurueck —
    dann ist die Stufe nicht pruefbar und der Checker schweigt.

    Kategorie-Kuerzel sind nicht global eindeutig: IRM heisst bei @dora
    IKT-Risikomanagement und bei @bait Informationsrisikomanagement, mit
    verschiedenen Stufen. Sind mehrere Extensions aktiv, die dasselbe Kuerzel
    fuehren, gilt die Vereinigung ihrer Stufen. Der Checker beanstandet dann
    nur eine Stufe, die keine der beiden Extensions vorsieht. Wer das
    scharfstellen will, aktiviert in specforge.json die Extension, die
    gemeint ist.
    """
    levels = set()
    for table in packages.values():
        row = table.get(category)
        if not row:
            continue
        if perspective and perspective in row:
            levels |= row[perspective]
        elif DEFAULT_COLUMN in row:
            levels |= row[DEFAULT_COLUMN]
    return levels or None
