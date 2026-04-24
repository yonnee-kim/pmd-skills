# pmd-skills

프로젝트 문서를 3레이어(L0 Vision / L1 원칙·제약 / L2 모듈 계약)로 쌓고 문서↔코드 drift를 자동 감지·해소 제안하는 Claude Code 플러그인. 두 스킬(`pyramid`, `pyramid-sync`)과 응답 끝마다 도는 Stop hook으로 구성.

새 프로젝트에선 질문형 대화로 비전·원칙·모듈 계약을 점진적으로 확립. 기존 대형 프로젝트에선 코드에서 거꾸로 계약을 뽑아낸다(distill). 코드를 바꾸고 문서를 안 바꾸면 응답 끝마다 한 줄로 알림이 오니, 커밋 전에 자연스럽게 sync 루틴이 생긴다.

시그니처·알고리즘은 코드가 진실 소스 — 문서엔 공개 경계·책임·invariant만 둔다.

## 설치

```
claude plugin marketplace add yonnee-kim/pmd-skills
claude plugin install pmd-skills@pmd-skills
```

user scope. 모든 프로젝트에서 즉시 활성. 의존: `python3` (Stop hook).

## 첫 사이클

빈 프로젝트에서 Claude Code 세션을 열고:

1. **"L0 vision 시작하자"** — `pyramid` init 모드가 4가지 질문(정체성·기존 도구 한계·성공 기준·범위 경계). 답을 받아 `_docs/L0-vision/` 아래 Write
2. **"L1 가자"** — 기술 원칙·절대 제약·v1 범위. 주제별 분할
3. **"첫 모듈 L2"** — 구현할 모듈 하나만. `_docs/L2-spec/modules/{module}.md` + frontmatter `implements: [src/...]`
4. **코드 작성** — L2 모듈 문서를 prior로 구현
5. **응답 끝마다 Stop hook** — 매핑 파일이 `git diff`에 있으면 한 줄: `pyramid-sync: N changed file(s) mapped to contract doc(s) — run /pyramid-sync to review`
6. **"sync 해줘"** — `/pyramid-sync`가 방향(아래) 판별, 한 파일씩 수정 제안. 자동 Edit 없음
7. **커밋** — drift 해소 후 커밋. hook은 커밋 전까진 계속 울림 (인식 시점 = 커밋 경계)

## drift 방향

- `code-ahead` — 코드에 새 export, 문서 누락
- `doc-ahead` — 문서 계획, 코드 없음 (정상 lifecycle일 수 있음)
- `divergent` — 이름 같음, 책임·불변식 어긋남
- `path-stale` — `implements:` 경로에 파일 없음 (rename·삭제)

## 기존 프로젝트에 도입

"이 코드에서 L2 계약 뽑아줘" → `pyramid`의 distill whole-project 모드. 디렉토리 트리 스캔 → 모듈 경계 후보 제시 → 사용자 확정 → 모듈별 L2 스텁 Write (시그니처 생략, 공개 경계 이름만). L1·L0은 코드만으로 추정하지 않고 대화로 확립. 이후 Stop hook + sync가 점진적으로 drift 보정.

## 문제 해결

- **hook이 안 뜸** — `PYRAMID_SYNC_DEBUG=1 python3 ${CLAUDE_PLUGIN_ROOT}/hooks/pyramid-sync-check.py` 실행. stderr에 단계별 결과. 흔한 원인: `implements:` 필드 누락·YAML 오타·새 `.md`가 `git add` 전
- **타입 필드 추가가 drift로 잡힘?** 아님. L2는 필드 수준 명세를 안 한다. 타입 이름 자체가 export/제거될 때만 drift
- **시그니처 차이가 drift?** 아님. 문서엔 시그니처 복붙 금지 — 이름·불변식 수준에서만 비교

## 업데이트

```
claude plugin update pmd-skills@pmd-skills
```

같은 version 내 commit 변경은 감지되지 않음 — 레포에서 version bump 후 업데이트되거나, `uninstall` → `install`.

## 더 알기

각 스킬의 `SKILL.md` 본문이 동작·모드·Gotchas까지 담고 있다. 경로:

```
~/.claude/plugins/cache/pmd-skills/pmd-skills/0.1.0/skills/pyramid/SKILL.md
~/.claude/plugins/cache/pmd-skills/pmd-skills/0.1.0/skills/pyramid-sync/SKILL.md
```
