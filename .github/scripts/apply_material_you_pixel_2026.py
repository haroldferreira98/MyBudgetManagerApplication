from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

marker = '/* MATERIAL-YOU-PIXEL-2026-V1 */'
if marker in text:
    raise SystemExit('Material You Pixel 2026 layer already present')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-material-you-pixel-2026-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

css = r'''

    /* MATERIAL-YOU-PIXEL-2026-V1 */
    :root {
      /* Tokens Material You - Design Pixel 2026 */
      --md-primary: #0b57d0;
      --md-on-primary: #ffffff;
      --md-primary-container: #d3e3fd;
      --md-on-primary-container: #041e49;

      --md-surface: #fdfbff;
      --md-on-surface: #1a1c1e;
      --md-surface-container: #f3f4f9;
      --md-surface-container-high: #e7e8ee;

      --md-outline: #74777f;

      --md-font-family: 'Google Sans', 'Roboto', system-ui, sans-serif;

      --md-shape-small: 8px;
      --md-shape-medium: 16px;
      --md-shape-large: 24px;
      --md-shape-fab: 16px;

      --md-elevation-1: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);

      /* Compatibility aliases for the existing UI. */
      --primary: var(--md-primary);
      --on-primary: var(--md-on-primary);
      --primary-container: var(--md-primary-container);
      --on-primary-container: var(--md-on-primary-container);
      --surface: var(--md-surface);
      --surface-bright: var(--md-surface);
      --surface-container-lowest: #ffffff;
      --surface-container-low: color-mix(in srgb, var(--md-surface) 54%, var(--md-surface-container));
      --surface-container: var(--md-surface-container);
      --surface-container-high: var(--md-surface-container-high);
      --surface-container-highest: var(--md-surface-container-high);
      --on-surface: var(--md-on-surface);
      --on-surface-variant: color-mix(in srgb, var(--md-on-surface) 72%, var(--md-surface));
      --outline: var(--md-outline);
      --outline-variant: color-mix(in srgb, var(--md-outline) 36%, transparent);
      --radius-card: var(--md-shape-large);
      --radius-sheet: var(--md-shape-large);
      --radius-small: var(--md-shape-medium);
    }

    html[data-theme="dark"] {
      --md-primary: #a8c7fa;
      --md-on-primary: #062e6f;
      --md-primary-container: #0842a0;
      --md-on-primary-container: #d3e3fd;

      --md-surface: #1a1c1e;
      --md-on-surface: #e2e2e6;
      --md-surface-container: #2f3033;
      --md-surface-container-high: #44474a;

      --md-outline: #8e9099;

      --primary: var(--md-primary);
      --on-primary: var(--md-on-primary);
      --primary-container: var(--md-primary-container);
      --on-primary-container: var(--md-on-primary-container);
      --surface: var(--md-surface);
      --surface-dim: var(--md-surface);
      --surface-bright: var(--md-surface-container-high);
      --surface-container-lowest: color-mix(in srgb, var(--md-surface) 84%, #000000);
      --surface-container-low: color-mix(in srgb, var(--md-surface) 62%, var(--md-surface-container));
      --surface-container: var(--md-surface-container);
      --surface-container-high: var(--md-surface-container-high);
      --surface-container-highest: var(--md-surface-container-high);
      --on-surface: var(--md-on-surface);
      --on-surface-variant: color-mix(in srgb, var(--md-on-surface) 72%, var(--md-surface));
      --outline: var(--md-outline);
      --outline-variant: color-mix(in srgb, var(--md-outline) 44%, transparent);
    }

    /* Fallback for pages that do not yet set an explicit app theme. */
    @media (prefers-color-scheme: dark) {
      html:not([data-theme]) {
        --md-primary: #a8c7fa;
        --md-on-primary: #062e6f;
        --md-primary-container: #0842a0;
        --md-on-primary-container: #d3e3fd;
        --md-surface: #1a1c1e;
        --md-on-surface: #e2e2e6;
        --md-surface-container: #2f3033;
        --md-surface-container-high: #44474a;
        --md-outline: #8e9099;
      }
    }

    html:not([data-theme="dsfr"]) body {
      background: var(--md-surface);
      color: var(--md-on-surface);
      font-family: var(--md-font-family);
    }

    html:not([data-theme="dsfr"]) .topbar {
      background: color-mix(in srgb, var(--md-surface) 90%, transparent);
    }

    html:not([data-theme="dsfr"]) .card,
    html:not([data-theme="dsfr"]) .empty-state,
    html:not([data-theme="dsfr"]) .profile-fold,
    html:not([data-theme="dsfr"]) .expense-category-group,
    html:not([data-theme="dsfr"]) .cloud-status {
      background: var(--md-surface-container);
      color: var(--md-on-surface);
      border: 1px solid color-mix(in srgb, var(--md-outline) 22%, transparent);
      border-radius: var(--md-shape-large) !important;
      box-shadow: none !important;
    }

    html:not([data-theme="dsfr"]) .hero-card {
      background: linear-gradient(
        145deg,
        var(--md-primary-container),
        color-mix(in srgb, var(--md-primary-container) 72%, var(--md-surface-container))
      );
      border: 0;
      border-radius: var(--md-shape-large) !important;
    }

    html:not([data-theme="dsfr"]) .expense-category-group[open] > .expense-category-summary {
      border-bottom-color: color-mix(in srgb, var(--md-outline) 22%, transparent);
    }

    html:not([data-theme="dsfr"]) .expense-category-items .list-item {
      background: transparent;
      border-bottom-color: color-mix(in srgb, var(--md-outline) 20%, transparent);
    }

    html:not([data-theme="dsfr"]) .btn {
      min-height: 44px;
      border-radius: var(--md-shape-medium) !important;
      font-family: var(--md-font-family);
      font-weight: 600;
      box-shadow: none !important;
      transition: background-color .18s ease, color .18s ease, transform .16s ease, box-shadow .18s ease;
    }

    html:not([data-theme="dsfr"]) .btn.primary {
      background: var(--md-primary);
      color: var(--md-on-primary);
    }

    html:not([data-theme="dsfr"]) .btn.tonal {
      background: var(--md-primary-container);
      color: var(--md-on-primary-container);
    }

    html:not([data-theme="dsfr"]) .btn.outlined {
      background: transparent;
      border: 1px solid var(--md-outline);
      color: var(--md-on-surface);
    }

    html:not([data-theme="dsfr"]) .btn:active {
      transform: scale(.98);
    }

    html:not([data-theme="dsfr"]) .icon-btn {
      background: var(--md-surface-container-high);
      color: var(--md-on-surface);
    }

    html:not([data-theme="dsfr"]) .fab {
      border-radius: var(--md-shape-fab) !important;
      background: var(--md-primary-container);
      color: var(--md-on-primary-container);
      box-shadow: var(--md-elevation-1);
    }

    html:not([data-theme="dsfr"]) .bottom-nav {
      background: color-mix(in srgb, var(--md-surface-container) 94%, transparent);
      border-color: color-mix(in srgb, var(--md-outline) 18%, transparent);
    }

    html:not([data-theme="dsfr"]) .nav-btn.active .material-symbols-outlined {
      background: var(--md-primary-container);
      color: var(--md-on-primary-container);
    }

    html:not([data-theme="dsfr"]) .sheet {
      background: var(--md-surface-container);
      color: var(--md-on-surface);
      border-radius: var(--md-shape-large) !important;
    }

    html:not([data-theme="dsfr"]) .field input,
    html:not([data-theme="dsfr"]) .field select,
    html:not([data-theme="dsfr"]) .field textarea {
      background: var(--md-surface);
      color: var(--md-on-surface);
      border-color: color-mix(in srgb, var(--md-outline) 55%, transparent);
      border-radius: var(--md-shape-medium) !important;
    }

    html:not([data-theme="dsfr"]) .field input:focus,
    html:not([data-theme="dsfr"]) .field select:focus,
    html:not([data-theme="dsfr"]) .field textarea:focus {
      border-color: var(--md-primary);
      box-shadow: 0 0 0 1px var(--md-primary);
    }

    html:not([data-theme="dsfr"]) .merchant-suggestion:hover,
    html:not([data-theme="dsfr"]) .merchant-suggestion:focus-visible,
    html:not([data-theme="dsfr"]) .expense-sort-option:hover,
    html:not([data-theme="dsfr"]) .expense-sort-option.active {
      background: var(--md-primary-container);
      color: var(--md-on-primary-container);
    }
'''

if text.count('</style>') != 1:
    raise SystemExit(f'unexpected style closing tag count: {text.count("</style>")}')
text = text.replace('</style>', css + '\n  </style>', 1)
path.write_text(text, encoding='utf-8')
