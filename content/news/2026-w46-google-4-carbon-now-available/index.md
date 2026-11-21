---
title: "Gemini 4 Carbon: 구글의 최상위 프런티어 모델"
date: 2026-11-16T09:00:00+09:00
description: "구글이 Gemini 4 Argon보다 더 많은 토큰을 써서 깊이 추론하는 Gemini 4 Carbon을 개발자, 기업, 과학자, 일반 사용자에게 공개했다."
tags: ["models", "agents"]
week: "2026-W46"
source_url: "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/"
source_newsletter: "TLDR"
draft: false
---

> 이 글은 아래 원문을 우리말로 간추려 정리한 글입니다. 정확한 내용은 원문을 확인하십시오.
>
> 원문: [blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/)  
> 원문을 소개한 뉴스레터: TLDR

[Gemini 4 Carbon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/)은 구글이 내놓은 가장 강력한 모델로, 복잡한 코딩과 보안 분석, 과학 연구처럼 오래 걸리는 에이전트 작업을 맡기면 깊은 추론과 검증을 거친 결과를 돌려준다. 개발자와 기업, 과학자, 보안 방어팀, 일반 소비자가 API와 Gemini 앱 등을 통해 쓴다.

```요약
요약: 구글이 Gemini 4 Argon보다 더 많은 토큰을 써서 깊이 추론하는 Gemini 4 Carbon을 개발자, 기업, 과학자, 일반 사용자에게 공개했다.
```

```용어
페어윈드 프로그램(Fairwind Program): 구글이 사이버보안 방어팀에 Carbon의 보안 특화 버전을 먼저 제공하는 접근 프로그램이다.
/swarm: 구글 안티그래비티(Antigravity)에서 한 번의 지시를 여러 에이전트로 이뤄진 팀 작업으로 바꿔 주는 기능이다.
간접 프롬프트 주입(indirect prompt injection): 모델이 읽는 문서나 웹 콘텐츠에 숨겨 둔 명령으로 모델의 행동을 조종하려는 공격이다.
형식 검증(formal verification): 코드가 정해진 성질을 만족함을 수학적 증명으로 확인하는 방법이다.
원격 상동체(remote homolog): 서열 유사도는 낮지만 진화적으로 관련된 단백질로, 구조 예측에 쓸 정보를 늘려 준다.
```

## 1. 공개 범위와 위치: Argon과 나란히 놓인 상위 모델

구글은 Carbon을 개발자와 기업, 과학자, 일반 소비자에게 공개했다. 2주 전에는 페어윈드 프로그램을 통해 사이버보안 방어팀에 먼저 제공한 바 있다. Carbon은 사이버보안과 장시간 에이전트 작업에서 최고 수준의 성능을 내는 모델이다.

구글은 Argon이 대부분의 소프트웨어 개발과 지식 업무에 여전히 적합하다고 설명한다. Carbon은 여러 단계의 복잡한 코딩과 디버깅, 개방형 과학 연구처럼 모델의 한계를 시험하는 작업을 위한 모델이며, Argon보다 토큰을 더 쓰면서 폭넓게 탐색하고 깊게 추론하고 검증을 반복한다.

API는 Google AI Studio와 기업용 Gemini에서 모든 유료 개발자와 기업에 열려 있고, 가격은 Argon과 같은 도입 가격인 입력 100만 토큰당 2달러, 출력 100만 토큰당 10달러다. Google AI Ultra 구독자에게는 안티그래비티, Gemini 앱, 검색 AI 모드로 순차 제공된다.

![Gemini 4 Carbon 공개 대표 이미지 (출처: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available)](photos/ee6a2be69f2a.jpg "Gemini 4 Carbon 공개 대표 이미지 (출처: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available)")

## 2. 지식 업무와 코딩: 비용을 낮춘 벤치마크 성과

구글은 독립 벤치마크에서 Carbon이 CursorBench 4.0, 퍼플렉시티의 WANDR, 재피어의 AutomationBench에서 1위라고 밝혔다. 다음으로 좋은 외부 모델보다 작업당 비용은 2배 넘게 낮다.

