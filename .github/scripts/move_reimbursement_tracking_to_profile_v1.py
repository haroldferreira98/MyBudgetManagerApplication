from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Build marker
text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-reimbursement-profile-tracking-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

# Independent reimbursement month + month picker context.
old_vars = '''    let selectedMonth = monthKey();
    let monthPickerYear = Number(selectedMonth.slice(0, 4));
    let preservedScrollY = null;'''
new_vars = '''    let selectedMonth = monthKey();
    let reimbursementTrackingMonth = monthKey();
    let monthPickerContext = "budget";
    let monthPickerYear = Number(selectedMonth.slice(0, 4));
    let preservedScrollY = null;'''
if text.count(old_vars) != 1:
    raise SystemExit(f'month vars anchor count={text.count(old_vars)}')
text = text.replace(old_vars, new_vars, 1)

# Reuse the month picker without coupling reimbursement tracking to the budget month.
old_picker = '''    function openMonthPicker() {
      const [year] = selectedMonth.split("-").map(Number);
      monthPickerYear = year || new Date().getFullYear();
      let modal = document.getElementById("monthPickerModal");
      if (!modal) {
        document.body.insertAdjacentHTML("beforeend", `
          <div class="sheet-backdrop" id="monthPickerModal" role="dialog" aria-modal="true" aria-labelledby="monthPickerTitle">
            <div class="sheet month-picker-sheet">
              <div class="sheet-handle"></div>
              <div class="sheet-head">
                <h2 class="sheet-title" id="monthPickerTitle">Choisir un mois</h2>
                <button class="icon-btn" data-close-modal="monthPickerModal" aria-label="Fermer"><span class="material-symbols-outlined">close</span></button>
              </div>
              <div class="sheet-body" id="monthPickerBody"></div>
            </div>
          </div>`);
        modal = document.getElementById("monthPickerModal");
      }
      renderMonthPicker();
      modal.classList.add("open");
    }

    function renderMonthPicker() {
      const body = document.getElementById("monthPickerBody");
      if (!body) return;
      const currentMonthIndex = Number(selectedMonth.slice(5, 7)) - 1;
      const selectedYear = Number(selectedMonth.slice(0, 4));
      const labels = Array.from({ length: 12 }, (_, index) => new Intl.DateTimeFormat("fr-FR", { month: "long" }).format(new Date(2026, index, 1)));
      body.innerHTML = `
        <div class="month-picker-year-row">
          <button class="month-picker-year-btn" data-picker-year="-1" aria-label="Année précédente"><span class="material-symbols-outlined">chevron_left</span></button>
          <strong>${monthPickerYear}</strong>
          <button class="month-picker-year-btn" data-picker-year="1" aria-label="Année suivante"><span class="material-symbols-outlined">chevron_right</span></button>
        </div>
        <div class="month-picker-grid">
          ${labels.map((label, index) => {
            const active = monthPickerYear === selectedYear && index === currentMonthIndex;
            return `<button class="month-picker-option ${active ? "active" : ""}" data-picker-month="${index}">${escapeHtml(label)}</button>`;
          }).join("")}
        </div>`;
    }
'''
new_picker = '''    function openMonthPicker(context = "budget") {
      monthPickerContext = context === "reimbursement" ? "reimbursement" : "budget";
      const targetMonth = monthPickerContext === "reimbursement" ? reimbursementTrackingMonth : selectedMonth;
      const [year] = targetMonth.split("-").map(Number);
      monthPickerYear = year || new Date().getFullYear();
      let modal = document.getElementById("monthPickerModal");
      if (!modal) {
        document.body.insertAdjacentHTML("beforeend", `
          <div class="sheet-backdrop" id="monthPickerModal" role="dialog" aria-modal="true" aria-labelledby="monthPickerTitle">
            <div class="sheet month-picker-sheet">
              <div class="sheet-handle"></div>
              <div class="sheet-head">
                <h2 class="sheet-title" id="monthPickerTitle">Choisir un mois</h2>
                <button class="icon-btn" data-close-modal="monthPickerModal" aria-label="Fermer"><span class="material-symbols-outlined">close</span></button>
              </div>
              <div class="sheet-body" id="monthPickerBody"></div>
            </div>
          </div>`);
        modal = document.getElementById("monthPickerModal");
      }
      const title = document.getElementById("monthPickerTitle");
      if (title) title.textContent = monthPickerContext === "reimbursement" ? "Mois du suivi" : "Choisir un mois";
      renderMonthPicker();
      modal.classList.add("open");
    }

    function renderMonthPicker() {
      const body = document.getElementById("monthPickerBody");
      if (!body) return;
      const targetMonth = monthPickerContext === "reimbursement" ? reimbursementTrackingMonth : selectedMonth;
      const currentMonthIndex = Number(targetMonth.slice(5, 7)) - 1;
      const selectedYear = Number(targetMonth.slice(0, 4));
      const labels = Array.from({ length: 12 }, (_, index) => new Intl.DateTimeFormat("fr-FR", { month: "long" }).format(new Date(2026, index, 1)));
      body.innerHTML = `
        <div class="month-picker-year-row">
          <button class="month-picker-year-btn" data-picker-year="-1" aria-label="Année précédente"><span class="material-symbols-outlined">chevron_left</span></button>
          <strong>${monthPickerYear}</strong>
          <button class="month-picker-year-btn" data-picker-year="1" aria-label="Année suivante"><span class="material-symbols-outlined">chevron_right</span></button>
        </div>
        <div class="month-picker-grid">
          ${labels.map((label, index) => {
            const active = monthPickerYear === selectedYear && index === currentMonthIndex;
            return `<button class="month-picker-option ${active ? "active" : ""}" data-picker-month="${index}">${escapeHtml(label)}</button>`;
          }).join("")}
        </div>`;
    }
'''
if text.count(old_picker) != 1:
    raise SystemExit(f'month picker anchor count={text.count(old_picker)}')
