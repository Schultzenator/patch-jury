"""Capture actual local UI screens and render an 80s offline edit with FFmpeg.
Optional build tools: playwright, Pillow, espeak, ffmpeg (or FFMPEG path).
No API key, external browser profile or Nebius console is used.
"""
import json, os, pathlib, shutil, subprocess, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
OUT=ROOT/'demo/submission'; OUT.mkdir(parents=True,exist_ok=True)
ffmpeg=os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not ffmpeg: raise SystemExit('Set FFMPEG to an installed ffmpeg binary')
server=subprocess.Popen([sys.executable,'-m','patchjury','--serve'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8000/api/fixtures',timeout=1) as r: r.read()
            break
        except OSError: time.sleep(.1)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=os.environ.get('CHROME') or shutil.which('google-chrome'),headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
        def capture(name):
            path=OUT/(name+'.png'); page.screenshot(path=str(path))
            capture_image=Image.open(path).convert('RGB').resize((1280,690))
            im=Image.new('RGB',(1280,720),'#101713'); im.paste(capture_image,(0,30)); draw=ImageDraw.Draw(im)
            draw.rectangle((0,0,1280,30),fill='#15231c')
            font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',14)
            draw.text((16,6),'OFFLINE SCREEN CAPTURE | AUTHORED INPUTS | NO NEBIUS INFERENCE | EDITED TIMING',font=font,fill='#c5f47b')
            im.save(path)
        page.goto('http://127.0.0.1:8000');page.wait_for_selector('#fixture option',state='attached');capture('01-start')
        page.locator('#run').scroll_into_view_if_needed();capture('02-patches')
        page.locator('#run').click();page.wait_for_selector('#results:not([hidden])',timeout=60000)
        report=page.evaluate('fetch("/api/compare",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({fixture:"pages",mode:"authored-example"})}).then(r=>r.json())')
        (ROOT/'evidence/submission-pages.json').write_text(json.dumps(report,indent=2)+'\n')
        page.locator('#results').scroll_into_view_if_needed();capture('03-verdict')
        page.locator('#cards').scroll_into_view_if_needed();capture('04-variants')
        page.locator('#cases').scroll_into_view_if_needed();capture('05-counterexamples')
        page.locator('#fixture').select_option('money');page.locator('#run').click();page.wait_for_selector('#results:not([hidden])',timeout=60000)
        page.locator('#cards').scroll_into_view_if_needed();capture('06-money')
        # This configuration card is explicitly a placeholder, never a real API response.
        page.set_content('<html><body style="margin:80px;background:#101713;color:#eaf0ed;font:24px monospace"><h1>Enable the live juror</h1><p>CONFIGURATION PLACEHOLDER · NO API CALL</p><pre>NEBIUS_API_KEY=&lt;OWNER_INJECTS_KEY&gt;\nNEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1\nMODEL=nvidia/Nemotron-3_5-Lightning\nNEBIUS_CREDITS_CONFIRMED=yes</pre><p>Restart server → choose Nemotron · live Nebius API</p><p>Input generation → trusted oracle → Docker → verdict</p></body></html>');capture('07-config')
        page.goto('http://127.0.0.1:8000');page.wait_for_selector('#fixture option',state='attached');capture('08-end')
        browser.close()
finally:
    server.terminate();server.wait(timeout=5)
scenes=[('01-start',8),('02-patches',8),('03-verdict',12),('04-variants',12),('05-counterexamples',14),('06-money',10),('07-config',10),('08-end',6)]
lines=[]
for name,duration in scenes:
    lines.extend([f"file '{name}.png'",f'duration {duration}'])
lines.append("file '08-end.png'")
(OUT/'frames.ffconcat').write_text('\n'.join(lines)+'\n')
subprocess.run(['espeak','-v','en-us','-s','180','-f','demo/submission-narration.txt','-w',str(OUT/'narration.wav')],check=True)
subprocess.run([ffmpeg,'-y','-f','concat','-safe','0','-i',str(OUT/'frames.ffconcat'),'-i',str(OUT/'narration.wav'),'-af','apad','-t','80','-c:v','libx264','-r','24','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(OUT/'submission-offline.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
print('Rendered demo/submission/submission-offline.mp4 (80 seconds, actual UI captures, offline)')
