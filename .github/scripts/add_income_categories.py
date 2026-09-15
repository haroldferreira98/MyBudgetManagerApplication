from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

repls = [
    (
        '    const EXPENSE_CATEGORIES = ["Courses", "Carburant", "Loisirs", "Restaurant", "Santé", "Autre"];\n',
        '    const EXPENSE_CATEGORIES = ["Courses", "Carburant", "Loisirs", "Restaurant", "Santé", "Autre"];\n    const INCOME_CATEGORIES = ["Salaire", "Prime", "Bonus", "Remboursement mutuelle", "Remboursement sécurité sociale", "Aide au logement", "Prime d’activité", "Allocations familiales", "Chômage", "Indemnités maladie", "Revenus freelance", "Revenus locatifs", "Intérêts", "Dividendes", "Remboursement d’un proche", "Vente"];\n'
    ),
    (
        '        incomes: Array.isArray(input.incomes) ? input.incomes : [],\n',
        '        incomes: Array.isArray(input.incomes) ? input.incomes.map(item => ({ ...item, category: item.category || "Salaire" })) : [],\n'
    ),
    (
        '''      } else if (type === "income") {\n        fields = `\n          <div class="field"><label>Libellé</label><input name="label" required maxlength="80" value="${escapeHtml(data.label || "")}" placeholder="Ex. Salaire"></div>\n          <div class="field-row">\n            <div class="field"><label>Montant (€)</label><input name="amount" type="number" min="0" step="0.01" inputmode="decimal" required value="${data.amount ?? ""}"></div>\n            <div class="field"><label>Date</label><input name="date" type="date" required value="${escapeHtml(data.date || today)}"></div>\n          </div>`;''',
        '''      } else if (type === "income") {\n        fields = `\n          <div class="field"><label>Libellé</label><input name="label" required maxlength="80" value="${escapeHtml(data.label || "")}" placeholder="Ex. Salaire"></div>\n          <div class="field-row">\n            <div class="field"><label>Montant (€)</label><input name="amount" type="number" min="0" step="0.01" inputmode="decimal" required value="${data.amount ?? ""}"></div>\n            <div class="field"><label>Date</label><input name="date" type="date" required value="${escapeHtml(data.date || today)}"></div>\n          </div>\n          <div class="field"><label>Catégorie</label><select name="category">${optionTags(INCOME_CATEGORIES, data.category || "Salaire")}</select></div>`;'''
    ),
    (
        '        item = { id: id || uid("inc"), label: String(fd.get("label") || "").trim(), amount: safeNumber(fd.get("amount")), date: fd.get("date") || todayISO() };\n',
        '        item = { id: id || uid("inc"), label: String(fd.get("label") || "").trim(), amount: safeNumber(fd.get("amount")), date: fd.get("date") || todayISO(), category: fd.get("category") || "Salaire" };\n'
    ),
    (
        '        subtitle: formatDate(item.date), amount: safeNumber(item.amount),\n        haystack: [item.label, item.date, "revenu", ...amountTokens(item.amount)].join(" ")\n',
        '        subtitle: `${item.category || "Salaire"} · ${formatDate(item.date)}`, amount: safeNumber(item.amount),\n        haystack: [item.label, item.category || "Salaire", item.date, "revenu", ...amountTokens(item.amount)].join(" ")\n'
    ),
    (
        '            <div class="list-sub">${formatDate(item.date)}</div>\n',
        '            <div class="list-sub">${escapeHtml(item.category || "Salaire")} · ${formatDate(item.date)}</div>\n'
    ),
    (
        '      state.incomes.forEach(x => rows.push(["revenu",x.id,x.label,x.amount,x.date,"","","","","","","","","","","",""]));\n',
        '      state.incomes.forEach(x => rows.push(["revenu",x.id,x.label,x.amount,x.date,x.category || "Salaire","","","","","","","","","","",""]));\n'
    ),
]

for old, new in repls:
    if old not in text:
        raise SystemExit(f'Target not found: {old[:120]}')
    text = text.replace(old, new, 1)

required = [
    'const INCOME_CATEGORIES = ["Salaire", "Prime", "Bonus"',
    '<label>Catégorie</label><select name="category">${optionTags(INCOME_CATEGORIES, data.category || "Salaire")}</select>',
    'category: fd.get("category") || "Salaire"',
]
for token in required:
    if token not in text:
        raise SystemExit(f'Missing after patch: {token}')

p.write_text(text, encoding='utf-8')
