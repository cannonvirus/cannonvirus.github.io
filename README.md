# 블로그

Hugo와 Terminal 테마로 만든 GitHub Pages 블로그입니다.

## 글 작성

1. 사이드 프로젝트 글은 `content/projects/글-이름/index.md`에 만듭니다. `hugo new content projects/글-이름/index.md`로 머리말이 포함된 파일을 만들 수 있습니다. News 글은 아래 "News 글" 절의 방식으로 만듭니다.
2. 작성한 md 본문을 머리말(`---` 구역) 아래에 붙여넣습니다.
3. 이미지는 같은 폴더에 두고 `![설명](파일명.png)`으로 참조합니다.
4. 게시할 때 `draft: false`로 바꿉니다.

머리말 항목은 `title`, `date`, `description`, `tags`, `draft`입니다. `description`은 검색 결과에 표시되는 문구입니다.

개발일지(Projects 구역)와 Weekly 구역 글의 작성 기준(내용, 문체, 제목과 문구, 그림)은 비공개 VISER 저장소의 `docs/writing-guide.md`를 정본으로 따릅니다.

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

- `assets/style.css`: 한글 글꼴(Noto Sans KR)과 줄 간격을 지정합니다. `extended_head.html`이 주소에 내용의 해시를 붙여 실으므로, 고친 내용이 배포 즉시 반영됩니다. `assets/reading.js`도 같습니다.
- `layouts/partials/extended_head.html`: 글꼴 불러오기와 검색 등록 인증 태그를 출력합니다.
- `layouts/robots.txt`: 사이트맵 주소를 포함합니다.
- `layouts/partials/footer.html`: 테마 바닥글의 Hugo와 테마 제작자 문구를 빼고 권리 표기만 출력합니다.
- `hugo.yaml`의 `readingTime: false`: 글 머리의 읽는 시간과 단어 수를 출력하지 않습니다.
- 2026-10-17 개편(분야·연재 분류, 주차별·연재별 목록, 옆 목차·읽기 진행률(`assets/reading.js`), 글꼴 구분, 보고서형 글 `layout: report`, 인쇄 색): 변경 목록과 적용 순서는 `docs/design-20261017.md`에 있습니다.

## News 글 (VISER 주간 보고서)

News 구역의 글은 VISER가 만든다. 이 저장소에서 손으로 고치지 않는다. 고칠 것이 있으면 VISER에 피드백을 주고
다시 만든다. 절차와 규칙은 VISER 저장소의 `docs/weekly.md` "블로그 게시"에 있다.

예외 1회(2026-10-17): 태그 개편으로 News 14편의 머리말 `tags` 줄만 `docs/design-20261017-migrate.py`로 바꿨다.
VISER로 다시 게시하면 체크가 남아 있는 글만 다시 쓰이므로 14편 전체를 한 번에 바꾸려고 이 방법을 썼다(사용자 결정).
본문은 바꾸지 않았다. 이후 태그는 다시 VISER가 붙인다. VISER의 태그 목록을 바꾸기 전에는 News 글을 다시 게시하지 않는다(`docs/design-20261017.md` 2.5절·5절).

```powershell
# VISER 저장소에서 실행한다
uv run python monitor.py    # b 주간 보고서 → 주간 페이지에서 실을 글을 체크 → c 블로그에서 y로 게시
```

- VISER 주간 보고서 페이지에서 블로그에 실을 글을 체크한다. 체크한 글만 이 저장소에 온다.
- 모니터의 `c`가 체크한 글을 보여 주고 `y`를 받으면 `content/news/<주차>-<이름>/`에 쓰고 그 폴더만 커밋·푸시한다.
- 초안 단계는 없다. 체크를 풀어도 게시한 글은 내려가지 않는다.
- 분야 태그는 VISER가 붙인다. 목록은 VISER의 `src/tasks/blog_tags.py`에 있다.
