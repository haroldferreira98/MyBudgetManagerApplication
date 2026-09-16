from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'COMPACT-CATEGORIES-IOS-LOCK-V1'
if marker in text:
    raise SystemExit('Patch already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260916-compact-categories-ios-lock-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

style_marker = '  </style>\n</head>'
if style_marker not in text:
    raise SystemExit('Style closing marker not found')

css = r'''

    /* COMPACT-CATEGORIES-IOS-LOCK-V1 */
    /* Le tri Catégories utilise exactement le même rythme visuel que Date/Montant. */
    .operation-list > .expense-category-group,
    html[data-theme="dsfr"] .operation-list > .expense-category-group {
      margin-top: 0 !important;
      border: 1px solid color-mix(in srgb, var(--outline-variant) 76%, transparent) !important;
      border-radius: var(--radius-small) !important;
      background: var(--surface-container-lowest) !important;
      box-shadow: none !important;
    }
    .operation-list > .expense-category-group + .expense-category-group {
      margin-top: 0 !important;
    }
    .operation-list > .expense-category-group > .expense-category-summary {
      min-height: 60px;
      padding: 10px 11px;
      gap: 10px;
    }

    /* Comportement d'application native sur iPhone : pas de sélection ni de pinch zoom. */
    html,
    body,
    .app-shell {
      touch-action: pan-y;
      -webkit-user-select: none;
      user-select: none;
      -webkit-touch-callout: none;
    }
    input,
    textarea,
    select,
    [contenteditable="true"] {
      -webkit-user-select: text !important;
      user-select: text !important;
      -webkit-touch-callout: default;
    }
'''
text = text.replace(style_marker, css + '\n' + style_marker, 1)

old_zoom = '''    // Désactive le zoom par pincement sur mobile sans bloquer le défilement à un doigt.\n    const preventZoomGesture = event => event.preventDefault();\n    ["gesturestart", "gesturechange", "gestureend"].forEach(type => {\n      document.addEventListener(type, preventZoomGesture, { passive: false });\n    });\n    document.addEventListener("touchmove", event => {\n      if (event.touches.length > 1) event.preventDefault();\n    }, { passive: false });'''

new_zoom = '''    // Verrouille le pinch-zoom iOS tout en gardant le scroll vertical à un doigt.\n    const preventZoomGesture = event => event.preventDefault();\n    ["gesturestart", "gesturechange", "gestureend"].forEach(type => {\n      document.addEventListener(type, preventZoomGesture, { passive: false, capture: true });\n    });\n    const preventMultiTouchZoom = event => {\n      if (event.touches && event.touches.length > 1) event.preventDefault();\n    };\n    document.addEventListener("touchstart", preventMultiTouchZoom, { passive: false, capture: true });\n    document.addEventListener("touchmove", preventMultiTouchZoom, { passive: false, capture: true });\n    document.addEventListener("selectstart", event => {\n      const editable = event.target?.closest?.('input, textarea, select, [contenteditable="true"]');\n      if (!editable) event.preventDefault();\n    }, { capture: true });'''

if text.count(old_zoom) != 1:
    raise SystemExit(f'Expected one zoom protection block, found {text.count(old_zoom)}')
text = text.replace(old_zoom, new_zoom, 1)

path.write_text(text, encoding='utf-8')
