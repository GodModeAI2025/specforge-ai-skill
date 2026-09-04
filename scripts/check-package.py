#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft ein gebautes Release-Artefakt, bevor es jemand herunterlaedt.

Aufruf:

    python scripts/check-package.py [pfad]

Ohne Argument wird dist/<Artefaktname aus der Versionsquelle> geprueft.

Die CI ruft dieses Skript bei jedem Lauf hinter package-skill.py auf, der
Release-Workflow zusaetzlich vor dem Hochladen. Ein kaputtes Paket faellt
damit auf, bevor jemand ein Tag setzt, nicht danach.

Die Erwartung wird aus dem Repo berechnet, nicht aus dem Bauskript
uebernommen. Sonst wuerde die Pruefung nur bestaetigen, was das Bauskript
ohnehin getan hat.

Geprueft wird:

1. Die Datei existiert, ist nicht leer und ist ein lesbares ZIP.
2. Alle Eintraege liegen unter specforge/. Keine absoluten Pfade, kein
   "..", keine Verzeichniseintraege, kein leerer Eintrag.
3. Der Payload stimmt: jede Datei unter references/ ist enthalten, keine
   zusaetzliche, und die Pflichtdateien SKILL.md, README.md, LICENSE,
   TRADEMARK.md und VERSION liegen daneben.
4. Die aus dem Repo uebernommenen Dateien sind Byte fuer Byte identisch.
   Ein Paket, das eine veraenderte Fassung ausliefert, waere schlimmer als
   gar keins.
5. Nichts Verbotenes ist drin: .git, .github, index.html, course.html,
   Landingpage-Assets, Beispiel-Prompts, Pruefskripte, Repo-Doku.
6. VERSION und das erzeugte README tragen die Version aus der
   Versionsquelle, und im README ist kein Platzhalter stehen geblieben.
7. Keine Mailadressen und kein Schluesselmaterial im Textinhalt.

Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import hashlib
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import release_version

PREFIX = "specforge/"
REQUIRED_TOP = ("LICENSE", "README.md", "SKILL.md", "TRADEMARK.md", "VERSION")
# Aus dem Repo uebernommen, also unveraendert erwartet.
COPIED_TOP = ("LICENSE", "SKILL.md", "TRADEMARK.md")
PAYLOAD_DIR = "references"
VERSION_PLACEHOLDER = "@VERSION@"

JUNK_NAMES = (".DS_Store", "Thumbs.db", "desktop.ini")
JUNK_SUFFIXES = (".swp", ".swo", "~", ".orig", ".rej")

# Repo-Innereien und Schluesselmaterial. Geprueft wird der Eintragsname in
# Kleinschreibung.
FORBIDDEN_FRAGMENTS = (
    ".git/", ".github", ".gitignore", "index.html", "course.html",
    "examples/", "docs/", "scripts/", "packaging/", "contributing",
    "changelog", "cli/", "evals/", "tests/", ".py",
    ".ds_store", "thumbs.db", ".env", "id_rsa", "id_ed25519",
    ".pem", ".key", ".p12", ".pfx", "secret", "credential",
)

MAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
KEY_RE = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|ssh-rsa AAAA|aws_secret_access_key",
    re.I)


def is_junk(name):
    if name in JUNK_NAMES or name.startswith("."):
        return True
    return any(name.endswith(suffix) for suffix in JUNK_SUFFIXES)


