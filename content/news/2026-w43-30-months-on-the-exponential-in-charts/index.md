---
title: "30개월 동안의 AI 변화: 그래프로 본 능력과 가격"
date: 2026-10-26T09:00:00+09:00
description: "METR 측정에서 AI가 50% 이상의 확률로 해내는 작업 길이는 2024년 4분에서 2026년 4월 17시간으로 늘었지만, 능력은 분야마다 고르지 않게 발전했다."
tags: ["models", "agents"]
week: "2026-W43"
source_url: "https://www.oneusefulthing.org/p/30-months-on-the-exponential-in-charts"
source_newsletter: "TLDR"
draft: false
---

> 이 글은 아래 원문을 우리말로 간추려 정리한 글입니다. 정확한 내용은 원문을 확인하십시오.
>
> 원문: [oneusefulthing.org/p/30-months-on-the-exponential-in-charts](https://www.oneusefulthing.org/p/30-months-on-the-exponential-in-charts)  
> 원문을 소개한 뉴스레터: TLDR

저자의 AI 책 Co-Intelligence는 2024년 4월에 나왔고, 30개월 뒤 두 번째 책 Co-Existence가 나왔다. 저자는 두 책 사이에 AI가 어떻게 달라졌는지 [그래프 여러 장으로 정리했다](https://www.oneusefulthing.org/p/30-months-on-the-exponential-in-charts). 그래프는 AI 에이전트가 자료 조사부터 레이아웃까지 맡아 만들었다. 다루는 내용은 모델 성능, AI가 해내는 작업 길이, 가격, 사람이 AI와 일하는 방식의 변화다.

```요약
요약: METR 측정에서 AI가 50% 이상의 확률로 해내는 작업 길이는 2024년 4분에서 2026년 4월 17시간으로 늘었지만, 능력은 분야마다 고르지 않게 발전했다.
```

```용어
오케스트레이터(orchestrator): 사용자와 대화하면서 필요할 때 다른 에이전트를 띄워 지시하고, 그 결과를 사용자에게 전하는 에이전트다.
오픈 웨이트(open weights): 누구나 쓰거나 고칠 수 있도록 공개한 모델이다.
METR 작업 길이: AI가 프롬프트 한 번으로 50% 이상의 확률로 해내는 작업을, 사람이 하면 걸리는 시간으로 잰 값이다.
GPQA Diamond: 대학원생도 자주 틀리는 박사 수준 과학 문제로 된 객관식 시험이다.
컨저러(conjurer): 사람이 일을 정의해 에이전트에게 맡기고, 돌아온 결과를 평가하는 작업 방식이다.
```

## 1. 그래프를 만든 에이전트 작업 방식

이 그래프들은 사람이 단계마다 이끌지 않고 에이전트에게 통째로 맡겨 만들었다. 저자는 Claude Projects에서 Opus 5.5를 썼고, 이 환경에서는 오케스트레이터 하나와 대화하면 그 에이전트가 필요한 만큼 다른 에이전트를 띄운다. 저자가 두어 문장으로 방향만 주자 AI는 조사, 그래프, 레이아웃, 이미지, 인용을 몇 분 만에 끝냈다. 저자가 혼자 했다면 몇 시간이 걸렸을 일이다.

저자가 직접 작업하지 않아도 되었으므로 AI에게 여러 안을 만들게 해서 고르고, 나머지에는 "더 좋게 해 달라" 같은 막연한 주문만 했다. 그러던 중 AI는 저자의 계산 실수도 찾아냈다. 저자는 원래 글 제목에 '28개월'을 넣으려 했다.

## 2. 선두 모델의 교체와 GPT-4를 넘은 모델 수

2023년 초부터 2024년 초까지 가장 뛰어난 모델은 OpenAI의 GPT-4였다. 다음 그림은 Epoch Capabilities Index에서 날마다 가장 높은 점수를 낸 모델을 이어 그린 것이다. GPT-4는 352일 동안 1위를 지켰다. 2024년 2월부터는 선두 모델이 20번 바뀌었고, 선두에 오른 모델은 모두 Anthropic, Google, OpenAI에서 나왔다.

![Epoch Capabilities Index 1위 모델의 교체 추이 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/74730fe87388.webp "Epoch Capabilities Index 1위 모델의 교체 추이 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

선두가 바뀐 것보다 GPT-4를 넘은 모델이 늘어난 변화가 더 크다. 출시 당시의 GPT-4보다 점수가 높은 모델은 180개이고, 그중 68개가 오픈 웨이트 모델이다. 이 180개 가운데 19개는 요즘 스마트폰에서도 돌아간다.

![GPT-4 이후 모델별 지수 점수 분포 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/fb18ea95e3d0.webp "GPT-4 이후 모델별 지수 점수 분포 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

## 3. AI가 해내는 작업 길이와 가격

METR이 잰 작업 길이는 GPT-4 출시부터 측정이 끝날 때까지 여덟 번 두 배가 됐다. 2024년 4월 최고 기록은 GPT-4 2023년 11월판의 4분이었고, 2026년 4월에는 Claude Mythos Preview가 17시간을 기록했다. 다만 METR은 16시간을 넘는 값은 믿기 어렵다며 지금 방식으로는 더 잴 수 없다고 밝혔다. 다음 그림의 세 칸은 같은 기록을 분, 시간, 주 단위로 넓혀 그린 것이고, 초록 막대는 다른 연구가 추정한 17주다.

![METR 작업 길이 기록의 추이 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/55462c178bab.webp "METR 작업 길이 기록의 추이 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

능력이 오르는 동안 값은 내렸다. GPQA Diamond에서 추측 정답을 보정한 75% 점수를 내는 데 드는 문제당 비용은 2025년 o3의 30센트에서 2026년 7월 GPT-5.6 Luna의 0.04센트로 725분의 1이 됐다. 이 비용 수치를 추정한 Epoch AI 연구진은 수치를 정확한 값으로 읽지 말라고 덧붙였다.

![GPQA Diamond 문제당 비용 비교 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/4f47bf1030ef.webp "GPQA Diamond 문제당 비용 비교 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

## 4. 고르지 않은 능력과 컨저러 방식

AI가 할 수 있는 일의 경계는 30개월 전처럼 지금도 들쭉날쭉하다(jagged). 수학 문제 풀이는 이 기간에 형편없던 수준에서 사람을 넘는 수준이 됐지만, 긴 글쓰기는 여전히 서툴다. METR의 소프트웨어 작업 228개 가운데 2024년 4월의 최고 모델은 98개를 해냈고, 2026년 4월까지 110개를 더 해냈다. 아직 못 한 작업은 20개이며, 사람이 10분이면 끝내는 작업도 그중 하나다. 다음 그림에서는 사람이 오래 걸리는 작업일수록 바깥쪽에 있다.

![METR 작업 228개의 해결 여부 분포 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/a07574bd355d.webp "METR 작업 228개의 해결 여부 분포 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

AI가 크게 발전했으므로 사람이 AI와 일하는 방식도 바뀌어야 한다. 앞의 책은 AI와 일을 나눠 맡는 켄타우로스(centaur) 방식과 AI와 일을 섞어 하는 사이보그(cyborg) 방식을 다뤘다. 두 방식 모두 사람이 작업 과정 안에 있어야 하므로 한 사람이 동시에 맡을 수 있는 일에는 한계가 있다. 이 때문에 새 책은 컨저러 방식을 더했다. 저자는 이 방식이 AI를 가장 강력하게 쓰는 방법이지만, AI가 결과를 내려고 무엇을 하는지 통제하기 어려워지는 위험도 따른다고 본다.

![AI와 일하는 세 방식의 비교 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/bb6945ab62da.webp "AI와 일하는 세 방식의 비교 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

## 5. 수달 시험과 늘어난 AI 사건

저자는 몇 년째 "와이파이를 쓰며 비행기에 탄 수달"이라는 프롬프트로 이미지와 영상 생성 도구를 시험해 왔다. 다음은 30개월 전 가장 뛰어난 이미지 생성기였던 Midjourney가 이 프롬프트로 만든 그림이다.

![Midjourney가 30개월 전 만든 수달 그림 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/15b84f8fc9a5.webp "Midjourney가 30개월 전 만든 수달 그림 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

이번에는 저자가 Opus 5.5에게 오타가 섞인 짧은 요청만 보내 같은 주제의 영상을 맡겼다. AI는 저자가 구독한 Google과 ElevenLabs 서비스를 써서 대본, 이미지, 구상, 음악, 제작 기술 문제까지 혼자 해결했다. 영상에는 결함이 몇 군데 있었다.

AI의 능력이 커지면서 AI를 둘러싼 사건도 늘었다. 다음 연표는 Co-Intelligence 출간 이후의 성과와 논란을 골라 담았다. 각 회사가 밝힌 주간 ChatGPT 사용자는 2024년 12월 3억 명에서 2026년 10월 12억 명으로 늘었다. 연표에서는 중요한 사건 수백 개가 빠졌다.

![2024년 4월부터 2026년 10월까지 AI 성과와 논란 연표 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)](photos/e5562398bce9.webp "2024년 4월부터 2026년 10월까지 AI 성과와 논란 연표 (출처: oneusefulthing.org/p/30-months-on-the-exponential-in-charts)")

Co-Existence는 빠르게 바뀌는 소식 대신 이 그래프들이 보여 준 추세를 다룬다. AI는 기하급수적으로 발전하지만 분야마다 고르지 않고, 쓰임새는 챗봇에서 실제 일을 하는 에이전트로 옮겨 가고 있다. 저자는 사람에게 남은 이점으로 깊은 지식, 넓은 지식, 안목, 주체성을 꼽는다.

## 출처와 작성 방식

- 원문: [oneusefulthing.org/p/30-months-on-the-exponential-in-charts](https://www.oneusefulthing.org/p/30-months-on-the-exponential-in-charts)
- 원문을 소개한 뉴스레터: TLDR
- 그림: 원문에 실린 그림을 인용한 것이며 저작권은 원저작자에게 있습니다. 그림 아래에 출처를 적었습니다.
- 작성 방식: 직접 만든 뉴스 정리 파이프라인(VISER)으로 생성하고 검수한 글입니다. 본문의 수치와 주장은 원문에서 가져온 것입니다.
- 정리 주차: 2026-W43
