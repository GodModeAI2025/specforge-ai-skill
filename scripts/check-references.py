#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft die references/-Pfade, die SKILL.md und die Module nennen.

Der Skill laedt Referenzdateien per Pfadangabe. Ohne Pruefung faellt ein
Tippfehler oder eine geloeschte Datei erst in der Session auf, und dort nur
als Text, den das Modell notfalls improvisiert.

Geprueft werden drei Regeln aus SKILL.md, Abschnitt "Fehlerbehandlung bei
fehlenden Referenzen":

1. Ablageregel: Erweiterungspunkte liegen unterhalb references/custom/.
   Jeder andere references/-Pfad ist Core und muss existieren.
2. Die als KRITISCH gefuehrten Dateien muessen existieren. Die Liste wird aus
   SKILL.md gelesen, nicht hier hartkodiert, damit beide nicht auseinander
   laufen.
3. Extension-Pakete: ein Paket references/custom/@name/, das im Repo liegt,
   ist ausgeliefert. Jeder Pfad, der in dieses Paket zeigt, muss existieren,
   ebenso alles, was seine manifest.md unter "Enthaltene Checklisten"
   auffuehrt. Nur Pfade in nicht vorhandene Pakete und die flachen
   references/custom/*.md duerfen fehlen.

Quelldateien: SKILL.md und references/**/*.md.
Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import os
import re
import sys

# Pfad-Token im Fliesstext, in Tabellen und in Code-Fences.
PATH_RE = re.compile(r"references/[A-Za-z0-9_@{}*./+-]+")
# Zeichen, die haeufig direkt am Pfad kleben, ohne dazuzugehoeren.
TRAILING = "`.,;:)\"'*_"
# Alles mit Platzhaltern ist kein pruefbarer Pfad.
PLACEHOLDER_RE = re.compile(r"[*{}]|\bNN\b")

CUSTOM_PREFIX = "references/custom/"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def source_files(root):
    files = []
    skill = os.path.join(root, "SKILL.md")
    if os.path.isfile(skill):
        files.append(skill)
    ref_dir = os.path.join(root, "references")
    for dirpath, dirnames, filenames in os.walk(ref_dir):
        dirnames.sort()
        for name in sorted(filenames):
            if name.endswith(".md"):
                files.append(os.path.join(dirpath, name))
    return files


def collect_paths(root, files):
    """Gibt {pfad: [(datei, zeile), ...]} zurueck."""
    found = {}
    for path in files:
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                for match in PATH_RE.finditer(line):
                    token = match.group(0).rstrip(TRAILING)
                    if not token:
                        continue
                    found.setdefault(token, []).append((rel, lineno))
    return found


def read_critical(root):
    """Liest die KRITISCH-Liste aus SKILL.md."""
    skill = os.path.join(root, "SKILL.md")
    critical = []
    inside = False
    with open(skill, encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith("**KRITISCH"):
                inside = True
                continue
            if inside:
                if stripped.startswith("- `"):
                    token = stripped.split("`")[1]
                    critical.append(token)
                elif stripped and not stripped.startswith("-"):
                    break
    return critical


def shipped_package(root, token):
    """Paketname, wenn der Pfad in ein im Repo vorhandenes @-Paket zeigt."""
    rest = token[len(CUSTOM_PREFIX):]
    if "/" not in rest:
        return None
    package = rest.split("/", 1)[0]
    if not package.startswith("@"):
        return None
    if os.path.isdir(os.path.join(root, "references", "custom", package)):
        return CUSTOM_PREFIX + package
    return None


def read_manifest_files(root):
    """Sammelt die von Extension-Manifesten deklarierten Dateien."""
    declared = []
    custom_dir = os.path.join(root, "references", "custom")
    if not os.path.isdir(custom_dir):
        return declared
    for entry in sorted(os.listdir(custom_dir)):
        manifest = os.path.join(custom_dir, entry, "manifest.md")
        if not os.path.isfile(manifest):
            continue
        inside = False
        with open(manifest, encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if stripped.startswith("#"):
                    inside = "Enthaltene Checklisten" in stripped
                    continue
                if inside and stripped.startswith("- `"):
                    token = stripped.split("`")[1]
                    rel = os.path.join("references", "custom", entry, token)
                    declared.append((rel.replace(os.sep, "/"),
                                     os.path.relpath(manifest, root)))
    return declared


def main():
    root = repo_root()
    files = source_files(root)
    found = collect_paths(root, files)

    placeholders = []
    non_files = []
    core = []
    extension = []

    for token in sorted(found):
        if PLACEHOLDER_RE.search(token):
            placeholders.append(token)
        elif not token.endswith(".md"):
            non_files.append(token)
        elif token.startswith(CUSTOM_PREFIX):
            extension.append(token)
        else:
            core.append(token)

    errors = []

    missing_core = [t for t in core if not os.path.isfile(os.path.join(root, t))]
    for token in missing_core:
        where = ", ".join("%s:%d" % loc for loc in found[token][:3])
        errors.append("Core-Pfad fehlt: %s (genannt in %s)" % (token, where))

    critical = read_critical(root)
    for token in critical:
        if not os.path.isfile(os.path.join(root, token)):
            errors.append("KRITISCH-Datei fehlt: %s (SKILL.md)" % token)
        elif token.startswith(CUSTOM_PREFIX):
            errors.append("KRITISCH-Datei liegt unter references/custom/, "
                          "das widerspricht der Ablageregel: %s" % token)

    declared = read_manifest_files(root)
    for token, manifest in declared:
        if not os.path.isfile(os.path.join(root, token)):
            errors.append("Vom Manifest deklarierte Datei fehlt: %s (%s)"
                          % (token, manifest))

    for token in extension:
        package = shipped_package(root, token)
        if package and not os.path.isfile(os.path.join(root, token)):
            where = ", ".join("%s:%d" % loc for loc in found[token][:3])
            errors.append("Verweis in das ausgelieferte Paket %s zeigt auf eine "
                          "Datei, die es dort nicht gibt: %s (genannt in %s)"
                          % (package, token, where))

    ext_present = [t for t in extension
                   if os.path.isfile(os.path.join(root, t))]
    ext_absent = [t for t in extension if t not in ext_present]

    print("Quelldateien:            %d (SKILL.md + references/**/*.md)" % len(files))
    print("Gefundene Pfad-Angaben:  %d eindeutig" % len(found))
    print("  davon Platzhalter:     %d (uebersprungen)" % len(placeholders))
    print("  davon keine .md-Datei: %d (uebersprungen)" % len(non_files))
    print("Gepruefte Pfade:         %d" % (len(core) + len(extension)))
    print("  Core (Pflicht):        %d, davon fehlend %d"
          % (len(core), len(missing_core)))
    print("  Erweiterungspunkte:    %d, davon angelegt %d, offen %d"
          % (len(extension), len(ext_present), len(ext_absent)))
    print("KRITISCH laut SKILL.md:  %d" % len(critical))
    print("Manifest-Deklarationen:  %d" % len(declared))

    if ext_absent:
        print("")
        print("Offene Erweiterungspunkte (dokumentiert, Fehlen erlaubt):")
        for token in ext_absent:
            print("  - %s" % token)

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: alle Core-Pfade, KRITISCH-Dateien und Manifest-Angaben vorhanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
