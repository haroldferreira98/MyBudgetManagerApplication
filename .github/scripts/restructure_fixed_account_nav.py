from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label, count=1):
    global s
    if s.count(old) < count:
        raise SystemExit(f'Missing patch target: {label}')
    s = s.replace(old, new, count)

css = '''

    /* FIXED-NAV-ACCOUNT-V2 */
    .bottom-nav { grid-template-columns: repeat(5, minmax(0, 1fr)) !important; }
    .nav-btn { min-width: 0; }
    .nav-btn > span:last-child { white-space: nowrap; font-size: 8.5px; }
    .fixed-charge-list { gap: 7px; }
    .fixed-charge-row {
      min-height: 62px;
      padding: 9px 11px;
      gap: 10px;
      transition: opacity .18s ease, background .18s ease;
    }
    .fixed-charge-row .list-icon {
      width: 36px;
      height: 36px;
      flex: 0 0 36px;
      border-radius: 13px;
    }
    .fixed-charge-row .list-icon .material-symbols-outlined { font-size: 21px; }
    .fixed-charge-row .list-title { font-size: 14px; }
    .fixed-charge-row .list-sub { margin-top: 2px; font-size: 11px; }
    .fixed-charge-row .list-amount { font-size: 14px; }
    .fixed-charge-row .item-actions { margin-left: 0; }
    .fixed-charge-row.pending {
      opacity: .52;
      background: color-mix(in srgb, var(--surface-container) 72%, var(--surface));
    }
    .fixed-charge-row.pending .list-icon {
      background: var(--surface-container-high);
      color: var(--on-surface-variant);
    }
    .account-profile-content { margin-top: 18px; padding-top: 4px; border-top: 1px solid color-mix(in srgb, var(--outline-variant) 55%, transparent); }
    .account-profile-content .section:first-child { margin-top: 14px; }
    #accountModal .sheet { max-height: calc(100dvh - var(--safe-top) - var(--safe-bottom) - 12px); }
    #screen-profile { display: none !important; }
    #screen-settings .settings-page-card { padding: 16px; }
'''
if '/* FIXED-NAV-ACCOUNT-V2 */' not in s:
    rep('\n</style>', css + '\n</style>', 'css marker')

old_top = '''      <div class="top-actions">\n        <button class="icon-btn" id="settingsBtn" type="button" aria-label="Paramètres" title="Paramètres">\n          <span class="material-symbols-outlined">settings</span>\n        </button>\n      </div>\n'''
rep(old_top, '', 'top settings button')

old_screens = '''      <section class="screen active" id="screen-home" data-title="Accueil"></section>\n      <section class="screen" id="screen-income" data-title="Revenus"></section>\n      <section class="screen" id="screen-expenses" data-title="Dépenses"></section>\n      <section class="screen" id="screen-profile" data-title="Profil & patrimoine"></section>'''
new_screens = '''      <section class="screen active" id="screen-home" data-title="Accueil"></section>\n      <section class="screen" id="screen-income" data-title="Revenus"></section>\n      <section class="screen" id="screen-fixed" data-title="Charges fixes"></section>\n      <section class="screen" id="screen-expenses" data-title="Dépenses"></section>\n      <section class="screen" id="screen-settings" data-title="Paramètres"></section>\n      <section class="screen" id="screen-profile" data-title="Profil & patrimoine" aria-hidden="true"></section>'''
rep(old_screens, new_screens, 'screens')

