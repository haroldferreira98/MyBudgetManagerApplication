from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-health-reimbursement-ui-v2" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

# Replace the initial reimbursement CSS with a compact mobile-first layout.
css_start = text.find('    /* HEALTH-REIMBURSEMENT-TRACKING-V1 */')
css_end = text.find('\n  </style>', css_start)
if css_start < 0 or css_end < 0:
    raise SystemExit('health reimbursement CSS block not found')

new_css = r'''    /* HEALTH-REIMBURSEMENT-TRACKING-V2 */
    .health-reimbursement-section {
      margin-top: 7px;
      border-top: 1px solid color-mix(in srgb, var(--outline-variant) 62%, transparent);
      padding-top: 9px;
    }
    .health-reimbursement-section[hidden],
    .health-reimbursement-details[hidden] { display: none !important; }
    .health-track-row {
      min-height: 52px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding: 8px 2px;
      cursor: pointer;
    }
    .health-track-copy {
      min-width: 0;
      display: grid;
      gap: 2px;
      flex: 1;
    }
    .health-track-copy strong {
      color: var(--on-surface);
      font-size: 13px;
      line-height: 1.2;
      font-weight: 700;
    }
    .health-track-copy small {
      color: var(--on-surface-variant);
      font-size: 10.5px;
      line-height: 1.3;
      font-weight: 400;
    }
    .health-switch-control {
      position: relative;
      flex: 0 0 42px;
      width: 42px;
      height: 24px;
      display: block;
    }
    #entityModal[data-entity-type="expense"] .health-switch-control input[type="checkbox"] {
      position: absolute !important;
      inset: 0 !important;
      width: 42px !important;
      height: 24px !important;
      min-width: 42px !important;
      max-width: 42px !important;
      margin: 0 !important;
      padding: 0 !important;
      opacity: 0 !important;
      cursor: pointer;
      z-index: 2;
    }
    .health-switch-ui {
      position: absolute;
      inset: 0;
      border-radius: 999px;
      background: var(--surface-container-highest);
      border: 1px solid var(--outline-variant);
      transition: background .16s ease, border-color .16s ease;
      pointer-events: none;
    }
    .health-switch-ui::after {
      content: "";
      position: absolute;
      top: 3px;
      left: 3px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--on-surface-variant);
      transition: transform .16s ease, background .16s ease;
    }
    .health-switch-control input:checked + .health-switch-ui {
      background: var(--primary);
      border-color: var(--primary);
    }
    .health-switch-control input:checked + .health-switch-ui::after {
      transform: translateX(18px);
      background: var(--on-primary);
    }
    .health-switch-control input:focus-visible + .health-switch-ui {
      outline: 3px solid color-mix(in srgb, var(--primary) 28%, transparent);
      outline-offset: 2px;
    }
    .health-reimbursement-details {
      display: grid;
      gap: 0;
      margin-top: 3px;
      border-top: 1px solid color-mix(in srgb, var(--outline-variant) 58%, transparent);
    }
    .health-refund-source {
      padding: 10px 2px 8px;
      border-bottom: 1px solid color-mix(in srgb, var(--outline-variant) 58%, transparent);
    }
    .health-refund-source-title {
      display: flex;
      align-items: center;
      gap: 7px;
      margin-bottom: 3px;
      color: var(--on-surface);
      font-size: 12px;
      line-height: 1.2;
      font-weight: 700;
    }
    .health-refund-source-title .material-symbols-outlined {
      font-size: 17px;
      color: var(--primary);
    }
    .health-refund-fields {
      grid-template-columns: minmax(0, .82fr) minmax(0, 1.18fr) !important;
      gap: 8px !important;
    }
    .health-refund-source .field {
      margin: 5px 0 2px !important;
      gap: 3px !important;
    }
    .health-refund-source .field label { font-size: 10.5px !important; }
    #entityModal[data-entity-type="expense"] .health-refund-source input {
      min-height: 42px !important;
      padding: 7px 9px !important;
      font-size: 14px !important;
    }
    .health-reimbursement-preview {
      margin-top: 10px;
      padding: 10px 11px;
      border-radius: var(--radius-small);
      background: color-mix(in srgb, var(--success-container) 25%, var(--surface-container-lowest));
      border: 1px solid color-mix(in srgb, var(--success) 22%, var(--outline-variant));
    }
    .health-reimbursement-preview-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 7px;
      font-size: 11.5px;
    }
    .health-reimbursement-preview-head span {
      color: var(--success);
      font-size: 13px;
      font-weight: 750;
    }
    .health-reimbursement-preview-grid,
    .health-category-reimbursement-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-top: 8px;
    }
    .health-reimbursement-preview-grid span,
    .health-category-reimbursement-grid span { min-width: 0; display: grid; gap: 2px; }
    .health-reimbursement-preview-grid small,
    .health-category-reimbursement-grid small {
      color: var(--on-surface-variant);
      font-size: 9px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .health-reimbursement-preview-grid strong,
    .health-category-reimbursement-grid strong { font-size: 11px; white-space: nowrap; }
    #entityModal.health-reimbursement-available .sheet {
      max-height: min(78dvh, 760px) !important;
    }
    #entityModal.health-reimbursement-open .sheet {
      max-height: calc(100dvh - var(--safe-top) - var(--safe-bottom) - 14px) !important;
    }
    #entityModal.health-reimbursement-open .sheet-body {
      min-height: 0;
      overflow-y: auto !important;
      overscroll-behavior: contain;
    }
    .health-reimbursement-row-meta { color: var(--success); }
    .health-reimbursement-operation .list-icon {
      color: var(--success);
      background: color-mix(in srgb, var(--success-container) 45%, var(--surface-container-low));
    }
    .health-category-reimbursement-summary {
      margin: 8px 10px 2px;
      padding: 10px 11px;
      border-radius: var(--radius-small);
      background: color-mix(in srgb, var(--success-container) 24%, var(--surface-container-lowest));
      border: 1px solid color-mix(in srgb, var(--success) 22%, var(--outline-variant));
    }
    .health-category-reimbursement-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-size: 11px;
    }
    .health-category-reimbursement-head > span {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--on-surface-variant);
      font-weight: 650;
    }
    .health-category-reimbursement-head .material-symbols-outlined { font-size: 17px; color: var(--success); }
    .health-category-reimbursement-head > strong { color: var(--success); font-size: 13px; }
'''
text = text[:css_start] + new_css + text[css_end:]

