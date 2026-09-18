from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Build marker
text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-prepared-meal-category-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

# Add category immediately before Autre so Autre remains last.
old_categories = '''      "VTC & Taxi",
      "Autre",
    ];'''
new_categories = '''      "VTC & Taxi",
      "Plat préparé",
      "Autre",
    ];'''
if text.count(old_categories) != 1:
    raise SystemExit(f'expense categories anchor count={text.count(old_categories)}')
text = text.replace(old_categories, new_categories, 1)

# Dedicated icon for prepared meals.
old_icon = '''        "Santé": "medical_services",
        "Autre": "category"'''
new_icon = '''        "Santé": "medical_services",
        "Plat préparé": "lunch_dining",
        "Autre": "category"'''
if text.count(old_icon) != 1:
    raise SystemExit(f'category icon anchor count={text.count(old_icon)}')
text = text.replace(old_icon, new_icon, 1)

path.write_text(text, encoding='utf-8')
