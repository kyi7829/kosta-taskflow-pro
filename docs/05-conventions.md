# 05. Conventions

> 이 문서는 코드 작성·커밋·테스트의 모든 규칙을 정의한다.
> 모든 기여는 이 문서의 기준을 따른다.

---

## 명명 규칙

### 케이스 규칙

| 대상 | 규칙 | 예시 |
|---|---|---|
| 백엔드 변수·함수·파일명 | `snake_case` | `task_id`, `get_task_list`, `task_router.py` |
| 프론트엔드 변수·함수 | `camelCase` | `taskId`, `getTaskList`, `renderCard` |
| 컴포넌트·클래스명 | `PascalCase` | `TaskCard`, `ModalDialog`, `TaskService` |
| 상수 | `UPPER_SNAKE_CASE` | `MAX_TITLE_LENGTH`, `API_BASE_URL` |
| DB 테이블·컬럼 | `snake_case` | `tasks`, `due_at`, `created_at` |
| CSS 클래스 | Tailwind 유틸리티 클래스 우선. 커스텀 필요 시 `kebab-case` | `task-card`, `modal-overlay` |

### 언어 규칙

| 대상 | 언어 |
|---|---|
| 변수·함수·클래스·파일명 등 모든 식별자 | **영어** |
| 코드 내 주석 | **한국어** |
| 커밋 메시지 본문 요약 | **한국어** |
| 문서(`docs/`) | **한국어** |

---

## 금지 항목

> 아래 5가지는 코드 리뷰에서 즉시 반려된다.

| 금지 | 이유 | 대안 |
|---|---|---|
| `print()` 디버깅 | 운영 환경에 노이즈 유입. 민감 정보 노출 위험 | `logging` 모듈 사용 (`logger.debug()`, `logger.info()`) |
| `bare except:` | 모든 예외를 삼켜 디버깅 불가. 시스템 예외(`KeyboardInterrupt` 등)까지 차단 | `except SpecificError as e:` 로 예외 종류 명시 |
| 비밀번호·API 키 하드코딩 | 코드 유출 시 보안 사고 직결. git 기록에 영구 남음 | `.env` 파일 + `os.getenv('KEY')` 사용. `.env`는 `.gitignore`에 포함 |
| `any` 타입 (TypeScript) | 타입 안전성 무력화. 컴파일러가 오류를 잡지 못함 | 명시적 타입 또는 `unknown` + 타입 가드 사용 |
| `!important` (CSS) | 우선순위 체계 붕괴. 이후 스타일 재정의 불가 | 셀렉터 구체성(specificity)을 높이거나 Tailwind 유틸리티 클래스 조합으로 해결 |

---

## 테스트 규칙

### 도구

| 항목 | 내용 |
|---|---|
| **프레임워크** | `pytest` |
| **위치** | `backend/tests/` |
| **파일명** | `test_*.py` 형식 |
| **실행 명령** | `pytest` (루트 또는 `backend/` 에서 실행) |

### 필수 테스트 케이스

모든 API 엔드포인트에 대해 아래 케이스를 **반드시** 작성한다.

| 케이스 유형 | 설명 | 예시 |
|---|---|---|
| **정상 케이스** | 올바른 입력으로 기대 응답 코드 반환 확인 | `POST /api/tasks` → `201` |
| **404 케이스** | 존재하지 않는 id 요청 시 404 반환 확인 | `GET /api/tasks/99999` → `404` |
| **400 케이스** | 잘못된 입력(필수 필드 누락, 형식 오류) 시 400 반환 확인 | `POST /api/tasks` (title 없음) → `400` |

### 테스트 작성 원칙

```python
# 테스트 함수명은 검증 대상을 명확히 표현한다
def test_create_task_returns_201_with_valid_data():
    ...

def test_create_task_returns_400_when_title_is_missing():
    ...

def test_get_task_returns_404_when_id_not_found():
    ...
```

- 테스트 함수명에 기대 동작을 포함한다 (`test_동사_조건_기대결과`)
- 테스트마다 독립적인 DB 상태를 유지한다 (픽스처로 초기화)
- 기능 구현 후 관련 테스트가 통과해야 완료로 간주한다 (절대 규칙 3번)

---

## Git 커밋 규칙

### 커밋 메시지 형식

```
<type>: <한국어 요약>

<선택: 본문 설명>
```

### 타입 정의

| 타입 | 사용 시점 | 예시 |
|---|---|---|
| `feat` | 새로운 기능 추가 | `feat: Task 생성 API 구현` |
| `fix` | 버그 수정 | `fix: due_at 시간대 변환 오류 수정` |
| `docs` | 문서 변경 (코드 변경 없음) | `docs: 04-tasks.md Phase 2 항목 갱신` |
| `refactor` | 기능 변경 없는 코드 구조 개선 | `refactor: Task 서비스 레이어 분리` |
| `test` | 테스트 코드 추가·수정 | `test: DELETE API 404 케이스 추가` |
| `chore` | 빌드 설정, 패키지 관리 등 | `chore: requirements.txt 업데이트` |

### 규칙

| 규칙 | 내용 |
|---|---|
| 요약 길이 | 50자 이내 |
| 언어 | 타입은 영어 소문자, 요약은 한국어 |
| 단위 | 하나의 커밋은 하나의 논리적 변경만 포함 |
| 본문 | 변경 이유가 비자명한 경우에만 작성. "무엇"이 아닌 "왜"를 설명 |
