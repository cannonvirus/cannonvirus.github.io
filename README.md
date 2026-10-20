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

사이트 검색은 `hugo server`에서는 동작하지 않습니다(색인이 없음). 검색까지 확인하려면 빌드한 뒤 색인을 만들어 띄웁니다.

```powershell
hugo; npx -y pagefind@1.5.2 --serve
```

## 배포

`main` 브랜치에 푸시하면 `.github/workflows/pages.yml`이 빌드, 검색 색인(Pagefind, 설정은 `pagefind.yml`), 배포를 수행합니다.
같은 워크플로가 매일 09:05 KST(00:05 UTC)에도 실행됩니다. 게시일이 미래인 글은 Hugo가 빌드에서 빼므로,
주간 글(게시일: 주차 다음 월요일 09시)처럼 미리 올린 글이 푸시 없이도 그날 공개됩니다. 예약 실행은 GitHub 부하에 따라 늦게 시작될 수 있습니다.
저장소 Settings → Pages → Source를 "GitHub Actions"로 설정해야 합니다.

## 검색 등록

`hugo.yaml`의 `params.verification`에 구글 서치 콘솔의 인증 값을 넣습니다. 네이버 서치어드바이저는 등록하지 않습니다(2026-10-20 사용자 결정).
사이트맵 주소는 `/sitemap.xml`입니다.

배포 워크플로는 배포가 끝나면 새로 생겼거나 수정일이 바뀐 주소를 IndexNow(Bing·네이버 등)에 알립니다(`indexnow` 작업).
공개된 사이트맵과 새로 만든 사이트맵을 비교해 고르고, 바뀐 것이 없으면 건너뜁니다. 키 파일은 `static/<키>.txt`이고
키를 바꾸면 파일 이름·내용과 워크플로의 `INDEXNOW_KEY`를 함께 바꿉니다. 구글은 IndexNow를 쓰지 않아 사이트맵으로 찾습니다.

## 방문 통계

GoatCounter를 씁니다. 가입할 때 정한 사이트 코드를 `hugo.yaml`의 `params.goatcounter`에 넣으면 배포용 빌드에만 스크립트가 실립니다(`layouts/partials/analytics.html`). 비어 있으면 싣지 않습니다. 통계는 `https://<코드>.goatcounter.com`에서 봅니다.

## 테마 보완 사항

