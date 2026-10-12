# 블로그

Hugo와 Terminal 테마로 만든 GitHub Pages 블로그입니다.

## 글 작성

1. 사이드 프로젝트 글은 `content/projects/글-이름/index.md`에 만듭니다. `hugo new content projects/글-이름/index.md`로 머리말이 포함된 파일을 만들 수 있습니다. 주간 글은 아래 "VISER 주간 보고서 가져오기"로 만듭니다.
2. 작성한 md 본문을 머리말(`---` 구역) 아래에 붙여넣습니다.
3. 이미지는 같은 폴더에 두고 `![설명](파일명.png)`으로 참조합니다.
4. 게시할 때 `draft: false`로 바꿉니다.

머리말 항목은 `title`, `date`, `description`, `tags`, `draft`입니다. `description`은 검색 결과에 표시되는 문구입니다.

## 미리보기

```powershell
hugo server --buildDrafts --disableFastRender
```

http://localhost:1313 에서 확인합니다.

## 배포

`main` 브랜치에 푸시하면 `.github/workflows/pages.yml`이 빌드와 배포를 수행합니다.
저장소 Settings → Pages → Source를 "GitHub Actions"로 설정해야 합니다.

## 검색 등록

`hugo.yaml`의 `params.verification`에 구글 서치 콘솔과 네이버 서치어드바이저의 인증 값을 넣습니다.
사이트맵 주소는 `/sitemap.xml`입니다.

## 규칙

글 10편을 게시하기 전에는 레이아웃과 스타일을 수정하지 않습니다.

## 테마 보완 사항

- `static/style.css`: 한글 글꼴(Noto Sans KR)과 줄 간격을 지정합니다.
- `layouts/partials/extended_head.html`: 글꼴 불러오기와 검색 등록 인증 태그를 출력합니다.
- `layouts/robots.txt`: 사이트맵 주소를 포함합니다.

## VISER 주간 보고서 가져오기

```powershell
python tools/import_weekly.py D:/coding/VISER/dataset/reports/2026-W41.md
```

- 기사마다 글 1편을 `content/news/<주차>-<이름>/`에 초안(`draft: true`)으로 만듭니다. 같은 주차를 다시 실행하면 덮어씁니다.
- 머리말 문단, 항목 ID, 요약 상자의 `숫자:` 줄, 부록은 옮기지 않습니다.
- 그래프(SVG)는 어두운 바탕 색으로 바꿔 복사합니다. 색 대응표는 스크립트의 `SHAPE_COLORS`입니다.
- 원문 사진은 `--photos omit`(기본, 제외) · `link`(원문 링크로 대체) · `keep`(그대로 게시) 중에서 고릅니다.
- 분야 태그(영문 소문자)는 `tools/topics.json`의 낱말 규칙으로 붙입니다. 초안에서 확인하고 틀린 태그는 글의 머리말에서 직접 고칩니다.
