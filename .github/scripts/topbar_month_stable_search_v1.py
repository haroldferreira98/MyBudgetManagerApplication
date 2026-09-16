from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'TOPBAR-MONTH-STABLE-SEARCH-V1'

if marker in text:
    raise SystemExit('Patch already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-topbar-month-stable-search-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

old_top = '''      <div class="top-actions">\n        <button class="icon-btn" id="settingsBtn" type="button" aria-label="Paramètres" title="Paramètres">'''
new_top = '''      <div class="top-actions">\n        <!-- TOPBAR-MONTH-STABLE-SEARCH-V1 -->\n        <button class="icon-btn" id="monthBtn" type="button" data-month-picker aria-label="Choisir un mois" title="Choisir un mois">\n          <span class="material-symbols-outlined">calendar_month</span>\n        </button>\n        <button class="icon-btn" id="settingsBtn" type="button" aria-label="Paramètres" title="Paramètres">'''
if text.count(old_top) != 1:
    raise SystemExit(f'Expected one topbar settings anchor, found {text.count(old_top)}')
text = text.replace(old_top, new_top, 1)

# The month picker stays fully functional, but its in-page switcher is removed everywhere.
text, month_calls = re.subn(r'^[ \t]*\$\{renderMonthSwitcher\(\)\}\s*\n', '', text, flags=re.M)
if month_calls < 1:
    raise SystemExit('No rendered month switcher calls found')

old_results = '          ${renderGlobalSearchResults(globalSearch)}'
new_results = '          <div id="globalSearchResultsHost">${renderGlobalSearchResults(globalSearch)}</div>'
if text.count(old_results) != 1:
    raise SystemExit(f'Expected one global search results anchor, found {text.count(old_results)}')
text = text.replace(old_results, new_results, 1)

old_handler = '''      const searchInput = document.getElementById("globalSearchInput");\n      if (searchInput) {\n        searchInput.addEventListener("input", event => {\n          globalSearch = event.target.value;\n          renderHome();\n          applyPrivacy();\n          requestAnimationFrame(() => {\n            const next = document.getElementById("globalSearchInput");\n            if (next) { next.focus(); next.setSelectionRange(next.value.length, next.value.length); }\n          });\n        });\n      }\n      document.getElementById("globalSearchClear")?.addEventListener("click", () => { globalSearch = ""; renderHome(); applyPrivacy(); });'''
new_handler = '''      const searchInput = document.getElementById("globalSearchInput");\n      const searchResultsHost = document.getElementById("globalSearchResultsHost");\n      const searchClear = document.getElementById("globalSearchClear");\n      const refreshGlobalSearch = () => {\n        if (searchResultsHost) searchResultsHost.innerHTML = renderGlobalSearchResults(globalSearch);\n        searchClear?.classList.toggle("hidden", !globalSearch);\n        applyPrivacy();\n      };\n      searchInput?.addEventListener("input", event => {\n        globalSearch = event.currentTarget.value;\n        refreshGlobalSearch();\n      });\n      searchClear?.addEventListener("click", () => {\n        globalSearch = "";\n        if (searchInput) {\n          searchInput.value = "";\n          searchInput.focus({ preventScroll: true });\n        }\n        refreshGlobalSearch();\n      });'''
if text.count(old_handler) != 1:
    raise SystemExit(f'Expected one global search input handler, found {text.count(old_handler)}')
text = text.replace(old_handler, new_handler, 1)

path.write_text(text, encoding='utf-8')
