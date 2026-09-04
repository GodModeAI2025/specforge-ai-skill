#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft NFR-Checklisten und Extension-Manifeste gegen das eigene Schema.

CONTRIBUTING-CHECKLISTS.md beschreibt eine Vier-Schritte-Pruefung, die bisher
nur von Hand abgehakt wurde. Dieses Skript uebernimmt den maschinell
pruefbaren Teil davon: Schritt 1 (IDs), Schritt 2 (F-Stufen) und Schritt 3
(Manifest). Schritt 4 bleibt ein Smoke-Test in der Session.

Geprueft wird je Checkliste:

1. Jede Pruefpunkt-Zeile traegt eine ID im Format {KAT}-{NN}, alle IDs einer
   Datei sind eindeutig und je Kategorie luecklos ab 01 nummeriert. Eine
   doppelt vergebene ID laesst zwei verschiedene Anforderungen unter
   derselben Referenz laufen, und genau darauf zeigen Specs und Audit Trail.
2. Alle Pruefpunkt-Zeilen einer Datei haben gleich viele Spalten, und die
   letzte Spalte ("Frage an Spec") ist eine Frage.
3. Es gibt eine F-Stufen-Zuordnungstabelle, sie nennt genau die Kategorien
   der Checkliste und nur gueltige Stufen F0 bis F5. Die Schreibweise F4
   und F 4 gilt dabei als gleichwertig, geprueft wird der Wert.

Zusaetzlich je Extension-Paket unter references/custom/@name/:

4. Die manifest.md enthaelt alle Pflicht-Abschnitte.
5. Die F-Stufen-Tabelle des Manifests deckt jede Perspektive aus dem
   Perspektiven-Mapping ab und hat die Pflicht-Spalte _default.
6. Der Abschnitt "Enthaltene Checklisten" nennt Pruefpunkt-Anzahl und
   Kategorien, und beides stimmt mit der Checkliste ueberein. Das ist die
   Angabe, die beim Erweitern einer Checkliste zuerst veraltet.

Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import os
import re
import sys

CHECKPOINT_RE = re.compile(r"^\|\s*([A-Z]{2,5})-(\d{2})\s*\|")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
BOLD_CODE_RE = re.compile(r"\*\*([A-Z]{2,5})\*\*")
F_LEVEL_RE = re.compile(r"\bF\s?(\d)\b")
BACKTICK_RE = re.compile(r"`([^`]+)`")
CONTENT_RE = re.compile(
    r"^- `([^`]+)`\s*[-–—]+\s*(\d+)\s*Prüfpunkte?\s+in\s+"
    r"(\d+)\s*Kategorien?\s*\(([^)]*)\)")

