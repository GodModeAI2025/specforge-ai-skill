#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut das Release-Artefakt: den Skill-Payload als ZIP.

Aufruf:

    python scripts/package-skill.py dist/specforge-skill.zip

Laeuft lokal, ohne Netz und ohne GitHub. Der Release-Workflow ruft genau
dieses Skript auf und haengt das Ergebnis an das Release. Damit ist das
Paket vor dem Tag pruefbar, nicht erst danach.

Was hineinkommt:

- SKILL.md und alles unter references/, also der Payload, den Claude laedt
- LICENSE und TRADEMARK.md, weil der Payload fremde Marken benennt
- README.md, erzeugt aus packaging/paket-readme.md, damit der entpackte
  Ordner fuer sich verstaendlich ist
- VERSION mit der Version aus der Versionsquelle

Was draussen bleibt: index.html, course.html, .github/, .git/, scripts/,
docs/, examples/, CHANGELOG und alles weitere Repo-Innere. Der Payload ist
nicht das Repo.

Reproduzierbarkeit: fester Zeitstempel, feste Rechte, sortierte
Reihenfolge, kein Zufallsname. Zwei Laeufe hintereinander ergeben dieselbe
Datei, Byte fuer Byte. Ohne das laesst sich nicht pruefen, ob ein Paket
inhaltlich vom vorigen abweicht oder nur neu gebaut wurde.

Exit 0 wenn das Paket geschrieben wurde, sonst 1. Nur Standardbibliothek.
"""

import hashlib
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import release_version

PREFIX = "specforge/"
TOP_FILES = ("SKILL.md", "LICENSE", "TRADEMARK.md")
PAYLOAD_DIR = "references"
README_TEMPLATE = os.path.join("packaging", "paket-readme.md")
VERSION_PLACEHOLDER = "@VERSION@"

# Fester Zeitstempel im Archiv. Kein Bezug zur Bauzeit, sonst waere jedes
# Paket ein anderes.
FIXED_DATE = (2026, 1, 1, 0, 0, 0)
FILE_MODE = 0o644 << 16
CREATE_SYSTEM_UNIX = 3

# Betriebssystem- und Editor-Reste, die nichts im Paket verloren haben.
JUNK_NAMES = (".DS_Store", "Thumbs.db", "desktop.ini")
JUNK_SUFFIXES = (".swp", ".swo", "~", ".orig", ".rej")


def is_junk(name):
    if name in JUNK_NAMES or name.startswith("."):
        return True
    return any(name.endswith(suffix) for suffix in JUNK_SUFFIXES)


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def collect_repo_files(root):
    """Gibt [(arcname, quellpfad)] fuer die Dateien aus dem Repo zurueck."""
    entries = []
    skipped = []
    for name in TOP_FILES:
        path = os.path.join(root, name)
        if not os.path.isfile(path):
            raise IOError("Pflichtdatei fehlt: %s" % name)
        entries.append((PREFIX + name, path))

    payload_root = os.path.join(root, PAYLOAD_DIR)
    if not os.path.isdir(payload_root):
        raise IOError("Verzeichnis fehlt: %s/" % PAYLOAD_DIR)
    for dirpath, dirnames, filenames in os.walk(payload_root):
        dirnames[:] = sorted(d for d in dirnames if not is_junk(d))
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if is_junk(name):
                skipped.append(rel)
                continue
            entries.append((PREFIX + rel, path))
    return entries, skipped


def build_generated(root, release):
    """Erzeugte Dateien: README.md aus der Vorlage und VERSION."""
    template_path = os.path.join(root, README_TEMPLATE)
    if not os.path.isfile(template_path):
        raise IOError("Vorlage fehlt: %s" % README_TEMPLATE)
    with open(template_path, encoding="utf-8") as handle:
        template = handle.read()
    if VERSION_PLACEHOLDER not in template:
        raise IOError("Vorlage %s enthaelt kein %s"
                      % (README_TEMPLATE, VERSION_PLACEHOLDER))
    readme = template.replace(VERSION_PLACEHOLDER, release["version"])
    return [
        (PREFIX + "README.md", readme.encode("utf-8")),
        (PREFIX + "VERSION", (release["version"] + "\n").encode("utf-8")),
    ]


def write_archive(target, items):
    """Schreibt das ZIP deterministisch. items ist [(arcname, bytes)]."""
    directory = os.path.dirname(os.path.abspath(target))
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for arcname, data in sorted(items, key=lambda item: item[0]):
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = CREATE_SYSTEM_UNIX
            info.external_attr = FILE_MODE
            archive.writestr(info, data, compresslevel=9)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv):
    if len(argv) != 2:
        print("Aufruf: package-skill.py <ausgabepfad>")
        print("Beispiel: python scripts/package-skill.py "
              "dist/specforge-skill.zip")
        return 1
    target = argv[1]

    root = release_version.repo_root()
    try:
        release = release_version.read_release(root)
    except release_version.VersionsquelleFehler as error:
        print("FEHLER: %s" % error)
        return 1

    try:
        repo_entries, skipped = collect_repo_files(root)
        items = [(arcname, read_bytes(path)) for arcname, path in repo_entries]
        items.extend(build_generated(root, release))
    except IOError as error:
        print("FEHLER: %s" % error)
        return 1

    empty = [arcname for arcname, data in items if not data]
    if empty:
        print("FEHLER: leere Datei im Paket: %s" % ", ".join(sorted(empty)))
        return 1

    write_archive(target, items)

    print("Versionsquelle:          CHANGELOG.md, Abschnitt Aktuelles Release")
    print("Version:                 %s (Tag %s, Skill-Version %s)"
          % (release["version"], release["tag"], release["skill_version"]))
    print("Artefaktname laut Quelle: %s" % release["artifact"])
    print("Ausgabepfad:             %s" % target)
    if os.path.basename(target) != release["artifact"]:
        print("Hinweis:                 Der Dateiname weicht vom Artefaktnamen "
              "der Versionsquelle ab.")
    if skipped:
        print("Uebersprungen:           %s" % ", ".join(skipped))
    print("Eintraege:               %d" % len(items))
    for arcname, data in sorted(items, key=lambda item: item[0]):
        print("  %-52s %7d" % (arcname, len(data)))
    print("Groesse:                 %d Bytes" % os.path.getsize(target))
    print("SHA256:                  %s" % sha256(target))
    print("")
    print("OK: Paket geschrieben.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
