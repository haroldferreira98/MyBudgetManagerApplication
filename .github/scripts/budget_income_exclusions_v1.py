from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'BUDGET-INCOME-EXCLUSIONS-V1'

if marker in text:
    raise SystemExit('Budget income exclusions already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-budget-income-exclusions-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

anchor = '    const FIXED_CHARGE_CATEGORIES = ['
if text.count(anchor) != 1:
    raise SystemExit(f'Expected one fixed charge category anchor, found {text.count(anchor)}')

addition = '''    // BUDGET-INCOME-EXCLUSIONS-V1\n    // These incoming cash flows stay visible in operations but do not increase budget income.\n    const BUDGET_INCOME_EXCLUDED_CATEGORIES = new Set([\n      "Remboursement d’un proche",\n      "Remboursement mutuelle",\n      "Remboursement sécurité sociale",\n      "Vente",\n    ]);\n\n    function isBudgetIncome(item) {\n      return !BUDGET_INCOME_EXCLUDED_CATEGORIES.has(String(item?.category || ""));\n    }\n\n'''
text = text.replace(anchor, addition + anchor, 1)

old = '      const income = sum(currentMonthIncomes(), x => x.amount);'
new = '      const income = sum(currentMonthIncomes().filter(isBudgetIncome), x => x.amount);'
if text.count(old) != 1:
    raise SystemExit(f'Expected one financialSnapshot income calculation, found {text.count(old)}')
text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