text = text.replace(old_picker, new_picker, 1)

# Remove reimbursement status/details from budget operation rows.
old_expense_rows = '''      currentMonthExpenses().forEach(item => {
        const hs = healthReimbursementSummary(item);
        rows.push({ type:"expense", group:"expense", id:item.id, title:item.label, category:item.category||"Dépense", amount:-safeNumber(item.amount), sortDate:String(item.date||""), meta:`${item.category || "Dépense"} · ${formatOperationDate(item.date)}`, icon:categoryIcon(item.category), healthMeta:hs ? `${hs.status} · ${hs.percent.toFixed(0)}% remboursé` : "" });
      });'''
new_expense_rows = '''      currentMonthExpenses().forEach(item => {
        rows.push({ type:"expense", group:"expense", id:item.id, title:item.label, category:item.category||"Dépense", amount:-safeNumber(item.amount), sortDate:String(item.date||""), meta:`${item.category || "Dépense"} · ${formatOperationDate(item.date)}`, icon:categoryIcon(item.category) });
      });'''
if text.count(old_expense_rows) != 1:
    raise SystemExit(f'operation expense rows anchor count={text.count(old_expense_rows)}')
text = text.replace(old_expense_rows, new_expense_rows, 1)

start = text.find('    function operationRowHtml(row, grouped = false) {')
end = text.find('\n    function operationCategoryItemsHtml(items) {', start)
if start < 0 or end < 0:
    raise SystemExit('operationRowHtml block not found')
new_operation_row = '''    function operationRowHtml(row, grouped = false) {
      const subtitle = !grouped && row.meta ? `<div class="list-sub">${escapeHtml(row.meta)}</div>` : "";
      return `
        <div class="list-item operation-list-item" data-edit-type="${row.type}" data-edit-id="${row.id}" role="button" tabindex="0">
          <div class="list-icon"><span class="material-symbols-outlined">${row.icon}</span></div>
          <div class="list-main"><div class="list-title">${escapeHtml(row.title)}</div>${subtitle}</div>
          <div class="list-side">${operationSignedAmount(row.amount)}</div>
        </div>`;
    }
'''
text = text[:start] + new_operation_row + text[end:]

old_group = '''          const sourceItems = category === "Santé" ? items.filter(item => !item.isHealthReimbursement) : items;
          const total = sum(sourceItems, item => item.amount);
          const operationCount = sourceItems.length;
          const healthSummaryHtml = category === "Santé" ? healthCategoryReimbursementSummaryHtml() : "";'''
new_group = '''          const total = sum(items, item => item.amount);
          const operationCount = items.length;'''
if text.count(old_group) != 1:
    raise SystemExit(f'health operation group anchor count={text.count(old_group)}')
text = text.replace(old_group, new_group, 1)
if text.count('              ${healthSummaryHtml}\n') != 1:
    raise SystemExit('health summary interpolation not found')
