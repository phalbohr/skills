import re
import sys
from pathlib import Path

MAX_FINDINGS = 5
VERDICTS = {"ADOPT", "REJECT", "ESCALATE"}
SEVERITIES = {"blocker", "major", "minor"}
FINDING = re.compile(r"^\s*F\d+[a-z]?\s*\|", re.MULTILINE)
SEPARATOR = re.compile(r"^\|[\s|:-]+\|$")


def table_rows(text):
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or SEPARATOR.match(line):
            continue
        cells = [c.strip().strip("`").strip() for c in line.strip("|").split("|")]
        if cells[0].lower() == "id":
            continue
        yield cells


def check(folder):
    problems = []
    if not (folder / "target.md").is_file():
        problems.append("target.md is missing")
    pushes = sorted(folder.glob("r[0-9]-*.md"))
    if not pushes:
        problems.append("no push file r<round>-<method>.md")
    for push in pushes:
        text = push.read_text(errors="ignore")
        section = re.split(r"^##\s*Findings\s*$", text, flags=re.MULTILINE | re.IGNORECASE)
        if len(section) < 2:
            problems.append(f"{push.name}: no '## Findings' section; send 'Return your findings in the shape of the brief.' to the same reader and save its new return verbatim")
            continue
        count = len(FINDING.findall(section[1]))
        if count == 0 and not re.search(r"^\s*No findings\.?\s*$", section[1], re.MULTILINE | re.IGNORECASE):
            problems.append(f"{push.name}: '## Findings' has no 'F<n> |' line and no 'No findings.'; send 'Return your findings in the shape of the brief.' to the same reader and save its new return verbatim")
        if count > MAX_FINDINGS:
            problems.append(f"{push.name}: {count} findings; ask the same reader to keep its {MAX_FINDINGS} worst")
    log = folder / "log.md"
    if not log.is_file():
        problems.append("log.md is missing")
        return problems
    rows = list(table_rows(log.read_text(errors="ignore")))
    if not rows:
        problems.append("log.md: no finding rows")
    for cells in rows:
        if len(cells) < 6:
            problems.append(f"log.md row {cells[0]}: needs 6 cells: ID | Push file | Severity | Verdict | Ground or change | Rebuttal")
            continue
        fid, files, severity, verdict, ground, rebuttal = cells[:6]
        for name in [n.strip().strip("`") for n in files.split(",") if n.strip()]:
            if not (folder / name).is_file():
                problems.append(f"log.md row {fid}: push file {name} does not exist")
        if severity.lower() not in SEVERITIES:
            problems.append(f"log.md row {fid}: severity '{severity}' is not blocker, major or minor")
        if verdict not in VERDICTS:
            problems.append(f"log.md row {fid}: verdict '{verdict}' is not ADOPT, REJECT or ESCALATE")
        if verdict == "REJECT" and not ground:
            problems.append(f"log.md row {fid}: REJECT without a ground")
        if verdict == "REJECT" and severity.lower() in {"blocker", "major"} and not re.search(r"\b(CONCEDE|HOLD)\b", rebuttal):
            problems.append(f"log.md row {fid}: {severity} REJECT has no rebuttal; send it to the same reader and log CONCEDE or HOLD")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check.py /tmp/elicit/<slug>")
    found = check(Path(sys.argv[1]))
    for p in found:
        print("FAIL", p)
    print("OK" if not found else f"{len(found)} problems")
    sys.exit(1 if found else 0)
