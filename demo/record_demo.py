"""Records a demo video of Truth-Finder answering a real question. Usage: python demo/record_demo.py [url] [question]"""
import sys, time, glob, os
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5002/"
Q = sys.argv[2] if len(sys.argv) > 2 else "Do vaccines cause autism?"
out = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1000, "height": 720}, record_video_dir=out, record_video_size={"width": 1000, "height": 720})
    pg = ctx.new_page(); pg.goto(URL); time.sleep(2)
    pg.click("#q"); pg.keyboard.type(Q, delay=90); time.sleep(0.8)
    pg.click("button"); t0 = time.time()
    pg.wait_for_selector(".headline, .warn, .card.Disputed", timeout=300000)
    pg.wait_for_function("!document.querySelector('#out').innerText.includes('Searching')", timeout=300000)
    print("result after", round(time.time() - t0), "s"); time.sleep(3)
    h = pg.evaluate("document.body.scrollHeight"); y = 0
    while y < min(h, 9000):
        y += 6; pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.02)
    time.sleep(1.5); pg.evaluate("window.scrollTo(0,0)"); time.sleep(1.5)
    pg.screenshot(path=os.path.join(out, "final_fullpage.png"), full_page=True)
    vid = pg.video.path(); ctx.close(); b.close()
    os.replace(vid, os.path.join(out, "demo_raw.webm")); print("saved")
