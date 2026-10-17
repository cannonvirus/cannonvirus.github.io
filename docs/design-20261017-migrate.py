"""분야 태그 개편(2026-10-17 설계안)의 머리말 변환.

사용: python docs/design-20261017-migrate.py <content 폴더> [--write]

- News 글: tags의 옛 이름을 새 이름으로 바꾼다. 같은 새 이름은 하나로 합치고 앞에서부터 2개까지 남긴다.
- Projects 글: tags의 연재 이름(VISER, game-ai)을 series로 옮기고 tags는 비운다.
- --write가 없으면 바꿀 내용만 출력한다. 머리말 밖의 본문은 읽지도 바꾸지도 않는다.

News 글은 VISER가 다시 게시하면 VISER의 태그로 다시 쓰인다. 이 변환은 VISER의 태그 목록을
같은 대응표로 바꾼 뒤에 한 번만 쓴다(설계안 "적용 순서").
"""
import re
import sys
from pathlib import Path

NEW_TAG = {
    "agent-platform": "agents",
    "multi-agent": "agents",
    "autonomous-research": "agents",
    "agent-eval": "agents",
    "prompt-context": "agents",
    "coding-agent": "coding-agents",
    "agent-skills": "coding-agents",
    "eng-practice": "coding-agents",
    "vlm": "vision",
    "robotics": "vision",
    "image-video-gen": "generative-media",
    "rag-retrieval": "rag",
    "inference-cost": "efficiency",
    "model-serving": "efficiency",
    "model-release": "models",
    "model-training": "models",
}
SERIES = {"VISER": "viser", "game-ai": "boardgame-ai"}
MAX_TAGS = 2

_FRONT = re.compile(r"\A(﻿?---\n)(.*?\n)(---\n)", re.DOTALL)
_TAGS = re.compile(r"^tags:\s*\[(.*)\]\s*$", re.MULTILINE)


def names(raw: str) -> list[str]:
    return [t.strip().strip('"').strip("'") for t in raw.split(",") if t.strip()]


def convert(front: str, section: str) -> str:
    hit = _TAGS.search(front)
    if not hit:
        return front
    old = names(hit.group(1))
    if section == "projects":
        series = [SERIES[t] for t in old if t in SERIES]
        line = 'tags: []\nseries: [' + ", ".join(f'"{s}"' for s in series) + "]"
    else:
        new: list[str] = []
        for t in old:
            t = NEW_TAG.get(t, t)
            if t not in new:
                new.append(t)
        line = "tags: [" + ", ".join(f'"{t}"' for t in new[:MAX_TAGS]) + "]"
    return front[:hit.start()] + line + front[hit.end():]


def main() -> None:
    root = Path(sys.argv[1])
    write = "--write" in sys.argv
    for section in ("news", "projects"):
        for path in sorted((root / section).glob("*/index.md")):
            raw = path.read_bytes()
            eol = "\r\n" if b"\r\n" in raw else "\n"  # 원래 줄 끝을 유지한다.
            text = raw.decode("utf-8").replace("\r\n", "\n")
            m = _FRONT.match(text)
            if not m:
                continue
            front = convert(m.group(2), section)
            if front == m.group(2):
                continue
            before = _TAGS.search(m.group(2)).group(0)
            after = "; ".join(ln for ln in front.splitlines() if ln.startswith(("tags:", "series:")))
            print(f"{section}/{path.parent.name}: {before} -> {after}")
            if write:
                path.write_text(m.group(1) + front + m.group(3) + text[m.end():], encoding="utf-8", newline=eol)


if __name__ == "__main__":
    main()
