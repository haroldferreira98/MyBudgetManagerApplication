from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'SETTINGS-ACCORDION-FOCUS-V1'
if marker in text:
    raise SystemExit('Patch already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-settings-accordion-focus-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

style_anchor = '  </style>\n</head>'
if text.count(style_anchor) != 1:
    raise SystemExit(f'Expected one style closing anchor, found {text.count(style_anchor)}')

css = r'''

    /* SETTINGS-ACCORDION-FOCUS-V1 */
    .settings-back-row {
      display: flex;
      align-items: center;
      margin: 2px 0 12px;
    }
    .settings-back-btn {
      min-height: 40px !important;
      padding-inline: 10px 13px !important;
      gap: 5px;
    }
    .settings-back-btn .material-symbols-outlined { font-size: 20px; }

    /* Une seule catégorie ouverte ; les autres passent au même blur que le mode œil. */
    .operation-list.has-open-category > .expense-category-group:not([open]) > .expense-category-summary > :not(.expense-category-chevron) {
      filter: blur(8px);
      -webkit-filter: blur(8px);
      user-select: none;
      -webkit-user-select: none;
      transition: filter .14s ease;
    }
    .operation-list > .expense-category-group > .expense-category-summary > :not(.expense-category-chevron) {
      transition: filter .14s ease;
    }
    .operation-list.has-open-category > .expense-category-group:not([open]) > .expense-category-summary > .expense-category-chevron {
      filter: none !important;
      -webkit-filter: none !important;
      opacity: 1;
      position: relative;
      z-index: 2;
    }
'''
text = text.replace(style_anchor, css + '\n' + style_anchor, 1)

old_settings = '''      container.innerHTML = `
        <div class="section">
          <div class="card settings-page-card">'''
new_settings = '''      container.innerHTML = `
        <div class="settings-back-row">
          <button class="btn outlined small settings-back-btn" type="button" data-screen="home" aria-label="Retour à l’accueil"><span class="material-symbols-outlined">arrow_back</span>Retour</button>
        </div>
        <div class="section">
          <div class="card settings-page-card">'''
if text.count(old_settings) != 1:
    raise SystemExit(f'Expected one settings render anchor, found {text.count(old_settings)}')
text = text.replace(old_settings, new_settings, 1)

old_toggle = '''      container.querySelectorAll("details[data-operation-category]").forEach(group => {
        group.addEventListener("toggle", () => {
          const category = group.dataset.operationCategory;
          if (!category) return;
          if (group.open) expandedOperationCategories.add(category);
          else expandedOperationCategories.delete(category);
        });
      });'''
new_toggle = '''      const operationCategoryList = container.querySelector(".operation-list");
      const syncOperationCategoryFocus = () => {
        const hasOpenCategory = !!container.querySelector("details[data-operation-category][open]");
        operationCategoryList?.classList.toggle("has-open-category", hasOpenCategory);
      };

      container.querySelectorAll("details[data-operation-category]").forEach(group => {
        group.addEventListener("toggle", () => {
          const category = group.dataset.operationCategory;
          if (!category) return;
          if (group.open) {
            container.querySelectorAll("details[data-operation-category][open]").forEach(other => {
              if (other !== group) other.open = false;
            });
            expandedOperationCategories.clear();
            expandedOperationCategories.add(category);
          } else {
            expandedOperationCategories.delete(category);
          }
          syncOperationCategoryFocus();
        });
      });
      syncOperationCategoryFocus();'''
if text.count(old_toggle) != 1:
    raise SystemExit(f'Expected one operation category toggle block, found {text.count(old_toggle)}')
text = text.replace(old_toggle, new_toggle, 1)

path.write_text(text, encoding='utf-8')
