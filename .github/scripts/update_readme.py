#!/usr/bin/env python3
"""Regenerates the progress section of README.md from problems/."""
import datetime as dt
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROBLEMS_DIR = ROOT / "problems"
README = ROOT / "README.md"

WEEKLY_GOAL = 15
START, END = "<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->"
FILE_RE = re.compile(r"^problem0*(\d+)\.([A-Za-z0-9]+)$")

LANGUAGES = {
    "py": "Python", "rs": "Rust", "cpp": "C++", "cc": "C++", "c": "C",
    "java": "Java", "js": "JavaScript", "ts": "TypeScript", "go": "Go",
    "kt": "Kotlin", "swift": "Swift", "rb": "Ruby", "cs": "C#",
    "scala": "Scala", "sql": "SQL",
}

ROADMAP = [
    ("Sliding Window", [3, 76, 209, 424, 567, 904]),
    ("Two Pointers", [11, 15, 16, 18, 42, 167]),
    ("Fast/Slow Pointers", [141, 142, 19, 876, 160, 234]),
    ("Binary Search on Sorted Data", [33, 34, 35, 153, 162, 704]),
    ("Binary Search on Answer", [875, 1011, 410, 774, 1283, 1482]),
    ("Hashing / Frequency Maps", [1, 49, 128, 217, 242, 347]),
    ("Prefix Sum", [303, 560, 724, 930, 974, 523]),
    ("Difference Array", [370, 1094, 1109, 1893, 1943, 2381]),
    ("Monotonic Stack", [739, 496, 503, 84, 85, 901]),
    ("Monotonic Queue / Deque", [239, 862, 1425, 1438, 1499, 1696]),
    ("Heap / Top K", [215, 347, 692, 703, 973, 1046]),
    ("Intervals", [56, 57, 252, 253, 435, 452]),
    ("Greedy", [45, 55, 406, 621, 763, 134]),
    ("Linked List Manipulation", [21, 23, 24, 25, 92, 138]),
    ("Tree DFS", [104, 112, 113, 543, 124, 226]),
    ("Tree BFS", [102, 103, 199, 515, 637, 116]),
    ("BST", [98, 99, 230, 235, 450, 700]),
    ("Backtracking Basics", [46, 47, 77, 78, 90, 39]),
    ("Backtracking with Constraints", [40, 17, 79, 131, 51, 52]),
    ("Graph BFS / DFS", [200, 695, 733, 994, 1091, 1254]),
]


def commit_dates() -> dict[str, dt.date]:
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--name-only", "--format=@%as", "--", "problems"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith("@"):
            current = dt.date.fromisoformat(line[1:])
        elif line.strip() and current:
            dates[Path(line).name] = current
    return dates


def week_start(d: dt.date) -> dt.date:
    return d - dt.timedelta(days=d.weekday())


def bar(done: int, total: int, width: int = 15) -> str:
    filled = min(width, round(width * done / total)) if total else 0
    return "█" * filled + "░" * (width - filled)


def build() -> str:
    today = dt.date.today()
    dates = commit_dates()

    solved = {}
    langs = defaultdict(set)
    lang_count = Counter()
    for f in sorted(PROBLEMS_DIR.glob("problem*")):
        m = FILE_RE.match(f.name)
        if not m:
            continue
        num, ext = int(m.group(1)), m.group(2).lower()
        d = dates.get(f.name, today)
        solved[num] = min(d, solved.get(num, d))
        langs[num].add((ext, f.name))
        lang_count[LANGUAGES.get(ext, ext)] += 1

    if not solved:
        return "_No problems solved yet._"

    per_week = Counter(week_start(d) for d in solved.values())
    this_week = week_start(today)
    weeks, w = [], min(per_week)
    while w <= this_week:
        weeks.append(w)
        w += dt.timedelta(weeks=1)

    streak = 0
    for w in reversed(weeks):
        if per_week[w] >= WEEKLY_GOAL:
            streak += 1
        elif w != this_week:
            break

    done_now = per_week[this_week]
    lines = [
        f"**{len(solved)}** problems solved · **{sum(lang_count.values())}** solutions · "
        f"**{streak}**-week goal streak",
        "",
        f"**This week:** `{bar(done_now, WEEKLY_GOAL)}` {done_now}/{WEEKLY_GOAL}",
        "",
        "### Languages",
        "",
        "| Language | Solutions |",
        "|---|---:|",
        *[f"| {name} | {n} |" for name, n in lang_count.most_common()],
        "",
        "### Weekly log",
        "",
        "| Week of | Solved | Goal |",
        "|---|---:|:---:|",
    ]
    for w in reversed(weeks):
        n = per_week[w]
        status = "✅" if n >= WEEKLY_GOAL else ("⏳" if w == this_week else "❌")
        lines.append(f"| {w:%b %d, %Y} | {n} | {status} |")

    lines += ["", "### Roadmap", "", "| Pattern | Progress | Problems |", "|---|:---:|---|"]
    for name, nums in ROADMAP:
        done = sum(n in solved for n in nums)
        cells = ", ".join(f"**{n}** ✓" if n in solved else str(n) for n in nums)
        mark = " ✅" if done == len(nums) else ""
        lines.append(f"| {name} | {done}/{len(nums)}{mark} | {cells} |")

    lines += ["", "### Solved", "", "| # | Solutions | Date |", "|---:|---|---|"]
    for num in sorted(solved, key=lambda n: (solved[n], n), reverse=True):
        links = " · ".join(
            f"[{LANGUAGES.get(ext, ext)}](problems/{name})" for ext, name in sorted(langs[num])
        )
        lines.append(f"| {num} | {links} | {solved[num]:%b %d} |")

    return "\n".join(lines)


def main() -> None:
    text = README.read_text(encoding="utf-8") if README.exists() else "# LeetCode\n"
    block = f"{START}\n{build()}\n{END}"
    if START in text and END in text:
        before, rest = text.split(START, 1)
        text = before + block + rest.split(END, 1)[1]
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
