#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft die Zahlenangaben in README.md und index.html gegen das Repo.

README und Landingpage behaupten Dateizahlen, Modulzahlen und
Pruefpunktzahlen. Diese Zahlen sind aus dem Repo berechenbar, also werden sie
berechnet und mit der Behauptung verglichen, statt sie ein weiteres Mal von
Hand fortzuschreiben. Genau hier lag der Fehler, der die Landingpage
unglaubwuerdig gemacht hat: "10 Fachmodule + 17 Support-Dateien = 28
Dateien" war nicht nur veraltet, es ging auch rechnerisch nicht auf.

Berechnet werden:

- Skill-Payload: SKILL.md plus alle Markdown-Dateien unter references/.
- Fachmodule: references/NN-name.md.
- Support-Dateien: alle uebrigen Dateien unter references/.
- Pruefpunkte je Checkliste: Zeilen mit einer ID {KAT}-{NN}.

Geprueft werden alle Vorkommen dieser Muster:

  "<n> Dateien"           gegen die Payload-Zahl
  "<n> Support-Dateien"   gegen die Zahl der Support-Dateien
  "<n> Module/Fachmodule" gegen die Zahl der Fachmodule
  "<n> ...Pruefpunkte"    gegen die Checkliste, die im Text daneben steht
                          (DORA, BAIT, KRITIS/NIS2)

Zeilenzahlen werden nicht mehr behauptet, weil sie sich mit jeder
Inhaltsaenderung verschieben. Das Skript meldet es, wenn eine solche Angabe
zurueckkommt.

Die Versionstabelle im README ist ein Changelog. Was dort steht, beschreibt
den Stand einer alten Version und wird nicht geprueft.

Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import os
import re
import sys

MODULE_FILE_RE = re.compile(r"^\d{2}-[a-z0-9-]+\.md$")
CHECKPOINT_RE = re.compile(r"^\|\s*[A-Z]{2,5}-\d{2}\s*\|", re.M)
TAG_RE = re.compile(r"<[^>]*>", re.S)

FILES_RE = re.compile(r"(\d+)\s+Dateien\b")
SUPPORT_RE = re.compile(r"(\d+)\s+Support-Dateien\b")
MODULE_RE = re.compile(r"(\d+)\s+(?:Fach)?Modul(?:e|en)\b")
CHECKPOINT_CLAIM_RE = re.compile(r"(\d+)\s+(?:\S*-)?Prüfpunkte\w*")
LINES_RE = re.compile(r"([\d.]+)\s+Zeilen\b")

# Stichwort im Umfeld einer Pruefpunkt-Zahl -> zustaendige Checkliste.
CHECKLIST_KEYWORDS = (
    ("dora", "references/custom/@dora/checklisten/dora-nfr.md"),
    ("bait", "references/custom/@bait/checklisten/bait-nfr.md"),
    ("kritis", "references/checklists/kritis-nfr.md"),
    ("nis2", "references/checklists/kritis-nfr.md"),
)
KEYWORD_WINDOW = 120

CHANGELOG_SECTION = "Versionierung"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def payload_counts(root):
    modules = []
    support = []
    ref_dir = os.path.join(root, "references")
    for dirpath, dirnames, filenames in os.walk(ref_dir):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            rel = rel.replace(os.sep, "/")
            if dirpath == ref_dir and MODULE_FILE_RE.match(name):
                modules.append(rel)
            else:
                support.append(rel)
    return modules, support


def checkpoint_counts(root):
    counts = {}
    for _, path in CHECKLIST_KEYWORDS:
        full = os.path.join(root, path)
        if os.path.isfile(full):
            counts[path] = len(CHECKPOINT_RE.findall(read(full)))
    return counts


def markdown_segments(text):
    """Zeilen des README ausserhalb des Changelogs, als (offset-text, zeile)."""
    segments = []
    section = ""
    for number, line in enumerate(text.split("\n"), 1):
        if line.startswith("## "):
            section = line[3:].strip()
        if section == CHANGELOG_SECTION:
            continue
        segments.append((line, number))
    return segments


