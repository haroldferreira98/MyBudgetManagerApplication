from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260917-health-reimbursement-linked-v3" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

standalone = '''      state.expenses.forEach(item => {
        healthReimbursementOperationRows(item)
          .filter(row => isCurrentMonth(row.sortDate))
          .forEach(row => rows.push(row));
      });
'''
if text.count(standalone) != 1:
    raise SystemExit(f'expected one standalone reimbursement block, got {text.count(standalone)}')
text = text.replace(standalone, '', 1)

pattern = re.compile(r'''    function operationRowHtml\(row, grouped = false\) \{.*?\n    \}\n\n    function operationCategoryItemsHtml''', re.S)
replacement = r'''    function operationRowHtml(row, grouped = false) {
      const subtitle = row.healthMeta ? `<div class="list-sub health-reimbursement-row-meta">${escapeHtml(row.healthMeta)}</div>`
        : row.isHealthReimbursement ? `<div class="list-sub health-reimbursement-row-meta">${escapeHtml(row.meta || "Remboursement lié")}</div>`
        : !grouped && row.meta ? `<div class="list-sub">${escapeHtml(row.meta)}</div>` : "";

      let linkedRefunds = "";
      if (row.type === "expense" && !row.isHealthReimbursement) {
        const sourceExpense = state.expenses.find(item => item.id === row.id);
        const refunds = healthReimbursementOperationRows(sourceExpense);
        if (refunds.length) {
          linkedRefunds = `<div class="health-linked-refunds">${refunds.map(refund => {
            const source = String(refund.title || "").replace(/^Remboursement\s*·\s*/, "");
            return `<div class="health-linked-refund"><span class="health-linked-refund-copy"><strong>${escapeHtml(source)}</strong><small>Reçu le ${escapeHtml(formatOperationDate(refund.sortDate))}</small></span><span class="health-linked-refund-amount money">+${formatMoney(refund.amount)}</span></div>`;
          }).join("")}</div>`;
        }
      }

      return `
        <div class="list-item operation-list-item ${row.isHealthReimbursement ? "health-reimbursement-operation" : ""}" data-edit-type="${row.type}" data-edit-id="${row.id}" role="button" tabindex="0">
          <div class="list-icon"><span class="material-symbols-outlined">${row.icon}</span></div>
          <div class="list-main"><div class="list-title">${escapeHtml(row.title)}</div>${subtitle}${linkedRefunds}</div>
          <div class="list-side">${operationSignedAmount(row.amount)}</div>
        </div>`;
    }

    function operationCategoryItemsHtml'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'operationRowHtml replacement count={count}')

css = r'''
    /* HEALTH-REIMBURSEMENT-LINKED-V3 */
    .health-linked-refunds {
      display: grid;
      gap: 5px;
      margin-top: 7px;
      padding-top: 7px;
      border-top: 1px solid color-mix(in srgb, var(--outline-variant) 58%, transparent);
    }
    .health-linked-refund {
      min-width: 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      color: var(--success);
      line-height: 1.15;
    }
    .health-linked-refund-copy {
      min-width: 0;
      display: flex;
      align-items: baseline;
      gap: 5px;
      overflow: hidden;
    }
    .health-linked-refund-copy strong {
      flex: 0 1 auto;
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 10.5px;
      font-weight: 700;
    }
    .health-linked-refund-copy small {
      flex: 0 1 auto;
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      color: var(--on-surface-variant);
      font-size: 9.5px;
    }
    .health-linked-refund-amount {
      flex: 0 0 auto;
      color: var(--success);
      font-size: 10.5px;
      font-weight: 750;
      white-space: nowrap;
    }
'''
style_end = text.find('\n  </style>')
if style_end < 0:
    raise SystemExit('style closing tag not found')
text = text[:style_end] + css + text[style_end:]

path.write_text(text, encoding='utf-8')
