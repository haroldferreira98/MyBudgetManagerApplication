from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old1 = '      const totalCreditBalance = sum(state.credits, credit => creditProgress(credit).calculatedBalance);'
new1 = '      const totalCreditMonthlyPayment = sum(state.credits, credit => safeNumber(credit.monthlyPayment));'
old2 = '<div class="section-header"><div><h2 class="section-title">Mes crédits</h2><p class="section-subtitle">Capital restant total : <strong class="money">${formatMoney(totalCreditBalance)}</strong></p></div><button class="btn tonal small" data-add-type="credit"><span class="material-symbols-outlined">add</span>Ajouter</button></div>'
new2 = '<div class="section-header"><div><h2 class="section-title">Mes crédits</h2><p class="section-subtitle">Total des mensualités : <strong class="money">${formatMoney(totalCreditMonthlyPayment)}</strong>/mois</p></div><button class="btn tonal small" data-add-type="credit"><span class="material-symbols-outlined">add</span>Ajouter</button></div>'
if old1 not in s:
    raise SystemExit('total credit balance declaration not found')
if old2 not in s:
    raise SystemExit('credit section header not found')
s = s.replace(old1, new1, 1).replace(old2, new2, 1)
if 'Capital restant total :' in s:
    raise SystemExit('old capital total label still present')
if 'Total des mensualités :' not in s:
    raise SystemExit('new monthly total label missing')
p.write_text(s, encoding='utf-8')
