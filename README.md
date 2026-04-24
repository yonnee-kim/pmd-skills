# pmd-skills

Prior–posterior 축으로 분리된 문서 피라미드 방법론. Opus 4.7 가정.

## 구조

- **`pyramid`** (prior 엔진) — 3레이어 문서(L0 Vision / L1 Principles / L2 Modules) 작성·개선·distill 컴패니언. 시그니처·구현은 코드(L4) 진실 소스
- **`pyramid-sync`** (posterior 엔진) — doc↔code drift 감지·해소 제안
- **Stop hook** — 응답 끝마다 자동 drift 체크 (silent success, 매핑 있을 때만 1줄)
- **매핑 규약** — 계약 문서(L2 모듈) frontmatter `implements:` 필드가 단일 정본 (`shared/mapping-spec.md`)

이전 `pyramid-skills`(6개 pmd-* 스킬)의 재설계. 백업은 `../pyramid-skills/`.

## 왜

Agentic coding에서 **맥락 주입 = prior**(system/skill/docs), **인프라 = posterior**(tool result, hook, verification). 두 축을 섞으면 각 스킬의 책임 경계가 흐려지고 중복이 쌓인다. 여기선 한 축당 한 엔진.

Opus 4.7 가정에서 prompt engineering ↓ harness engineering ↑. prior는 희소·고신호, posterior는 밀도·신뢰도 우선.

## 설치

Claude Code에서:

```
/plugin marketplace add yonnee-kim/pmd-skills
/plugin install pmd-skills@pmd-skills
```

의존: `python3` (Stop hook). 활성화 시 `pyramid`·`pyramid-sync` 스킬과 Stop hook 자동 로드.

## 업데이트

레포에 새 커밋이 올라간 뒤:

```
/plugin marketplace update pmd-skills
/plugin update pmd-skills@pmd-skills
```

## 사용

- `/pyramid` — 문서 피라미드 작성·개선 대화 시작
- `/pyramid-sync` — 변경 파일 중 계약 매핑된 것의 drift 체크
- 그 외엔 자연어로 스킬을 트리거 (예: "L0 vision 다듬자", "sync 해줘", "이 모듈 L2 뽑아줘")

### 한 사이클

1. **init** — 새 프로젝트에서 "L0 vision 시작하자" → `pyramid` init 모드가 대화로 L0부터 채움. `_docs/L0-vision/`은 스킬이 사용자 답 받은 뒤 Write (미리 만들 필요 없음)
2. **레이어 쌓기** — L0 승인 후 L1(원칙·제약·범위), L2(모듈) 순. L2는 구현할 모듈만 수직 슬라이싱 — 한 번에 전부 쓰지 말 것
3. **코드 작성** — L2 모듈 문서를 prior로 코드 작성. `implements: [...]` frontmatter 필수 (없으면 drift 미탐지)
4. **drift** — 응답 끝마다 Stop hook이 체크. 매핑된 파일이 `git diff`에 있으면 1줄: `pyramid-sync: N changed file(s) mapped to contract doc(s) — run /pyramid-sync to review`
5. **sync** — `/pyramid-sync` → 방향(code-ahead/doc-ahead/divergent/path-stale) 판별, 한 파일씩 제안. 자동 Edit 없음
6. **commit** — drift 해소 후 커밋. 커밋 전까진 hook이 계속 울림 (인식 시점이 커밋 경계 — 버그 아님)

### Notes

- 마켓플레이스 설치는 user scope(모든 프로젝트 공용). 프로젝트별 설정 불필요
- 스킬 자체를 로컬에서 고쳐가며 테스트할 때만 `claude --plugin-dir /path/to/pmd-skills`
- hook 진단: `PYRAMID_SYNC_DEBUG=1 python3 ${CLAUDE_PLUGIN_ROOT}/hooks/pyramid-sync-check.py` (stderr에 단계별 결과)

세부는 각 SKILL.md 참조.