old_nav = '''      <button class="nav-btn active" data-screen="home" aria-label="Accueil">\n        <span class="material-symbols-outlined">home</span><span>Accueil</span>\n      </button>\n      <button class="nav-btn" data-screen="income" aria-label="Revenus">\n        <span class="material-symbols-outlined">payments</span><span>Revenus</span>\n      </button>\n      <button class="nav-btn" data-screen="expenses" aria-label="Dépenses">\n        <span class="material-symbols-outlined">receipt_long</span><span>Dépenses</span>\n      </button>\n      <button class="nav-btn" data-screen="profile" aria-label="Profil">\n        <span class="material-symbols-outlined">person</span><span>Profil</span>\n      </button>'''
new_nav = '''      <button class="nav-btn active" data-screen="home" aria-label="Accueil">\n        <span class="material-symbols-outlined">home</span><span>Accueil</span>\n      </button>\n      <button class="nav-btn" data-screen="income" aria-label="Revenus">\n        <span class="material-symbols-outlined">payments</span><span>Revenus</span>\n      </button>\n      <button class="nav-btn" data-screen="fixed" aria-label="Charges fixes">\n        <span class="material-symbols-outlined">event_repeat</span><span>Charges fixes</span>\n      </button>\n      <button class="nav-btn" data-screen="expenses" aria-label="Dépenses">\n        <span class="material-symbols-outlined">receipt_long</span><span>Dépenses</span>\n      </button>\n      <button class="nav-btn" data-screen="settings" aria-label="Paramètres">\n        <span class="material-symbols-outlined">settings</span><span>Paramètres</span>\n      </button>'''
rep(old_nav, new_nav, 'bottom nav')

income_const = '    const INCOME_CATEGORIES = ["Salaire", "Prime", "Bonus", "Remboursement mutuelle", "Remboursement sécurité sociale", "Aide au logement", "Prime d’activité", "Allocations familiales", "Chômage", "Indemnités maladie", "Revenus freelance", "Revenus locatifs", "Intérêts", "Dividendes", "Remboursement d’un proche", "Vente"];\n'
if 'const FIXED_CHARGE_CATEGORIES' not in s:
    rep(income_const, income_const + '    const FIXED_CHARGE_CATEGORIES = ["Loyer", "Assurances", "Abonnements", "Forfait mobile", "Forfait internet", "Cotisations bancaires", "Électricité", "Gaz", "Eau", "Mutuelle", "Transport", "Parking", "Charges de copropriété", "Taxe foncière", "Frais de garde", "Pension alimentaire"];\n', 'fixed categories')

rep('''      renderHome();\n      renderIncome();\n      renderExpenses();\n      renderProfile();\n      applyPrivacy();''', '''      renderHome();\n      renderIncome();\n      renderFixedCharges();\n      renderExpenses();\n      renderSettings();\n      renderProfile();\n      renderAccountModal();\n      applyPrivacy();''', 'renderAll')

old_account_end = '''      } else {\n        body.innerHTML = `\n          <div class="account-modal-profile">\n            <div class="account-modal-avatar"><span class="account-letter">G</span></div>\n            <div><div class="account-modal-name">Compte Google</div><div class="account-modal-email">Connecte-toi pour retrouver automatiquement tes données Firebase.</div></div>\n          </div>\n          <button class="btn primary full" id="accountSignInBtn"><span class="material-symbols-outlined">login</span>Se connecter avec Google</button>`;\n      }\n    }\n\n    function sum'''
new_account_end = '''      } else {\n        body.innerHTML = `\n          <div class="account-modal-profile">\n            <div class="account-modal-avatar"><span class="account-letter">G</span></div>\n            <div><div class="account-modal-name">Compte Google</div><div class="account-modal-email">Connecte-toi pour retrouver automatiquement tes données Firebase.</div></div>\n          </div>\n          <button class="btn primary full" id="accountSignInBtn"><span class="material-symbols-outlined">login</span>Se connecter avec Google</button>`;\n      }\n      const profile = document.getElementById("screen-profile");\n      if (profile && profile.childNodes.length) {\n        const wrap = document.createElement("div");\n        wrap.className = "account-profile-content";\n        while (profile.firstChild) wrap.appendChild(profile.firstChild);\n        body.appendChild(wrap);\n      }\n    }\n\n    function sum'''
rep(old_account_end, new_account_end, 'account profile content')

rep("document.querySelectorAll('#settingsModal [data-theme-choice]')", "document.querySelectorAll('[data-theme-choice]')", 'settings ui')

