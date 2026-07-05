"""Capture README screenshots. Requires server: python main.py"""

from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
OUT = Path(__file__).resolve().parent.parent / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 700})

        page.goto(BASE, wait_until="networkidle")
        page.screenshot(path=str(OUT / "game.png"))

        page.goto(f"{BASE}/docs", wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUT / "swagger.png"), full_page=True)

        page.goto(BASE, wait_until="networkidle")
        page.evaluate("""async () => {
            for (let i = 0; i < 200; i++) {
                const r = await fetch('/api/game/hit', { method: 'POST', credentials: 'same-origin' });
                const d = await r.json();
                if (d.killed) break;
            }
        }""")
        page.click("#boss")
        page.evaluate("""() => {
            const zov = document.getElementById('zov');
            zov.innerHTML = '<span>ZOV!</span>';
            zov.classList.add('show');
            document.getElementById('flash').classList.add('on');
            document.getElementById('boss').classList.add('dead');
            document.getElementById('name').textContent = '...';
        }""")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUT / "zov.png"))

        browser.close()

    print("saved to", OUT)


if __name__ == "__main__":
    main()
