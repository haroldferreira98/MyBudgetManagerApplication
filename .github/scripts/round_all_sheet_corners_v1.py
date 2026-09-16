from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '20260917-rounded-sheet-corners-v1'

if marker in text:
    raise SystemExit('Fix already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-rounded-sheet-corners-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

old = '''    .sheet {
      width: min(100%, 748px);
      max-height: calc(100dvh - var(--safe-top) - var(--safe-bottom) - 20px);
      background: var(--surface-container-low);
      border-radius: var(--radius-sheet);
      box-shadow: 0 -20px 50px var(--shadow);
      display: flex;
      flex-direction: column;
      animation: sheetUp .25s cubic-bezier(.2,.8,.2,1);
    }'''
new = '''    .sheet {
      width: min(100%, 748px);
      max-height: calc(100dvh - var(--safe-top) - var(--safe-bottom) - 20px);
      background: var(--surface-container-low);
      border-radius: var(--radius-sheet);
      background-clip: padding-box;
      overflow: hidden;
      box-shadow: 0 -20px 50px var(--shadow);
      display: flex;
      flex-direction: column;
      animation: sheetUp .25s cubic-bezier(.2,.8,.2,1);
    }'''
if text.count(old) != 1:
    raise SystemExit(f'Expected one base .sheet block, found {text.count(old)}')
text = text.replace(old, new, 1)

old_body = '    .sheet-body { overflow-y: auto; padding: 8px 18px 20px; }'
new_body = '    .sheet-body { min-height: 0; overflow-y: auto; padding: 8px 18px 20px; }'
if text.count(old_body) != 1:
    raise SystemExit(f'Expected one .sheet-body rule, found {text.count(old_body)}')
text = text.replace(old_body, new_body, 1)

path.write_text(text, encoding='utf-8')