old_charges = '''      const chargesHtml = charges.length ? charges.map(charge => {\n        const paid = (charge.paidMonths || []).includes(selectedMonth);\n        return `\n          <div class="list-item">\n            <div class="list-icon"><span class="material-symbols-outlined">${paid ? "check_circle" : "event"}</span></div>\n            <div class="list-main">\n              <div class="list-title">${escapeHtml(charge.label)}</div>\n              <div class="list-sub">Jour ${safeNumber(charge.day, 1)} · ${paid ? "Prélevé" : "À venir"}</div>\n            </div>\n            <div class="list-side">\n              <div class="list-amount money">${formatMoney(charge.amount)}</div>\n              <button class="mini-btn" data-toggle-charge="${charge.id}" title="${paid ? "Marquer à venir" : "Marquer prélevé"}" aria-label="${paid ? "Marquer à venir" : "Marquer prélevé"}"><span class="material-symbols-outlined">${paid ? "undo" : "done"}</span></button>\n            </div>\n            <div class="item-actions"><button class="mini-btn" data-edit-type="fixed" data-edit-id="${charge.id}" aria-label="Modifier"><span class="material-symbols-outlined">edit</span></button></div>\n          </div>`;\n      }).join("") : emptyState("calendar_month", "Aucune charge fixe", "Ajoute tes charges récurrentes pour obtenir un reste à vivre précis.");\n'''
rep(old_charges, '      const chargesHtml = renderFixedChargeRows(charges);\n', 'home fixed rows')

home_section = '''\n        <div class="section">\n          <div class="section-header">\n            <div><h2 class="section-title">Charges fixes</h2><p class="section-subtitle">Le statut n'enlève pas la charge du montant engagé.</p></div>\n            <button class="btn tonal small" data-add-type="fixed"><span class="material-symbols-outlined">add</span>Ajouter</button>\n          </div>\n          <div class="list">${chargesHtml}</div>\n        </div>'''
rep(home_section, '', 'remove home fixed section')

marker = '    function renderIncome() {'
funcs = '''    function fixedChargeIsPending(charge) {\n      const current = monthKey();\n      if (selectedMonth < current) return false;\n      if (selectedMonth > current) return true;\n      return safeNumber(charge.day, 1) > new Date().getDate();\n    }\n\n    function renderFixedChargeRows(charges = [...activeFixedCharges()].sort((a,b) => safeNumber(a.day, 1) - safeNumber(b.day, 1))) {\n      if (!charges.length) return emptyState("calendar_month", "Aucune charge fixe", "Ajoute tes charges récurrentes pour obtenir un reste à vivre précis.");\n      return charges.map(charge => {\n        const pending = fixedChargeIsPending(charge);\n        const category = charge.category || "Charge fixe";\n        return `\n          <div class="list-item fixed-charge-row ${pending ? "pending" : ""}">\n            <div class="list-icon"><span class="material-symbols-outlined">event_repeat</span></div>\n            <div class="list-main">\n              <div class="list-title">${escapeHtml(charge.label)}</div>\n              <div class="list-sub">${escapeHtml(category)} · Jour ${safeNumber(charge.day, 1)}</div>\n            </div>\n            <div class="list-side"><div class="list-amount money">${formatMoney(charge.amount)}</div></div>\n            <div class="item-actions"><button class="mini-btn" data-edit-type="fixed" data-edit-id="${charge.id}" aria-label="Modifier"><span class="material-symbols-outlined">edit</span></button></div>\n          </div>`;\n      }).join("");\n    }\n\n    function renderFixedCharges() {\n      const container = document.getElementById("screen-fixed");\n      if (!container) return;\n      const charges = [...activeFixedCharges()].sort((a,b) => safeNumber(a.day, 1) - safeNumber(b.day, 1));\n      const total = sum(charges, x => x.amount);\n      container.innerHTML = `\n        ${renderMonthSwitcher()}\n        <div class="section">\n          <div class="card hero-card">\n            <div class="hero-label">Charges fixes du mois</div>\n            <div class="hero-value money">${formatMoney(total)}</div>\n            <div class="hero-meta"><span class="daily-pill"><span class="material-symbols-outlined">event_repeat</span>${charges.length} prélèvement${charges.length > 1 ? "s" : ""}</span></div>\n          </div>\n        </div>\n        <div class="section">\n          <div class="section-header"><div><h2 class="section-title">Charges fixes</h2><p class="section-subtitle">Les prélèvements dont la date n'est pas encore arrivée sont affichés en attente.</p></div><button class="btn tonal small" data-add-type="fixed"><span class="material-symbols-outlined">add</span>Ajouter</button></div>\n          <div class="list fixed-charge-list">${renderFixedChargeRows(charges)}</div>\n        </div>`;\n    }\n\n    function renderSettings() {\n      const container = document.getElementById("screen-settings");\n      if (!container) return;\n      container.innerHTML = `\n        <div class="section">\n          <div class="card settings-page-card">\n            <div class="section-header"><div><h2 class="section-title">Apparence</h2><p class="section-subtitle">Le mode Automatique suit le thème de l’iPhone.</p></div></div>\n            <div class="segmented">\n              <button data-theme-choice="light">Clair</button>\n              <button data-theme-choice="dark">Sombre</button>\n              <button data-theme-choice="auto">Automatique</button>\n            </div>\n          </div>\n        </div>`;\n      updateSettingsUI();\n    }\n\n'''
if 'function renderFixedCharges()' not in s:
    rep(marker, funcs + marker, 'fixed/settings renderers')

