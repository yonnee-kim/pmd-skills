---
name: pyramid-sync
description: 계약 문서(L2 모듈 등)와 구현 코드 간 drift 감지·해소 제안. 사용자가 "sync", "drift", "동기화", "정합성", "문서-코드 맞추기"를 말하거나 Stop hook이 drift 알림을 출력했을 때 호출. 자동 수정하지 않고 방향만 제안.
---

# pyramid-sync — doc↔code 정합성 (posterior 엔진)

계약 문서(`implements:` 필드가 있는 문서 — 기본 구조에선 L2 모듈 파일)와 구현 코드 간 drift를 감지하고 어느 방향으로 맞출지 제안. 매핑 규약은 `${CLAUDE_PLUGIN_ROOT}/shared/mapping-spec.md` — 먼저 읽을 것.

## 실행

1. 매핑 규약(`${CLAUDE_PLUGIN_ROOT}/shared/mapping-spec.md`) Read
2. 변경 파일 수집: `git diff --name-only` + staged + untracked
3. 계약 문서 탐색(규약의 "문서 루트 탐색" 따름) 후 `implements` 역매핑 인덱스 구성
4. 교집합 각 파일에 대해 방향 판별 — 판단 근거를 사용자에게 드러낼 것
5. drift 없으면 `sync clean` 한 줄만 출력하고 종료

## 방향 판별

코드의 export/class/interface/함수 이름·invariant를 추출해 계약 문서의 "공개 경계"·"Invariants" 섹션과 대조. **구체 시그니처는 코드가 진실 소스** — 문서와 시그니처가 다르다고 drift로 판정하지 말 것. 이름·불변식 수준에서만 비교.

- `code-ahead` — 코드에 있음, 문서에 없음
- `doc-ahead` — 문서에 있음, 코드에 없음
- `divergent` — 이름은 같으나 invariant/책임이 어긋남
- `path-stale` — `implements` 경로에 코드 없음

자동 판정 우기지 말 것 — 애매하면 상황을 제시하고 물을 것.

## Direction별 해소 단계

### code-ahead
1. 새 export가 **의도한 공개 API**인지 사용자 확인 — 내부용이면 `_` prefix 또는 export 제거(코드 쪽 수정)
2. 공개 API면 대상 문서 "공개 경계"에 이름 + 한 줄 설명 추가 (시그니처 복붙 금지)
3. 새 invariant가 필요하면 "Invariants" 섹션에 추가
4. 한 섹션씩 Edit, 매번 사용자 확인

### doc-ahead
1. 해당 항목이 **여전히 계획 중인지** 사용자 확인 — 폐기됐으면 문서에서 제거
2. 계획 유지면 그대로 둠 (doc-ahead는 정상 lifecycle). `TODO(why)` 주석 허용
3. 일정이 모호해지면 L1 `scope.md`의 v1 범위 재배치 검토 제안

### divergent
1. 코드·문서 양쪽 의미를 나란히 제시 (1~3줄 차이 요약)
2. **기준을 사용자에게 선택 요청** — 코드 기준(문서 맞춤) vs 문서 기준(코드 맞춤)
3. 선택된 쪽만 수정. 절충 금지 (drift 원흉)
4. 수정 후 다시 실행하여 clean 확인

### path-stale
1. 이동·리네임 여부 확인 — `git log --follow`·grep. 이동이면 `implements:` 경로만 수정
2. 삭제면 `implements:` 리스트에서 제거. 모듈 전체 소멸이면 문서 파일도 제거 검토
3. 오타면 직접 수정. 외부 리소스(rules 파일 등)는 실제 경로 확인 후 수정

모든 direction 공통: 한 파일씩 Edit, 매 수정마다 재실행으로 sync 확인.

## 출력

```
[direction] code_path ↔ doc_path
  - 차이: ...
  → 제안: ...
```

마지막에 전체 요약 1~2줄, 진행 여부 확인.

## 수정 규칙

- 자동 Edit 금지. 방향 확정 후 한 파일씩 수정, 매 수정마다 확인
- 문서 업데이트 시 `implements` 경로도 함께 검증
- 코드 수정 시 다른 코드를 "정리"하지 말 것 (surgical)
- **시그니처를 문서에 복붙하지 말 것** — drift 반복 원인

## 진단 ("왜 hook이 안 떠요?")

사용자가 hook 동작이 의심되면 debug 실행:

```
PYRAMID_SYNC_DEBUG=1 python3 ${CLAUDE_PLUGIN_ROOT}/hooks/pyramid-sync-check.py
```

stderr에 각 단계 결과가 출력된다 (stdout·캐시엔 영향 없음). 흔한 원인:
- `changed files: 0` — 작업 트리 clean. git staged·untracked 모두 비어있음
- `contract docs discovered: 0` — `implements:` 필드 있는 문서가 tracked `.md`에 없음 (frontmatter 오타, gitignored, 새 파일이 아직 `git add` 안 됨)
- `index entries: 0` — 문서는 있으나 `implements:` 파싱 실패 (YAML 오타)
- `drift: 0` — 변경 파일이 매핑에 없음 (정상: 매핑 밖 파일만 수정됨)

## Gotchas

- `implements` 누락된 문서는 인덱스에 없음 → 미탐지. prior 엔진(`pyramid`)에서 메타데이터 보강 요청
- glob·심볼 단위 매핑은 현 단계에서 미지원 (규약 참조)
- **Hook은 drift와 "동기화 Edit 직후 pending commit"을 구분 못함** — 문서를 방금 업데이트해서 의미상 정합 상태여도 git diff가 비어있지 않으면 hook이 또 fires. 커밋 후에야 조용해짐. 이건 기능(인식 시점이 commit 경계) — 버그 아님
- **타입 필드 추가·수정은 drift 아님** — L2는 필드 수준 명세를 하지 않으므로 `Route`에 `tags` 필드 추가 같은 변경은 정합. 타입 이름 자체가 새로 export되거나 제거될 때만 공개 경계 drift로 간주
