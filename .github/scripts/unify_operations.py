from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

if 'id="screen-operations"' in text:
    raise SystemExit("Operations screen already exists")

text = re.sub(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260916-unified-operations-v1" />',
    text,
    count=1,
)

home_line = '      <section class="screen active" id="screen-home" data-title="Accueil"></section>\n'
if home_line not in text:
    raise SystemExit("Home screen anchor not found")
text = text.replace(
    home_line,
    home_line + '      <section class="screen" id="screen-operations" data-title="Opérations"></section>\n',
    1,
)

nav_pattern = re.compile(r'    <nav class="bottom-nav" aria-label="Navigation principale">.*?    </nav>', re.S)
nav_new = '''    <nav class="bottom-nav" aria-label="Navigation principale">
      <button class="nav-btn active" data-screen="home" aria-label="Accueil">
        <span class="material-symbols-outlined">home</span><span>Accueil</span>
      </button>
      <button class="nav-btn" data-screen="operations" aria-label="Opérations">
        <span class="material-symbols-outlined">receipt_long</span><span>Opérations</span>
      </button>
    </nav>'''
text, n = nav_pattern.subn(nav_new, text, count=1)
if n != 1:
    raise SystemExit("Bottom navigation block not found")

style_marker = '  </style>\n</head>'
if style_marker not in text:
    raise SystemExit("Style marker not found")
operations_css = r'''

    /* UNIFIED-OPERATIONS-V1 */
    .bottom-nav { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
    #screen-income, #screen-fixed, #screen-expenses { display: none !important; }
    .operations-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin: 14px 0 10px;
    }
    .operations-toolbar-actions { display: flex; align-items: center; gap: 7px; flex: 0 0 auto; }
    .operation-type-bar {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 5px;
      margin: 10px 0 12px;
      padding: 4px;
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-small);
      background: var(--surface-container-lowest);
    }
    .operation-type-btn {
      min-width: 0;
      min-height: 38px;
      padding: 6px 5px;
      border: 0;
      border-radius: 4px;
      background: transparent;
      color: var(--on-surface-variant);
      font-size: 11px;
      font-weight: 650;
      line-height: 1.15;
      cursor: pointer;
    }
    .operation-type-btn.active { background: var(--primary-container); color: var(--on-primary-container); }
    .operation-menu-wrap { position: relative; }
    .operation-menu {
      position: absolute;
      z-index: 12;
      top: calc(100% + 6px);
      right: 0;
      min-width: 185px;
      padding: 4px;
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-small);
      background: var(--surface-container-lowest);
      box-shadow: 0 12px 28px color-mix(in srgb, var(--shadow) 54%, transparent);
    }
    .operation-menu button {
      width: 100%;
      min-height: 38px;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 7px 9px;
      border: 0;
      border-radius: 4px;
      background: transparent;
      color: var(--on-surface);
      text-align: left;
      cursor: pointer;
      font-size: 12.5px;
    }
    .operation-menu button:hover,
    .operation-menu button.active { background: var(--primary-container); color: var(--on-primary-container); }
    .operation-menu .material-symbols-outlined { width: 18px; font-size: 18px; }
    .operation-list { gap: 7px; }
    .operation-list .list-title { font-weight: 500; }
    .operations-category-items .list-title { font-weight: 400 !important; }
    .operations-category-items .list-sub { display: none; }
    @media (max-width: 430px) {
      .operation-type-bar { gap: 3px; }
      .operation-type-btn { font-size: 10px; padding-inline: 3px; }
      .operations-toolbar { align-items: flex-end; }
      .operations-toolbar-actions { gap: 5px; }
    }
'''
text = text.replace(style_marker, operations_css + "\n" + style_marker, 1)

state_anchor = '    const expandedExpenseCategories = new Set();\n'
if state_anchor not in text:
    raise SystemExit("Operations state anchor not found")
text = text.replace(
    state_anchor,
    state_anchor + '    let operationTypeFilter = "all";\n    let operationSort = "date";\n    let operationSearch = "";\n    const expandedOperationCategories = new Set();\n',
    1,
)

