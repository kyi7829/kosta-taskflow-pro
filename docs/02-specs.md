# 02. Specs

---

## 데이터 모델 — Task

### 필드 정의

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | INTEGER (PK, AUTO_INCREMENT) | - | 자동 생성 | 고유 식별자 |
| `title` | VARCHAR(200) | **필수** | - | 업무 제목 |
| `description` | TEXT | 선택 | NULL | 업무 상세 설명 |
| `status` | ENUM | - | `todo` | 진행 상태. `todo` / `in_progress` / `done` |
| `due_at` | DATETIME (UTC) | 선택 | NULL | 마감 시각. ISO 8601 형식으로 저장 |
| `created_at` | DATETIME (UTC) | - | 자동 생성 | 레코드 생성 시각 |
| `updated_at` | DATETIME (UTC) | - | 자동 갱신 | 레코드 최종 수정 시각 |

### ERD (단순 표현)

```
Task
├── id           INTEGER  PK  AUTO_INCREMENT
├── title        VARCHAR(200)  NOT NULL
├── description  TEXT          NULL
├── status       ENUM('todo','in_progress','done')  DEFAULT 'todo'
├── due_at       DATETIME      NULL
├── created_at   DATETIME      NOT NULL
└── updated_at   DATETIME      NOT NULL
```

---

## 검증 규칙

| 조건 | 응답 코드 | 메시지 예시 |
|---|---|---|
| `title` 누락 또는 빈 문자열 | `400 Bad Request` | `"title은 필수입니다."` |
| `title` 200자 초과 | `400 Bad Request` | `"title은 200자 이내여야 합니다."` |
| `status` 허용값 외 값 | `400 Bad Request` | `"status는 todo, in_progress, done 중 하나여야 합니다."` |
| `due_at` ISO 8601 형식 위반 | `400 Bad Request` | `"due_at은 ISO 8601 형식이어야 합니다. 예) 2026-05-12T18:00:00Z"` |
| 존재하지 않는 `id` 요청 | `404 Not Found` | `"해당 Task를 찾을 수 없습니다."` |

### ISO 8601 허용 형식 예시

```
2026-05-12T18:00:00Z          # UTC 명시
2026-05-12T18:00:00+09:00     # KST 오프셋 명시
```

---

## REST API

**Base URL:** `/api/tasks`

### 1. 업무 생성

```
POST /api/tasks
```

| 항목 | 내용 |
|---|---|
| 성공 응답 | `201 Created` |
| Request Body | `title`(필수), `description`(선택), `status`(선택), `due_at`(선택) |
| Response Body | 생성된 Task 전체 필드 (description 포함) |

**Request 예시**
```json
{
  "title": "디자인 시안 검토",
  "description": "Figma 링크 확인 후 피드백 작성",
  "status": "todo",
  "due_at": "2026-05-12T18:00:00Z"
}
```

**Response 예시**
```json
{
  "id": 1,
  "title": "디자인 시안 검토",
  "description": "Figma 링크 확인 후 피드백 작성",
  "status": "todo",
  "due_at": "2026-05-12T18:00:00Z",
  "created_at": "2026-05-14T09:00:00Z",
  "updated_at": "2026-05-14T09:00:00Z"
}
```

---

### 2. 업무 목록 조회

```
GET /api/tasks
```

| 항목 | 내용 |
|---|---|
| 성공 응답 | `200 OK` |
| 특이사항 | `description` 필드 **제외**. 목록 성능 최적화 |
| 정렬 | `created_at` 내림차순 (최신순) |

**Response 예시**
```json
[
  {
    "id": 1,
    "title": "디자인 시안 검토",
    "status": "todo",
    "due_at": "2026-05-12T18:00:00Z",
    "created_at": "2026-05-14T09:00:00Z",
    "updated_at": "2026-05-14T09:00:00Z"
  }
]
```

---

### 3. 업무 단건 조회

```
GET /api/tasks/:id
```

| 항목 | 내용 |
|---|---|
| 성공 응답 | `200 OK` |
| 특이사항 | `description` 필드 **포함** |
| 없는 id | `404 Not Found` |

