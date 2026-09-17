from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '20260917-default-expense-category-view-v1'

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    f'<meta name="app-build" content="{marker}" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

old = '''    let operationTypeFilter = "all";
    let operationSort = "date";'''
new = '''    let operationTypeFilter = "expense";
    let operationSort = "category";'''
if text.count(old) != 1:
    raise SystemExit(f'Expected default operation filter/sort block once, found {text.count(old)}')
text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
