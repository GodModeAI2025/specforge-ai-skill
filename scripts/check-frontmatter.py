#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft das YAML-Frontmatter von SKILL.md gegen die Skill-Konventionen.

Claude laedt einen Skill ueber das Frontmatter. Ein grossgeschriebener oder
mit Leerzeichen versehener name macht den Skill unauffindbar, eine zu lange
description wird abgeschnitten, und ein unbekannter Schluessel faellt erst
beim Laden auf. Alles davon ist ein Ein-Zeichen-Fehler in einer Datei, die
sonst niemand systematisch liest.

Geprueft wird:

1. Die Datei beginnt mit einem Frontmatter-Block, der mit --- oeffnet und
   mit --- schliesst.
2. name ist vorhanden, klein geschrieben, nur a-z, 0-9 und Bindestrich,
   hoechstens 64 Zeichen.
3. description ist vorhanden, nicht leer und hoechstens 1024 Zeichen lang.
   Der Block-Skalar (description: >) wird dabei zusammengefaltet gezaehlt,
   also so, wie der Wert nach dem Parsen aussieht.
4. Nur bekannte Schluessel. Ein Tippfehler wie "descripton" wuerde sonst
   dazu fuehren, dass der Skill ohne Beschreibung ausgeliefert wird. Kommt
   ein neuer Schluessel legitim dazu, gehoert er in KNOWN_KEYS.
5. Keine Tabulatoren im Frontmatter. YAML verbietet sie zur Einrueckung.

Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")

NAME_MAX = 64
DESCRIPTION_MAX = 1024
KNOWN_KEYS = ("name", "description", "license", "allowed-tools",
              "metadata", "version", "compatibility")
REQUIRED_KEYS = ("name", "description")


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def split_frontmatter(text):
    """Gibt (frontmatter_zeilen, fehler) zurueck."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, "SKILL.md beginnt nicht mit einer Zeile ---"
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], None
    return None, "Frontmatter in SKILL.md wird nicht mit --- geschlossen"


def parse_frontmatter(lines):
    """Flacher Parser fuer skalare Werte und Block-Skalare (> und |).

    Reicht fuer Skill-Frontmatter und vermeidet die Abhaengigkeit auf PyYAML,
    die sonst nur fuer diese eine Datei im Workflow installiert wuerde.
    """
    values = {}
    order = []
    current = None
    block = []
    for raw in lines:
        if current is not None and (raw.startswith("  ") or not raw.strip()):
            block.append(raw.strip())
            continue
        if current is not None:
            values[current] = " ".join(part for part in block if part)
            current = None
            block = []
        match = KEY_RE.match(raw)
        if not match:
            continue
        key, rest = match.group(1), match.group(2).strip()
        order.append(key)
        if rest in (">", "|", ">-", "|-"):
            current = key
            block = []
        else:
            values[key] = rest
    if current is not None:
        values[current] = " ".join(part for part in block if part)
    return values, order


def main():
    root = repo_root()
    path = os.path.join(root, "SKILL.md")
    if not os.path.isfile(path):
        print("FEHLER: SKILL.md nicht gefunden")
        return 1

    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    lines, error = split_frontmatter(text)
    if error:
        print("FEHLER: %s" % error)
        return 1

    errors = []
    if any("\t" in line for line in lines):
        errors.append("Frontmatter enthaelt einen Tabulator")

    values, order = parse_frontmatter(lines)

    for key in REQUIRED_KEYS:
        if key not in values:
            errors.append("Pflichtschluessel fehlt: %s" % key)

    for key in order:
        if key not in KNOWN_KEYS:
            errors.append("Unbekannter Schluessel im Frontmatter: %s "
                          "(erlaubt: %s)" % (key, ", ".join(KNOWN_KEYS)))

    duplicates = sorted({key for key in order if order.count(key) > 1})
    for key in duplicates:
        errors.append("Schluessel doppelt vergeben: %s" % key)

    name = values.get("name", "")
    if "name" in values:
        if not name:
            errors.append("name ist leer")
        else:
            if not NAME_RE.match(name):
                errors.append("name '%s' verletzt das Muster "
                              "a-z, 0-9 und Bindestrich, klein geschrieben"
                              % name)
            if len(name) > NAME_MAX:
                errors.append("name ist %d Zeichen lang, erlaubt sind %d"
                              % (len(name), NAME_MAX))

    description = values.get("description", "")
    if "description" in values:
        if not description:
            errors.append("description ist leer")
        elif len(description) > DESCRIPTION_MAX:
            errors.append("description ist %d Zeichen lang, erlaubt sind %d"
                          % (len(description), DESCRIPTION_MAX))

    print("Frontmatter-Zeilen:      %d" % len(lines))
    print("Schluessel:              %s" % (", ".join(order) or "keine"))
    print("name:                    %s" % (name or "-"))
    print("description:             %d von %d Zeichen"
          % (len(description), DESCRIPTION_MAX))

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: Frontmatter erfuellt name-, description- und Schluessel-Regeln.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
