# pmd-skills 설계 핸드오프

이전 세션(`../pyramid-skills`, 백업) 결론. 새 세션은 이 문서부터 읽고 이어간다.

## 프레이밍

agentic coding에서
- **맥락 주입 = prior 조형** (system prompt, CLAUDE.md, memory, skill, 문서)
- **인프라(harness) = posterior update** (tool 결과, hook, 검증, 권한)

Opus 4.7 가정에서는 prompt engineering ↓, harness engineering ↑. Prior는 희소·고신호, posterior 채널은 밀도·신뢰도 우선.

기존 pyramid-skills는 이 두 축을 여러 스킬에 혼재시켜 복잡도·중복을 낳았다. 재설계에서는 **한 축당 한 엔진**으로 압축한다.

## 확정 방향

**2 skills + 1 hook + 매핑 규약**

### 1. `pyramid` — prior 엔진 (유일)
- L0~L3 문서의 확립·진화·주입 모두 담당
- 자연어 대화, 내부 상태 판독으로 init/migration/draft/improve 자동 분기
- 절차 스킬이 아닌 **prior 제작 컴패니언**. 원칙·템플릿·질문 프롬프트 제공자
- L4 코드 생성은 하지 않음. Opus 4.7은 L3 prior만 있으면 직접 코딩 가능

### 2. `pyramid-sync` — posterior 엔진 (유일)
- doc↔code drift 감지·해소 제안
- 방향 판별: code-ahead(문서 업데이트) / doc-ahead(미구현 계약)
- 범위는 변경 스코프 기준

### 3. Stop hook — 자동 drift 감지
- `PostToolUse` 아님 (빈도 폭발). **Stop**만 사용 — 응답당 1회
- 설계 원칙:
  - **Silent success**: drift 없으면 stdout 비움 + exit 0 → 토큰 0, 캐시 유지
  - **연산 오프로드**: shell script가 `git diff` + `grep`으로 판별, Claude 토큰 소비 없음
  - **출력 예산**: drift 시에도 1~2줄. 세부는 `pyramid-sync` 대화에 위임
  - **Matcher**: 변경 파일이 L3 매핑 경로일 때만 분석
- 목표 프로파일
  - drift 없는 세션: 토큰 0, 캐시 유지
  - drift 있는 세션: 1~2줄 + 캐시 1회 breakage

### 4. 매핑 규약 (prior 엔진 출력 요건)
- L3 문서 frontmatter에 `implements: [path/to/code.ts]` 필드
- hook이 O(1) 역매핑 가능해야 함
- **이 규약이 prior 엔진 출력물의 필수 스펙**

## 평가 기준

Prior 품질
- Prior S/N: 모든 토큰이 load-bearing인가
- 비파생성: 코드/문서에서 재도출 가능한 정보는 prior에 없음
- 캘리브레이션: 과·저 scaffold 없음 (Opus 4.7 가정)

Posterior 품질
- Silent success 비율 ≥ 90%
- 평균 주입 토큰/세션 < 50
- False positive < 5%
- Hook 실행 latency < 500ms

Joint
- KL(prior → posterior): 증거가 prior를 흔들 수 있는가
- 교정 amortization: 교정이 설정/memory/hook으로 굳는 비율
- 수렴 사이클 수: 올바른 행동까지 iteration

## 아직 열린 결정

1. **prior 엔진 단일화 확정 여부**  
   greenfield/brownfield 분기가 내부 추론으로 충분한지, 실제 스킬 작성 단계에서 재검토 필요.

2. **hook의 heuristic 깊이**  
   시그니처 grep / 필드 매칭 정도로 충분한가, 아니면 더 정밀한 판별이 필요한가 — 시작은 최소로.

3. **매핑 규약의 granularity**  
   파일 단위인지 심볼 단위인지. 시작은 파일 단위 권장.

4. **백업 폴더 운명**  
   `../pyramid-skills`는 참조용 백업. 재사용 가능한 템플릿·프롬프트 패턴이 있다면 추려 올 수 있음.

## 시작 순서 제안

1. 이 HANDOFF 검토 후 확정/수정
2. 매핑 규약 스펙 먼저 정의 (hook·prior 양쪽의 공통 의존)
3. `pyramid-sync` 스킬 + Stop hook 최소 구현 (posterior 엔진 먼저 — 검증 가능해지므로)
4. `pyramid` 스킬 구현 (prior 엔진)
5. 기존 pyramid-skills에서 쓸 만한 템플릿·원칙 선별 이관

## 참고

- 백업: `../pyramid-skills` (6개 pmd-* 스킬, 실험 결과)
- 사용자 메모리: `~/.claude/projects/-Users-kim-vlabcorp-pyramid-skills/memory/` — 새 프로젝트용 메모리 경로는 세션 시작 시 갱신됨. 기존 메모(특히 `feedback_*`, `project_plugin_migration_deferred`)는 여전히 유효한 원칙