- `assets/style.css`: 글꼴(본문·글 제목은 Pretendard, 메뉴·날짜·절 제목·코드는 Fira Code와 Nanum Gothic Coding)과 줄 간격을 지정합니다. 맨 위에 사이트 글꼴(CV Sans·CV Coding)의 정의가 있습니다. `extended_head.html`이 주소에 내용의 해시를 붙여 실으므로, 고친 내용이 배포 즉시 반영됩니다. `assets/reading.js`도 같습니다.
- `layouts/partials/extended_head.html`: 본문 글꼴 미리 받기와 검색 등록 인증 태그를 출력합니다.
- 글꼴(2026-10-20): Pretendard와 Nanum Gothic Coding을 CDN에서 받지 않고, 사이트에 쓰인 글자만 남긴 파일 다섯 개(`/fonts/site/`)를 이 사이트에서 보냅니다. CDN은 글자를 조각내 보내 글 한 편에 글꼴 요청 52개, 약 800KB였고, 바꾼 뒤에는 6개, 약 400KB이며 다음 페이지부터는 받지 않습니다. 배포 워크플로가 빌드와 검색 색인 뒤에 `tools/subset_fonts.py`로 다시 만들어 새 글의 글자도 들어갑니다. 원본은 `assets/fonts/`입니다. 두 글꼴은 이름이 예약되어 있어(SIL OFL 1.1 Reserved Font Name) 덜어 낸 파일은 CV Sans(Pretendard)·CV Coding(Nanum Gothic Coding)이라는 이름으로 부릅니다. `static/fonts/site/`는 로컬 미리보기용 기준본이라, 미리보기에서 새 글의 처음 나온 글자만 다른 글꼴로 보일 수 있습니다. 기준본을 새로 만들려면 `hugo -d <폴더>` 뒤에 `python -X utf8 tools/subset_fonts.py <폴더> static/fonts/site`를 실행합니다(fonttools, brotli 필요).
- `layouts/robots.txt`: 사이트맵 주소를 포함합니다.
- `layouts/partials/footer.html`: 테마 바닥글의 Hugo와 테마 제작자 문구를 빼고 권리 표기와 About·RSS·GitHub 링크만 출력합니다. 위쪽 메뉴의 마지막 항목은 GitHub 대신 About입니다(2026-10-20).
- `layouts/partials/head.html`: 테마의 head.html을 덮어써 공유 이미지를 글마다 만든 그림으로 바꾸고, 트위터 카드를 큰 그림형으로 합니다. 테마 CSS 13개는 한 파일(`css/theme.css`)로 묶어 싣습니다.
- About 페이지: `content/about.md`. 글 목록·RSS·사이트맵에는 넣지 않고 바닥글에서 연결합니다.
- `layouts/partials/og-image.html`: 글별 공유 이미지(1200×630)를 빌드할 때 만듭니다. 바탕은 `assets/og-base.png`, 글꼴은 `assets/fonts/`(SIL Open Font License 1.1, 라이선스 파일 동봉)입니다.
- `layouts/_default/_markup/render-image.html`: 그림에 가로·세로 크기를 적습니다. PNG는 무손실 webp로, JPG는 손실 webp(q85)로 바꾸고 긴 변을 1600px 이하로 줄입니다. 이미 webp인 그림은 다시 압축하지 않습니다. 움직이는 그림은 GIF 대신 무손실 애니메이션 webp로 넣습니다(빌드 때 GIF를 바꾸면 메모리가 부족합니다).
- 사이트 검색: `content/search.md`, `layouts/_default/search.html`. 색인 대상은 글 본문(`data-pagefind-body`)이고 목차·연재 목록·관련 글은 뺍니다.
- `hugo.yaml`의 `readingTime: false`: 글 머리의 읽는 시간과 단어 수를 출력하지 않습니다.
- 연재 페이지(`/series/<이름>/`, `layouts/_default/term.html`): 글을 최신순으로 보이고, 목록 위에 가장 오래된 글(1회)로 가는 "첫 회 읽기" 단추를 둡니다(2026-10-19). Projects 목록(`list-projects.html`)의 연재별 묶음과 글 끝 연재 목록(`series-nav.html`)도 최신순이며, 목록 번호는 `reversed`로 회차와 같게 둡니다.
- 연재 이전·다음 회(2026-10-20): 연재 글은 글 머리 날짜 옆에 "연재 N편 중 N회"를 적고, 글 끝 연재 목록 위에 같은 연재 기준 "← 이전 회 / 다음 회 →" 버튼을 둡니다(`series-pos.html`, `series-nav.html`). 테마의 이전/다음 글은 구역(Projects) 기준이라 다른 연재로 넘어가므로 연재 글에서는 빼고, 연재가 아닌 글에만 남깁니다.
- 그림 확대(2026-10-20, `assets/zoom.js`): 넓은 화면(1,100px 이상, 마우스)에서 띄우면 1.25배 넘게 커지는 그림에만 돋보기 커서를 달고, 누르면 화면에 맞춰 띄웁니다. 원본보다 크게 늘리지 않습니다. 아무 데나 누르기, Esc, 뒤로 가기로 닫힙니다. 모바일에서는 띄워도 커지지 않고 두 손가락 확대가 이미 되므로 동작하지 않습니다.
- 표(2026-10-20): Projects 글의 표는 그림으로 그리지 않고 마크다운 표로 씁니다. 그림으로 넣은 표는 모바일에서 글자가 9px 안팎으로 작아졌고 검색·복사가 되지 않았습니다. 표 아래 `{caption="제목" pick="3"}`처럼 열 번호를 적으면 그 열(고른 쪽)을 강조합니다(`render-table.html`). 표 글자는 685px 이상 화면에서 16px, 그보다 좁은 화면에서 15.2px입니다.
- 목차·용어 상자 접기(2026-10-20): 본문 위 목차(`toc-inline.html`, 옆 목차가 없는 1,100px 미만 화면)는 접어 두고, 용어 상자(`render-codeblock-용어.html`)는 685px 미만 화면에서만 접습니다(`fold-init.html`). 펼쳐 두면 모바일에서 첫 절 제목이 화면 2.4장 아래에 있었습니다(접으면 1.5장). 인쇄할 때는 `reading.js`가 모두 펼칩니다.
- 목록 제목(2026-10-20): 첫 화면·News·Projects 목록의 글 제목은 Pretendard로 쓰고 밑줄은 가리킬 때만 긋습니다.
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
