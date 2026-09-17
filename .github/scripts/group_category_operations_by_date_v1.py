from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '20260917-category-date-separators-v1'

if marker in text:
    raise SystemExit('Patch already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    f'<meta name="app-build" content="{marker}" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

# Full date heading for grouped operations.
old_date_fn = '''    function formatOperationDate(value) {
      if (!value) return "";
      const date = new Date(`${value}T12:00:00`);
      if (Number.isNaN(date.getTime())) return "";
      return new Intl.DateTimeFormat("fr-FR", { day: "numeric", month: "long" }).format(date);
    }
'''
new_date_fn = old_date_fn + '''
    function formatOperationGroupDate(value) {
      if (!value) return "";
      const date = new Date(`${value}T12:00:00`);
      if (Number.isNaN(date.getTime())) return "";
      return new Intl.DateTimeFormat("fr-FR", { day: "numeric", month: "long", year: "numeric" }).format(date);
    }
'''
if text.count(old_date_fn) != 1:
    raise SystemExit(f'Expected one formatOperationDate function, found {text.count(old_date_fn)}')
text = text.replace(old_date_fn, new_date_fn, 1)

# In grouped category mode, date/category are shown by the surrounding group, so hide the redundant subtitle.
old_subtitle = '      const subtitle = row.meta ? `<div class="list-sub">${escapeHtml(row.meta)}</div>` : "";'
new_subtitle = '      const subtitle = !grouped && row.meta ? `<div class="list-sub">${escapeHtml(row.meta)}</div>` : "";'
if text.count(old_subtitle) != 1:
    raise SystemExit(f'Expected one grouped operation subtitle line, found {text.count(old_subtitle)}')
text = text.replace(old_subtitle, new_subtitle, 1)

# Within a category, sort newest dates first before falling back to title.
old_category_sort = '''          const categoryCompare = String(a.category).localeCompare(String(b.category), "fr", { sensitivity: "base" });
          if (categoryCompare) return categoryCompare;
          return String(a.title).localeCompare(String(b.title), "fr", { sensitivity: "base" });'''
new_category_sort = '''          const categoryCompare = String(a.category).localeCompare(String(b.category), "fr", { sensitivity: "base" });
          if (categoryCompare) return categoryCompare;
          const dateCompare = String(b.sortDate).localeCompare(String(a.sortDate));
          if (dateCompare) return dateCompare;
          return String(a.title).localeCompare(String(b.title), "fr", { sensitivity: "base" });'''
if text.count(old_category_sort) != 1:
    raise SystemExit(f'Expected one category sort block, found {text.count(old_category_sort)}')
text = text.replace(old_category_sort, new_category_sort, 1)

# Add a renderer that groups one category's rows by date (descending).
anchor = '''    function renderOperations() {
'''
helper = '''    function operationCategoryItemsHtml(items) {
      const sortedItems = [...items].sort((a, b) => {
        const dateCompare = String(b.sortDate).localeCompare(String(a.sortDate));
        if (dateCompare) return dateCompare;
        return String(a.title).localeCompare(String(b.title), "fr", { sensitivity: "base" });
      });
      const groups = new Map();
      sortedItems.forEach(item => {
        const dateKey = String(item.sortDate || "");
        if (!groups.has(dateKey)) groups.set(dateKey, []);
        groups.get(dateKey).push(item);
      });
      return [...groups.entries()].map(([dateKey, dateItems]) => `
        <div class="operation-date-group">
          <div class="operation-date-heading">${escapeHtml(formatOperationGroupDate(dateKey))}</div>
          <div class="operation-date-items">${dateItems.map(item => operationRowHtml(item, true)).join("")}</div>
        </div>`).join("");
    }

'''
if text.count(anchor) != 1:
    raise SystemExit(f'Expected one renderOperations anchor, found {text.count(anchor)}')
text = text.replace(anchor, helper + anchor, 1)

old_items = '<div class="expense-category-items operations-category-items">${items.map(item => operationRowHtml(item, true)).join("")}</div>'
new_items = '<div class="expense-category-items operations-category-items">${operationCategoryItemsHtml(items)}</div>'
if text.count(old_items) != 1:
    raise SystemExit(f'Expected one grouped category item renderer, found {text.count(old_items)}')
text = text.replace(old_items, new_items, 1)

# Override card-like rows with compact list rows and inset dividers.
css_anchor = '''    .operations-category-items .list-item:last-child {
      border-bottom: 1px solid color-mix(in srgb, var(--outline-variant) 50%, transparent) !important;
    }
'''
css_add = css_anchor + '''    .operations-category-items {
      display: block;
      gap: 0;
      padding: 0 10px 8px;
    }
    .operation-date-group + .operation-date-group { margin-top: 8px; }
    .operation-date-heading {
      padding: 12px 12px 6px;
      color: var(--on-surface-variant);
      font-size: 12px;
      line-height: 1.2;
      font-weight: 700;
      letter-spacing: .01em;
    }
    .operations-category-items .operation-date-items .list-item,
    html[data-theme="dsfr"] .operations-category-items .operation-date-items .list-item {
      position: relative;
      min-height: 56px !important;
      margin: 0 !important;
      padding: 9px 12px !important;
      gap: 10px;
      border: 0 !important;
      border-radius: 0 !important;
      background: transparent !important;
      box-shadow: none !important;
    }
    .operations-category-items .operation-date-items .list-item:last-child {
      border-bottom: 0 !important;
    }
    .operations-category-items .operation-date-items .list-item::after {
      content: none;
    }
    .operations-category-items .operation-date-items .list-item:not(:last-child)::after {
      content: "";
      position: absolute;
      left: 12px;
      right: 12px;
      bottom: 0;
      height: 1px;
      background: color-mix(in srgb, var(--outline-variant) 62%, transparent);
      pointer-events: none;
    }
'''
if text.count(css_anchor) != 1:
    raise SystemExit(f'Expected one operations last-child CSS anchor, found {text.count(css_anchor)}')
text = text.replace(css_anchor, css_add, 1)

path.write_text(text, encoding='utf-8')
