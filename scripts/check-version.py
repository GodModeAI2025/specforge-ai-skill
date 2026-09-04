#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueft Versionsangaben und Artefaktnamen gegen die Versionsquelle.

Aufruf:

    python scripts/check-version.py
    python scripts/check-version.py --tag v3.2.0

Die Version steht in CHANGELOG.md, Abschnitt "Aktuelles Release". README,
Landingpage, Release-Workflow und CI nennen sie erneut, weil ein Mensch sie
dort lesen will. Genau daraus entsteht der Fehler, den niemand bemerkt: eine
Stelle wird nachgezogen, die andere nicht. Also wird verglichen.

Geprueft wird:

1. Die Versionsquelle ist lesbar und in sich stimmig (Tag, Skill-Version,
   Artefaktname).
2. Die Versionsgeschichte in CHANGELOG.md endet bei der Skill-Version, die
   das Release paketiert.
3. README.md nennt dieselbe Skill-Version ("aktuell X.Y") und denselben Tag.
4. index.html nennt dieselbe Skill-Version an allen vier Stellen, an denen
   sie steht: JSON-LD, generator-Meta, Badge und Crawler-Zusammenfassung.
5. Jede Download-URL in README.md und index.html endet auf den
   Artefaktnamen aus der Versionsquelle. Das ist der Teil, der beim ersten
   Release schweigend danebengehen wuerde: der Link waere da, das Paket
   hiesse anders, und der Download bliebe 404.
6. Die Workflows bauen und pruefen genau diesen Dateinamen, und der
   Release-Workflow haengt an Tags v*.
7. docs/ci-example.yml pinnt die Composite Action auf denselben Tag. Ein
   veralteter Pin dort schickt fremde Pipelines auf eine Referenz, die es
   nicht gibt, und faellt in diesem Repo sonst nie auf.
8. Mit --tag: der uebergebene Tag ist der aus der Versionsquelle. Der
   Release-Workflow ruft das so auf, damit ein vertipptes Tag kein Release
   erzeugt.

Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import release_version

HISTORY_HEADING = "## Versionsgeschichte"
SEPARATOR_RE = re.compile(r"^[:\- ]+$")
HISTORY_VERSION_RE = re.compile(r"^(\d+\.\d+)")

CURRENT_RE = re.compile(r"aktuell (\d+\.\d+)")
FULL_TAG_RE = re.compile(r"\bv\d+\.\d+\.\d+\b")
# Nur URLs mit Dateinamen. Die blosse Nennung des Verzeichnisses
# `releases/latest/download/` im Fliesstext ist kein Artefaktname.
DOWNLOAD_RE = re.compile(
    r"releases/(?:latest/)?download/([A-Za-z0-9][A-Za-z0-9._-]*\.[A-Za-z0-9]+)")
WORKFLOW_ZIP_RE = re.compile(r"dist/([A-Za-z0-9._-]+\.zip)")

# Stellen in index.html, an denen die Skill-Version steht. Fehlt eine, ist
# die Seite umgebaut worden und die Pruefung muss nachgezogen werden.
HTML_ANCHORS = (
    ("JSON-LD softwareVersion",
     re.compile(r'"softwareVersion"\s*:\s*"([\d.]+)"')),
    ("generator-Meta",
     re.compile(r'<meta name="generator" content="SpecForge v([\d.]+)">')),
    ("Badge im Kopf",
     re.compile(r'badge-green">v([\d.]+)<')),
    ("Crawler-Zusammenfassung",
     re.compile(r'Claude-Skill \(v([\d.]+)\)')),
)

WORKFLOWS = (
    os.path.join(".github", "workflows", "ci.yml"),
    os.path.join(".github", "workflows", "release.yml"),
)

# Beispiel fuer fremde Repositories. Der Tag darin pinnt die Composite
# Action und muss mitwandern.
EXAMPLE_WORKFLOW = os.path.join("docs", "ci-example.yml")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def history_versions(text):
    """Versionen der Tabelle unter '## Versionsgeschichte', in Reihenfolge."""
    versions = []
    inside = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            if inside:
                break
            inside = stripped == HISTORY_HEADING
            continue
        if not inside or not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or all(SEPARATOR_RE.match(cell or "-") for cell in cells):
            continue
        match = HISTORY_VERSION_RE.match(cells[0])
        if match:
            versions.append(match.group(1))
    return versions


