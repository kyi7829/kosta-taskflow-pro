"""
프론트엔드 E2E 테스트 — pytest-playwright
사전 조건: uvicorn이 http://localhost:8000 에서 실행 중이어야 함
검증 범위: 01-product.md 성공 기준 5항목 + CRUD UI 동작
"""
import time
import pytest
import httpx
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


# ─── 세션 픽스처: 서버 기동 여부 확인 ────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def check_server():
    try:
        httpx.get(f"{BASE_URL}/api/tasks", timeout=3)
    except Exception:
        pytest.skip("서버가 실행 중이지 않습니다. uvicorn을 먼저 시작하세요.")


# ─── 테스트별 DB 초기화 ───────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def clean_db():
    """각 테스트 전/후 실 서버의 태스크 전체 삭제"""
    def _cleanup():
        with httpx.Client() as client:
            tasks = client.get(f"{BASE_URL}/api/tasks").json()
            for task in tasks:
                client.delete(f"{BASE_URL}/api/tasks/{task['id']}")
    _cleanup()
    yield
    _cleanup()


# ─── 1. 페이지 로드 ───────────────────────────────────────────────────────────
def test_page_loads(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("TaskFlow Pro")
    expect(page.locator("h1")).to_have_text("TaskFlow Pro")


# ─── 2. 추가 버튼 비활성화 (title 없을 때) ────────────────────────────────────
def test_add_btn_disabled_without_title(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#addBtn")).to_be_disabled()

    page.fill("#newTitle", "제목 입력")
    expect(page.locator("#addBtn")).to_be_enabled()

    page.fill("#newTitle", "")
    expect(page.locator("#addBtn")).to_be_disabled()


# ─── 3. CRUD — Create ────────────────────────────────────────────────────────
def test_create_task(page: Page):
    page.goto(BASE_URL)
    page.fill("#newTitle", "Playwright 추가 테스트")
    page.locator("#addBtn").click()

    expect(page.locator(".task-card")).to_have_count(1)
    expect(page.locator(".task-card p")).to_contain_text("Playwright 추가 테스트")


# ─── 4. CRUD — Read ──────────────────────────────────────────────────────────
def test_read_task_list(page: Page):
    with httpx.Client() as client:
        client.post(f"{BASE_URL}/api/tasks", json={"title": "목록 테스트 1"})
        client.post(f"{BASE_URL}/api/tasks", json={"title": "목록 테스트 2"})

    page.goto(BASE_URL)
    expect(page.locator(".task-card")).to_have_count(2)


# ─── 5. CRUD — Update ────────────────────────────────────────────────────────
def test_update_task(page: Page):
    with httpx.Client() as client:
        client.post(f"{BASE_URL}/api/tasks", json={"title": "수정 전 제목"})

    page.goto(BASE_URL)
    page.locator(".task-card").click()

    # 모달이 열릴 때까지 대기
    expect(page.locator("#modalOverlay")).to_be_visible()
    page.fill("#editTitle", "수정 후 제목")
    page.locator("#editForm button[type='submit']").click()

    expect(page.locator("#modalOverlay")).not_to_be_visible()
    expect(page.locator(".task-card p")).to_contain_text("수정 후 제목")


# ─── 6. CRUD — Delete ────────────────────────────────────────────────────────
def test_delete_task(page: Page):
    with httpx.Client() as client:
        client.post(f"{BASE_URL}/api/tasks", json={"title": "삭제할 업무"})

    page.goto(BASE_URL)
    expect(page.locator(".task-card")).to_have_count(1)

    # confirm 다이얼로그 자동 수락
    page.on("dialog", lambda d: d.accept())
    page.locator(".delete-btn").click()

    expect(page.locator(".task-card")).to_have_count(0)


# ─── 7. 테마 토글: 라이트 ↔ 다크 ────────────────────────────────────────────
def test_theme_toggle(page: Page):
    page.goto(BASE_URL)
    # localStorage 초기화 후 라이트 상태로 시작
    page.evaluate("localStorage.removeItem('theme')")
    page.evaluate("document.documentElement.classList.remove('dark')")

    # 다크 전환
    page.locator("#themeBtn").click()
    expect(page.locator("html")).to_have_class("dark")
    assert page.evaluate("localStorage.getItem('theme')") == "dark"

    # 라이트 전환
    page.locator("#themeBtn").click()
    expect(page.locator("html")).not_to_have_class("dark")
    assert page.evaluate("localStorage.getItem('theme')") == "light"


# ─── 8. 새로고침 후 테마 유지 ─────────────────────────────────────────────────
def test_theme_persists_after_reload(page: Page):
    page.goto(BASE_URL)
    page.evaluate("localStorage.setItem('theme', 'dark')")
    page.reload()
    expect(page.locator("html")).to_have_class("dark")

    page.evaluate("localStorage.setItem('theme', 'light')")
    page.reload()
    expect(page.locator("html")).not_to_have_class("dark")


# ─── 9. 새로고침 후 데이터 유지 ───────────────────────────────────────────────
def test_data_persists_after_reload(page: Page):
    page.goto(BASE_URL)
    page.fill("#newTitle", "새로고침 후에도 남아야 함")
    page.locator("#addBtn").click()
    expect(page.locator(".task-card")).to_have_count(1)

    page.reload()
    expect(page.locator(".task-card")).to_have_count(1)
    expect(page.locator(".task-card p")).to_contain_text("새로고침 후에도 남아야 함")


# ─── 10. 360px 반응형: 레이아웃 깨짐 없음 ────────────────────────────────────
def test_360px_responsive(page: Page):
    page.set_viewport_size({"width": 360, "height": 640})
    page.goto(BASE_URL)

    # 헤더가 뷰포트를 벗어나지 않음
    header_box = page.locator("header").bounding_box()
    assert header_box["x"] >= 0
    assert header_box["width"] <= 360

    # 추가 폼이 뷰포트를 벗어나지 않음
    form_box = page.locator("#taskForm").bounding_box()
    assert form_box["x"] >= 0
    assert form_box["x"] + form_box["width"] <= 360

    # 카드 추가 후 카드도 뷰포트 안에 있음
    page.fill("#newTitle", "360px 테스트")
    page.locator("#addBtn").click()
    expect(page.locator(".task-card")).to_have_count(1)
    card_box = page.locator(".task-card").bounding_box()
    assert card_box["x"] >= 0
    assert card_box["x"] + card_box["width"] <= 360


# ─── 11. API 응답 200ms 이내 ──────────────────────────────────────────────────
def test_api_response_time(page: Page):
    with httpx.Client() as client:
        # 워밍업 1회
        client.get(f"{BASE_URL}/api/tasks")
        # 실측
        start = time.perf_counter()
        client.get(f"{BASE_URL}/api/tasks")
        elapsed_ms = (time.perf_counter() - start) * 1000

    assert elapsed_ms < 200, f"API 응답 시간 초과: {elapsed_ms:.1f}ms (기준: 200ms)"
