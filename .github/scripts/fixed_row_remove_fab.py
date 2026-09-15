from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Keep the four navigation destinations evenly spaced after removing the central add FAB.
s = s.replace(
    '      grid-template-columns: 1fr 1fr 72px 1fr 1fr;',
    '      grid-template-columns: repeat(4, minmax(0, 1fr));',
    1,
)
s = s.replace(
    '      .bottom-nav { grid-template-columns: 1fr 1fr 64px 1fr 1fr; }',
    '      .bottom-nav { grid-template-columns: repeat(4, minmax(0, 1fr)); }',
    1,
)

fab_html = '''      <button class="fab" id="fabAdd" aria-label="Ajouter">\n        <span class="material-symbols-outlined">add</span>\n      </button>\n'''
if fab_html not in s:
    raise SystemExit('Central FAB markup not found')
s = s.replace(fab_html, '', 1)

fab_js = '''    const fabAdd = document.getElementById("fabAdd");\n    fabAdd?.addEventListener("click", () => {\n      if (currentScreen === "income") openEntityModal("income", null, null, true);\n      else if (currentScreen === "expenses" || currentScreen === "home") openEntityModal("expense", null, null, true);\n      else openEntityModal("expense");\n    });\n'''
if fab_js not in s:
    raise SystemExit('Central FAB listener not found')
s = s.replace(fab_js, '', 1)

# The fixed-charge form already groups amount/day in .field-row, but the global
# mobile media query stacks every .field-row. Add a specific late override.
marker = '\n</style>'
css = '''\n    /* FIXED-CHARGE-ROW-NO-FAB-V1 */\n    #entityModal[data-entity-type="fixed"] .field-row {\n      display: grid !important;\n      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;\n      gap: 12px !important;\n      width: 100% !important;\n      min-width: 0 !important;\n    }\n    #entityModal[data-entity-type="fixed"] .field-row > .field {\n      min-width: 0 !important;\n      width: auto !important;\n      max-width: 100% !important;\n    }\n    #entityModal[data-entity-type="fixed"] .field-row input {\n      width: 100% !important;\n      min-width: 0 !important;\n      max-width: 100% !important;\n      box-sizing: border-box !important;\n    }\n'''
if marker not in s:
    raise SystemExit('Style end not found')
s = s.replace(marker, css + marker, 1)

for required in [
    'Montant mensuel (€)',
    'Jour de prélèvement',
    'data-screen="home"',
    'data-screen="income"',
    'data-screen="expenses"',
    'data-screen="profile"',
]:
    if required not in s:
        raise SystemExit(f'Missing expected app feature: {required}')

if 'id="fabAdd"' in s:
    raise SystemExit('FAB markup still present')
if 'const fabAdd =' in s:
    raise SystemExit('FAB JS still present')

p.write_text(s, encoding='utf-8')
