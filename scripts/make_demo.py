"""Capture real CLI output, render a labeled terminal replay, add English TTS."""
import json, os, pathlib, pty, select, subprocess, sys, time, wave
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
records=[]
for fixture in ['pages','money','intervals']:
    command=[sys.executable,'-m','patchjury','--fixture',fixture,'--output',f'evidence/{fixture}.json']
    master,slave=pty.openpty(); started=time.monotonic()
    proc=subprocess.Popen(command,stdout=slave,stderr=slave); os.close(slave)
    chunks=[]
    while True:
        try: data=os.read(master,8192)
        except OSError: break
        if not data: break
        chunks.append({'seconds':round(time.monotonic()-started,3),'text':data.decode()})
    os.close(master)
    if proc.wait()!=0: raise SystemExit('CLI recording failed')
    records.append({'fixture':fixture,'command':command,'chunks':chunks})
(ROOT/'demo/terminal-recording.json').write_text(json.dumps(records,indent=2)+'\n')
subprocess.run(['espeak','-v','en-us','-s','155','-f','demo/narration.txt','-w','demo/narration.wav'],check=True)
with wave.open('demo/narration.wav') as w: duration=w.getnframes()/w.getframerate()
frames=ROOT/'demo/frames';frames.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',17)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',14)
large=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',27)
# Actual transcript lines only; progressive reveals with edited timing for readability.
scene_ranges=[(0,.15),(.15,.40),(.40,.61),(.61,1)]
import math,textwrap
for second in range(math.ceil(duration)+1):
    fraction=second/duration
    idx=0 if fraction<.40 else 1 if fraction<.61 else 2
    start=0 if idx==0 else .40 if idx==1 else .61
    end=.40 if idx==0 else .61 if idx==1 else 1
    progress=min(1,max(0,(fraction-start)/(end-start)))
    record=records[idx]
    text=''.join(chunk['text'] for chunk in record['chunks']).replace('\r','')
    lines=text.splitlines(); reveal=min(len(lines),max(3,int(progress*len(lines)*1.4)))
    visible=lines[max(0,reveal-22):reveal]
    im=Image.new('RGB',(1280,720),'#101713');draw=ImageDraw.Draw(im)
    draw.text((36,24),'PATCH JURY  /  EVIDENCE BEFORE MERGE',font=large,fill='#c5f47b')
    draw.text((36,70),'OFFLINE PREVIEW · ACTUAL CLI RECORDING · HAND-AUTHORED CASES · NO API CALL',font=small,fill='#ffbf9c')
    draw.rounded_rectangle((28,110,1252,657),12,fill='#19241c',outline='#486046')
    draw.text((48,130),'$ python3 -m patchjury --fixture '+record['fixture'],font=font,fill='#c5f47b')
    for i,line in enumerate(visible):
        color='#ffa385' if 'FAIL' in line else '#c5f47b' if 'PASS' in line else '#eaf0ed'
        draw.text((48,168+i*21),line[:112],font=font,fill=color)
    draw.text((36,680),'Model proposes inputs → trusted oracle → isolated execution → inspectable evidence',font=small,fill='#b3c5b5')
    im.save(frames/f'{second:04d}.png')
ffmpeg=os.environ.get('FFMPEG','ffmpeg')
subprocess.run([ffmpeg,'-y','-framerate','1','-i',str(frames/'%04d.png'),'-i','demo/narration.wav','-c:v','libx264','-r','24','-pix_fmt','yuv420p','-c:a','aac','-shortest','-movflags','+faststart','demo/preview.mp4'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
(ROOT/'demo/preview-first-frame.png').write_bytes((frames/'0000.png').read_bytes())
print(json.dumps({'seconds':round(duration,2),'bytes':(ROOT/'demo/preview.mp4').stat().st_size,'mode':'offline terminal replay'}))
