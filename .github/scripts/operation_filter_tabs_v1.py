from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-operation-filter-tabs-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

old_toolbar = '''          <div class="operations-toolbar">
            <div>
              <h2 class="section-title">Opérations</h2>
              <p class="section-subtitle">${rows.length} opération${rows.length > 1 ? "s" : ""} affichée${rows.length > 1 ? "s" : ""}</p>
            </div>
            <div class="operations-toolbar-actions">
              <div class="operation-menu-wrap">
                <button class="btn outlined small operation-filter-toggle" type="button" data-operation-filter-toggle aria-label="Filtrer" title="Filtrer" aria-expanded="false"><span class="material-symbols-outlined">filter_alt</span></button>
                <div class="operation-menu operation-filter-menu" data-operation-filter-menu hidden>
                  <div class="operation-menu-title">Filtrer par</div>
                  ${typeOptions.map(([value, label]) => `<button type="button" class="${operationTypeFilter === value ? "active" : ""}" data-operation-type="${value}"><span class="material-symbols-outlined">${operationTypeFilter === value ? "check" : ""}</span>${label}</button>`).join("")}
                </div>
              </div>
              <div class="operation-menu-wrap">
                <button class="btn tonal small" type="button" data-operation-add-toggle aria-expanded="false"><span class="material-symbols-outlined">add</span>Ajouter</button>
                <div class="operation-menu" data-operation-add-menu hidden>
                  <button type="button" data-add-type="income"><span class="material-symbols-outlined">payments</span>Revenu</button>
                  <button type="button" data-add-type="fixed"><span class="material-symbols-outlined">event_repeat</span>Charge fixe</button>
                  <button type="button" data-add-type="expense"><span class="material-symbols-outlined">receipt_long</span>Dépense</button>
                </div>
              </div>
            </div>
          </div>
'''

new_toolbar = '''          <div class="operations-toolbar">
            <div>
              <h2 class="section-title">Opérations</h2>
              <p class="section-subtitle">${rows.length} opération${rows.length > 1 ? "s" : ""} affichée${rows.length > 1 ? "s" : ""}</p>
            </div>
            <div class="operations-toolbar-actions">
              <div class="operation-menu-wrap">
                <button class="btn tonal small" type="button" data-operation-add-toggle aria-expanded="false"><span class="material-symbols-outlined">add</span>Ajouter</button>
                <div class="operation-menu" data-operation-add-menu hidden>
                  <button type="button" data-add-type="income"><span class="material-symbols-outlined">payments</span>Revenu</button>
                  <button type="button" data-add-type="fixed"><span class="material-symbols-outlined">event_repeat</span>Charge fixe</button>
                  <button type="button" data-add-type="expense"><span class="material-symbols-outlined">receipt_long</span>Dépense</button>
                </div>
              </div>
            </div>
          </div>

          <div class="operation-filter-tabs" role="tablist" aria-label="Filtrer les opérations">
            ${typeOptions.map(([value, label]) => `<button type="button" class="operation-filter-tab ${operationTypeFilter === value ? "active" : ""}" data-operation-type="${value}" role="tab" aria-selected="${operationTypeFilter === value ? "true" : "false"}">${label}</button>`).join("")}
          </div>
'''

if text.count(old_toolbar) != 1:
    raise SystemExit(f'operations toolbar anchor count={text.count(old_toolbar)}')
text = text.replace(old_toolbar, new_toolbar, 1)

old_filter_handler = '''      container.querySelector("[data-operation-filter-toggle]")?.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        toggleOperationMenu("[data-operation-filter-menu]", event.currentTarget);
      });

'''
if text.count(old_filter_handler) != 1:
    raise SystemExit(f'filter handler anchor count={text.count(old_filter_handler)}')
text = text.replace(old_filter_handler, '', 1)

css = r'''
    /* OPERATION-FILTER-TABS-V1 */
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

style_end = text.find('\n  </style>')
if style_end < 0:
    raise SystemExit('style closing tag not found')
text = text[:style_end] + css + text[style_end:]

path.write_text(text, encoding='utf-8')
