# CLAUDE.md (pmd-skills 레포용)

이 레포는 `pyramid`/`pyramid-sync` 스킬 본체. 소비 프로젝트의 `_docs/`·소스가 아니라 **스킬 파일 자체**가 산출물.

## 편집 원칙

1. **prior–posterior 분리 유지** — 스킬 한 개가 두 축을 섞지 않는다. 섞이려는 변화는 구조 재설계 신호
2. **opus 4.7 가정 간결함** — 자명한 단계·중복 체크리스트·장황한 종료 조건 금지. 모든 문장이 load-bearing
3. **단일 진실의 원천** — `shared/mapping-spec.md`는 hook과 스킬이 공유하는 단일 정본 (SKILL.md 참조는 `${CLAUDE_PLUGIN_ROOT}/shared/mapping-spec.md`). 복붙 금지
4. **자동 동기화 선호** — 수동 status 게이트·top-down RFI cascade를 도입하지 말 것. 자동 drift 감지로 해결
5. **표 형식 금지** — 스킬·문서 어디에도 markdown 표(`|---|`) 쓰지 말 것. 행당 한 줄 리스트로. 셀 폭 정렬에 시선 낭비되고 편집 시 깨지기 쉬움

## 파일 맵 (Claude Code 플러그인)

- `.claude-plugin/plugin.json` — 플러그인 매니페스트
- `skills/pyramid/` — prior 엔진 (SKILL.md + layers/L{0..3}.md)
- `skills/pyramid-sync/` — posterior 엔진 (SKILL.md)
- `hooks/hooks.json` — Stop hook 선언
- `hooks/pyramid-sync-check.py` — Stop hook 스크립트
- `shared/mapping-spec.md` — 매핑 규약 (hook·skill 공통 참조, `${CLAUDE_PLUGIN_ROOT}/shared/mapping-spec.md`)

## 테스트

Hook 동작 확인 (직접 실행, 플러그인 로드 없이):

```
# silent (매핑 없음)
python3 hooks/pyramid-sync-check.py; echo $?

# positive (임시 레포에 L3 + implements 추가 후)
```

## 스킬 자체를 개선할 때

이전 `pyramid-skills`의 `pmd-improve` 같은 메타 스킬을 두지 않음. 편집은 직접. 반복 이슈가 보이면 "구조 변경 선호" 원칙에 따라 구조안부터 제시.