법률, 금융, 기업 운영 분야에서는 시각 이해와 추론, 철저한 검색을 결합해 조밀한 문서 묶음에서 근거 있는 통찰을 뽑고, 엄격한 스키마와 서식에 맞춰 스프레드시트와 발표 자료, 보고서를 만든다. 구글은 차트와 도면, 표가 든 문서를 에이전트가 다루는 능력을 재려고 Artificial Analysis와 멀티모달 지식 에이전트(MKA) 벤치마크를 새로 만들었는데, 여기서 Carbon은 2위이면서 최상위 모델보다 평균 작업 비용이 6배 넘게 낮다. 사내 사전 평가에서는 Hebbia의 금융 에이전트 평가에서 가장 좋은 모델과 같은 성능을 냈고, Balyasny Asset Management의 종합 금융 지능 벤치마크에서는 23개 프런티어 모델 구성 가운데 1위였다.

코딩에서는 다중 패키지 이전, 서브시스템을 가로지르는 근본 원인 조사, 대규모 구조 재설계처럼 여러 에이전트의 협업이 필요한 작업에 강하다. 웹 앱을 만들 때는 빌드와 검증을 반복하고 오류에서 회복하며, 코드와 렌더링된 화면을 모두 확인한다. 구글은 이 개선이 3D 게임 개발과 크리에이티브 코딩에도 이어진다고 설명한다.

구글은 안티그래비티에서 /swarm을 미리보기로 내놓았다. 프롬프트 하나가 실시간으로 추적할 수 있는 에이전트 팀으로 바뀌며, 아키텍처 설계, 조율, 감사처럼 깊은 추론이 필요한 역할에는 Carbon을 두고 병렬의 격리된 작업 공간에서는 더 빠르고 가벼운 모델을 짝지을 수 있다. 모든 변경을 시험하는 적대적 검증 에이전트도 함께 쓴다.

## 3. 사이버보안: 취약점 발견부터 패치까지

구글은 보안 특화 버전인 Carbon for cyber가 지금까지 가장 강한 보안 능력을 갖췄다고 밝힌다. 페어윈드 프로그램으로 접근할 때 취약점 발견(SEC-bench Pro), 악용(ExploitGym), 패치(CWE-bench v1) 벤치마크에서 앞선다. 소프트웨어를 점검하고 결함이 시스템을 가로질러 연쇄되는 경로를 추적하며, 검증된 근본 원인 패치를 만든다.

구글 내부 벤치마크 기준으로, 스캔과 분류, 수정을 아우르는 자율 시스템 프로젝트 포티파이(Project Fortify)에서 Carbon은 스캔 재현율 100%, 분류 정밀도 95%를 기록했다. 오픈소스 저장소 시험에서는 Argon의 이미 높은 재현율보다 상대적으로 25% 넘게 개선되어, 이전에 발견하지 못한 실제 논리 결함을 찾아냈다.

외부 사례도 있다. 구글 클라우드 취약점 연구팀은 Carbon으로 인기 오픈소스 소프트웨어의 버그 두 건이 실제 악용 가능한 취약점임을 증명했고, 개념 증명 코드를 만들어 유지관리자가 심각도를 치명적으로 재분류하고 패치를 내도록 도왔다. 세부 내용은 책임 있는 공개 절차가 끝난 뒤 공유된다. Wiz는 Scan for Good 프로그램에서 두 대형 SaaS 제공업체를 스캔해 두 시간도 안 되어 0-day 취약점을 찾았다. 몇 주가 걸릴 취약점 연구를 한나절로 줄인 셈이며, 영향받는 조직과 협력해 빠르게 조치해 수만 개 기업에 미칠 수 있는 피해를 줄였다.

## 4. 과학과 수학: 증명, 실험 분석, 단백질 구조

Carbon은 물리, 수학, 생명과학에서 실험 데이터를 종합하고 가설을 시험하며 여러 단계의 도메인 문제를 추론하는 성능이 크게 좋아졌다. 약물 독성 연구 기업 Axiom Bio에서는 번역 과학 분야 최고 성능 모델이 되어 이전에 찾지 못한 독성 기전을 발견했고, Axiom은 운영 중인 과학 분석과 에이전트를 Carbon과 Argon으로 옮기고 있다.

구글 연구진은 안티그래비티에서 Carbon으로 세 가지 작업을 했다.

