from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

if "SINGLE-PAGE-HOME-OPERATIONS-V2" in text:
    raise SystemExit("Single page layout already applied")

text = re.sub(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260916-single-page-operations-v2" />',
    text,
    count=1,
)

text, n = re.subn(
    r'\n  <div class="nav-wrap">\s*<nav class="bottom-nav" aria-label="Navigation principale">.*?</nav>\s*</div>\n',
    '\n',
    text,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit("Bottom navigation block not found")

home_anchor = '''        <div class="section">
          <div class="section-header"><div><h2 class="section-title">Équilibre 50 / 30 / 20</h2><p class="section-subtitle balance-section-subtitle">50% fixes · 30% quotidien · 20% disponible</p></div></div>
          <div class="card balance-card">${bucketCards}</div>
        </div>
`;'''

home_replacement = '''        <div class="section">
          <div class="section-header"><div><h2 class="section-title">Équilibre 50 / 30 / 20</h2><p class="section-subtitle balance-section-subtitle">50% fixes · 30% quotidien · 20% disponible</p></div></div>
          <div class="card balance-card">${bucketCards}</div>
        </div>

        <div id="homeOperations" class="home-operations"></div>
`;'''

if home_anchor not in text:
    raise SystemExit("Home balance anchor not found")
text = text.replace(home_anchor, home_replacement, 1)

old_target = '      const container = document.getElementById("screen-operations");\n      if (!container) return;'
new_target = '      const container = document.getElementById("homeOperations") || document.getElementById("screen-operations");\n      if (!container) return;'
if old_target not in text:
    raise SystemExit("Operations render target not found")
text = text.replace(old_target, new_target, 1)

old_screen = '      currentScreen = ["home", "operations", "settings"].includes(screen) ? screen : "home";'
new_screen = '      currentScreen = ["home", "settings"].includes(screen) ? screen : "home";'
if old_screen not in text:
    raise SystemExit("Current screen whitelist not found")
text = text.replace(old_screen, new_screen, 1)

old_settings = '      if (settings) { setCurrentScreen("settings"); return; }'
new_settings = '      if (settings) { setCurrentScreen(currentScreen === "settings" ? "home" : "settings"); return; }'
if old_settings not in text:
    raise SystemExit("Settings handler not found")
text = text.replace(old_settings, new_settings, 1)

style_marker = '  </style>\n</head>'
if style_marker not in text:
    raise SystemExit("Style marker not found")

css = r'''

    /* SINGLE-PAGE-HOME-OPERATIONS-V2 */
    .app-shell { padding-bottom: calc(28px + var(--safe-bottom)) !important; }
    .home-operations { margin-top: 24px; }
    .home-operations > .month-switcher { display: none !important; }
    .home-operations .search-shell { display: none !important; }
    .home-operations > .section { margin-top: 0 !important; margin-bottom: 28px; }
    #screen-operations { display: none !important; }
'''

text = text.replace(style_marker, css + "\n" + style_marker, 1)
path.write_text(text, encoding="utf-8")