text = text.replace('              ${healthSummaryHtml}\n', '', 1)

# Remove health reimbursement synthetic results from global budget search.
old_global = '''      state.expenses.forEach(item => {
        const hs = healthReimbursementSummary(item);
        rows.push({ type:"expense", id:item.id, icon:categoryIcon(item.category), kind:"Dépense", title:item.label,
          subtitle: hs ? `${item.category} · ${formatDate(item.date)} · ${hs.status} ${hs.percent.toFixed(0)}%` : `${item.category} · ${formatDate(item.date)}`, amount:-safeNumber(item.amount),
          haystack:[item.label,item.category,item.date,"dépense","depense",hs?.status||"",hs?`${hs.percent.toFixed(0)}%`:"",...amountTokens(item.amount)].join(" ") });
        healthReimbursementOperationRows(item).forEach(r => rows.push({ type:"expense", id:item.id, icon:r.icon, kind:"Remboursement santé", title:r.title, subtitle:`${r.meta} · ${formatDate(r.sortDate)}`, amount:r.amount, haystack:[r.title,r.meta,r.sortDate,"remboursement","santé","sante",...amountTokens(r.amount)].join(" ") }));
      });'''
new_global = '''      state.expenses.forEach(item => {
        rows.push({ type:"expense", id:item.id, icon:categoryIcon(item.category), kind:"Dépense", title:item.label,
          subtitle:`${item.category} · ${formatDate(item.date)}`, amount:-safeNumber(item.amount),
          haystack:[item.label,item.category,item.date,"dépense","depense",...amountTokens(item.amount)].join(" ") });
      });'''
if text.count(old_global) != 1:
    raise SystemExit(f'global health search anchor count={text.count(old_global)}')
text = text.replace(old_global, new_global, 1)

# Dedicated profile tracking UI, using original health expense month rather than the budget month.
insert_anchor = '\n\n\n    function renderProfile() {'
if text.count(insert_anchor) != 1:
    raise SystemExit(f'renderProfile insert anchor count={text.count(insert_anchor)}')
helpers = r'''

    // REIMBURSEMENT-PROFILE-TRACKING-V1
    function reimbursementMonthLabel(month = reimbursementTrackingMonth) {
      const [year, monthNumber] = String(month || monthKey()).split("-").map(Number);
      const date = new Date(year, Math.max(0, (monthNumber || 1) - 1), 1, 12, 0, 0);
      const label = new Intl.DateTimeFormat("fr-FR", { month: "long", year: "numeric" }).format(date);
      return label.charAt(0).toUpperCase() + label.slice(1);
    }

    function reimbursementTrackingItems(month = reimbursementTrackingMonth) {
      return state.expenses
        .filter(item => item.category === "Santé" && monthKey(item.date) === month && healthReimbursementSummary(item))
        .sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")) || String(a.label || "").localeCompare(String(b.label || ""), "fr", { sensitivity: "base" }));
    }

    function reimbursementSourceRow(label, icon, entry) {
      const amount = safeNumber(entry?.amount);
      const received = amount > 0 && entry?.date;
      return `<div class="reimbursement-source-row">
        <span class="reimbursement-source-name"><span class="material-symbols-outlined">${icon}</span><span><strong>${escapeHtml(label)}</strong><small>${received ? `Reçu le ${escapeHtml(formatOperationDate(entry.date))}` : "En attente"}</small></span></span>
        <strong class="money ${amount > 0 ? "positive" : ""}">${amount > 0 ? `+${formatMoney(amount)}` : "—"}</strong>
      </div>`;
    }

    function reimbursementTrackingHtml() {
      const items = reimbursementTrackingItems();
      if (!items.length) return emptyState("medical_information", "Aucun remboursement suivi", `Aucune dépense Santé suivie en ${reimbursementMonthLabel().toLowerCase()}.`);

      const summaries = items.map(item => ({ item, summary: healthReimbursementSummary(item) })).filter(entry => entry.summary);
      const gross = sum(summaries, entry => entry.summary.gross);
      const refunded = sum(summaries, entry => entry.summary.total);
      const remaining = sum(summaries, entry => entry.summary.remaining);
      const percent = gross > 0 ? refunded / gross * 100 : 0;
      const overview = `<div class="card reimbursement-overview-card">
        <div class="reimbursement-overview-head"><span>${items.length} soin${items.length > 1 ? "s" : ""} suivi${items.length > 1 ? "s" : ""}</span><strong>${percent.toFixed(0)}%</strong></div>
        <div class="reimbursement-overview-grid">
          <span><small>Dépensé</small><strong class="money">${formatMoney(gross)}</strong></span>
          <span><small>Remboursé</small><strong class="money positive">${formatMoney(refunded)}</strong></span>
          <span><small>Reste</small><strong class="money">${formatMoney(remaining)}</strong></span>
        </div>
      </div>`;

      const cards = summaries.map(({ item, summary }) => {
        const reimbursement = summary.reimbursement;
        const displayStatus = summary.gross <= .005 ? "Montant à renseigner" : summary.status;
        return `<div class="card reimbursement-tracking-card" data-edit-type="expense" data-edit-id="${item.id}" role="button" tabindex="0">
          <div class="reimbursement-card-head">
            <div><h3>${escapeHtml(item.label || "Dépense Santé")}</h3><p>${escapeHtml(formatOperationGroupDate(item.date))} · <span class="money">${formatMoney(summary.gross)}</span></p></div>
            <span class="reimbursement-percent">${summary.percent.toFixed(0)}%</span>
          </div>
          <div class="reimbursement-status-row"><span>${escapeHtml(displayStatus)}</span><strong class="money">Reste ${formatMoney(summary.remaining)}</strong></div>
          <div class="progress-track"><div class="progress-fill success" style="width:${clamp(summary.percent,0,100)}%"></div></div>
          <div class="reimbursement-sources">
            ${reimbursementSourceRow("Sécurité sociale", "health_and_safety", reimbursement.socialSecurity)}
            ${reimbursementSourceRow("Mutuelle", "verified_user", reimbursement.mutual)}
          </div>
        </div>`;
      }).join("");
      return `${overview}<div class="reimbursement-tracking-list">${cards}</div>`;
    }
'''
text = text.replace(insert_anchor, helpers + insert_anchor, 1)