- 코드 검증: 형식 검증용 에이전트 프레임워크 AlphaProof Code를 만들어 시그널(Signal) 암호 프로토콜의 실제 코드를 수학적으로 증명했다. 보안 목표를 수학 정리로 옮기고, 에이전트들이 Carbon으로 증명 언어 Lean 코드를 수백만 줄 생성해 핵심 보안 속성을 몇 주 만에 증명했다. 전문가 팀이 보통 수년 걸리는 일이다. - 효소 분석법 개발: 실험 노트와 원시 데이터만 받은 Carbon이 해석하기 어려운 이상치를 짚어 깊은 웰의 자동 혼합 불완전 같은 실험 오류를 진단했고, 재현성이 크게 좋아졌다. 크로마토그래피 피크 분리 방법을 개선하고 장비의 미량 시료 이월도 잡아냈다. - 단백질 구조 예측: AlphaFold 3 같은 모델은 일치 서열이 적은 단백질에서 어려움을 겪는다. 연구진은 다중 에이전트 환경에서 Carbon으로 방대한 미주석 서열 보관소와 3D 구조 데이터베이스를 탐색해 원격 상동체를 찾게 했다. CASP17 블라인드 시험 집합의 상동체가 적은 단백질 가족 7개에서 검색된 상동체 수가 평균 40배로 늘었고, 재학습은 필요 없었다. 더 넓은 벤치마크는 진행 중이다.

구글은 연구자 1만 명에게 6개월간 무료로 Argon을 제공하는 프로그램을 4주 전에 열었고 이미 수천 명이 합류했다. 이제 현재와 미래 참가자에게 Carbon 접근을 넓히며, 신청은 계속 열려 있고 자격과 수용 능력, 선발에 따라 매주 순차적으로 받는다.

## 5. 안전과 보안: 오용 방지와 정렬 지표

구글은 Carbon의 더 강한 사이버 능력에 맞춰 Argon의 안전 체계 위에 오용과 프롬프트 주입에 대한 방어를 보강했다고 밝힌다. 사이버 공격 모의 환경(ExploitBench, CyScenarioBench)에서 공격 계획을 막힌 뒤 다시 고쳐 시도하는 적응형 레드팀 에이전트의 공격 경로를 Carbon은 99% 차단했다. 시도당 침해율은 0.8%로 Argon의 3.1%보다 낮다. Gray Swan 시험에서 자동 사이버 공격 질의 성공률은 2.17%로 Argon의 9.86%보다 낮았고, Trajectory Labs의 외부 시험은 132시간, 요청 1만 3천 건 이상에서 새로운 범용 탈옥을 찾지 못했다.

정렬 면에서는 375개 과제로 된 에이전트 정직성 벤치마크에서 Carbon이 92%를 통과해 Argon의 70%를 넘었다. 누락된 실험 데이터를 임의로 채우지 않은 비율이 98%, 방법론의 결함을 짚은 비율이 68%다.

간접 프롬프트 주입은 2주 전 Gray Swan IPI 벤치마크에서 공격 성공률 0%를 처음 달성했다고 밝혔다. 다만 구글은 이 분야가 계속 개선할 영역이며, 자동 레드팀이 일부 분포의 정교한 공격에는 모델을 더 개선할 여지가 있음을 보여 준다고 덧붙였다.

구글은 모델 수명 주기 전반의 오정렬 지표를 보여 주는 그림도 함께 공개했다.

![모델 수명 주기에 걸친 오정렬 지표 차트 (출처: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available)](photos/8e85b0f30aa8.jpg "모델 수명 주기에 걸친 오정렬 지표 차트 (출처: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available)")

## 6. 이용 경로: 대상별 접근 방법

Carbon은 Argon과 함께 구글 제품군에서 쓸 수 있다. 개발자는 AI Studio와 Android Studio의 Gemini API 유료 등급을 쓰고, Google AI Ultra 구독자는 안티그래비티와 AI Studio에서 쓴다. 기업은 API나 모델 선택 메뉴로 기업용 Gemini, 안티그래비티, CodeMender에서 쓴다. 일반 사용자는 AI Ultra 구독자라면 Gemini 앱과 검색 AI 모드에서 쓴다.

과학자와 연구자는 안티그래비티 최고 사용량 등급을 6개월 무료로 쓰도록 신청할 수 있고, 사이버보안 방어팀은 페어윈드 프로그램에 신청하면 순차적으로 Carbon for cyber를 받는다.

## 출처와 작성 방식

- 원문: [blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/)
- 원문을 소개한 뉴스레터: TLDR
- 그림: 아래에 출처가 적힌 그림은 원문에 실린 그림을 인용한 것이며 저작권은 원저작자에게 있습니다. 출처가 없는 그래프는 원문에 적힌 값으로 직접 그린 것입니다.
- 작성 방식: 직접 만든 뉴스 정리 파이프라인(서재)으로 생성하고 검수한 글입니다. 본문의 수치와 주장은 원문에서 가져온 것입니다.
- 정리 주차: 2026-W46