MANIFEST_SECTIONS = ("Scope", "Trigger-Begriffe", "Trigger-Modi",
                     "Perspektiven-Mapping", "F-Stufen-Zuordnung",
                     "Enthaltene Checklisten")


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_lines(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().split("\n")


def split_row(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_checkpoints(lines):
    """Gibt (ids, spaltenzahlen, fehlerhafte_fragen) zurueck."""
    ids = []
    widths = set()
    no_question = []
    for number, line in enumerate(lines, 1):
        match = CHECKPOINT_RE.match(line)
        if not match:
            continue
        cells = split_row(line)
        widths.add(len(cells))
        ids.append((match.group(1), int(match.group(2)), number))
        if not cells[-1].endswith("?"):
            no_question.append((number, cells[-1][:60]))
    return ids, widths, no_question


def find_f_table(lines, start=0):
    """Sucht die erste Tabelle, deren erste Spalte 'Kategorie' heisst.

    Gibt (spaltenkoepfe, {kategorie: [zellen]}) zurueck.
    """
    for index in range(start, len(lines)):
        row = TABLE_ROW_RE.match(lines[index])
        if not row:
            continue
        header = split_row(lines[index])
        if not header or header[0].lower() != "kategorie":
            continue
        rows = {}
        cursor = index + 2  # Trennzeile ueberspringen
        while cursor < len(lines) and TABLE_ROW_RE.match(lines[cursor]):
            cells = split_row(lines[cursor])
            code = BOLD_CODE_RE.search(cells[0])
            if code:
                rows[code.group(1)] = cells[1:]
            else:
                rows[cells[0]] = cells[1:]
            cursor += 1
        return header, rows
    return None, None


def check_f_table(label, header, rows, categories, errors):
    if header is None:
        errors.append("%s: keine F-Stufen-Tabelle mit Spalte 'Kategorie' "
                      "gefunden" % label)
        return
    listed = set(rows)
    if listed != categories:
        missing = sorted(categories - listed)
        extra = sorted(listed - categories)
        if missing:
            errors.append("%s: F-Stufen-Tabelle ohne Kategorie %s"
                          % (label, ", ".join(missing)))
        if extra:
            errors.append("%s: F-Stufen-Tabelle nennt Kategorie %s, die es in "
                          "der Checkliste nicht gibt" % (label, ", ".join(extra)))
    for category in sorted(rows):
        for position, cell in enumerate(rows[category]):
            levels = F_LEVEL_RE.findall(cell)
            if not levels:
                errors.append("%s: F-Stufen-Tabelle, Kategorie %s, Spalte %d "
                              "ohne F-Stufe" % (label, category, position + 2))
                continue
            for level in levels:
                if int(level) > 5:
                    errors.append("%s: ungueltige F-Stufe F%s bei Kategorie %s"
                                  % (label, level, category))


def check_checklist(root, rel, errors):
    lines = read_lines(os.path.join(root, rel))
    ids, widths, no_question = parse_checkpoints(lines)

    if not ids:
        errors.append("%s: keine Pruefpunkt-Zeilen gefunden" % rel)
        return set(), 0

    if len(widths) > 1:
        errors.append("%s: Pruefpunkt-Zeilen mit unterschiedlicher "
                      "Spaltenzahl (%s)" % (rel, sorted(widths)))
    for number, cell in no_question:
        errors.append("%s:%d: letzte Spalte ist keine Frage: %s"
                      % (rel, number, cell))

    seen = {}
    per_category = {}
    for category, index, number in ids:
        key = "%s-%02d" % (category, index)
        if key in seen:
            errors.append("%s:%d: ID %s ist schon in Zeile %d vergeben"
                          % (rel, number, key, seen[key]))
        else:
            seen[key] = number
        per_category.setdefault(category, []).append(index)

    for category in sorted(per_category):
        numbers = per_category[category]
        expected = list(range(1, len(numbers) + 1))
        if sorted(numbers) != expected:
            errors.append("%s: Kategorie %s ist nicht luecklos ab 01 "
                          "nummeriert (%s)" % (rel, category, numbers))

    categories = set(per_category)
    header, rows = find_f_table(lines)
    check_f_table(rel, header, rows, categories, errors)
    return categories, len(ids)


def manifest_sections(lines):
    return [line.lstrip("#").strip() for line in lines if line.startswith("#")]


def parse_perspectives(lines):
    """Perspective-Werte aus der Tabelle unter 'Perspektiven-Mapping'."""
    values = []
    inside = False
    for line in lines:
        if line.startswith("#"):
            inside = "Perspektiven-Mapping" in line
            continue
        if not inside or not TABLE_ROW_RE.match(line):
            continue
        cells = split_row(line)
        code = BACKTICK_RE.search(cells[0])
        if code:
            values.append(code.group(1))
    return values


def check_manifest(root, package, errors):
    """Prueft ein Extension-Paket und gibt die deklarierten Checklisten zurueck."""
    rel = "references/custom/%s/manifest.md" % package
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        errors.append("%s: manifest.md fehlt" % package)
        return []
    lines = read_lines(path)

    headings = manifest_sections(lines)
    for section in MANIFEST_SECTIONS:
        if not any(heading.startswith(section) for heading in headings):
            errors.append("%s: Pflicht-Abschnitt '%s' fehlt" % (rel, section))

    perspectives = parse_perspectives(lines)
    if not perspectives:
        errors.append("%s: Perspektiven-Mapping ohne perspective-Werte" % rel)

    start = 0
    for index, line in enumerate(lines):
        if line.startswith("#") and "F-Stufen-Zuordnung" in line:
            start = index
            break
    header, rows = find_f_table(lines, start)
    if header is not None:
        columns = [cell.strip("` ") for cell in header]
        for value in perspectives:
            if value not in columns:
                errors.append("%s: Perspektive %s fehlt als Spalte in der "
                              "F-Stufen-Tabelle" % (rel, value))
        if "_default" not in columns:
            errors.append("%s: Pflicht-Spalte _default fehlt in der "
                          "F-Stufen-Tabelle" % rel)
    else:
        errors.append("%s: keine F-Stufen-Tabelle gefunden" % rel)

    declared = []
    inside = False
    for line in lines:
        if line.startswith("#"):
            inside = "Enthaltene Checklisten" in line
            continue
        if not inside or not line.startswith("- "):
            continue
        entry = CONTENT_RE.match(line)
        if not entry:
            errors.append("%s: Eintrag unter 'Enthaltene Checklisten' folgt "
                          "nicht dem Muster '- `pfad` - N Pruefpunkte in M "
                          "Kategorien (KAT, ...)': %s" % (rel, line.strip()))
            continue
        categories = [item.strip() for item in entry.group(4).split(",")
                      if item.strip()]
        declared.append({
            "manifest": rel,
            "path": "references/custom/%s/%s" % (package, entry.group(1)),
            "count": int(entry.group(2)),
            "category_count": int(entry.group(3)),
            "categories": set(categories),
        })
    if not declared:
        errors.append("%s: keine Checkliste deklariert" % rel)
    return declared, rows


def main():
    root = repo_root()
    errors = []
    report = []

    core_dir = os.path.join(root, "references", "checklists")
    core = sorted("references/checklists/" + name
                  for name in os.listdir(core_dir)
                  if name.endswith("-nfr.md"))
    for rel in core:
        categories, count = check_checklist(root, rel, errors)
        report.append((rel, count, len(categories), "Core"))

    custom_dir = os.path.join(root, "references", "custom")
    packages = sorted(name for name in os.listdir(custom_dir)
                      if name.startswith("@")
                      and os.path.isdir(os.path.join(custom_dir, name)))

    for package in packages:
        result = check_manifest(root, package, errors)
        if not result:
            continue
        declared, manifest_rows = result
        for entry in declared:
            if not os.path.isfile(os.path.join(root, entry["path"])):
                errors.append("%s: deklarierte Checkliste fehlt: %s"
                              % (entry["manifest"], entry["path"]))
                continue
            categories, count = check_checklist(root, entry["path"], errors)
            report.append((entry["path"], count, len(categories), package))
            if count != entry["count"]:
                errors.append("%s: Manifest nennt %d Pruefpunkte, die "
                              "Checkliste hat %d"
                              % (entry["manifest"], entry["count"], count))
            if len(categories) != entry["category_count"]:
                errors.append("%s: Manifest nennt %d Kategorien, die "
                              "Checkliste hat %d"
                              % (entry["manifest"], entry["category_count"],
                                 len(categories)))
            if entry["categories"] != categories:
                errors.append("%s: Manifest listet die Kategorien %s, die "
                              "Checkliste hat %s"
                              % (entry["manifest"],
                                 ", ".join(sorted(entry["categories"])),
                                 ", ".join(sorted(categories))))
            if manifest_rows is not None and set(manifest_rows) != categories:
                errors.append("%s: F-Stufen-Tabelle im Manifest deckt %s ab, "
                              "die Checkliste hat %s"
                              % (entry["manifest"],
                                 ", ".join(sorted(manifest_rows)),
                                 ", ".join(sorted(categories))))

    print("Geprueft: %d Checkliste(n), %d Extension-Paket(e)"
          % (len(report), len(packages)))
    for rel, count, categories, origin in report:
        print("  %-52s %3d Pruefpunkte, %d Kategorien  [%s]"
              % (rel, count, categories, origin))

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: IDs eindeutig, F-Stufen gueltig, Manifest-Angaben stimmen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