def expected_payload(root):
    """Alle references/-Dateien des Repos als Archivnamen."""
    expected = {}
    payload_root = os.path.join(root, PAYLOAD_DIR)
    for dirpath, dirnames, filenames in os.walk(payload_root):
        dirnames[:] = sorted(d for d in dirnames if not is_junk(d))
        for name in sorted(filenames):
            if is_junk(name):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            expected[PREFIX + rel] = path
    return expected


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv):
    root = release_version.repo_root()
    try:
        release = release_version.read_release(root)
    except release_version.VersionsquelleFehler as error:
        print("FEHLER: %s" % error)
        return 1

    if len(argv) > 2:
        print("Aufruf: check-package.py [pfad]")
        return 1
    target = argv[1] if len(argv) == 2 else os.path.join(
        root, "dist", release["artifact"])

    if not os.path.isfile(target):
        print("FEHLER: Artefakt fehlt: %s" % target)
        return 1
    size = os.path.getsize(target)
    if size == 0:
        print("FEHLER: Artefakt ist leer: %s" % target)
        return 1
    if not zipfile.is_zipfile(target):
        print("FEHLER: Artefakt ist kein lesbares ZIP: %s" % target)
        return 1

    errors = []
    if os.path.basename(target) != release["artifact"]:
        errors.append("Dateiname '%s' weicht vom Artefaktnamen der "
                      "Versionsquelle ab ('%s')"
                      % (os.path.basename(target), release["artifact"]))

    with zipfile.ZipFile(target) as archive:
        broken = archive.testzip()
        if broken is not None:
            print("FEHLER: beschaedigter Eintrag im Archiv: %s" % broken)
            return 1
        names = archive.namelist()
        contents = {}
        for name in names:
            contents[name] = archive.read(name)
        sizes = dict((info.filename, info.file_size)
                     for info in archive.infolist())

    for name in sorted(names):
        if name.endswith("/"):
            errors.append("Verzeichniseintrag im Archiv: %s" % name)
        if name.startswith("/") or ".." in name.split("/") or "\\" in name:
            errors.append("Unsicherer Pfad im Archiv: %s" % name)
        if not name.startswith(PREFIX):
            errors.append("Eintrag liegt nicht unter %s: %s" % (PREFIX, name))
        if sizes.get(name, 0) == 0:
            errors.append("Leerer Eintrag im Archiv: %s" % name)
        lowered = name.lower()
        for fragment in FORBIDDEN_FRAGMENTS:
            if fragment in lowered:
                errors.append("Verbotener Inhalt im Archiv: %s "
                              "(Muster '%s')" % (name, fragment))

    expected = expected_payload(root)
    packed_payload = set(n for n in names
                         if n.startswith(PREFIX + PAYLOAD_DIR + "/"))
    for name in sorted(set(expected) - packed_payload):
        errors.append("Payload-Datei fehlt im Archiv: %s" % name)
    for name in sorted(packed_payload - set(expected)):
        errors.append("Archiv enthaelt eine Datei, die es unter %s/ nicht "
                      "gibt: %s" % (PAYLOAD_DIR, name))

    top_level = set(n for n in names
                    if n.startswith(PREFIX)
                    and "/" not in n[len(PREFIX):])
    for name in REQUIRED_TOP:
        if PREFIX + name not in top_level:
            errors.append("Pflichtdatei fehlt im Archiv: %s" % (PREFIX + name))
    for name in sorted(top_level):
        if name[len(PREFIX):] not in REQUIRED_TOP:
            errors.append("Unerwartete Datei im Archiv: %s" % name)

    unchanged = 0
    for name in sorted(set(expected) & packed_payload):
        if contents[name] != read_bytes(expected[name]):
            errors.append("Inhalt weicht vom Repo ab: %s" % name)
        else:
            unchanged += 1
    for name in COPIED_TOP:
        arcname = PREFIX + name
        source = os.path.join(root, name)
        if arcname in contents and os.path.isfile(source):
            if contents[arcname] != read_bytes(source):
                errors.append("Inhalt weicht vom Repo ab: %s" % arcname)
            else:
                unchanged += 1

    version_entry = PREFIX + "VERSION"
    if version_entry in contents:
        packed_version = contents[version_entry].decode("utf-8").strip()
        if packed_version != release["version"]:
            errors.append("VERSION im Archiv ist '%s', die Versionsquelle "
                          "sagt '%s'" % (packed_version, release["version"]))

    readme_entry = PREFIX + "README.md"
    if readme_entry in contents:
        readme = contents[readme_entry].decode("utf-8")
        if VERSION_PLACEHOLDER in readme:
            errors.append("Platzhalter %s steht noch im README des Pakets"
                          % VERSION_PLACEHOLDER)
        if release["version"] not in readme:
            errors.append("README des Pakets nennt die Version %s nicht"
                          % release["version"])

    mails = []
    keys = []
    for name in sorted(names):
        try:
            text = contents[name].decode("utf-8")
        except UnicodeDecodeError:
            errors.append("Eintrag ist kein UTF-8-Text: %s" % name)
            continue
        for match in MAIL_RE.finditer(text):
            mails.append("%s: %s" % (name, match.group(0)))
        if KEY_RE.search(text):
            keys.append(name)
    for entry in mails:
        errors.append("Mailadresse im Paket: %s" % entry)
    for entry in keys:
        errors.append("Schluesselmaterial im Paket: %s" % entry)

    print("Geprueftes Artefakt:     %s" % target)
    print("Groesse:                 %d Bytes" % size)
    print("SHA256:                  %s" % sha256(target))
    print("Version laut Quelle:     %s (Tag %s)"
          % (release["version"], release["tag"]))
    print("Eintraege:               %d" % len(names))
    print("  Payload references/:   %d von %d erwartet"
          % (len(packed_payload), len(expected)))
    print("  Pflichtdateien:        %d von %d"
          % (len(top_level), len(REQUIRED_TOP)))
    print("  unveraendert aus Repo: %d" % unchanged)
    print("Verbotene Muster:        %d geprueft, 0 Treffer erwartet"
          % len(FORBIDDEN_FRAGMENTS))
    print("Mailadressen:            %d" % len(mails))
    print("Schluesselmaterial:      %d" % len(keys))

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: Paket vollstaendig, unveraendert und frei von Repo-Innereien.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
