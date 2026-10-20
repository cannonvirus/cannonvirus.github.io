"""사이트 글꼴을 쓰인 글자만 남겨 만든다(2026-10-20 사용자 결정).

Pretendard(본문·글 제목)와 Nanum Gothic Coding(고정폭 자리의 한글)을 CDN에서 받으면 글 한 편에 글꼴 조각 52개, 약 800KB를
받았다. 빌드한 페이지에 나오는 글자만 남긴 파일 다섯 개를 이 사이트에서 보내면 한 번 받은 파일로 사이트 전체를 그린다.

    python tools/subset_fonts.py <빌드한 사이트 폴더> <글꼴을 쓸 폴더>

- 배포 워크플로(pages.yml)가 빌드와 검색 색인 뒤에 public/fonts/site/에 다시 만든다. 새 글에 처음 나온 글자도 들어간다.
- static/fonts/site/는 로컬 미리보기용 기준본이다. 글꼴 설정을 바꿨을 때만 다시 만들어 커밋한다.
- 원본은 assets/fonts/에 있다(SIL Open Font License 1.1). Pretendard 1.3.9, Nanum Gothic Coding 2.000, Fira Code 5.2.
- 두 글꼴 모두 이름이 예약되어 있다(Reserved Font Name: Pretendard, Nanum…). 글자를 덜어 낸 파일은 OFL의 수정본이라
  같은 이름을 쓸 수 없어, 글꼴 안의 이름을 CV Sans·CV Coding으로 바꾼다. CSS에서도 이 이름으로 부른다.
  저작권 표기와 라이선스(name 표의 0·13·14번)는 그대로 둔다.
- 선 문자(├── 등, U+2500~257F)는 Fira Code에서 따로 뽑는다. 테마의 Fira Code에는 이 글자가 없어 Nanum Gothic Coding의
  넓은 선 문자로 그려졌고, 코드 상자의 폴더 구조에서 오른쪽 설명 줄이 어긋났다. Fira Code는 이름이 예약되어 있지 않아
  CSS에서 테마와 같은 "Fira Code" 이름에 글자 범위만 더한다.
"""
import pathlib
import sys

from fontTools import subset

FONTS = pathlib.Path(__file__).resolve().parent.parent / "assets" / "fonts"

# (원본, 만들 파일, 새 이름, 굵기 이름, 고정폭 한글용인지)
JOBS = [
    ("Pretendard-Regular.woff2", "cv-sans-400.woff2", "CV Sans", "Regular", False),
    ("Pretendard-SemiBold.woff2", "cv-sans-600.woff2", "CV Sans", "SemiBold", False),
    ("Pretendard-Bold.ttf", "cv-sans-700.woff2", "CV Sans", "Bold", False),
    ("NanumGothicCoding-Regular.ttf", "cv-coding-400.woff2", "CV Coding", "Regular", True),
    ("NanumGothicCoding-Bold.ttf", "cv-coding-700.woff2", "CV Coding", "Bold", True),
]

# 페이지에 없어도 넣는 글자: 기본 라틴·라틴-1·일반 문장 부호. 검색창에 치는 영문과 숫자도 같은 글꼴로 보인다.
BASE = "U+0020-007E,U+00A0-00FF,U+2000-206F"


def site_chars(site: pathlib.Path) -> set[str]:
    """페이지 HTML의 모든 글자. 태그와 스크립트까지 읽는다(대체 문구, 검색 화면의 한글 문구가 그 안에 있다)."""
    chars: set[str] = set()
    for page in site.rglob("*.html"):
        chars |= set(page.read_text(encoding="utf-8", errors="ignore"))
    # 검색 화면이 쓰는 Pagefind 기본 한국어 문구("검색 중" 등). 다른 언어 문구는 한글만 골라 빼고 읽지 않는다.
    ui = site / "pagefind" / "pagefind-ui.js"
    if ui.exists():
        chars |= {c for c in ui.read_text(encoding="utf-8", errors="ignore") if "가" <= c <= "힣"}
    return {c for c in chars if c.isprintable() and not c.isspace()}


def rename(font, family: str, style: str, origin: str) -> None:
    """예약된 이름이 남지 않게 글꼴 이름(1·3·4·6·16·17번)을 바꾸고, 원본을 설명(10번)에 적는다."""
    full = f"{family} {style}"
    names = {1: family, 2: style, 3: f"{full}; subset of {origin}", 4: full, 6: full.replace(" ", ""), 16: family, 17: style}
    table = font["name"]
    table.names = [r for r in table.names if r.nameID not in (*names, 10, 18, 21, 22)]
    for nid, value in names.items():
        table.setName(value, nid, 3, 1, 0x409)
    table.setName(f"Subset of {origin} for cannonvirus.github.io (SIL OFL 1.1)", 10, 3, 1, 0x409)
    if "CFF " in font:
        font["CFF "].cff.fontNames = [full.replace(" ", "")]


# 선 문자. 페이지에 없어도 범위 전체를 넣는다(글자 128개, 몇 KB).
BOX = "U+2500-257F"


def main() -> None:
    site, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    chars = site_chars(site)
    # 고정폭 자리의 ASCII는 테마의 Fira Code가 그리므로 Nanum Gothic Coding에는 그 밖의 글자만 넣는다.
    # 선 문자는 Fira Code가 그리므로 뺀다.
    wide = "".join(sorted(c for c in chars if ord(c) > 0x7E and not 0x2500 <= ord(c) <= 0x257F))
    for src, dst, family, style, mono in JOBS:
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]  # 기본값은 0~6번만 남겨 라이선스(13·14번)가 빠진다
        opts.name_languages = ["*"]
        opts.hinting = not mono  # Nanum Gothic Coding의 힌팅 정보가 파일 크기의 절반을 넘는다. 빼도 화면 차이가 없었다
        font = subset.load_font(str(FONTS / src), opts)
        sub = subset.Subsetter(opts)
        if mono:
            sub.populate(text=wide)
        else:
            sub.populate(text="".join(chars), unicodes=subset.parse_unicodes(BASE))
        sub.subset(font)
        rename(font, family, style, src.split("-")[0] + " " + font["name"].getDebugName(5))
        subset.save_font(font, str(out / dst), opts)
        print(f"{dst}: {(out / dst).stat().st_size // 1024}KB")
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    font = subset.load_font(str(FONTS / "FiraCode-Regular.ttf"), opts)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=subset.parse_unicodes(BOX))
    sub.subset(font)
    subset.save_font(font, str(out / "fira-code-box.woff2"), opts)
    print(f"fira-code-box.woff2: {(out / 'fira-code-box.woff2').stat().st_size // 1024}KB")
    hangul = sum("가" <= c <= "힣" for c in chars)
    print(f"글자 {len(chars)}개(한글 {hangul}자)")


if __name__ == "__main__":
    main()
