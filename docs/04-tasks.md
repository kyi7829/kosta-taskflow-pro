# 04. Tasks

> MVP를 3개 Phase로 순서대로 진행한다.
> **병렬 작업 금지. 각 단계의 검증을 통과해야 다음 단계로 넘어간다.**

---

## 진행 규칙

| 규칙 | 내용 |
|---|---|
| 순서 준수 | Phase 1 → Phase 2 → Phase 3 순서대로만 진행 |
| 병렬 금지 | 이전 단계 검증 완료 전에 다음 단계 착수 불가 |
| 단계별 검증 필수 | 각 단계의 검증 방법을 실제로 확인한 후 ✅ 표시 |
| 확장 단계 제외 | JWT 로그인, Kanban 등 확장 기능은 이 문서에서 다루지 않는다 |

---

## Phase 1 — 설계 `완료`

> CLAUDE.md 및 docs/ 6종 문서 작성. 프로젝트의 모든 결정 근거를 문서화한다.

| # | 작업 | 검증 방법 | 상태 |
|---|---|---|---|
| 1 | Git 저장소 초기화 및 로컬 사용자 설정 | `git config --local --list` 에서 name·email 확인 | ✅ |
| 2 | GitHub 원격 저장소 연결 | `git remote -v` 에서 origin URL 확인 | ✅ |
| 3 | `.gitignore` 작성 (node_modules, .env, .claude/ 등) | `.claude/` 수정 후 `git status` 에 미추적으로 나타나는지 확인 | ✅ |
| 4 | `CLAUDE.md` 운영 지침 작성 (역할·절대규칙·모호한요청 처리) | 파일 열어 5개 절대 규칙 항목 육안 확인 | ✅ |
| 5 | `docs/00-overview.md` 작성 (문서 지도·읽는 순서·분리 이유) | 파일 열어 매핑표 6행 확인 | ✅ |
| 6 | `docs/01-product.md` 작성 (목표·페르소나·MVP 범위·성공 기준) | 파일 열어 성공 기준 5항목 확인 | ✅ |
| 7 | `docs/02-specs.md` 작성 (데이터 모델·API 명세·화면 명세) | 파일 열어 API 5종 엔드포인트 확인 | ✅ |
| 8 | `docs/03-design.md` 작성 (기술 결정 8종·의존성 추가 정책) | 파일 열어 결정표 8행 확인 | ✅ |
| 9 | `docs/04-tasks.md` 작성 (이 파일 — Phase 1·2·3 체크리스트) | 파일 열어 Phase 3까지 항목 존재 확인 | ✅ |
| 10 | `docs/05-conventions.md` 작성 + 전체 원격 push | `git log --oneline` 에서 커밋 6종 이상 확인, GitHub에서 docs/ 폴더 노출 확인 | ⬜ |

---

## Phase 2 — 백엔드

> `backend/` 디렉토리에 FastAPI 앱을 구성하고 CRUD API 5개를 구현한다.
> Swagger UI(`/docs`)에서 모든 엔드포인트가 정상 동작해야 Phase 완료.

| # | 작업 | 검증 방법 | 상태 |
|---|---|---|---|
| 1 | `backend/` 폴더 구조 생성 (`app/`, `tests/` 등) | `ls backend/` 에서 디렉토리 구조 확인 | ⬜ |
| 2 | Python 가상환경(venv) 생성 및 패키지 설치 (`fastapi`, `uvicorn`, `sqlalchemy`, `pytest`) | `pip list` 에서 4개 패키지 확인 | ⬜ |
| 3 | FastAPI 앱 진입점 `main.py` 작성 및 서버 기동 | `uvicorn app.main:app --reload` 실행 후 `http://localhost:8000/docs` 접속 확인 | ⬜ |
| 4 | SQLAlchemy Task 모델 정의 (7개 필드, `02-specs.md` 기준) | Python REPL에서 모델 import 오류 없음 확인 | ⬜ |
| 5 | DB 초기화 (`create_all`) 및 SQLite 파일 생성 확인 | `ls backend/` 에서 `.db` 파일 존재 확인 | ⬜ |
| 6 | `POST /api/tasks` 구현 (201, title 필수 검증, due_at ISO 8601 검증) | Swagger에서 정상 title → 201, 빈 title → 400 확인 | ⬜ |
| 7 | `GET /api/tasks` 구현 (200, description 제외, created_at 내림차순) | Swagger에서 목록 조회 후 description 필드 없음 확인 | ⬜ |
| 8 | `GET /api/tasks/{id}` 구현 (200, description 포함, 없는 id → 404) | Swagger에서 존재 id → 200·description 포함, 없는 id → 404 확인 | ⬜ |
| 9 | `PUT /api/tasks/{id}` 구현 (200, 부분 수정, updated_at 자동 갱신) | Swagger에서 status만 전송 후 updated_at 변경 확인 | ⬜ |
| 10 | `DELETE /api/tasks/{id}` 구현 (204, 없는 id → 404) + pytest 전체 통과 | `pytest` 실행 시 PASSED 확인, Swagger에서 DELETE 후 GET 목록에서 제거 확인 | ⬜ |

---

## Phase 3 — 프론트엔드

> `frontend/` 디렉토리에 Vanilla JS + Tailwind CDN으로 UI를 구성하고 백엔드 API에 연결한다.

| # | 작업 | 검증 방법 | 상태 |
|---|---|---|---|
| 1 | `frontend/` 폴더 구조 생성 및 `index.html` 기본 레이아웃 작성 (Tailwind CDN, 시스템 폰트, macOS 톤) | 브라우저에서 `index.html` 열어 레이아웃 깨짐 없음 확인 | ⬜ |
| 2 | 라이트/다크 테마 토글 구현 (`localStorage('theme')`, `prefers-color-scheme` 초기값) | 토글 클릭 → 테마 전환, 새로고침 후 테마 유지 확인 | ⬜ |
| 3 | 업무 추가 폼 구현 (`title` 필수, `due_at` 날짜+시간 picker, `status` select) | title 비운 채 제출 시 버튼 비활성화 또는 오류 메시지 확인 | ⬜ |
| 4 | 업무 목록 카드 렌더링 구현 (status 배지, D-N HH:MM 마감 표시, 마감 초과 시 빨간색) | 마감 지난 항목이 빨간색으로 표시되는지 확인 | ⬜ |
| 5 | 수정 모달 구현 (카드 클릭 → 모달 오픈, 저장/취소, 모달 바깥 클릭 닫힘) | 카드 클릭 → 모달 열림, 바깥 클릭 → 닫힘, 저장 후 목록 갱신 확인 | ⬜ |
| 6 | 삭제 확인 다이얼로그 구현 (휴지통 아이콘 → 확인 → 목록에서 즉시 제거) | 삭제 후 목록에서 해당 카드 사라짐 확인 | ⬜ |
| 7 | 백엔드 API 연결 + 3초 폴링 구현 | 브라우저 Network 탭에서 3초마다 `GET /api/tasks` 요청 확인, 응답 200ms 이내 확인 | ⬜ |
| 8 | 360px 반응형 검증 + 전체 성공 기준 점검 + `git push` | 브라우저 DevTools에서 360px 너비로 레이아웃 깨짐 없음 확인, `01-product.md` 성공 기준 5항목 체크 후 push | ⬜ |

---

## 진행 현황 요약

| Phase | 이름 | 진행률 | 상태 |
|---|---|---|---|
| Phase 1 | 설계 | 9 / 10 | 진행 중 |
| Phase 2 | 백엔드 | 0 / 10 | 대기 |
| Phase 3 | 프론트엔드 | 0 / 8 | 대기 |
