# 블로그

Hugo와 PaperMod 테마로 만든 GitHub Pages 블로그입니다.

## 글 작성

1. `content/posts/글-이름/index.md`를 만듭니다. `hugo new content posts/글-이름/index.md`로 머리말이 포함된 파일을 만들 수 있습니다.
2. 작성한 md 본문을 머리말(`---` 구역) 아래에 붙여넣습니다.
3. 이미지는 같은 폴더에 두고 `![설명](파일명.png)`으로 참조합니다.
4. 게시할 때 `draft: false`로 바꿉니다.

머리말 항목은 `title`, `date`, `description`, `tags`, `draft`입니다. `description`은 검색 결과에 표시되는 문구입니다.

## 미리보기

```powershell
hugo server --buildDrafts
```

http://localhost:1313 에서 확인합니다.

## 배포

`main` 브랜치에 푸시하면 `.github/workflows/pages.yml`이 빌드와 배포를 수행합니다.
저장소 Settings → Pages → Source를 "GitHub Actions"로 설정해야 합니다.

## 검색 등록

`hugo.yaml`의 `params.analytics`에 구글 서치 콘솔과 네이버 서치어드바이저의 인증 값을 넣습니다.
사이트맵 주소는 `/sitemap.xml`입니다.

## 규칙

글 10편을 게시하기 전에는 레이아웃과 스타일을 수정하지 않습니다.
