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

Claude Code 플러그인.

```
claude --plugin-dir /path/to/pmd-skills
```

또는 marketplace 등록 후 설치. 의존: `python3` (Stop hook). 플러그인 활성화 시 `pyramid`·`pyramid-sync` 스킬과 Stop hook이 자동 로드.

## 사용

- `/pyramid` — 문서 피라미드 작성·개선 대화 시작
- `/pyramid-sync` — 변경 파일 중 계약 매핑된 것의 drift 체크
- 그 외엔 자연어로 스킬을 트리거 (예: "L0 vision 다듬자", "sync 해줘", "이 모듈 L2 뽑아줘")

세부는 각 SKILL.md 참조.