def html_segment(text):
    """Gibt (text_ohne_tags, zeilennummer_je_zeichen) zurueck."""
    out = []
    lines = []
    line = 1
    index = 0
    length = len(text)
    while index < length:
        match = TAG_RE.match(text, index)
        if match:
            out.append(" ")
            lines.append(line)
            line += match.group(0).count("\n")
            index = match.end()
            continue
        char = text[index]
        out.append(" " if char == "\n" else char)
        lines.append(line)
        if char == "\n":
            line += 1
        index += 1
    return "".join(out), lines


def nearest_checklist(text, start, end):
    """Ordnet eine Pruefpunkt-Angabe einer Checkliste zu.

    Zuerst gilt das Stichwort in der Angabe selbst ("41 KRITIS/NIS2-
    Pruefpunkte"), sonst das naechste Stichwort links davon
    ("DORA (EU 2022/2554, 58 Pruefpunkte)"). Ein Stichwort rechts der Zahl
    zaehlt nicht, sonst gewinnt in einer Aufzaehlung die falsche Extension.
    """
    inside = text[start:end].lower()
    for keyword, path in CHECKLIST_KEYWORDS:
        if keyword in inside:
            return path
    before = text[max(0, start - KEYWORD_WINDOW):start].lower()
    best = None
    best_position = -1
    for keyword, path in CHECKLIST_KEYWORDS:
        position = before.rfind(keyword)
        if position > best_position:
            best = path
            best_position = position
    return best if best_position >= 0 else None


def check_segment(label, text, line_of, expected, counts, errors):
    """Prueft einen Textabschnitt. line_of(position) liefert die Zeilennummer."""
    hits = 0
    for regex, name, value in (
            (SUPPORT_RE, "Support-Dateien", expected["support"]),
            (FILES_RE, "Dateien", expected["files"]),
            (MODULE_RE, "Fachmodule", expected["modules"])):
        for match in regex.finditer(text):
            hits += 1
            claimed = int(match.group(1))
            if claimed != value:
                errors.append("%s:%d: %s als %d angegeben, tatsaechlich %d"
                              % (label, line_of(match.start()), name,
                                 claimed, value))

    for match in CHECKPOINT_CLAIM_RE.finditer(text):
        hits += 1
        claimed = int(match.group(1))
        path = nearest_checklist(text, match.start(), match.end())
        if path is None:
            errors.append("%s:%d: Angabe '%s' ohne erkennbaren Bezug auf eine "
                          "Checkliste (DORA, BAIT, KRITIS oder NIS2 muss in "
                          "der Naehe stehen)"
                          % (label, line_of(match.start()),
                             match.group(0).strip()))
            continue
        value = counts.get(path)
        if value is None:
            errors.append("%s:%d: Checkliste %s fehlt im Repo"
                          % (label, line_of(match.start()), path))
        elif claimed != value:
            errors.append("%s:%d: %d Pruefpunkte angegeben, %s hat %d"
                          % (label, line_of(match.start()), claimed, path,
                             value))

    for match in LINES_RE.finditer(text):
        errors.append("%s:%d: Zeilenzahl '%s' wird behauptet. Zeilenzahlen "
                      "aendern sich mit jeder Inhaltsaenderung und werden "
                      "hier nicht gefuehrt."
                      % (label, line_of(match.start()), match.group(0).strip()))
    return hits


def main():
    root = repo_root()
    modules, support = payload_counts(root)
    counts = checkpoint_counts(root)
    expected = {
        "files": 1 + len(modules) + len(support),
        "modules": len(modules),
        "support": len(support),
    }

    errors = []
    checked = 0

    readme = read(os.path.join(root, "README.md"))
    for line, number in markdown_segments(readme):
        checked += check_segment("README.md", line, lambda _pos, n=number: n,
                                 expected, counts, errors)

    html = read(os.path.join(root, "index.html"))
    flat, line_map = html_segment(html)
    checked += check_segment("index.html", flat,
                             lambda pos: line_map[pos], expected, counts,
                             errors)

    print("Skill-Payload:           %d Dateien (SKILL.md + references/)"
          % expected["files"])
    print("  Fachmodule:            %d" % expected["modules"])
    print("  Support-Dateien:       %d" % expected["support"])
    for path in sorted(counts):
        print("Pruefpunkte %-46s %d" % (path, counts[path]))
    print("Gepruefte Zahlenangaben: %d in README.md und index.html" % checked)

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: alle geprueften Zahlenangaben stimmen mit dem Repo ueberein.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