# Insert the new section immediately after monthly envelopes.
old_profile_sections = '''        <div class="section">
          <div class="section-header"><div><h2 class="section-title">Enveloppes mensuelles</h2></div><button class="btn tonal small" data-add-type="envelope"><span class="material-symbols-outlined">add</span>Ajouter</button></div>
          <div>${envelopesHtml}</div>
        </div>

        <div class="section">
          <div class="section-header"><div><h2 class="section-title">Sauvegarde & données</h2><p class="section-subtitle">Firebase synchronise automatiquement le compte Google connecté.</p></div></div>'''
new_profile_sections = '''        <div class="section">
          <div class="section-header"><div><h2 class="section-title">Enveloppes mensuelles</h2></div><button class="btn tonal small" data-add-type="envelope"><span class="material-symbols-outlined">add</span>Ajouter</button></div>
          <div>${envelopesHtml}</div>
        </div>

        <div class="section reimbursement-profile-section">
          <div class="section-header reimbursement-section-header">
            <div><h2 class="section-title">Suivi de remboursement</h2><p class="section-subtitle">${escapeHtml(reimbursementMonthLabel())}</p></div>
            <button class="mini-btn reimbursement-calendar-btn" type="button" data-reimbursement-month-picker aria-label="Choisir le mois du suivi" title="Choisir le mois"><span class="material-symbols-outlined">calendar_month</span></button>
          </div>
          <div>${reimbursementTrackingHtml()}</div>
        </div>

        <div class="section">
          <div class="section-header"><div><h2 class="section-title">Sauvegarde & données</h2><p class="section-subtitle">Firebase synchronise automatiquement le compte Google connecté.</p></div></div>'''
if text.count(old_profile_sections) != 1:
    raise SystemExit(f'profile sections anchor count={text.count(old_profile_sections)}')
text = text.replace(old_profile_sections, new_profile_sections, 1)

# Calendar handler and context-aware month selection.
old_month_handler = '''      const monthPicker = event.target.closest("[data-month-picker]");
      if (monthPicker) { openMonthPicker(); return; }

      const pickerYear = event.target.closest("[data-picker-year]");
      if (pickerYear) { monthPickerYear += safeNumber(pickerYear.dataset.pickerYear); renderMonthPicker(); return; }

      const pickerMonth = event.target.closest("[data-picker-month]");
      if (pickerMonth) {
        selectedMonth = `${monthPickerYear}-${String(safeNumber(pickerMonth.dataset.pickerMonth) + 1).padStart(2, "0")}`;
        closeModal("monthPickerModal");
        renderAll();
        return;
      }'''
