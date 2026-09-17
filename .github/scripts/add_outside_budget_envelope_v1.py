from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '20260917-outside-budget-envelope-v1'

if marker in text:
    raise SystemExit('Fix already applied')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-outside-budget-envelope-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('App build marker not found')

anchor = '''    function renderProfile() {
      const container = document.getElementById("screen-profile");
      const monthExpenses = currentMonthExpenses();
'''
insertion = '''    function renderProfile() {
      const container = document.getElementById("screen-profile");
      const monthExpenses = currentMonthExpenses();
      const hasAllCategoriesEnvelope = state.envelopes.some(env => env.category === "Toutes");
      const budgetedCategories = new Set(
        state.envelopes
          .map(env => env.category)
          .filter(category => category && category !== "Toutes")
      );
      const outsideBudgetExpenses = hasAllCategoriesEnvelope
        ? []
        : monthExpenses.filter(item => !budgetedCategories.has(item.category));
      const outsideBudgetAmount = sum(outsideBudgetExpenses, item => item.amount);
      const outsideBudgetCount = outsideBudgetExpenses.length;
      const outsideBudgetHtml = outsideBudgetCount ? `
        <div class="card" style="border-color:color-mix(in srgb, var(--warning) 34%, var(--outline-variant))">
          <div class="section-header" style="margin:0">
            <div>
              <h3 class="section-title" style="font-size:16px">Hors budget</h3>
              <p class="section-subtitle">${outsideBudgetCount} ${outsideBudgetCount > 1 ? "dépenses" : "dépense"} · <span class="money">${formatMoney(outsideBudgetAmount)}</span></p>
            </div>
            <span class="material-symbols-outlined" style="color:var(--warning)" aria-hidden="true">warning</span>
          </div>
          <div class="tiny" style="margin-top:7px">Dépenses dans des catégories sans enveloppe mensuelle.</div>
        </div>` : "";
'''
if text.count(anchor) != 1:
    raise SystemExit(f'Expected one renderProfile anchor, found {text.count(anchor)}')
text = text.replace(anchor, insertion, 1)

old_start = '      const envelopesHtml = state.envelopes.length ? state.envelopes.map(env => {'
new_start = '      const regularEnvelopesHtml = state.envelopes.length ? state.envelopes.map(env => {'
if text.count(old_start) != 1:
    raise SystemExit(f'Expected one envelopesHtml start, found {text.count(old_start)}')
text = text.replace(old_start, new_start, 1)

old_end = '      }).join("") : emptyState("account_balance_wallet", "Aucune enveloppe", "Crée des plafonds mensuels par catégorie pour suivre tes dépenses.");'
new_end = '''      }).join("") : "";

      const envelopesHtml = regularEnvelopesHtml || outsideBudgetHtml
        ? `${regularEnvelopesHtml}${outsideBudgetHtml}`
        : emptyState("account_balance_wallet", "Aucune enveloppe", "Crée des plafonds mensuels par catégorie pour suivre tes dépenses.");'''
if text.count(old_end) != 1:
    raise SystemExit(f'Expected one envelopesHtml end, found {text.count(old_end)}')
text = text.replace(old_end, new_end, 1)

path.write_text(text, encoding='utf-8')