old_markup = '''          <div class="health-reimbursement-section" data-health-reimbursement-section hidden>
            <label class="checkbox-row health-reimbursement-toggle"><input name="healthReimbursementTracked" type="checkbox" ${normalizeHealthReimbursement(data.healthReimbursement).tracked ? "checked" : ""}><span><strong>Suivi de remboursement</strong><small>Suivre la Sécurité sociale et la mutuelle</small></span></label>
            <div class="health-reimbursement-details" data-health-reimbursement-details hidden>
              ${[["socialSecurity","Sécurité sociale","health_and_safety","healthSocialSecurityAmount","healthSocialSecurityDate"],["mutual","Mutuelle","verified_user","healthMutualAmount","healthMutualDate"]].map(([key,label,icon,amountName,dateName]) => { const h=normalizeHealthReimbursement(data.healthReimbursement)[key]; return `<div class="health-refund-source"><div class="health-refund-source-title"><span class="material-symbols-outlined">${icon}</span>${label}</div><div class="field-row"><div class="field"><label>Montant remboursé (€)</label>${moneyInputMarkup(amountName,h.amount)}</div><div class="field"><label>Date du remboursement</label><input name="${dateName}" type="date" value="${escapeHtml(h.date)}"></div></div></div>`; }).join("")}
              <div class="health-reimbursement-preview" data-health-reimbursement-preview></div>
            </div>
          </div>`;'''
new_markup = '''          <div class="health-reimbursement-section" data-health-reimbursement-section hidden>
            <label class="health-track-row">
              <span class="health-track-copy"><strong>Suivi de remboursement</strong><small>Associer les remboursements à cette dépense santé</small></span>
              <span class="health-switch-control"><input name="healthReimbursementTracked" type="checkbox" ${normalizeHealthReimbursement(data.healthReimbursement).tracked ? "checked" : ""}><span class="health-switch-ui"></span></span>
            </label>
            <div class="health-reimbursement-details" data-health-reimbursement-details hidden>
              ${[["socialSecurity","Sécurité sociale","health_and_safety","healthSocialSecurityAmount","healthSocialSecurityDate"],["mutual","Mutuelle","verified_user","healthMutualAmount","healthMutualDate"]].map(([key,label,icon,amountName,dateName]) => { const h=normalizeHealthReimbursement(data.healthReimbursement)[key]; return `<div class="health-refund-source"><div class="health-refund-source-title"><span class="material-symbols-outlined">${icon}</span>${label}</div><div class="field-row health-refund-fields"><div class="field"><label>Montant (€)</label>${moneyInputMarkup(amountName,h.amount)}</div><div class="field"><label>Reçu le</label><input name="${dateName}" type="date" value="${escapeHtml(h.date)}"></div></div></div>`; }).join("")}
              <div class="health-reimbursement-preview" data-health-reimbursement-preview></div>
            </div>
          </div>`;'''