def check_all(label, text, regex, expected, what, errors, required=True):
    """Jeder Treffer muss expected sein, und es muss einen geben."""
    hits = regex.findall(text)
    for hit in hits:
        if hit != expected:
            errors.append("%s: %s steht als '%s', die Versionsquelle sagt '%s'"
                          % (label, what, hit, expected))
    if required and not hits:
        errors.append("%s: %s nicht gefunden. Wurde die Datei umgebaut, muss "
                      "check-version.py nachgezogen werden." % (label, what))
    return len(hits)


def main(argv):
    tag_argument = None
    rest = argv[1:]
    if rest[:1] == ["--tag"]:
        if len(rest) != 2:
            print("Aufruf: check-version.py [--tag <tag>]")
            return 1
        tag_argument = rest[1]
    elif rest:
        print("Aufruf: check-version.py [--tag <tag>]")
        return 1

    root = release_version.repo_root()
    try:
        release = release_version.read_release(root)
    except release_version.VersionsquelleFehler as error:
        print("FEHLER: %s" % error)
        return 1

    skill = release["skill_version"]
    tag = release["tag"]
    artifact = release["artifact"]
    errors = []
    checked = 0

    changelog = read(release_version.changelog_path(root))
    history = history_versions(changelog)
    if not history:
        errors.append("CHANGELOG.md: Abschnitt '%s' ohne Tabellenzeilen"
                      % HISTORY_HEADING)
    elif history[-1] != skill:
        errors.append("CHANGELOG.md: juengster Eintrag der Versionsgeschichte "
                      "ist %s, das Release paketiert %s"
                      % (history[-1], skill))
    checked += 1

    readme = read(os.path.join(root, "README.md"))
    html = read(os.path.join(root, "index.html"))

    tag_sources = [("README.md", readme), ("index.html", html)]
    example = os.path.join(root, EXAMPLE_WORKFLOW)
    if os.path.isfile(example):
        tag_sources.append((EXAMPLE_WORKFLOW, read(example)))

    checked += check_all("README.md", readme, CURRENT_RE, skill,
                         "die Skill-Version", errors)
    for label, text in tag_sources:
        for hit in FULL_TAG_RE.findall(text):
            checked += 1
            if hit != tag:
                errors.append("%s: Tag '%s' genannt, die Versionsquelle sagt "
                              "'%s'" % (label, hit, tag))

    for what, regex in HTML_ANCHORS:
        checked += check_all("index.html", html, regex, skill, what, errors)

    for label, text in (("README.md", readme), ("index.html", html)):
        checked += check_all(label, text, DOWNLOAD_RE, artifact,
                             "der Artefaktname in der Download-URL", errors)

    for relative in WORKFLOWS:
        path = os.path.join(root, relative)
        if not os.path.isfile(path):
            errors.append("Workflow fehlt: %s" % relative)
            continue
        workflow = read(path)
        checked += check_all(relative, workflow, WORKFLOW_ZIP_RE, artifact,
                             "der gebaute Dateiname", errors)
        for script in ("scripts/package-skill.py", "scripts/check-package.py"):
            if script not in workflow:
                errors.append("%s: ruft %s nicht auf" % (relative, script))

    release_workflow = read(os.path.join(root, WORKFLOWS[1]))
    if "tags:" not in release_workflow or "'v*'" not in release_workflow:
        errors.append("%s: reagiert nicht auf push von Tags 'v*'"
                      % WORKFLOWS[1])
    if "contents: write" not in release_workflow:
        errors.append("%s: fehlende Berechtigung contents: write"
                      % WORKFLOWS[1])

    if tag_argument is not None:
        checked += 1
        if tag_argument != tag:
            errors.append("Uebergebener Tag '%s' passt nicht zur "
                          "Versionsquelle '%s'" % (tag_argument, tag))

    print("Versionsquelle:          CHANGELOG.md, Abschnitt Aktuelles Release")
    print("Tag:                     %s" % tag)
    print("Skill-Version:           %s" % skill)
    print("Artefakt:                %s" % artifact)
    print("Versionsgeschichte:      %d Eintraege, zuletzt %s"
          % (len(history), history[-1] if history else "-"))
    if tag_argument is not None:
        print("Uebergebener Tag:        %s" % tag_argument)
    print("Gepruefte Angaben:       %d in CHANGELOG.md, README.md, "
          "index.html, den Workflows und %s" % (checked, EXAMPLE_WORKFLOW))

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: Version und Artefaktname stimmen ueberall mit der "
          "Versionsquelle ueberein.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
