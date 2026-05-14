# 03. Design Decisions

> 이 문서는 기술·설계 결정의 근거를 기록한다.
> **새로운 의존성을 도입하기 전, 반드시 이 문서에 사유를 먼저 작성해야 한다.**

---

## 기술 결정표

### 1. 백엔드 프레임워크

| 항목 | 내용 |
|---|---|
| **선택** | FastAPI |
| **대안** | Django, Express |
| **근거** | 타입 힌트 기반 자동 유효성 검사, 자동 생성 OpenAPI 문서, 비동기 지원으로 확장성 확보. Python 생태계 유지로 데이터 처리 라이브러리 연동 용이 |
| **트레이드오프** | Django 대비 내장 기능(admin, ORM, auth)이 없어 직접 구성 필요. 팀에 Python 경험 없으면 Express보다 러닝커브 존재 |

---

### 2. 프론트엔드

| 항목 | 내용 |
|---|---|
| **선택** | Vanilla JS + Tailwind CSS CDN |
| **대안** | React, Vue |
| **근거** | MVP 규모(단일 페이지, 단순 CRUD)에서 프레임워크 오버헤드 불필요. 빌드 도구 없이 브라우저에서 즉시 실행. 학습·유지보수 비용 최소화 |
| **트레이드오프** | 컴포넌트 재사용·상태 동기화를 수동으로 관리해야 함. 기능 확장 시 React 등으로 마이그레이션 비용 발생 가능 |

---

### 3. 데이터베이스

| 항목 | 내용 |
|---|---|
| **선택** | SQLite (개발) → PostgreSQL (운영) + SQLAlchemy ORM |
| **대안** | MySQL, MongoDB |
| **근거** | SQLite는 설치·설정 없이 즉시 사용 가능해 개발 속도 최대화. SQLAlchemy로 ORM 레이어를 추상화하면 운영 전환 시 DB 교체 비용 최소화 |
| **트레이드오프** | SQLite는 동시 쓰기에 취약(Write Lock). 운영 전환을 빠뜨리면 SQLite가 그대로 배포될 위험 있음. 환경변수로 DB URL을 반드시 분리해야 함 |

---

### 4. CSS 방식

| 항목 | 내용 |
|---|---|
| **선택** | Tailwind CSS 단독 사용 |
| **대안** | styled-components, CSS Modules, 순수 CSS |
| **근거** | 유틸리티 클래스로 별도 CSS 파일 없이 인라인 스타일링 가능. macOS UI 토큰(`rounded-xl`, `shadow-lg`, `backdrop-blur`)을 클래스 조합만으로 표현. CDN 방식으로 빌드 설정 불필요 |
| **트레이드오프** | HTML 마크업에 클래스가 많아져 가독성 저하 가능. 동적 스타일(JS 연동 복잡 케이스)은 별도 처리 필요. **styled-components는 이 프로젝트에서 사용 금지** (빌드 도구 필요, Vanilla JS와 충돌) |

---

### 5. 실시간 데이터 동기화

| 항목 | 내용 |
|---|---|
| **선택** | 폴링 3초 간격 (MVP) |
| **대안** | WebSocket, Server-Sent Events |
| **근거** | MVP 범위에서 구현 복잡도 최소화. 3초 폴링은 10명 규모 팀에서 체감 지연이 없으며, 서버 부하도 허용 범위 이내 |
| **트레이드오프** | 변경 없을 때도 불필요한 요청 발생. 팀 규모 확장 시 서버 부하 증가. WebSocket은 확장 단계(JWT 로그인 도입 후)로 보류 |

---

### 6. 프론트엔드 상태 관리

| 항목 | 내용 |
|---|---|
| **선택** | 모듈 변수 + DOM 직접 갱신 |
| **대안** | Redux, Zustand, MobX, Context API |
| **근거** | Vanilla JS 환경에서 외부 상태 라이브러리 도입 시 번들러 필요. 단순 CRUD 목록은 모듈 스코프 변수(`let tasks = []`)로 충분히 관리 가능 |
| **트레이드오프** | 상태와 DOM이 분리되지 않아 기능 증가 시 동기화 버그 위험. 추후 React 마이그레이션 시 상태 로직 재작성 필요 |

---

### 7. 디자인 시스템

| 항목 | 내용 |
|---|---|
| **선택** | macOS UI 톤 자체 구성 |
| **대안** | Material Design, Ant Design |
| **근거** | 외부 디자인 시스템 의존 없이 Tailwind 토큰 조합만으로 macOS 특유의 정돈된 느낌 구현 가능. 번들 크기 최소화 |
| **트레이드오프** | 컴포넌트를 직접 만들어야 하므로 초기 구현 비용 발생. 접근성(ARIA) 속성도 직접 챙겨야 함 |

**적용 디자인 토큰**

| 토큰 | Tailwind 클래스 | 역할 |
|---|---|---|
| 둥근 모서리 | `rounded-xl` | 카드, 버튼, 모달 모서리 |
| 부드러운 그림자 | `shadow-lg` | 카드 및 모달 깊이감 |
| 반투명 배경 | `backdrop-blur-md` | 카드 배경 블러 효과 |
| 시스템 폰트 | `font-sans` (CSS: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`) | 전체 폰트 |
| 터치 타깃 | `min-h-[44px] min-w-[44px]` | 버튼, 아이콘 등 인터랙션 요소 최소 크기 |

---

### 8. 테마 (라이트 / 다크)

| 항목 | 내용 |
|---|---|
| **선택** | Tailwind `dark:` 변형 + `localStorage('theme')` |
| **대안** | CSS 변수 수동 토글, 별도 테마 라이브러리 |
| **근거** | Tailwind의 `dark:` 유틸리티로 추가 CSS 없이 다크 스타일 선언 가능. `localStorage`로 새로고침 후에도 선택 유지 |
| **트레이드오프** | Tailwind CDN 방식에서 `darkMode: 'class'` 설정이 기본 비활성화되어 있어 `<html>` 태그에 `dark` 클래스를 JS로 수동 제어해야 함 |

**테마 초기화 로직**

```js
// 페이지 로드 시 실행 (깜빡임 방지를 위해 <head> 최상단에 배치)
const saved = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
if (saved === 'dark' || (!saved && prefersDark)) {
  document.documentElement.classList.add('dark');
}
```

- `localStorage('theme')` 저장값 우선 적용
- 저장값 없을 경우 `prefers-color-scheme` 시스템 설정을 초기값으로 사용
- 토글 시 `localStorage`에 `'light'` 또는 `'dark'` 저장

---

## 의존성 추가 정책

> **새로운 라이브러리·패키지 도입 전, 이 문서(`03-design.md`)에 결정표 항목을 먼저 작성해야 한다.**
> 사유 없이 의존성을 추가하는 것은 절대 규칙 위반(돌발 의존성 금지)에 해당한다.

### 도입 절차

1. `03-design.md`에 결정 항목 추가 (선택 / 대안 / 근거 / 트레이드오프)
2. 사용자 승인
3. 패키지 설치 및 구현

### 판단 기준

| 질문 | 기준 |
|---|---|
| 이 기능을 직접 구현할 수 있는가? | 30줄 이내로 가능하면 직접 구현 |
| 번들러 없이 동작하는가? | Vanilla JS 환경이므로 빌드 도구 불필요한 것만 허용 |
| 마지막 릴리스가 1년 이내인가? | 관리되지 않는 라이브러리 금지 |
| 라이선스가 상업적 사용 가능한가? | MIT, Apache 2.0 등만 허용 |
