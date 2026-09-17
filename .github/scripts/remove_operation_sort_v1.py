from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-fixed-category-sort-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

old_state = '    let operationSort = "category";'
new_state = '    const operationSort = "category";'
if text.count(old_state) != 1:
    raise SystemExit(f'Expected one operationSort state, found {text.count(old_state)}')
text = text.replace(old_state, new_state, 1)

old_options = '      const sortOptions = [["category", "Catégorie"], ["date", "Date"], ["amount", "Montant"]];\n'
if text.count(old_options) != 1:
    raise SystemExit(f'Expected one sortOptions declaration, found {text.count(old_options)}')
text = text.replace(old_options, '', 1)

old_menu = '''              <div class="operation-menu-wrap">
                <button class="btn outlined small operation-sort-toggle" type="button" data-operation-sort-toggle aria-label="Trier" title="Trier" aria-expanded="false"><span class="material-symbols-outlined">swap_vert</span></button>
                <div class="operation-menu" data-operation-sort-menu hidden>
                  <div class="operation-menu-title">Trier par</div>
                  ${sortOptions.map(([value, label]) => `<button type="button" class="${operationSort === value ? "active" : ""}" data-operation-sort="${value}"><span class="material-symbols-outlined">${operationSort === value ? "check" : ""}</span>${label}</button>`).join("")}
                </div>
              </div>
'''
if text.count(old_menu) != 1:
    raise SystemExit(f'Expected one operation sort menu, found {text.count(old_menu)}')
text = text.replace(old_menu, '', 1)

old_handlers = '''      container.querySelector("[data-operation-sort-toggle]")?.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        toggleOperationMenu("[data-operation-sort-menu]", event.currentTarget);
      });
      container.querySelectorAll("[data-operation-sort]").forEach(button => {
        button.addEventListener("click", () => {
          operationSort = button.dataset.operationSort || "date";
          renderOperations();
        });
      });
'''
if text.count(old_handlers) != 1:
    raise SystemExit(f'Expected one operation sort handlers block, found {text.count(old_handlers)}')
text = text.replace(old_handlers, '', 1)

path.write_text(text, encoding='utf-8')
