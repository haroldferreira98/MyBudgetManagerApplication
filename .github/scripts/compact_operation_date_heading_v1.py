from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

if '20260917-compact-operation-date-heading-v1' in text:
    raise SystemExit('Fix already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-compact-operation-date-heading-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

old_group = '    .operation-date-group + .operation-date-group { margin-top: 8px; }'
new_group = '    .operation-date-group + .operation-date-group { margin-top: 4px; }'
if text.count(old_group) != 1:
    raise SystemExit(f'Expected one date-group spacing rule, found {text.count(old_group)}')
text = text.replace(old_group, new_group, 1)

pattern = re.compile(r'(    \.operation-date-heading \{\n)(.*?)(    \}\n)', re.S)
match = pattern.search(text)
if not match:
    raise SystemExit('operation-date-heading block not found')
block = match.group(2)
block2 = block
block2 = block2.replace('      padding: 12px 12px 6px;\n', '      padding: 6px 12px 3px;\n', 1)
block2 = block2.replace('      font-size: 12px;\n', '      font-size: 11px;\n', 1)
block2 = block2.replace('      line-height: 1.2;\n', '      line-height: 1.15;\n', 1)
if block2 == block:
    raise SystemExit('operation-date-heading styles were not changed')
text = text[:match.start(2)] + block2 + text[match.end(2):]

path.write_text(text, encoding='utf-8')
