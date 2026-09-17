from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '20260917-personal-care-home-care-v1'

if marker in text:
    raise SystemExit('Fix already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    f'<meta name="app-build" content="{marker}" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

# Keep the expense category list readable and grouped alphabetically.
replacements = [
    ('      "Animaux",\n      "Boulangerie",',
     '      "Animaux",\n      "Beauté & soins",\n      "Boulangerie",'),
    ('      "Enfants",\n      "Impôts",\n      "Hygiène",',
     '      "Enfants",\n      "Entretien maison",\n      "Impôts",\n      "Hygiène corporelle",'),
    ('        "Carburant": "local_gas_station",\n        "Hygiène": "soap",\n        "Loisirs": "sports_esports",',
     '        "Carburant": "local_gas_station",\n        "Beauté & soins": "spa",\n        "Entretien maison": "cleaning_services",\n        "Hygiène corporelle": "soap",\n        "Loisirs": "sports_esports",'),
    ('        expenses: Array.isArray(input.expenses) ? input.expenses : [],',
     '        expenses: Array.isArray(input.expenses) ? input.expenses.map(item => ({ ...item, category: item.category === "Hygiène" ? "Hygiène corporelle" : item.category })) : [],'),
    ('        envelopes: Array.isArray(input.envelopes) ? input.envelopes : []',
     '        envelopes: Array.isArray(input.envelopes) ? input.envelopes.map(item => ({ ...item, category: item.category === "Hygiène" ? "Hygiène corporelle" : item.category })) : []'),
]

for old, new in replacements:
    if text.count(old) != 1:
        raise SystemExit(f'Expected exactly one anchor, found {text.count(old)} for: {old[:80]!r}')
    text = text.replace(old, new, 1)

# Guard against accidental duplicate category entries in the selectable list.
for label in ('Beauté & soins', 'Entretien maison', 'Hygiène corporelle'):
    if text.count(f'      "{label}",') != 1:
        raise SystemExit(f'Unexpected list count for {label}')

path.write_text(text, encoding='utf-8')
