"""VISER 주간 보고서(Markdown)를 기사별 블로그 글로 변환한다.

사용 예:
    python tools/import_weekly.py D:/coding/VISER/dataset/reports/2026-W41.md

보고서 파일은 읽기만 한다. 결과는 content/posts/<주차>-<이름>/ 아래에 초안으로 쓴다.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# VISER chart_runner의 밝은 바탕 색을 블로그의 어두운 바탕 색으로 바꾼다.
# ACCENT는 블로그 테마의 강조색(--accent)과 같다. 검증기의 명도 범위(0.48~0.67)보다 밝지만
# 테마와 맞추려고 그대로 쓴다. 색각 이상 구분·대비 등 나머지 항목은 바탕 #211d13 위에서 통과했다.
SURFACE = "#211d13"
SHAPE_COLORS = {
    "#fcfaf6": SURFACE,    # SURFACE
    "#ffffff": "#322c20",  # 칸 바탕
    "#22201d": "#eceae5",  # INK
    "#6f685f": "#a8a194",  # MUTED
    "#b8452f": "#eec35e",  # ACCENT
    "#2f6ea8": "#4a90d9",  # BLUE
    "#b07f14": "#de6a4c",  # GOLD (노랑은 ACCENT가 쓰므로 주황으로 옮긴다)
    "#f3eee7": "#2b261b",  # PALE
    "#e2dbd0": "#453e30",  # LINE
    "#b9b0a4": "#6f685c",  # GRAY
    "#e3edf6": "#1e2b3a",  # COOL
    "#b9cfe4": "#3b5674",  # COOL_EDGE
    "#f6e3dd": "#3a3118",  # WARM
    "#e2b3a6": "#7d6a35",  # WARM_EDGE
}
# 글자의 흰색은 색 칸 위에 놓인 것이므로 어두운 색으로 바꾼다.
TEXT_COLORS = {**SHAPE_COLORS, "#ffffff": "#1a170f"}
# 흰색 테두리는 칸 사이를 띄우는 선이므로 바탕색으로 바꾼다.
STROKE_WHITE = SURFACE

_TAG = re.compile(r"<(\w+)\b[^>]*>")
_PROP = re.compile(r"\b(fill|stroke|stop-color):\s*(#[0-9a-fA-F]{6})\b")
_ITEM = re.compile(r"^## 1-(\d+)\. (.+)$", re.M)
_META = re.compile(r"^(\d{8}-\d+) · (.+?) · \[[^\]]*\]\(([^)]+)\)\s*(.*)$")
_IMAGE = re.compile(r'^!\[(.*)\]\((photos/[^)\s]+)(?:\s+"[^"]*")?\)\s*$')
_CREDIT = re.compile(r"\s*\(출처: [^)]*\)\s*$")
TOPICS = ROOT / "tools" / "topics.json"
TOPIC_MIN, TOPIC_MAX = 5, 3


def topics_for(title: str, text: str) -> list[str]:
    """분야 태그를 낱말 규칙으로 정한다. VISER의 관심 분류(#일하는 방법 등)는 쓰지 않는다."""
    rules = json.loads(TOPICS.read_text(encoding="utf-8"))
    scored = []
    for topic, words in rules.items():
        if topic.startswith("_"):
            continue
        patterns = [re.compile(rf"(?<![A-Za-z]){re.escape(w)}(?![A-Za-z])", re.I) for w in words]
        count = sum(len(p.findall(text)) for p in patterns)
        in_title = any(p.search(title) for p in patterns)
        if in_title or count >= TOPIC_MIN:
            scored.append((not in_title, -count, topic))
    return [topic for _, _, topic in sorted(scored)[:TOPIC_MAX]]


def recolor_svg(svg: str, unknown: set[str]) -> str:
    def tag(match: re.Match) -> str:
        colors = TEXT_COLORS if match.group(1) == "text" else SHAPE_COLORS

        def prop(m: re.Match) -> str:
            name, color = m.group(1), m.group(2).lower()
            if name == "stroke" and color == "#ffffff":
                return f"{name}: {STROKE_WHITE}"
            if color not in colors:
                unknown.add(color)
                return m.group(0)
            return f"{name}: {colors[color]}"

        return _PROP.sub(prop, match.group(0))

    return _TAG.sub(tag, svg)


def week_date(week: str) -> dt.date:
    """주차가 끝난 다음 날(월요일)을 게시일로 쓴다."""
    year, number = week.split("-W")
    return dt.date.fromisocalendar(int(year), int(number), 7) + dt.timedelta(days=1)


def slug_for(week: str, url: str) -> str:
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    if parsed.netloc.endswith("github.com"):
        name = "-".join(parts[:2])
    else:
        name = parts[-1] if parts else parsed.netloc
    name = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{week.lower()}-{name}"[:80].rstrip("-")


def display_url(url: str) -> str:
    parsed = urlparse(url)
    return (parsed.netloc.removeprefix("www.") + parsed.path).rstrip("/")


def yaml_str(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert_item(week, title, block, report_dir, out_root, photos, unknown):
    lines = block.strip("\n").split("\n")
    meta = _META.match(lines[0])
    if not meta:
        raise ValueError(f"항목 머리줄을 읽지 못했습니다: {lines[0][:80]}")
    _id, newsletter, url, _viser_topic = meta.groups()

    post_dir = out_root / slug_for(week, url)
    if post_dir.exists():
        shutil.rmtree(post_dir)
    (post_dir / "photos").mkdir(parents=True)

    body, summary, fence, charts, dropped = [], "", None, 0, 0
    for line in lines[1:]:
        if line.startswith("```"):
            fence = None if fence else line[3:].strip()
            body.append(line)
            continue
        if fence == "요약":
            if line.startswith("숫자:"):
                continue  # VISER 첫 화면 카드용 자료다.
            if line.startswith("요약:"):
                summary = line[3:].strip()
        if fence is None and line.startswith("###"):
            line = line[1:]  # 글 하나가 한 페이지이므로 소제목을 한 단계 올린다.
        image = _IMAGE.match(line) if fence is None else None
        if image:
            caption, src = image.groups()
            source = report_dir / src
            if src.endswith(".svg"):
                svg = recolor_svg(source.read_text(encoding="utf-8"), unknown)
                (post_dir / src).write_text(svg, encoding="utf-8", newline="\n")
                charts += 1
            elif photos == "keep":
                shutil.copyfile(source, post_dir / src)
            elif photos == "link":
                caption = _CREDIT.sub("", caption)
                body.append(f"*원문 그림: [{caption}]({url})*")
                dropped += 1
                continue
            else:
                dropped += 1
                if body and body[-1] == "":
                    body.pop()
                continue
            line = f"![{caption}]({src})"
        body.append(line)

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip()
    shown = display_url(url)
    notice = (
        f"> 이 글은 아래 원문을 우리말로 간추려 정리한 글입니다. 정확한 내용은 원문을 확인하십시오.\n"
        f">\n"
        f"> 원문: [{shown}]({url})  \n"
        f"> 원문을 소개한 뉴스레터: {newsletter}"
    )
    footer = [
        "## 출처와 작성 방식",
        "",
        f"- 원문: [{shown}]({url})",
        f"- 원문을 소개한 뉴스레터: {newsletter}",
    ]
    if charts:
        footer.append("- 그래프: 원문에 적힌 값으로 새로 그린 그림입니다. 원문에 실린 그림이 아닙니다.")
    if photos == "keep" and dropped == 0:
        footer.append("- 사진: 원문에 실린 그림이며 저작권은 원저작자에게 있습니다. 그림마다 출처를 적었습니다.")
    footer += [
        "- 작성 방식: 직접 만든 뉴스 정리 파이프라인(VISER)으로 생성하고 검수한 글입니다. "
        "본문의 수치와 주장은 원문에서 가져온 것입니다.",
        f"- 정리 주차: {week}",
    ]
    front = [
        "---",
        f"title: {yaml_str(title)}",
        f"date: {week_date(week).isoformat()}T09:00:00+09:00",
        f"description: {yaml_str(summary)}",
        "tags: [" + ", ".join(yaml_str(t) for t in [*topics_for(title, text), week]) + "]",
        f"source_url: {yaml_str(url)}",
        f"source_newsletter: {yaml_str(newsletter)}",
        "draft: true",
        "---",
    ]
    content = "\n".join(front) + "\n\n" + notice + "\n\n" + text + "\n\n" + "\n".join(footer) + "\n"
    (post_dir / "index.md").write_text(content, encoding="utf-8", newline="\n")
    if not any((post_dir / "photos").iterdir()):
        (post_dir / "photos").rmdir()
    return post_dir, charts, dropped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("report", type=Path, help="VISER 주간 보고서 Markdown 경로")
    parser.add_argument("--out", type=Path, default=ROOT / "content" / "posts")
    parser.add_argument(
        "--photos",
        choices=["omit", "link", "keep"],
        default="omit",
        help="원문 사진 처리: omit 제외(기본), link 원문 링크로 대체, keep 그대로 게시",
    )
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    week = re.search(r"\d{4}-W\d{2}", args.report.name)
    if not week:
        parser.error("파일 이름에서 주차(YYYY-Www)를 찾지 못했습니다.")
    text = args.report.read_text(encoding="utf-8")
    text = re.split(r"^# 부록", text, maxsplit=1, flags=re.M)[0]  # 부록은 내부 후보 목록이다.
    text = re.sub(r"\n---\s*$", "\n", text.rstrip() + "\n")

    marks = list(_ITEM.finditer(text))
    if not marks:
        parser.error("'## 1-N. 제목' 형식의 항목을 찾지 못했습니다.")
    unknown: set[str] = set()
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        post_dir, charts, dropped = convert_item(
            week.group(0), mark.group(2).strip(), text[mark.end():end],
            args.report.parent, args.out, args.photos, unknown,
        )
        print(f"{post_dir.relative_to(ROOT)}: 그래프 {charts}장, 원문 사진 {dropped}장 {'링크 대체' if args.photos == 'link' else '제외'}"
              if dropped else f"{post_dir.relative_to(ROOT)}: 그래프 {charts}장")
    if unknown:
        print("색상표에 없는 색이 있어 그대로 두었습니다: " + ", ".join(sorted(unknown)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