old_fixed_fields = '''      } else if (type === "fixed") {\n        fields = `\n          <div class="field"><label>Libellé</label><input name="label" required maxlength="80" value="${escapeHtml(data.label || "")}" placeholder="Ex. Loyer"></div>\n          <div class="field-row">\n            <div class="field"><label>Montant mensuel (€)</label><input name="amount" type="number" min="0" step="0.01" inputmode="decimal" required value="${data.amount ?? ""}"></div>\n            <div class="field"><label>Jour de prélèvement</label><input name="day" type="number" min="1" max="31" required value="${data.day ?? new Date().getDate()}"></div>\n          </div>`;'''
new_fixed_fields = '''      } else if (type === "fixed") {\n        fields = `\n          <div class="field"><label>Libellé</label><input name="label" required maxlength="80" value="${escapeHtml(data.label || "")}" placeholder="Ex. Loyer"></div>\n          <div class="field-row">\n            <div class="field"><label>Montant mensuel (€)</label><input name="amount" type="number" min="0" step="0.01" inputmode="decimal" required value="${data.amount ?? ""}"></div>\n            <div class="field"><label>Jour de prélèvement</label><input name="day" type="number" min="1" max="31" required value="${data.day ?? new Date().getDate()}"></div>\n          </div>\n          <div class="field"><label>Catégorie</label><select name="category">${optionTags(FIXED_CHARGE_CATEGORIES, data.category || "Abonnements")}</select></div>`;'''
rep(old_fixed_fields, new_fixed_fields, 'fixed fields')

old_fixed_submit = '''          id: id || uid("fix"), label: String(fd.get("label") || "").trim(), amount: safeNumber(fd.get("amount")),\n          day: clamp(Math.round(safeNumber(fd.get("day"), 1)), 1, 31), bucket: "needs", active: true,\n          paidMonths: current?.paidMonths || []'''
new_fixed_submit = '''          id: id || uid("fix"), label: String(fd.get("label") || "").trim(), amount: safeNumber(fd.get("amount")),\n          day: clamp(Math.round(safeNumber(fd.get("day"), 1)), 1, 31), category: String(fd.get("category") || current?.category || "Abonnements"), bucket: "needs", active: true,\n          paidMonths: current?.paidMonths || []'''
rep(old_fixed_submit, new_fixed_submit, 'fixed submit')

rep('<span class="material-symbols-outlined">delete_forever</span>${cloudUser ? "Tout supprimer du cloud" : "Connexion Google requise"}', '<span class="material-symbols-outlined">delete_forever</span>${cloudUser ? "Supprimer toutes les opérations" : "Connexion Google requise"}', 'delete label')
rep('currentScreen = ["home", "income", "expenses", "profile"].includes(screen) ? screen : "home";', 'currentScreen = ["home", "income", "fixed", "expenses", "settings"].includes(screen) ? screen : "home";', 'screen allowlist')
rep('''        renderProfile();\n        return;''', '''        renderProfile();\n        renderAccountModal();\n        return;''', 'profile fold refresh')

p.write_text(s, encoding='utf-8')
