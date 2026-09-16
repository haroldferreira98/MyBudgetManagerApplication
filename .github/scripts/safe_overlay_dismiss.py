from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

marker = "SAFE-OVERLAY-DISMISS-V1"
if marker in text:
    raise SystemExit("Safe overlay dismissal patch already applied")
if "function closeOperationMenus()" in text:
    raise SystemExit("Unexpected existing closeOperationMenus implementation")


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, found {count}")
    text = text.replace(old, new, 1)


text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260916-safe-overlay-dismiss-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit("App build marker not found")

style_marker = '  </style>\n</head>'
css = r'''

    /* SAFE-OVERLAY-DISMISS-V1 */
    .operation-menu { z-index: 66; }
    .operation-menu-backdrop {
      position: fixed;
      inset: 0;
      z-index: 65;
      background: transparent;
      cursor: default;
      touch-action: manipulation;
    }
    .operation-menu-backdrop[hidden] { display: none !important; }
'''
replace_once(style_marker, css + "\n" + style_marker, "Style marker")

toolbar_anchor = '          <div class="operations-toolbar">'
replace_once(
    toolbar_anchor,
    '          <div class="operation-menu-backdrop" data-operation-menu-backdrop hidden aria-hidden="true"></div>\n\n' + toolbar_anchor,
    "Operations toolbar",
)

listeners_anchor = '''          <div class="list operation-list">${listHtml}</div>
        </div>`;

      container.querySelectorAll("[data-operation-type]").forEach(button => {'''
listeners_replacement = '''          <div class="list operation-list">${listHtml}</div>
        </div>`;

      const operationBackdrop = container.querySelector("[data-operation-menu-backdrop]");
      const toggleOperationMenu = (selector, toggle) => {
        const menu = container.querySelector(selector);
        const willOpen = !!menu?.hidden;
        closeOperationMenus();
        if (willOpen && menu) {
          menu.hidden = false;
          toggle?.setAttribute("aria-expanded", "true");
          if (operationBackdrop) operationBackdrop.hidden = false;
        }
      };
      operationBackdrop?.addEventListener("pointerdown", event => {
        event.stopPropagation();
      });
      operationBackdrop?.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        closeOperationMenus();
      });

      container.querySelectorAll("[data-operation-type]").forEach(button => {'''
replace_once(listeners_anchor, listeners_replacement, "Operations listeners")

old_filter = '''      container.querySelector("[data-operation-filter-toggle]")?.addEventListener("click", event => {
        const menu = container.querySelector("[data-operation-filter-menu]");
        const willOpen = !!menu?.hidden;
        if (menu) menu.hidden = !willOpen;
        event.currentTarget.setAttribute("aria-expanded", String(willOpen));
        const sortMenu = container.querySelector("[data-operation-sort-menu]");
        if (sortMenu) sortMenu.hidden = true;
      });'''
new_filter = '''      container.querySelector("[data-operation-filter-toggle]")?.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        toggleOperationMenu("[data-operation-filter-menu]", event.currentTarget);
      });'''
replace_once(old_filter, new_filter, "Filter toggle")

old_sort = '''      container.querySelector("[data-operation-sort-toggle]")?.addEventListener("click", event => {
        const menu = container.querySelector("[data-operation-sort-menu]");
        const willOpen = !!menu?.hidden;
        if (menu) menu.hidden = !willOpen;
        event.currentTarget.setAttribute("aria-expanded", String(willOpen));
        const filterMenu = container.querySelector("[data-operation-filter-menu]");
        if (filterMenu) filterMenu.hidden = true;
        const addMenu = container.querySelector("[data-operation-add-menu]");
        if (addMenu) addMenu.hidden = true;
      });'''
new_sort = '''      container.querySelector("[data-operation-sort-toggle]")?.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        toggleOperationMenu("[data-operation-sort-menu]", event.currentTarget);
      });'''
replace_once(old_sort, new_sort, "Sort toggle")

old_add = '''      container.querySelector("[data-operation-add-toggle]")?.addEventListener("click", event => {
        const menu = container.querySelector("[data-operation-add-menu]");
        const willOpen = !!menu?.hidden;
        if (menu) menu.hidden = !willOpen;
        event.currentTarget.setAttribute("aria-expanded", String(willOpen));
        const sortMenu = container.querySelector("[data-operation-sort-menu]");
        if (sortMenu) sortMenu.hidden = true;
      });'''
new_add = '''      container.querySelector("[data-operation-add-toggle]")?.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        toggleOperationMenu("[data-operation-add-menu]", event.currentTarget);
      });
      container.querySelectorAll("[data-operation-add-menu] [data-add-type]").forEach(button => {
        button.addEventListener("click", () => closeOperationMenus());
      });'''
replace_once(old_add, new_add, "Add toggle")

modal_anchor = '''    function openModal(id) {
      document.getElementById(id)?.classList.add("open");'''
modal_replacement = '''    function closeOperationMenus() {
      document.querySelectorAll("[data-operation-filter-menu], [data-operation-sort-menu], [data-operation-add-menu]").forEach(menu => {
        menu.hidden = true;
      });
      document.querySelectorAll("[data-operation-filter-toggle], [data-operation-sort-toggle], [data-operation-add-toggle]").forEach(toggle => {
        toggle.setAttribute("aria-expanded", "false");
      });
      document.querySelectorAll("[data-operation-menu-backdrop]").forEach(backdrop => {
        backdrop.hidden = true;
      });
    }

    function openModal(id) {
      closeOperationMenus();
      document.getElementById(id)?.classList.add("open");'''
replace_once(modal_anchor, modal_replacement, "openModal")

old_sheet_listener = '''    document.querySelectorAll(".sheet-backdrop").forEach(backdrop => {
      backdrop.addEventListener("click", event => {
        if (event.target === backdrop) closeModal(backdrop.id);
      });
    });'''
new_sheet_listener = '''    document.addEventListener("click", event => {
      const backdrop = event.target.closest?.(".sheet-backdrop.open");
      if (!backdrop || event.target !== backdrop) return;
      event.preventDefault();
      event.stopPropagation();
      closeModal(backdrop.id);
    }, true);'''
replace_once(old_sheet_listener, new_sheet_listener, "Sheet backdrop listener")

old_escape = '      if (event.key === "Escape") document.querySelectorAll(".sheet-backdrop.open").forEach(el => closeModal(el.id));'
new_escape = '''      if (event.key === "Escape") {
        const hadOperationMenu = !!document.querySelector("[data-operation-filter-menu]:not([hidden]), [data-operation-sort-menu]:not([hidden]), [data-operation-add-menu]:not([hidden])");
        const openSheets = [...document.querySelectorAll(".sheet-backdrop.open")];
        closeOperationMenus();
        openSheets.forEach(el => closeModal(el.id));
        if (hadOperationMenu || openSheets.length) event.preventDefault();
      }'''
replace_once(old_escape, new_escape, "Escape handler")

path.write_text(text, encoding="utf-8")