if text.count(old_markup) != 1:
    raise SystemExit(f'health reimbursement markup anchor count={text.count(old_markup)}')
text = text.replace(old_markup, new_markup, 1)

setup_pattern = re.compile(r'''    function setupHealthReimbursementFields\(target\) \{.*?\n    \}\n\n    function renderEntityFields''', re.S)
new_setup = '''    function setupHealthReimbursementFields(target) {
      const category = target.querySelector('[name="category"]');
      const section = target.querySelector("[data-health-reimbursement-section]");
      const tracking = target.querySelector('[name="healthReimbursementTracked"]');
      const details = target.querySelector("[data-health-reimbursement-details]");
      const modal = document.getElementById("entityModal");
      if (!category || !section || !tracking || !details) return;

      const sync = () => {
        const isHealth = category.value === "Santé";
        const isTracking = isHealth && tracking.checked;
        section.hidden = !isHealth;
        details.hidden = !isTracking;
        modal?.classList.toggle("health-reimbursement-available", isHealth);
        modal?.classList.toggle("health-reimbursement-open", isTracking);
        if (isTracking) updateHealthReimbursementPreview(target);
      };

      category.addEventListener("change", sync);
      tracking.addEventListener("change", sync);
      ["amount", "healthSocialSecurityAmount", "healthMutualAmount"].forEach(name => {
        target.querySelector(`[name="${name}"]`)?.addEventListener("input", () => updateHealthReimbursementPreview(target));
      });
      sync();
    }

    function renderEntityFields'''
text, count = setup_pattern.subn(new_setup, text, count=1)
if count != 1:
    raise SystemExit(f'setupHealthReimbursementFields replacement count={count}')

old_setup_call = '      if (type === "expense") { setupHealthReimbursementFields(target); requestAnimationFrame(() => target.querySelector(\'[name="amount"]\')?.focus()); }'
new_setup_call = '''      const healthModal = document.getElementById("entityModal");
      if (type === "expense") {
        setupHealthReimbursementFields(target);
        requestAnimationFrame(() => target.querySelector('[name="amount"]')?.focus());
      } else {
        healthModal?.classList.remove("health-reimbursement-available", "health-reimbursement-open");
      }'''
if text.count(old_setup_call) != 1:
    raise SystemExit(f'health setup call anchor count={text.count(old_setup_call)}')
text = text.replace(old_setup_call, new_setup_call, 1)

# Reimbursements are displayed in the month they actually reach the account,
# even when their source healthcare expense belongs to an earlier month.
old_rows = '''      currentMonthExpenses().forEach(item => {
        const hs = healthReimbursementSummary(item);
        rows.push({ type:"expense", group:"expense", id:item.id, title:item.label, category:item.category||"Dépense", amount:-safeNumber(item.amount), sortDate:String(item.date||""), meta:`${item.category || "Dépense"} · ${formatOperationDate(item.date)}`, icon:categoryIcon(item.category), healthMeta:hs ? `${hs.status} · ${hs.percent.toFixed(0)}% remboursé` : "" });
        healthReimbursementOperationRows(item).filter(r => isCurrentMonth(r.sortDate)).forEach(r => rows.push(r));
      });'''
new_rows = '''      currentMonthExpenses().forEach(item => {
        const hs = healthReimbursementSummary(item);
        rows.push({ type:"expense", group:"expense", id:item.id, title:item.label, category:item.category||"Dépense", amount:-safeNumber(item.amount), sortDate:String(item.date||""), meta:`${item.category || "Dépense"} · ${formatOperationDate(item.date)}`, icon:categoryIcon(item.category), healthMeta:hs ? `${hs.status} · ${hs.percent.toFixed(0)}% remboursé` : "" });
      });

      state.expenses.forEach(item => {
        healthReimbursementOperationRows(item)
          .filter(row => isCurrentMonth(row.sortDate))
          .forEach(row => rows.push(row));
      });'''
if text.count(old_rows) != 1:
    raise SystemExit(f'operation reimbursement rows anchor count={text.count(old_rows)}')
text = text.replace(old_rows, new_rows, 1)

path.write_text(text, encoding='utf-8')
