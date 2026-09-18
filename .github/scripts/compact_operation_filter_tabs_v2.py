from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-operation-filter-tabs-v2" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

old = '''    /* OPERATION-FILTER-TABS-V1 */
    .operation-filter-tabs {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 5px;
      margin: 10px 0 12px;
      padding: 4px;
      border-radius: var(--radius-small);
      background: var(--surface-container-low);
      border: 1px solid color-mix(in srgb, var(--outline-variant) 58%, transparent);
    }
    .operation-filter-tab {
      min-width: 0;
      min-height: 38px;
      padding: 7px 4px;
      border: 1px solid transparent;
      border-radius: calc(var(--radius-small) - 4px);
      background: transparent;
      color: var(--on-surface-variant);
      font-size: clamp(10px, 2.85vw, 12px);
      line-height: 1.1;
      font-weight: 650;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      transition: background .14s ease, color .14s ease, transform .12s ease;
    }
    .operation-filter-tab.active {
      background: var(--primary-container);
      color: var(--on-primary-container);
      box-shadow: 0 1px 2px color-mix(in srgb, var(--shadow) 28%, transparent);
    }
    .operation-filter-tab:active { transform: scale(.97); }
    @media (max-width: 360px) {
      .operation-filter-tabs { gap: 3px; padding: 3px; }
      .operation-filter-tab { min-height: 36px; padding-inline: 2px; font-size: 9.8px; }
    }
'''

new = '''    /* OPERATION-FILTER-TABS-V2 */
    .operation-filter-tabs {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 2px;
      margin: 7px 0 10px;
      padding: 2px;
      border-radius: 12px;
      background: var(--surface-container-low);
      border: 1px solid color-mix(in srgb, var(--outline-variant) 58%, transparent);
    }
    .operation-filter-tab {
      min-width: 0;
      min-height: 32px;
      padding: 4px 1px;
      border: 1px solid transparent;
      border-radius: 9px;
      background: transparent;
      color: var(--on-surface-variant);
      font-size: clamp(9px, 2.45vw, 10.5px);
      letter-spacing: -.015em;
      line-height: 1;
      font-weight: 650;
      white-space: nowrap;
      overflow: visible;
      text-overflow: clip;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      transition: background .14s ease, color .14s ease, transform .12s ease;
    }
    .operation-filter-tab.active {
      background: var(--primary-container);
      color: var(--on-primary-container);
      box-shadow: 0 1px 2px color-mix(in srgb, var(--shadow) 24%, transparent);
    }
    .operation-filter-tab:active { transform: scale(.97); }
    @media (max-width: 360px) {
      .operation-filter-tabs { gap: 1px; padding: 2px; }
      .operation-filter-tab { min-height: 30px; padding-inline: 0; font-size: 8.5px; letter-spacing: -.025em; }
    }
'''

if text.count(old) != 1:
    raise SystemExit(f'filter tabs CSS anchor count={text.count(old)}')
text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