new_month_handler = '''      const reimbursementMonthPicker = event.target.closest("[data-reimbursement-month-picker]");
      if (reimbursementMonthPicker) { openMonthPicker("reimbursement"); return; }

      const monthPicker = event.target.closest("[data-month-picker]");
      if (monthPicker) { openMonthPicker("budget"); return; }

      const pickerYear = event.target.closest("[data-picker-year]");
      if (pickerYear) { monthPickerYear += safeNumber(pickerYear.dataset.pickerYear); renderMonthPicker(); return; }

      const pickerMonth = event.target.closest("[data-picker-month]");
      if (pickerMonth) {
        const chosenMonth = `${monthPickerYear}-${String(safeNumber(pickerMonth.dataset.pickerMonth) + 1).padStart(2, "0")}`;
        closeModal("monthPickerModal");
        if (monthPickerContext === "reimbursement") {
          reimbursementTrackingMonth = chosenMonth;
          renderProfile();
          renderAccountModal();
        } else {
          selectedMonth = chosenMonth;
          renderAll();
        }
        return;
      }'''
if text.count(old_month_handler) != 1:
    raise SystemExit(f'month event handler anchor count={text.count(old_month_handler)}')
text = text.replace(old_month_handler, new_month_handler, 1)

# Compact profile reimbursement visuals.
css = r'''

    /* REIMBURSEMENT-PROFILE-TRACKING-V1 */
    .reimbursement-section-header { align-items: center; }
    .reimbursement-calendar-btn {
      width: 40px;
      height: 40px;
      flex: 0 0 40px;
      border-radius: 12px;
    }
    .reimbursement-overview-card {
      padding: 14px;
      background: color-mix(in srgb, var(--success-container) 42%, var(--surface-container-lowest));
      border-color: color-mix(in srgb, var(--success) 24%, var(--outline-variant));
    }
    .reimbursement-overview-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 13px;
      font-weight: 700;
    }
    .reimbursement-overview-head strong { color: var(--success); font-size: 17px; }
    .reimbursement-overview-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-top: 11px;
    }
    .reimbursement-overview-grid span { display: grid; gap: 2px; min-width: 0; }
    .reimbursement-overview-grid small { color: var(--on-surface-variant); font-size: 10px; }
    .reimbursement-overview-grid strong { font-size: 13px; white-space: nowrap; }
    .reimbursement-tracking-list { display: grid; gap: 9px; margin-top: 10px; }
    .reimbursement-tracking-card {
      padding: 13px 14px;
      cursor: pointer;
    }
    .reimbursement-tracking-card:active { transform: scale(.995); }
    .reimbursement-card-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
    }
    .reimbursement-card-head h3 { margin: 0; font-size: 15px; line-height: 1.2; }
    .reimbursement-card-head p { margin: 3px 0 0; color: var(--on-surface-variant); font-size: 11px; }
    .reimbursement-percent {
      flex: 0 0 auto;
      color: var(--success);
      font-size: 16px;
      line-height: 1;
      font-weight: 750;
    }
    .reimbursement-status-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin: 10px 0 6px;
      color: var(--on-surface-variant);
      font-size: 10.5px;
    }
    .reimbursement-status-row strong { color: var(--on-surface); font-size: 10.5px; white-space: nowrap; }
    .reimbursement-sources { margin-top: 9px; border-top: 1px solid color-mix(in srgb, var(--outline-variant) 62%, transparent); }
    .reimbursement-source-row {
      min-height: 42px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 7px 0;
    }
    .reimbursement-source-row + .reimbursement-source-row { border-top: 1px solid color-mix(in srgb, var(--outline-variant) 46%, transparent); }
    .reimbursement-source-name { display: flex; align-items: center; gap: 8px; min-width: 0; }
    .reimbursement-source-name > .material-symbols-outlined { color: var(--success); font-size: 18px; }
    .reimbursement-source-name > span { display: grid; gap: 1px; min-width: 0; }
    .reimbursement-source-name strong { font-size: 11px; }
    .reimbursement-source-name small { color: var(--on-surface-variant); font-size: 9.5px; }
    .reimbursement-source-row > strong { flex: 0 0 auto; font-size: 11.5px; }
'''
style_end = text.find('\n  </style>')
if style_end < 0:
    raise SystemExit('style closing tag not found')
text = text[:style_end] + css + text[style_end:]

path.write_text(text, encoding='utf-8')