**Response 예시**
```json
{
  "id": 1,
  "title": "디자인 시안 검토",
  "description": "Figma 링크 확인 후 피드백 작성",
  "status": "todo",
  "due_at": "2026-05-12T18:00:00Z",
  "created_at": "2026-05-14T09:00:00Z",
  "updated_at": "2026-05-14T09:00:00Z"
}
```

---

### 4. 업무 수정

```
PUT /api/tasks/:id
```

| 항목 | 내용 |
|---|---|
| 성공 응답 | `200 OK` |
| 특이사항 | **부분 수정** 허용. 전달한 필드만 업데이트. `updated_at` 자동 갱신 |
| 없는 id | `404 Not Found` |

**Request 예시** (status만 변경하는 경우)
```json
{
  "status": "in_progress"
}
```

**Response 예시**
```json
{
  "id": 1,
  "title": "디자인 시안 검토",
  "description": "Figma 링크 확인 후 피드백 작성",
  "status": "in_progress",
  "due_at": "2026-05-12T18:00:00Z",
  "created_at": "2026-05-14T09:00:00Z",
  "updated_at": "2026-05-14T10:30:00Z"
}
```

---

### 5. 업무 삭제

```
DELETE /api/tasks/:id
```

| 항목 | 내용 |
|---|---|
| 성공 응답 | `204 No Content` |
| Response Body | 없음 |
| 없는 id | `404 Not Found` |

---

### API 요약표

| Method | Endpoint | 성공 코드 | description 포함 |
|---|---|---|---|
| `POST` | `/api/tasks` | `201` | O |
| `GET` | `/api/tasks` | `200` | X |
| `GET` | `/api/tasks/:id` | `200` | O |
| `PUT` | `/api/tasks/:id` | `200` | O |
| `DELETE` | `/api/tasks/:id` | `204` | - |

---

## 화면 명세 — CRUD 4종 UI

### 추가 — 업무 생성 폼

| 요소 | 상세 |
|---|---|
| **입력 필드** | `title` (텍스트, 필수) / `due_at` (날짜+시간 picker) / `status` (select: todo·in_progress·done) |
| **제출** | 폼 하단 "추가" 버튼. `title` 비어 있으면 버튼 비활성화 |
| **성공** | 목록에 즉시 반영. 폼 초기화 |
| **실패** | 서버 400 응답 시 필드 하단에 오류 메시지 표시 |

---

### 목록 — 업무 카드 리스트

| 요소 | 상세 |
|---|---|
| **카드 구성** | `title` / `status` 배지 / 마감 시각 `D-N HH:MM` |
| **status 배지** | `todo` 회색 / `in_progress` 파란색 / `done` 초록색 |
| **마감 표시** | `due_at` 기준. 오늘이면 `D-0 18:00`, 3일 후면 `D-3 18:00` 형식 |
| **마감 초과** | `due_at`이 현재보다 이전이면 빨간색으로 강조 표시 |
| **due_at 없음** | 마감 시각 영역 비워둠 (빈 칸) |

---

### 수정 — 카드 클릭 → 모달

| 요소 | 상세 |
|---|---|
| **진입** | 업무 카드 클릭 시 수정 모달 열림 |
| **모달 내용** | `title` / `description` (textarea) / `status` / `due_at` 편집 가능 |
| **저장** | "저장" 버튼 → `PUT /api/tasks/:id` 호출 → 모달 닫힘, 목록 갱신 |
| **취소** | "취소" 버튼 또는 모달 바깥 클릭 → 변경 사항 미저장, 모달 닫힘 |

---

### 삭제 — 휴지통 아이콘 → 확인 → DELETE

| 요소 | 상세 |
|---|---|
| **진입** | 카드 내 휴지통(🗑) 아이콘 클릭 |
| **확인** | "정말 삭제하시겠습니까?" 확인 다이얼로그 표시 |
| **확인 시** | `DELETE /api/tasks/:id` 호출 → 목록에서 즉시 제거 |
| **취소 시** | 아무 동작 없이 다이얼로그 닫힘 |
