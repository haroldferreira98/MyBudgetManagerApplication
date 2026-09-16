from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'HOME-SUMMARY-BALANCE-V2'
if marker in text:
    raise SystemExit('Refinement already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260916-home-summary-balance-v2" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

style_marker = '  </style>\n</head>'
if style_marker not in text:
    raise SystemExit('Style closing marker not found')

css = r'''

    /* HOME-SUMMARY-BALANCE-V2 */
    .summary-bottom {
      grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    }
    .summary-mini,
    html[data-theme="dsfr"] .summary-mini {
      padding-left: 6px;
      padding-right: 6px;
    }
    .summary-mini-label {
      font-size: clamp(8.5px, 2.25vw, 10.5px) !important;
    }
    .summary-mini-value,
    html[data-theme="dsfr"] .summary-mini-value {
      font-size: clamp(12px, 3.25vw, 16px) !important;
    }

    .operations-category-items {
      gap: 7px !important;
      padding: 7px 10px 7px !important;
    }
    .operations-category-items .list-item,
    html[data-theme="dsfr"] .operations-category-items .list-item {
      min-height: 60px;
      padding: 10px 11px;
      gap: 10px;
      border: 1px solid color-mix(in srgb, var(--outline-variant) 50%, transparent) !important;
      border-radius: var(--radius-small) !important;
      background: var(--surface-container-lowest) !important;
    }
    .operations-category-items .list-item:last-child {
      border-bottom: 1px solid color-mix(in srgb, var(--outline-variant) 50%, transparent) !important;
    }

    .balance-card .progress-track,
    html[data-theme="dsfr"] .balance-card .progress-track {
      height: 15px !important;
      position: relative;
      overflow: hidden;
    }
    .balance-card .progress-fill,
    html[data-theme="dsfr"] .balance-card .progress-fill {
      height: 100%;
    }
    .balance-progress-label {
      position: absolute;
      top: 50%;
      transform: translate(-50%, -50%);
      z-index: 2;
      font-size: 9.5px;
      line-height: 1;
      font-weight: 700;
      color: var(--on-surface-variant);
      font-variant-numeric: tabular-nums;
      pointer-events: none;
      user-select: none;
      white-space: nowrap;
    }
    .balance-progress-label.on-fill {
      color: var(--on-primary);
    }
'''
text = text.replace(style_marker, css + '\n' + style_marker, 1)

old_summary = '''            <div class="summary-bottom">
              <div class="summary-mini">
                <span class="summary-mini-label">Revenus</span>
                <strong class="summary-mini-value money">${formatMoney(s.income)}</strong>
              </div>
              <div class="summary-mini">
                <span class="summary-mini-label">Dépenses</span>
                <strong class="summary-mini-value money">${formatMoney(s.engaged)}</strong>
              </div>
              <div class="summary-mini">
                <span class="summary-mini-label">Charges fixes</span>
                <strong class="summary-mini-value money">${formatMoney(s.fixed)}</strong>
              </div>
            </div>'''
new_summary = '''            <div class="summary-bottom">
              <div class="summary-mini">
                <span class="summary-mini-label">Revenus</span>
                <strong class="summary-mini-value money">${formatMoney(s.income)}</strong>
              </div>
              <div class="summary-mini">
                <span class="summary-mini-label">Charges fixes</span>
                <strong class="summary-mini-value money">${formatMoney(s.fixed)}</strong>
              </div>
              <div class="summary-mini">
                <span class="summary-mini-label">Dépenses</span>
                <strong class="summary-mini-value money">${formatMoney(s.expenses)}</strong>
              </div>
              <div class="summary-mini">
                <span class="summary-mini-label">Total</span>
                <strong class="summary-mini-value money">${formatMoney(s.engaged)}</strong>
              </div>
            </div>'''
if text.count(old_summary) != 1:
    raise SystemExit(f'Expected one home summary block, found {text.count(old_summary)}')
text = text.replace(old_summary, new_summary, 1)

old_balance = '''          <div class="balance-row">
            <div class="balance-head">
              <div class="balance-label"><strong>${item.label}</strong><span class="target-badge">${item.target}%</span></div>
              <span class="balance-value"><span class="money">${formatMoney(item.value)}</span><span class="balance-pct">${pctIncome.toFixed(0)}%</span></span>
            </div>
            <div class="progress-track"><div class="progress-fill ${over ? "warn" : ""}" style="width:${fill}%"></div></div>
          </div>`;'''
new_balance = '''          <div class="balance-row">
            <div class="balance-head">
              <div class="balance-label"><strong>${item.label}</strong></div>
              <span class="balance-value"><span class="money">${formatMoney(item.value)}</span></span>
            </div>
            <div class="progress-track balance-progress-track">
              <div class="progress-fill ${over ? "warn" : ""}" style="width:${fill}%"></div>
              <span class="balance-progress-label ${fill >= 18 ? "on-fill" : ""}" style="left:${clamp(fill - 7, 8, 91)}%">${pctIncome.toFixed(0)}%</span>
            </div>
          </div>`;'''
if text.count(old_balance) != 1:
    raise SystemExit(f'Expected one balance row template, found {text.count(old_balance)}')
text = text.replace(old_balance, new_balance, 1)

path.write_text(text, encoding='utf-8')
