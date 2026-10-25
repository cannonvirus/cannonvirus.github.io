---
title: "vLLM push 방식 KV 전송: 분리형 추론용 커넥터"
date: 2026-10-26T09:00:00+09:00
description: "push 방식 NIXL 커넥터는 디코드 쪽 준비를 프리필 계산과 겹쳐 처리하며, EFA로 연결한 Amazon EC2 P5en 인스턴스의 1P1D 구성에서 Qwen3-32B를 돌렸을 때 pull 방식보다 TTFT를 최대 3배, TPOT를 최대 30% 개선했다."
tags: ["efficiency"]
week: "2026-W43"
source_url: "https://aws.amazon.com/blogs/machine-learning/push-based-kv-transfer-to-improve-ttft-and-tpot-for-disaggregated-inference-in-vllm/"
source_newsletter: "TLDR AI"
draft: false
---

> 이 글은 아래 원문을 우리말로 간추려 정리한 글입니다. 정확한 내용은 원문을 확인하십시오.
>
> 원문: [aws.amazon.com/blogs/machine-learning/push-based-kv-transfer-to-improve-ttft-and-tpot-for-disaggregated-inference-in-vllm](https://aws.amazon.com/blogs/machine-learning/push-based-kv-transfer-to-improve-ttft-and-tpot-for-disaggregated-inference-in-vllm/)  
> 원문을 소개한 뉴스레터: TLDR AI

대규모 언어 모델(LLM) 추론은 두 단계로 나뉜다. 프리필(prefill)은 입력 프롬프트를 처리해 KV 캐시를 만들고, 디코드(decode)는 그 캐시로 출력 토큰을 하나씩 만든다. vLLM은 두 단계를 서로 다른 엔진 인스턴스에서 돌리는 분리형 추론(disaggregated inference)을 지원하지만, 이 방식에서는 토큰을 만들기 전에 KV 캐시를 프리필 쪽에서 디코드 쪽으로 옮겨야 한다. AWS가 vLLM에 기여한 [push 방식 NIXL 커넥터](https://aws.amazon.com/blogs/machine-learning/push-based-kv-transfer-to-improve-ttft-and-tpot-for-disaggregated-inference-in-vllm/)는 디코드 인스턴스가 받을 자리를 미리 잡아 두게 하고, 프리필 인스턴스가 계산을 마치는 대로 KV 캐시를 그 자리에 직접 써 넣는다.

```요약
요약: push 방식 NIXL 커넥터는 디코드 쪽 준비를 프리필 계산과 겹쳐 처리하며, EFA로 연결한 Amazon EC2 P5en 인스턴스의 1P1D 구성에서 Qwen3-32B를 돌렸을 때 pull 방식보다 TTFT를 최대 3배, TPOT를 최대 30% 개선했다.
```

```용어
TTFT: 요청이 들어온 뒤 첫 출력 토큰이 나오기까지 걸리는 시간(time-to-first-token)이다.
TPOT: 출력 토큰 하나를 만드는 데 걸리는 시간(time-per-output-token)이다.
NIXL: NVIDIA Inference Xfer Library의 약자다. vLLM이 인스턴스 사이에서 KV 블록을 옮길 때 쓰는 전송 라이브러리다.
RDMA: Remote Direct Memory Access의 약자로, 호스트 메모리를 거치지 않고 다른 서버의 장치 메모리에 직접 읽고 쓰는 방식이다. AWS에서는 EFA(Elastic Fabric Adapter) 네트워크가 이를 지원한다.
```

## 1. pull 방식이 첫 토큰을 늦추는 이유

NIXL 커넥터는 기본으로 pull 방식으로 동작하는데, 이 방식에서는 프리필이 끝난 뒤에야 전송 준비가 시작된다. 프리필 인스턴스가 KV 캐시 계산을 마치면 라우터가 프리필 블록 ID를 담은 원본 메타데이터를 디코드 인스턴스에 전달한다. 디코드 인스턴스는 그제야 KV 캐시를 받을 블록을 할당하고 전송을 준비한 뒤, NIXL READ로 프리필 쪽 블록을 읽어 온다.

이 단계들은 프리필 뒤에 차례로 일어나므로 첫 토큰이 나오기 전에 반드시 거치는 경로(critical path)에 그만큼 시간이 더해진다. 다음 그림은 프리필 엔진, 라우터, 디코드 엔진이 맡은 작업을 시간 축 위에 이어 그린 것이고, 상자 길이는 실제 시간 비율과 다르다.

![pull 방식에서 첫 토큰까지 이어지는 처리 순서 (출처: aws.amazon.com)](photos/81d42e9bfa3b.webp "pull 방식에서 첫 토큰까지 이어지는 처리 순서 (출처: aws.amazon.com)")

## 2. push 방식의 구성과 전송 절차

push 방식은 디코드 쪽 준비를 프리필 계산과 동시에 진행해 pull 방식에서 차례로 이어지던 구간을 없앤다. 라우터가 요청을 프리필과 디코드 양쪽에 동시에 보내면, 디코드 인스턴스는 프리필이 계산하는 동안 블록을 할당하고 그 위치를 프리필 인스턴스에 등록한다. 이 때문에 프리필 블록이 준비되는 즉시 전송을 시작할 수 있고, 디코드 쪽이 블록 ID를 알아내려고 한 차례 더 주고받던 과정이 첫 토큰 경로에서 빠진다.

전송 절차는 세 단계다.

1. 등록(디코드 쪽): 디코드 인스턴스는 블록을 할당한 엔진 단계 안에서 자기 식별 정보와 예약한 블록 위치를 NIXL 알림으로 프리필 인스턴스에 보낸다.
2. 짝 맞추기(rendezvous, 프리필 쪽): 등록과 프리필 완료 가운데 먼저 도착한 쪽을 붙잡아 두었다가 나머지가 도착하면 전송을 시작한다. 요청은 ID로 짝을 짓고, 선점되거나 재시도된 요청도 올바르게 연결한다.
3. 전송(프리필 쪽): 디코드 인스턴스와 연결을 새로 맺거나 기존 연결을 다시 쓰고, NIXL WRITE로 KV 블록을 디코드 쪽 메모리에 직접 복사한다.

두 인스턴스의 블록 배치는 서로 달라도 된다. 각 쪽이 전송 시점에 블록 위치를 자기 물리 배치로 바꾸므로 블록 크기가 달라도 전송할 수 있다. 쓰기마다 완료 알림이 붙고, 디코드 인스턴스는 자기에게 쓰는 프리필 랭크 수만큼 알림이 모두 도착해야 KV 캐시를 받은 것으로 보고 디코드를 시작한다. 다음 그림의 왼쪽은 프리필 엔진, 오른쪽은 디코드 엔진이며, 보라색 상자가 두 조건을 기다리는 짝 맞추기 지점이다.

![push 방식 KV 전송의 구성과 전송 순서 (출처: aws.amazon.com)](photos/0a77442ac8a3.webp "push 방식 KV 전송의 구성과 전송 순서 (출처: aws.amazon.com)")

## 3. 전송 준비를 맡는 백그라운드 스레드

push 커넥터는 모델 실행과 전송 준비를 서로 다른 스레드에 맡긴다. 프리필 워커마다 전송 전용 백그라운드 스레드가 하나씩 있다. 프리필 메인 루프는 등록과 KV 캐시가 모두 준비되면 블록을 이 스레드에 넘기고 곧바로 모델 실행으로 돌아간다. 넘겨받은 스레드는 NIXL 연결을 확보하고, 블록 ID를 메모리 디스크립터로 바꾸고, 이어진 블록을 큰 전송 영역으로 합친 뒤 NIXL WRITE를 제출한다.

요청마다 드는 이 준비 작업을 지연에 민감한 메인 루프 밖에서 처리하므로 모델 실행이 늦춰지지 않는다. 전송이 끝나면 NIXL이 디코드 인스턴스에 완료 알림을 보내고, 디코드는 그때 토큰 생성을 시작한다. 다음 그림은 한 요청을 처리하는 동안 두 엔진의 메인 스레드와 백그라운드 스레드가 작업을 넘기는 순서를 번호로 보여 준다.

![메인 스레드와 백그라운드 스레드의 작업 분담 (출처: aws.amazon.com)](photos/99885669e2f1.webp "메인 스레드와 백그라운드 스레드의 작업 분담 (출처: aws.amazon.com)")

## 4. 두 방식의 시간 흐름과 라우팅 조건

두 방식은 같은 NIXL과 EFA/RDMA 데이터 경로를 쓰고, 디코드 쪽 준비를 언제 하느냐만 다르다. pull 방식은 메타데이터 전달과 디코드 쪽 준비를 프리필 뒤에 하지만, push 방식은 이를 프리필과 겹쳐 처리해 프리필 이후 경로에서 뺀다. 다음 그림의 위쪽이 pull, 아래쪽이 push의 흐름이다.

![pull과 push의 첫 토큰까지 시간 흐름 비교 (출처: aws.amazon.com)](photos/435297923258.webp "pull과 push의 첫 토큰까지 시간 흐름 비교 (출처: aws.amazon.com)")

다만 push 방식에서는 디코드 인스턴스를 더 일찍 정해야 한다. pull 방식에서는 라우터가 프리필이 끝난 뒤 디코드 인스턴스를 고르므로, 부하를 보고 요청을 나누거나 서비스 품질을 관리하기가 쉽다. 반면 push 방식은 프롬프트 KV와 목적지 등록이 갖춰지는 즉시 전송을 시작하므로, 비슷한 부하에서는 프리필 인스턴스가 KV 블록을 더 일찍 비울 수 있다.

## 5. Qwen3-32B 측정 결과

AWS는 EFA로 연결한 Amazon EC2 P5en 인스턴스로 프리필 노드 1대와 디코드 노드 1대(1P1D)를 꾸리고 Qwen3-32B로 두 방식을 비교했다. 입력 길이는 1k~16k 토큰, 요청률은 초당 1~8건(QPS)으로 바꿔 가며 쟀고 출력 토큰은 128개였다. 디코드 노드가 겹치는 프롬프트의 캐시를 다시 써서 전송을 건너뛰면 비교 결과가 왜곡되므로, 프리픽스 캐싱을 끄고 요청마다 KV 캐시 전체를 옮기게 했다.

**TTFT 차이는 부하가 클수록 벌어졌다.** 부하가 낮고 프롬프트가 짧을 때는 두 방식이 거의 같았지만, 8 QPS와 16k 입력에서는 pull이 약 1,744 ms, push가 약 540 ms로 약 3배 차이가 났다. AWS는 그 원인으로 pull 방식의 디코드 워커가 엔진 루프 안에서 NIXL 디스크립터를 동기로 올리느라 토큰 생성이 멈추는 점을 들었다. 다음 그래프에서 빨간 선이 pull, 초록 선이 push다.

![요청률별 입력 길이에 따른 TTFT 비교 (출처: aws.amazon.com)](photos/b89c8326412b.webp "요청률별 입력 길이에 따른 TTFT 비교 (출처: aws.amazon.com)")

**TPOT도 TTFT와 같은 경향을 보였다.** 부하가 가벼울 때 두 방식은 약 5.6~5.8 ms로 비슷했지만, 4~8 QPS와 16k 입력에서 pull은 약 10.4 ms까지 올랐고 push는 7 ms 안팎에 머물렀다. push 방식은 디스크립터 준비와 전송 제출을 디코드 워커에서 덜어 내므로, 동시 요청이 많고 컨텍스트가 길어도 토큰당 지연이 거의 늘지 않는다.

![요청률별 입력 길이에 따른 TPOT 비교 (출처: aws.amazon.com)](photos/526d4576a6d6.webp "요청률별 입력 길이에 따른 TPOT 비교 (출처: aws.amazon.com)")

AWS는 이 기능을 AWS Trainium 클러스터에서 만들고 검증한 뒤 가속기 종류에 매이지 않는 기능으로 vLLM에 기여했으며, 이번 GPU 측정은 같은 효과가 GPU에서도 나타난다는 근거로 제시됐다. 결과는 하드웨어, 모델, 워크로드, 네트워크 구성에 따라 달라지고, 벤치마크를 재현하는 절차는 원문의 별도 안내서에 정리되어 있다.

push 커넥터는 프리필 계산과 디코드 쪽 블록 할당·등록을 겹쳐 처리해, 프리필 뒤에 라우터를 한 번 더 거치던 과정과 디코드 쪽 전송 준비를 첫 토큰 경로에서 뺀다. AWS는 디코드 노드를 일찍 정해도 되고 TTFT가 우선인 경우에는 push 방식을 쓰라고 권한다. 반면 양방향 KV 전송이 필요하거나 부하를 보고 라우팅하려고 디코드 인스턴스를 프리필 뒤에 골라야 하는 워크로드에는 pull 방식이 더 맞다고 본다. AWS는 백그라운드 스레드 구조를 pull 방식 커넥터에도 적용하는 방안을 검토하고 있다.

## 출처와 작성 방식

- 원문: [aws.amazon.com/blogs/machine-learning/push-based-kv-transfer-to-improve-ttft-and-tpot-for-disaggregated-inference-in-vllm](https://aws.amazon.com/blogs/machine-learning/push-based-kv-transfer-to-improve-ttft-and-tpot-for-disaggregated-inference-in-vllm/)
- 원문을 소개한 뉴스레터: TLDR AI
- 그림: 원문에 실린 그림을 인용한 것이며 저작권은 원저작자에게 있습니다. 그림 아래에 출처를 적었습니다.
- 작성 방식: 직접 만든 뉴스 정리 파이프라인(VISER)으로 생성하고 검수한 글입니다. 본문의 수치와 주장은 원문에서 가져온 것입니다.
- 정리 주차: 2026-W43
