---
title: "PageIndex: 트리 인덱스 기반 RAG 엔진"
date: 2026-10-05T09:00:00+09:00
description: "PageIndex는 벡터 DB와 청킹 없이 문서의 트리 인덱스를 LLM이 추론으로 탐색하는 RAG 엔진이고, 개발팀은 재무 문서 질의응답 벤치마크 FinanceBench에서 정확도 98.7%를 기록했다고 밝혔다."
tags: ["rag-retrieval"]
source_url: "https://github.com/VectifyAI/PageIndex"
source_newsletter: "AlphaSignal"
draft: false
---

> 이 글은 아래 원문을 우리말로 간추려 정리한 글입니다. 정확한 내용은 원문을 확인하십시오.
>
> 원문: [github.com/VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex)  
> 원문을 소개한 뉴스레터: AlphaSignal

수백 쪽짜리 재무 보고서에서 "2023년 영업이익률은 얼마였나"를 찾을 때, 흔히 쓰는 벡터 검색은 질문과 뜻이 비슷한 문단을 골라 온다. 그런데 비슷한 문단이 곧 필요한 문단은 아니어서, 길고 복잡한 전문 문서에서는 관련이 있어도 표현이 다른 대목을 놓치고 표현만 닮은 대목을 가져오는 일이 생긴다. PageIndex 팀이 공개한 [PageIndex](https://github.com/VectifyAI/PageIndex)는 PDF 문서를 넣으면 목차처럼 생긴 트리 인덱스를 만들어 두고, 질문이 들어오면 LLM이 그 트리를 따라 내려가며 필요한 부분만 읽어 답하는 검색 엔진이다.

```요약
요약: PageIndex는 벡터 DB와 청킹 없이 문서의 트리 인덱스를 LLM이 추론으로 탐색하는 RAG 엔진이고, 개발팀은 재무 문서 질의응답 벤치마크 FinanceBench에서 정확도 98.7%를 기록했다고 밝혔다.
```

```용어
RAG: LLM이 답하기 전에 문서에서 관련 내용을 찾아 와 그것을 근거로 답하게 하는 방식이다.
벡터 검색: 글을 숫자 배열로 바꿔 두고, 질문과 의미가 가까운 문단을 유사도로 골라 오는 검색이다.
청킹: 긴 문서를 검색 단위가 되는 작은 조각으로 잘라 두는 작업이다.
트리 인덱스: 문서를 장, 절, 하위 절처럼 위아래 계층으로 정리한 색인이다. 칸 하나를 노드라고 부른다.
추론 강도: 모델이 답하기 전에 얼마나 깊이 따져 볼지 정하는 설정으로, 이 기사에서는 none, low, medium, high 네 단계다.
```

## 1. 유사도 검색과 트리 탐색의 차이

개발팀이 짚는 문제는 유사도와 관련성이 다르다는 점이다. 검색에 필요한 것은 관련성이고, 관련성을 가리려면 문맥 이해와 여러 단계의 추론이 따라야 한다고 본다.

PageIndex는 두 단계로 움직인다. 먼저 문서마다 트리 인덱스를 만들고, 질문이 오면 LLM이 전문가가 긴 보고서에서 해당 절을 펴 읽듯 트리를 탐색한다. ==벡터 인덱스 자리에 트리를 두고, 유사도 계산 자리에 LLM의 추론을 둔다.== 벡터 검색은 질문 임베딩만 쓰지만 이 방식은 대화 기록과 분야 지식까지 문맥으로 쓰고, 어느 대목을 근거로 삼았는지 추적할 수 있다고 개발팀은 설명한다.

![문서가 트리로 바뀌고 LLM이 트리의 한 경로를 따라가 답에 이르는 과정 (출처: github.com/VectifyAI/PageIndex)](photos/4974de3a5686.webp "문서가 트리로 바뀌고 LLM이 트리의 한 경로를 따라가 답에 이르는 과정 (출처: github.com/VectifyAI/PageIndex)")

## 2. 인덱싱 비용과 시간

트리는 문서마다 한 번만 만들고 이후 질문은 모두 그것을 다시 쓴다. 트리의 뼈대는 LLM 없이 문서 레이아웃에서 뽑아내고 인덱스 모델은 요약과 다듬기만 맡으므로, 기본급 모델을 써도 품질이 떨어지지 않았다고 한다.

`gpt-5.6-luna`를 인덱스 모델로 써서 로컬에서 돌린 결과, 9쪽부터 1,098쪽까지 PDF 9개의 평균 비용은 쪽당 0.0011달러였다. 1,000쪽 교재라면 1달러를 조금 넘는다.

![쪽수가 늘수록 인덱싱 비용이 쪽당 0.0011달러 기준선을 따라 늘어난다 (출처: github.com/VectifyAI/PageIndex)](photos/da139fddccac.webp "쪽수가 늘수록 인덱싱 비용이 쪽당 0.0011달러 기준선을 따라 늘어난다 (출처: github.com/VectifyAI/PageIndex)")

시간도 문서 길이에 따라 예측할 수 있게 늘어난다. 같은 환경에서 9개 문서는 약 13초에서 4.5분 사이에 끝났다.

![같은 문서 9개의 인덱싱 시간도 쪽수에 비례해 늘어난다 (출처: github.com/VectifyAI/PageIndex)](photos/23b39fa263b6.webp "같은 문서 9개의 인덱싱 시간도 쪽수에 비례해 늘어난다 (출처: github.com/VectifyAI/PageIndex)")

## 3. 질문 비용과 정확도

트리를 탐색하는 채팅 모델은 사정이 다르다. 개발팀은 MMLongBench-Doc-V2에서 고른 PDF 34개, 1,945쪽에 걸친 조회 질문 62개로 로컬 모드를 측정했다. OCR은 쓰지 않았고, 답이 모두 본문에 적힌 사실이어서 오답은 검색이나 읽기 실패를 뜻한다.

그래프를 보면 가장 작은 `gpt-5.6-luna`는 추론 강도 high에서 96.8%였고, `gpt-5.6-terra`는 high에서, `gpt-5.6-sol`은 medium과 high에서 100%였다. sol은 none과 low에서도 96.8%였다. ==같은 모델 안에서는 추론 강도를 올려도 비용은 거의 그대로이고 정확도만 올랐다.== 비용 차이는 모델을 바꿀 때 벌어져서, 질문당 평균 비용이 luna는 0.003달러 근처, terra는 0.03달러 근처에 놓였다.

![모델마다 추론 강도 네 단계가 세로로 늘어서고 모델 사이에서 비용이 벌어진다 (출처: github.com/VectifyAI/PageIndex)](photos/b6e5faa29ef1.webp "모델마다 추론 강도 네 단계가 세로로 늘어서고 모델 사이에서 비용이 벌어진다 (출처: github.com/VectifyAI/PageIndex)")

## 4. PDF 통째 입력과의 비용 비교

검색을 쓰지 않으면 질문마다 PDF 전체를 모델에 넘겨야 하고, 그 비용은 문서가 길수록 커진다. PageIndex는 추론이 닿은 노드만 읽으므로 문서 길이에 따라 늘지 않는다.

두 방식이 같은 답을 낸 문서에서 `gpt-5.6-sol`로 프롬프트 캐싱을 빼고 견주면, PDF를 그대로 넣는 쪽이 52쪽에서 2.1배, 85쪽에서 3.4배, 198쪽에서 7.8배, 420쪽에서 16.6배 비쌌다. ==805쪽 문서는 컨텍스트 윈도에 아예 들어가지 않았다.==

![PageIndex 비용을 1로 놓았을 때 PDF를 통째로 넣는 비용이 쪽수에 따라 커진다 (출처: github.com/VectifyAI/PageIndex)](photos/53d22c980359.webp "PageIndex 비용을 1로 놓았을 때 PDF를 통째로 넣는 비용이 쪽수에 따라 커진다 (출처: github.com/VectifyAI/PageIndex)")

## 5. FinanceBench 결과와 클라우드판

개발팀은 재무 문서 질의응답 벤치마크인 FinanceBench에서 98.7%를 기록했다고 밝혔다. 함께 실린 그래프에는 벡터 RAG가 50%로 표시되어 있다. 비교한 벡터 RAG의 구성은 자료에 없고, 전체 평가 결과는 별도 저장소와 블로그 글에 있다.

![FinanceBench 정확도에서 PageIndex 98.7퍼센트와 벡터 RAG 50퍼센트를 견준다 (출처: github.com/VectifyAI/PageIndex)](photos/e1f38a9fff37.webp "FinanceBench 정확도에서 PageIndex 98.7퍼센트와 벡터 RAG 50퍼센트를 견준다 (출처: github.com/VectifyAI/PageIndex)")

오픈소스판은 텍스트 기반 PDF를 로컬에서 처리하고 인용을 쪽 단위로 단다. PageIndex Cloud는 파싱, OCR, 이미지 이해, 인덱스 구축과 저장을 대신 맡아 스캔 문서와 이미지가 많은 문서까지 다루고, 인용은 블록 단위다. 수백만 건 규모의 문서 전체를 파일 단위 트리로 탐색하는 PageIndex File System은 클라우드에서만 제공된다. 설치 명령과 모델 설정 예시는 원문에 정리되어 있다.

## 출처와 작성 방식

- 원문: [github.com/VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex)
- 원문을 소개한 뉴스레터: AlphaSignal
- 그림: 원문에 실린 그림을 인용한 것이며 저작권은 원저작자에게 있습니다. 그림 아래에 출처를 적었습니다.
- 작성 방식: 직접 만든 뉴스 정리 파이프라인(VISER)으로 생성하고 검수한 글입니다. 본문의 수치와 주장은 원문에서 가져온 것입니다.
- 정리 주차: 2026-W40