snapshot_pattern = re.compile(r'    function financialSnapshot\(\) \{.*?\n    \}\n\n    function financialStatus', re.S)
snapshot_new = '''    function financialSnapshot() {
      const income = sum(currentMonthIncomes(), x => x.amount);
      const expenses = sum(currentMonthExpenses(), x => x.amount);
      const fixed = sum(activeFixedCharges(), x => x.amount);
      const credits = sum(activeCredits(), x => x.monthlyPayment);
      const projects = 0;
      const engaged = fixed + credits + expenses;
      const remaining = income - engaged;
      const daily = expenses / averageDayCount();

      return {
        income, expenses, fixed, credits, projects, engaged, remaining, daily,
        buckets: {
          needs: fixed + credits,
          wants: expenses,
          savings: Math.max(0, remaining)
        }
      };
    }

    function financialStatus'''
text, n = snapshot_pattern.subn(snapshot_new, text, count=1)
if n != 1:
    raise SystemExit("financialSnapshot function not found")

render_income_anchor = '    function renderIncome() {'
if render_income_anchor not in text:
    raise SystemExit("renderIncome anchor not found")

operations_js = r'''    function operationSignedAmount(amount) {
      const value = safeNumber(amount);
      const sign = value < 0 ? "−" : value > 0 ? "+" : "";
      const klass = value < 0 ? "negative" : value > 0 ? "positive" : "";
      return `<div class="list-amount money ${klass}">${sign}${formatMoney(Math.abs(value))}</div>`;
    }

    function operationRowsForSelectedMonth() {
      const rows = [];

      currentMonthIncomes().forEach(item => rows.push({
        type: "income",
        group: "income",
        id: item.id,
        title: item.label,
        category: item.category || "Salaire",
        amount: safeNumber(item.amount),
        sortDate: String(item.date || ""),
        meta: `${item.category || "Salaire"} · ${formatDate(item.date)}`,
        icon: "payments"
      }));

      currentMonthExpenses().forEach(item => rows.push({
        type: "expense",
        group: "expense",
        id: item.id,
        title: item.label,
        category: item.category || "Dépense",
        amount: -safeNumber(item.amount),
        sortDate: String(item.date || ""),
        meta: `${item.category || "Dépense"} · ${formatDate(item.date)}`,
        icon: categoryIcon(item.category)
      }));

      activeFixedCharges().forEach(item => {
        const day = clamp(Math.round(safeNumber(item.day, 1)), 1, 31);
        rows.push({
          type: "fixed",
          group: "fixed",
          id: item.id,
          title: item.label,
          category: item.category || "Charge fixe",
          amount: -safeNumber(item.amount),
          sortDate: `${selectedMonth}-${String(day).padStart(2, "0")}`,
          meta: "",
          icon: "event_repeat"
        });
      });

      activeCredits().forEach(item => rows.push({
        type: "credit",
        group: "fixed",
        id: item.id,
        title: item.name,
        category: "Crédits",
        amount: -safeNumber(item.monthlyPayment),
        sortDate: `${selectedMonth}-00`,
        meta: "",
        icon: "credit_card"
      }));

      return rows;
    }

    function operationRowHtml(row, grouped = false) {
      const subtitle = (!grouped && row.meta) ? `<div class="list-sub">${escapeHtml(row.meta)}</div>` : "";
      return `
        <div class="list-item operation-list-item" data-edit-type="${row.type}" data-edit-id="${row.id}" role="button" tabindex="0">
          <div class="list-icon"><span class="material-symbols-outlined">${row.icon}</span></div>
          <div class="list-main">
            <div class="list-title">${escapeHtml(row.title)}</div>
            ${subtitle}
          </div>
          <div class="list-side">${operationSignedAmount(row.amount)}</div>
        </div>`;
    }

    function renderOperations() {
      const container = document.getElementById("screen-operations");
      if (!container) return;

      const searchNeedle = normalizeSearch(operationSearch);
      let rows = operationRowsForSelectedMonth().filter(row => {
        const typeOk = operationTypeFilter === "all" || row.group === operationTypeFilter;
        if (!typeOk) return false;
        if (!searchNeedle) return true;
        return normalizeSearch([row.title, row.category, row.meta, Math.abs(row.amount), formatMoney(Math.abs(row.amount))].join(" ")).includes(searchNeedle);
      });

      rows.sort((a, b) => {
        if (operationSort === "category") {
          const categoryCompare = String(a.category).localeCompare(String(b.category), "fr", { sensitivity: "base" });
          if (categoryCompare) return categoryCompare;
          return String(a.title).localeCompare(String(b.title), "fr", { sensitivity: "base" });
        }
        if (operationSort === "amount") {
          const amountCompare = Math.abs(b.amount) - Math.abs(a.amount);
          if (amountCompare) return amountCompare;
          return String(b.sortDate).localeCompare(String(a.sortDate));
        }
        const dateCompare = String(b.sortDate).localeCompare(String(a.sortDate));
        if (dateCompare) return dateCompare;
        return String(a.title).localeCompare(String(b.title), "fr", { sensitivity: "base" });
      });

      let listHtml = "";
      if (!rows.length) {
        listHtml = emptyState("receipt_long", "Aucune opération", "Aucune opération ne correspond aux filtres sélectionnés.");
      } else if (operationSort === "category") {
        const groups = new Map();
        rows.forEach(row => {
          if (!groups.has(row.category)) groups.set(row.category, []);
          groups.get(row.category).push(row);
        });
        listHtml = [...groups.entries()].map(([category, items]) => {
          const total = sum(items, item => item.amount);
          return `
            <details class="expense-category-group" data-operation-category="${escapeHtml(category)}" ${expandedOperationCategories.has(category) ? "open" : ""}>
              <summary class="expense-category-summary">
                <div>
                  <div class="expense-category-label">${escapeHtml(category)}</div>
                  <div class="expense-category-meta">${items.length} opération${items.length > 1 ? "s" : ""}</div>
                </div>
                <div class="expense-category-total">${operationSignedAmount(total)}</div>
                <span class="material-symbols-outlined expense-category-chevron">expand_more</span>
              </summary>
              <div class="expense-category-items operations-category-items">${items.map(item => operationRowHtml(item, true)).join("")}</div>
            </details>`;
        }).join("");
      } else {
        listHtml = rows.map(item => operationRowHtml(item, false)).join("");
      }

      const typeOptions = [
        ["all", "Toutes"],
        ["income", "Revenus"],
        ["fixed", "Charges fixes"],
        ["expense", "Dépenses"]
      ];
      const sortOptions = [["category", "Catégorie"], ["date", "Date"], ["amount", "Montant"]];

      container.innerHTML = `
        ${renderMonthSwitcher()}
        <div class="section" style="margin-top:12px">
          <div class="search-shell">
            <span class="material-symbols-outlined">search</span>
            <input id="operationSearchInput" type="search" inputmode="search" autocomplete="off" placeholder="Rechercher une opération…" value="${escapeHtml(operationSearch)}">
            <button class="icon-btn ${operationSearch ? "" : "hidden"}" id="operationSearchClear" type="button" aria-label="Effacer"><span class="material-symbols-outlined">close</span></button>
          </div>

          <div class="operation-type-bar" aria-label="Filtrer les opérations">
            ${typeOptions.map(([value, label]) => `<button class="operation-type-btn ${operationTypeFilter === value ? "active" : ""}" type="button" data-operation-type="${value}">${label}</button>`).join("")}
          </div>

          <div class="operations-toolbar">
            <div>
              <h2 class="section-title">Opérations</h2>
              <p class="section-subtitle">${rows.length} opération${rows.length > 1 ? "s" : ""} affichée${rows.length > 1 ? "s" : ""}</p>
            </div>
            <div class="operations-toolbar-actions">
              <div class="operation-menu-wrap">
                <button class="btn outlined small" type="button" data-operation-sort-toggle aria-expanded="false"><span class="material-symbols-outlined">sort</span>Trier</button>
                <div class="operation-menu" data-operation-sort-menu hidden>
                  ${sortOptions.map(([value, label]) => `<button type="button" class="${operationSort === value ? "active" : ""}" data-operation-sort="${value}"><span class="material-symbols-outlined">${operationSort === value ? "check" : ""}</span>${label}</button>`).join("")}
                </div>
              </div>
              <div class="operation-menu-wrap">
                <button class="btn tonal small" type="button" data-operation-add-toggle aria-expanded="false"><span class="material-symbols-outlined">add</span>Ajouter</button>
                <div class="operation-menu" data-operation-add-menu hidden>
                  <button type="button" data-add-type="income"><span class="material-symbols-outlined">payments</span>Revenu</button>
                  <button type="button" data-add-type="fixed"><span class="material-symbols-outlined">event_repeat</span>Charge fixe</button>
                  <button type="button" data-add-type="credit"><span class="material-symbols-outlined">credit_card</span>Crédit</button>
                  <button type="button" data-add-type="expense"><span class="material-symbols-outlined">receipt_long</span>Dépense</button>
                </div>
              </div>
            </div>
          </div>

          <div class="list operation-list">${listHtml}</div>
        </div>`;

      container.querySelectorAll("[data-operation-type]").forEach(button => {
        button.addEventListener("click", () => {
          operationTypeFilter = button.dataset.operationType || "all";
          renderOperations();
        });
      });

      const searchInput = document.getElementById("operationSearchInput");
      searchInput?.addEventListener("input", event => {
        operationSearch = event.target.value;
        renderOperations();
        requestAnimationFrame(() => {
          const next = document.getElementById("operationSearchInput");
          if (next) {
            next.focus();
            next.setSelectionRange(next.value.length, next.value.length);
          }
        });
      });
      document.getElementById("operationSearchClear")?.addEventListener("click", () => {
        operationSearch = "";
        renderOperations();
      });

      container.querySelector("[data-operation-sort-toggle]")?.addEventListener("click", event => {
        const menu = container.querySelector("[data-operation-sort-menu]");
        const willOpen = !!menu?.hidden;
        if (menu) menu.hidden = !willOpen;
        event.currentTarget.setAttribute("aria-expanded", String(willOpen));
        const addMenu = container.querySelector("[data-operation-add-menu]");
        if (addMenu) addMenu.hidden = true;
      });
      container.querySelectorAll("[data-operation-sort]").forEach(button => {
        button.addEventListener("click", () => {
          operationSort = button.dataset.operationSort || "date";
          renderOperations();
        });
      });
      container.querySelector("[data-operation-add-toggle]")?.addEventListener("click", event => {
        const menu = container.querySelector("[data-operation-add-menu]");
        const willOpen = !!menu?.hidden;
        if (menu) menu.hidden = !willOpen;
        event.currentTarget.setAttribute("aria-expanded", String(willOpen));
        const sortMenu = container.querySelector("[data-operation-sort-menu]");
        if (sortMenu) sortMenu.hidden = true;
      });

      container.querySelectorAll("details[data-operation-category]").forEach(group => {
        group.addEventListener("toggle", () => {
          const category = group.dataset.operationCategory;
          if (!category) return;
          if (group.open) expandedOperationCategories.add(category);
          else expandedOperationCategories.delete(category);
        });
      });
    }

'''
text = text.replace(render_income_anchor, operations_js + render_income_anchor, 1)

screen_old = '      currentScreen = ["home", "income", "fixed", "expenses", "settings"].includes(screen) ? screen : "home";'
screen_new = '      currentScreen = ["home", "operations", "settings"].includes(screen) ? screen : "home";'
if screen_old not in text:
    raise SystemExit("setCurrentScreen route list not found")
text = text.replace(screen_old, screen_new, 1)

render_all_anchor = '      renderHome();\n      renderIncome();'
if render_all_anchor not in text:
    raise SystemExit("renderAll anchor not found")
text = text.replace(render_all_anchor, '      renderHome();\n      renderOperations();\n      renderIncome();', 1)

text = text.replace(',{value:"project",label:"Projet d\'épargne"}', '', 1)

project_section = re.compile(
    r'\n        <div class="section">\n          <div class="section-header"><div><h2 class="section-title">Projets d\'épargne</h2>.*?(?=\n        <div class="section">\n          <div class="section-header"><div><h2 class="section-title">Sauvegarde & données</h2>)',
    re.S,
)
text, removed = project_section.subn('', text, count=1)
if removed != 1:
    raise SystemExit("Project savings section not found")

path.write_text(text, encoding="utf-8")
