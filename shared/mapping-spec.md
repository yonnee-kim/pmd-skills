# 매핑 규약 (doc↔code)

`pyramid`(prior 엔진), `pyramid-sync`(posterior 엔진), Stop hook(자동 감지)이 공유하는 단일 정본. 여기가 유일한 진실의 원천이다.

## 왜 필요한가

Hook이 값싼 drift 감지를 하려면 "변경된 코드 파일 → 해당 계약 문서"를 O(1)로 역매핑해야 한다. 매핑이 prior 문서에 구조적으로 내장돼야 전체 시스템이 성립한다.

## 필드

계약 문서 frontmatter에 `implements:` 필드를 둔다. **layer 무관** — 이 필드가 있는 문서는 모두 "계약"으로 간주 (기본 레이어 구조에선 L2 모듈 파일).

```yaml
---
layer: L2
id: route
implements:
  - lib/route/store.ts
  - lib/route/types.ts
---
```

- 값은 레포 루트 기준 **상대 경로** 배열
- 파일 단위. 심볼 단위는 현 단계에서 지원하지 않음
- glob 금지 (정확한 경로만). 여러 파일은 명시적으로 나열
- 존재하지 않는 경로도 허용 — doc-ahead(미구현 계약) 상태가 정상적 lifecycle
- 단일 파일은 `implements: [src/x.ts]` 또는 다중 라인 리스트 모두 가능

## 역매핑 인덱스

Hook·sync 스킬은 `implements:`가 있는 모든 문서를 스캔하여 `code_path → doc_path` 맵을 구성한다.

- 출력: 메모리 내 dict. 파일 시스템 캐시 없음 (세션당 재계산, git diff 범위 작아서 무시 가능)
- 충돌 처리: 같은 코드 파일이 2개 이상 문서에 `implements`로 걸리면 양쪽 모두 drift 체크 대상

## 문서 루트 탐색

문서 위치 컨벤션은 `_docs/L2-spec/modules/{module}.md` (L0·L1과 동일 루트 `_docs/` 하위).

탐색은 content-based — path 관례가 아니라 **frontmatter `implements:` 필드**가 SSOT 신호. `git ls-files *.md`로 tracked `.md`만 긁은 뒤 frontmatter에 `implements:`가 있는 것만 인덱스. gitignore 자동 존중, 관례 이탈(예: 모듈별 co-location `src/foo/_docs/contract.md`)도 자연스럽게 흡수.

Override: 환경 변수 `PYRAMID_CONTRACT_GLOB` 설정 시 그 glob 결과만 사용 (content 체크 생략, 사용자 책임).

## Hook 관점의 계약

Shell script가 보는 최소 정보:
- 변경 파일 리스트: `git diff --name-only`
- 매핑 인덱스: 위 역매핑
- 판별: 변경 파일이 인덱스에 있으면 해당 문서에 "잠재 drift". 세부 판단은 sync 스킬에 위임

Hook은 매핑 유무만 확인, 내용 비교는 하지 않는다. 이것이 "값싼 heuristic"의 구체화.

## 비기능 요건

- 계약 문서 ≤ 수백 개 규모 전제. 그 이상이면 캐시 도입 고려 (현 단계 스킵)
- frontmatter 파싱은 단순 YAML — 줄단위 읽기 + 블록 추출로 충분

## 검증

규약이 깨지는 대표 케이스:
1. 계약 문서 생성 시 `implements` 누락 → prior 엔진이 작성 시 강제할 것
2. 코드 이동/리네임 시 경로 stale → sync 스킬이 path not found로 리포트, 수정 제안
3. 동일 코드가 여러 문서에 걸침 → 허용, 양쪽 모두 체크

## 향후 확장 (지금은 하지 않음)

- 심볼 단위 매핑 (`implements: [src/x.ts#MyClass.method]`)
- 반대 방향 역참조 (코드 주석에 `@pyramid-doc` 태그)
- glob 지원
