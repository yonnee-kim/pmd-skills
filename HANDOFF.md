# Next-session 핸드오프

**토픽**: pmd-skills 플러그인 배포·사용법

## 현 상태

플러그인 구조 완성, 8 커밋 누적 (최신 `896cc32`). `.claude-plugin/plugin.json` v0.1.0, skills 2개(pyramid·pyramid-sync), Stop hook, mapping-spec, shared/.

Dogfood 완료 (별도 sandbox는 이 세션에서 제거됨, 결과는 커밋+project memory에 보존).

## 다음 세션에서 탐구할 것

**1. 배포 옵션**
- `claude --plugin-dir /path/to/pmd-skills` — 로컬 dev 모드 (이전 세션에서 패턴 검증됨, project memory 참조)
- Marketplace 등록 — 공개 배포 흐름·메타데이터·review 절차
- 팀 내부 사용: git 저장소 공유 + 각자 `--plugin-dir` vs 마켓플레이스 private
- 버전 관리·업데이트 전파

**2. 사용법 (consumer 프로젝트 관점)**
- 플러그인 활성화 후 첫 호출 — `/pyramid` 언제, `/pyramid-sync` 언제
- 실제 워크플로우: init → 코딩 → drift → sync 한 사이클 구체화
- `_docs/` 디렉토리 초기 구조 사용자가 직접 만들어야 하는지 자동인지
- 여러 프로젝트에서 동시 사용 시 설정 공유 방식

**3. 검증할 것**
- `--plugin-dir`로 실제 세션 띄워 `/pyramid` 호출 가능한지
- Stop hook이 실제 세션에서 발동하는지
- `${CLAUDE_PLUGIN_ROOT}` 치환이 SKILL.md 본문에서 올바르게 작동하는지 (이전 세션 메모에 validated)

## 참고

- 플러그인 구조 검증 메모: `~/.claude/projects/-Users-kim-vlabcorp-pmd-skills/memory/project_pmd_skills_design.md`
- 이전 pyramid-skills 플러그인 실험 메모 (deferred): `~/.claude/projects/-Users-kim-vlabcorp-pyramid-skills/memory/project_plugin_migration_deferred.md` — 패턴 A/B/C 검증 결과 저장됨
