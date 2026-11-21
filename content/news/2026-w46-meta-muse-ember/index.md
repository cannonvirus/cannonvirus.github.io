---
title: "Muse Ember: Meta의 가장 작고 효율적인 에이전트용 모델"
date: 2026-11-16T09:00:00+09:00
description: "Meta가 도구 호출, 코딩 하위 작업, 문서 분석 같은 반복 업무에 맞춘 소형 모델 Muse Ember를 공개했고, 같은 지수 점수를 경쟁 소형 모델보다 훨씬 낮은 비용에 내는 점을 내세웠다."
tags: ["models", "efficiency"]
week: "2026-W46"
source_url: "https://research.meta.ai/blog/muse-ember"
source_newsletter: "Simon Willison’s Newsletter"
draft: false
---

> 이 글은 아래 원문을 우리말로 간추려 정리한 글입니다. 정확한 내용은 원문을 확인하십시오.
>
> 원문: [research.meta.ai/blog/muse-ember](https://research.meta.ai/blog/muse-ember)  
> 원문을 소개한 뉴스레터: Simon Willison’s Newsletter

[Muse Ember](https://research.meta.ai/blog/muse-ember)는 텍스트, 이미지, 오디오, 영상을 넣으면 도구 호출, 코드 수정, 문서 정보 추출 같은 결과를 내놓는 Meta의 가장 작은 모델이다. 에이전트 서비스를 만드는 개발자와 기업이 하루 종일 되풀이되는 작업을 낮은 비용으로 처리할 때 쓴다. 가장 어려운 문제는 상위 모델이 계획하고, 물량이 많은 하위 작업은 이 모델이 맡는 구성을 염두에 두고 만들었다.

```요약
요약: Meta가 도구 호출, 코딩 하위 작업, 문서 분석 같은 반복 업무에 맞춘 소형 모델 Muse Ember를 공개했고, 같은 지수 점수를 경쟁 소형 모델보다 훨씬 낮은 비용에 내는 점을 내세웠다.
```

```용어
추론 강도(reasoning effort): 모델이 답하기 전에 들이는 사고량을 정하는 설정으로, 높일수록 점수가 오르지만 작업당 비용도 함께 는다.
효율 경계선(efficiency frontier): 같은 비용에서 가장 높은 점수를 내는 모델들이 이루는 선으로, 이 선 위의 모델보다 싸면서 점수가 높은 모델은 없다.
컨텍스트 창(context window): 모델이 한 번의 호출에서 입력으로 받아들일 수 있는 텍스트의 최대 길이이다.
라우팅(routing): 들어온 요청을 처리에 알맞은 모델이나 도구로 나누어 보내는 일이다.
pass@1: 한 번만 시도해서 과제를 통과한 비율을 재는 방식이다.
```

## 1. 개요: 반복 작업을 맡는 가장 작은 모델

Meta는 Muse Ember를 도구 호출, 코딩 하위 작업, 라우팅, 정보 추출, 긴 문서 분석처럼 에이전트가 하루 종일 되풀이하는 일에 맞춘 가장 작고 효율적인 모델로 소개했다. 에이전트는 토큰 대부분을 작고 정형화된 여러 단계에 쓰기 때문에, 이런 단계에서 비용을 줄이는 것이 핵심 목표다. 레코드를 불러오고, 도구를 차례로 호출하고, 여러 앱의 시스템을 갱신하는 업무 흐름을 처음부터 끝까지 수행할 수 있다고 한다.

입력은 텍스트, 이미지, 오디오, 영상을 모두 받는다. 별도 모델 없이 스크린샷, 차트, 스캔 문서를 읽고 음성 메모나 회의 녹음, 영상도 다룬다. 컨텍스트 창(context window)은 100만 토큰이고 출력은 최대 51만 2천 토큰이어서, 코드베이스 전체나 문서 묶음을 한 번의 호출로 넣을 수 있다.

Meta는 이 모델을 자사 라인업의 한 축으로 자리매김했다. 가장 어려운 문제는 Muse Wonder, 코딩과 에이전트 업무는 Muse Spark, 대량의 반복 업무는 Muse Ember가 맡는 구도다. Muse Ember는 Muse Wonder Full로 훈련한 첫 모델이며, 어려운 문제에서는 Muse Wonder가 계획을 세우고 Muse Ember가 물량을 처리하는 조합을 제안한다.

![Muse Ember 소개 대표 그림 (출처: research.meta.ai/blog/muse-ember)](photos/deedb05de472.jpg "Muse Ember 소개 대표 그림 (출처: research.meta.ai/blog/muse-ember)")

## 2. 비용 대비 성능: Artificial Analysis 기준

Meta는 외부 평가 기관 Artificial Analysis의 지수와 작업당 비용을 추론 강도(reasoning effort)별로 비교해, Muse Ember가 Claude Haiku 5.5와 GPT-6 Luna보다 달러당 지능이 높다고 밝혔다. 원문 그래프의 Muse Ember 비용은 제안 가격 기준 추정치다. Haiku 5.5는 가장 높은 설정에서 36.2점을 내는 데 작업당 $0.411가 들지만, Muse Ember는 35.8점을 $0.136에 낸다. 즉 Haiku의 최고 점수에 맞먹는 수준을 약 3분의 1 비용으로 얻는다는 설명이다.

GPT-6 Luna는 가장 높은 설정에서도 27.8점에 작업당 $0.152여서, Muse Ember의 모든 설정이 Luna의 어떤 설정보다 높은 점수를 낸다. max 설정의 지수는 Muse Ember와 Haiku 5.5가 36점, Luna가 28점이다. Meta는 전체 Artificial Analysis 순위표에서도 Muse Ember가 효율 경계선(efficiency frontier) 위에 있어, 더 적은 비용으로 더 높은 점수를 내는 모델이 없다고 주장한다.

같은 계열의 Muse Spark 1.3과도 비교했다. 지수는 Muse Spark 1.3이 37점으로 근소하게 높지만, 지수 작업당 비용은 Muse Ember가 $0.14, Muse Spark 1.3이 $2.39이다. 100만 토큰당 입출력 가격도 Muse Ember는 $0.10과 $0.50이고 Muse Spark 1.3은 $1.25와 $4.25이다.

## 3. 에이전트 업무: 비즈니스 워크플로와 종합 과제

Meta는 에이전트 영역에서 세 가지 벤치마크를 내세웠고, 모두 max 설정에서 Haiku 5.5와 GPT-6 Luna를 앞섰다. 가장 격차가 큰 것은 업무 자동화를 재는 AutomationBench-AA다. 엄격한 pass@1 기준으로 Muse Ember는 37.8%, Luna는 20.2%, Haiku 5.5는 13.9%를 기록했다. SiliconANGLE는 이 벤치마크가 Gmail, Salesforce 같은 클라우드 앱에 걸친 657개 과제로 이뤄졌다고 전했다.

나머지 두 지표는 격차가 더 작다. 에이전트 종단 과제를 보는 Agents' Last Exam(Meta 내부 평가, 리눅스 하위 집합)에서는 Muse Ember가 61.6%, Luna가 57.1%, Haiku 5.5가 57.0%였다. 개인 업무와 지식 업무를 묶은 Meta 내부 종합 지표 Personal Superintelligence Index에서는 Muse Ember 46.8%, Luna 37.0%, Haiku 5.5 36.1%였다.

![AutomationBench-AA 점수 (max 설정, 엄격 pass@1)](photos/chart-1.png "업무 자동화 벤치마크에서 Muse Ember가 가장 큰 격차로 앞섰다.")

## 4. 코딩: 에이전트가 수백 번 보내는 하위 작업

Meta는 Muse Ember를 파일 읽기, 테스트 실행, 국소적 수정처럼 에이전트가 한 세션에 수백 번 맡기는 코딩 하위 작업용으로 설계했다. 각 모델을 가장 좋은 공개 하네스에서 돌린 Terminal-Bench 4.0에서는 Muse Ember가 40.9%, Haiku 5.5가 39.2%, Luna가 16.4%였다. 실제 에이전트 하네스에서의 코딩을 보는 Coding Agent Index-AA는 Muse Ember 46, Haiku 5.5 37, Luna 31로 차이가 가장 컸다.

모든 코딩 지표에서 앞선 것은 아니다. 실제 엔지니어링 과제를 병합 가능성으로 판정하는 FrontierCode 2.0-AA에서는 Haiku 5.5가 34.9%로 1위이고, Muse Ember는 27.2%, Luna는 25.2%였다. Meta는 가장 어려운 문제에는 Muse Wonder를 함께 쓰라고 안내한다.

![Coding Agent Index-AA 점수 (max 설정)](photos/chart-2.png "실제 에이전트 하네스에서의 코딩 점수 비교.")

## 5. 멀티모달: 긴 문서, 컴퓨터 조작, 시각 인식

Meta는 긴 문서 처리, 화면 기반 컴퓨터 조작, 미세한 시각 정보 구분에서도 결과를 공개했다. 긴 문서 위의 전문 업무를 보는 GDP.pdf-AA에서는 Muse Ember와 Luna가 22.8%로 같고 Haiku 5.5는 20.8%였다. 이 항목에서는 Muse Ember가 단독 우위가 아니라 Luna와 공동 1위다.

데스크톱 앱 전반의 컴퓨터 사용을 보는 OSWorld 2.1(Meta 내부 평가)에서는 부분 점수 기준으로 Muse Ember 69.5%, Haiku 5.5 68.9%, Luna 50.5%였다. 성공 여부만 보는 이진 기준으로는 각각 33.8%, 27.8%, 17.0%였다. 도구를 쓰는 조건의 PerceptionBench(Meta 내부 평가)에서는 Muse Ember 80.6%, Haiku 5.5 78.6%, Luna 62.8%였다.

## 6. 안전성 평가와 제공 조건

Meta는 출시 전에 Meta Superintelligence Scaling Framework에 따라 화학·생물, 사이버보안, 통제 상실 위험을 평가했고, 평가한 모든 범주에서 Muse Ember가 이 프레임워크의 고위험 기준 아래에 머물렀다고 밝혔다. 작은 모델이지만 핵심 안전 훈련과 시험은 같은 수준으로 거쳤다고 한다. 사용자를 대신해 움직일 때의 행동도 평가했다. 사용자 의도를 지키는지, 민감한 정보를 적절히 다루는지, 웹 페이지나 문서, 도구 출력에 숨은 지시에 흔들리지 않는지, 영향이 큰 행동 전에 사람의 입력을 구하는지가 대상이다.

Muse Ember는 Muse Code와 Meta Model API에서 muse-ember-1.0이라는 이름으로 제공된다. 가격은 입력 100만 토큰당 $0.10, 캐시된 입력 100만 토큰당 $0.004, 출력 100만 토큰당 $0.50이다. Muse Ember, Muse Spark, Muse Wonder는 Google Cloud와 Oracle Cloud에서도 쓸 수 있으며, Meta는 더 효율적인 모델을 훈련 중이라고 예고했다.

## 출처와 작성 방식

- 원문: [research.meta.ai/blog/muse-ember](https://research.meta.ai/blog/muse-ember)
- 원문을 소개한 뉴스레터: Simon Willison’s Newsletter
- 함께 본 글: [Meta introduces Muse Ember to power cost-efficient AI agents](https://siliconangle.com/2026/11/09/meta-introduces-muse-ember-to-power-cost-efficient-ai-agents/) (Deep Learning Weekly 소개)
- 그림: 아래에 출처가 적힌 그림은 원문에 실린 그림을 인용한 것이며 저작권은 원저작자에게 있습니다. 출처가 없는 그래프는 원문에 적힌 값으로 직접 그린 것입니다.
- 작성 방식: 직접 만든 뉴스 정리 파이프라인(서재)으로 생성하고 검수한 글입니다. 본문의 수치와 주장은 원문에서 가져온 것입니다.
- 정리 주차: 2026-W46
