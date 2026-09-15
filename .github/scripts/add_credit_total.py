from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old_start = '''    function renderProfile() {
      const container = document.getElementById("screen-profile");
      const monthExpenses = currentMonthExpenses();
'''
new_start = '''    function renderProfile() {
      const container = document.getElementById("screen-profile");
      const monthExpenses = currentMonthExpenses();
      const totalCreditBalance = sum(state.credits, credit => creditProgress(credit).calculatedBalance);
'''
if old_start not in text:
    raise SystemExit('renderProfile start not found')
text = text.replace(old_start, new_start, 1)

old_header = '''          <div class="section-header"><div><h2 class="section-title">Mes crédits</h2></div><button class="btn tonal small" data-add-type="credit"><span class="material-symbols-outlined">add</span>Ajouter</button></div>'''
new_header = '''          <div class="section-header"><div><h2 class="section-title">Mes crédits</h2><p class="section-subtitle">Capital restant total : <strong class="money">${formatMoney(totalCreditBalance)}</strong></p></div><button class="btn tonal small" data-add-type="credit"><span class="material-symbols-outlined">add</span>Ajouter</button></div>'''
if old_header not in text:
    raise SystemExit('credit section header not found')
text = text.replace(old_header, new_header, 1)

p.write_text(text, encoding='utf-8')
