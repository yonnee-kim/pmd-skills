# CLAUDE.md (pmd-skills 레포용)

이 레포는 `pyramid`/`pyramid-sync` 스킬 본체. 소비 프로젝트의 `_docs/`·소스가 아니라 **스킬 파일 자체**가 산출물.

## 편집 원칙

1. **prior–posterior 분리 유지** — 스킬 한 개가 두 축을 섞지 않는다. 섞이려는 변화는 구조 재설계 신호
2. **opus 가정 간결함** — 자명한 단계·중복 체크리스트·장황한 종료 조건 금지. 모든 문장이 load-bearing
3. **단일 진실의 원천** — `shared/mapping-spec.md`는 hook과 스킬이 공유하는 단일 정본. 복붙 금지
4. **자동 동기화 선호** — 수동 status 게이트·top-down RFI cascade를 도입하지 말 것. 자동 drift 감지로 해결

## 파일 맵

- `.claude/skills/pyramid/` — prior 엔진 (SKILL.md + layers/L{0..3}.md)
- `.claude/skills/pyramid-sync/` — posterior 엔진 (SKILL.md)
- `.claude/hooks/pyramid-sync-check.py` — Stop hook
- `.claude/settings.json` — hook 등록
- `shared/mapping-spec.md` — 매핑 규약 (hook·skill 공통 참조)

## 테스트

Hook 동작 확인:
```
# silent (매핑 없음)
python3 .claude/hooks/pyramid-sync-check.py; echo $?

# positive (임시 레포에 L3 + implements 추가 후)
```

## 스킬 자체를 개선할 때

이전 `pyramid-skills`의 `pmd-improve` 같은 메타 스킬을 두지 않음. 편집은 직접. 반복 이슈가 보이면 "구조 변경 선호" 원칙에 따라 구조안부터 제시.
