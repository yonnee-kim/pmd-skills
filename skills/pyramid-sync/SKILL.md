---
name: pyramid-sync
description: L3 문서와 구현 코드 간 drift 감지·해소 제안. 사용자가 "sync", "drift", "동기화", "정합성", "문서-코드 맞추기"를 말하거나 Stop hook이 drift 알림을 출력했을 때 호출. 자동 수정하지 않고 방향만 제안.
---

# pyramid-sync — doc↔code 정합성 (posterior 엔진)

L3 계약(prior)과 구현 코드 간 drift를 감지하고 어느 방향으로 맞출지 제안한다. 매핑 규약은 `${CLAUDE_PLUGIN_ROOT}/shared/mapping-spec.md` — 먼저 읽을 것.

## 실행

1. 매핑 규약(`${CLAUDE_PLUGIN_ROOT}/shared/mapping-spec.md`) Read
2. 변경 파일 수집: `git diff --name-only` + staged + untracked
3. L3 문서 탐색(규약의 "문서 루트 탐색" 따름) 후 `implements` 역매핑 인덱스 구성
4. 교집합 각 파일에 대해 방향 판별 — 판단 근거를 사용자에게 드러낼 것
5. drift 없으면 `sync clean` 한 줄만 출력하고 종료

## 방향 판별

코드의 export/class/interface/함수 시그니처·필드명을 읽어 L3 문서의 Contract 섹션(또는 시그니처 블록)과 대조.

- `code-ahead` — 코드에 있음, 문서에 없음 → L3 문서 업데이트
- `doc-ahead` — 문서에 있음, 코드에 없음 → 미구현 계약 리스트로 남김
- `divergent` — 양쪽 있으나 시그니처/필드가 다름 → 사용자에게 기준 선택 요청
- `path-stale` — `implements` 경로에 코드 없음 → L3 경로 수정 또는 `implements` 제거

자동 판정 우기지 말 것 — 애매하면 상황을 제시하고 물을 것.

## 출력

```
[direction] code_path ↔ doc_path
  - 차이: ...
  → 제안: ...
```

마지막에 전체 요약 1~2줄, 진행 여부 확인.

## 수정 규칙

- 자동 Edit 금지. 방향 확정 후 한 파일씩 수정, 매 수정마다 확인
- L3 문서 업데이트 시 `implements` 경로도 함께 검증
- 코드 수정 시 다른 코드를 "정리"하지 말 것 (surgical)

## Gotchas

- `implements` 누락된 L3는 인덱스에 없음 → 미탐지. prior 엔진(`pyramid`)에서 메타데이터 보강 요청
- glob·심볼 단위 매핑은 현 단계에서 미지원 (규약 참조)
