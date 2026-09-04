# -*- coding: utf-8 -*-
"""Liest die F-Stufen-Tabellen der Regulatorik-Extensions.

Jede Extension unter references/custom/@name/ fuehrt in ihrer manifest.md
einen Abschnitt "F-Stufen-Zuordnung": je Kategorie eine Zeile, je Perspektive
eine Spalte, dazu die Pflicht-Spalte _default. Genau das ist die Tabelle, die
in der Session entscheidet, welche F-Stufe eine fehlende Anforderung bekommt.

Welche Pakete gelten, sagt das Feld extensions in der specforge.json. Es ist
fehlertolerant nach der falschen Seite gewesen: "@DORA" statt "@dora" ergab
"Extensions: keine" und liess die F-Stufen-Pruefung kommentarlos entfallen,
eine leere Liste galt als "nicht gesetzt" und lud alles. Jetzt werden die
Namen normalisiert, ein unbekannter Name ist ein Aufrufproblem, und die
leere Liste heisst ausdruecklich "keine Extension".

Der Checker liest die Tabelle, statt sie zu wiederholen. Eine Zelle kann mehrere
Stufen nennen ("F4 (TLPT) / F3", "F4 (PII) / F3"), und die Bedingung dahinter
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


class ExtensionFehler(ValueError):
    """Die Angabe extensions in der specforge.json ist nicht benutzbar."""


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


def normalise_name(value):
    """'@DORA', 'DORA', ' dora ' und '@dora' sind derselbe Name."""
    return str(value).strip().casefold().lstrip("@")


def available(base):
    return sorted(entry for entry in os.listdir(base)
                  if entry.startswith("@")
                  and os.path.isdir(os.path.join(base, entry)))


def load(root, names=None):
    """Laedt die Extension-Pakete unter references/custom/.

    names ist die Angabe aus specforge.json:

        None  Feld nicht gesetzt, alle vorhandenen Pakete gelten
        []    ausdruecklich keine Extension
        [...] genau diese, unabhaengig von Schreibweise und fuehrendem @

    Ein Name, zu dem es kein Paket gibt, ist ein Aufrufproblem und keine
    Kleinigkeit: die Datei wollte eine Regulatorik aktivieren, und ein
    stilles Ignorieren nimmt genau die Pruefung heraus, um derentwillen sie
    dasteht.
    """
    base = os.path.join(root, "references", "custom")
    if not os.path.isdir(base):
        if names:
            raise ExtensionFehler(
                "kein Verzeichnis references/custom/ unter %s, aber "
                "extensions verlangt %s" % (root, ", ".join(map(str, names))))
        return {}

    entries = available(base)
    known = dict((normalise_name(entry), entry) for entry in entries)

    wanted = None
    if names is not None:
        if not isinstance(names, (list, tuple)):
            raise ExtensionFehler(
                "extensions muss eine Liste von Namen sein, gefunden %r"
                % (names,))
        wanted = {}
        for name in names:
            if not isinstance(name, str) or not name.strip():
                raise ExtensionFehler(
                    "extensions enthaelt einen leeren oder nicht "
                    "textwertigen Eintrag: %r" % (name,))
            wanted[normalise_name(name)] = name
        unknown = [wanted[key] for key in sorted(wanted) if key not in known]
        if unknown:
            raise ExtensionFehler(
                "unbekannte Extension %s. Vorhanden unter references/custom/: "
                "%s" % (", ".join("'%s'" % item for item in unknown),
                        ", ".join(entries) or "keine"))

    packages = {}
    for entry in entries:
        requested = wanted is not None
        if requested and normalise_name(entry) not in wanted:
            continue
        manifest = os.path.join(base, entry, "manifest.md")
        if not os.path.isfile(manifest):
            if requested:
                raise ExtensionFehler(
                    "Extension '%s' hat keine manifest.md" % entry)
            continue
        table = parse_manifest(manifest)
        if not table:
            if requested:
                raise ExtensionFehler(
                    "Extension '%s' fuehrt keinen Abschnitt '%s'"
                    % (entry, SECTION))
            continue
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
