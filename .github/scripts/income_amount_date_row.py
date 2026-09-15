from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '    /* PROFILE-FOLD-MONTH-PICKER-V1 */'
css = '''/* INCOME-AMOUNT-DATE-ROW-V1 */
#entityModal[data-entity-type="income"] .field-row {
  display: grid !important;
  grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr) !important;
  gap: 12px !important;
  width: 100% !important;
  min-width: 0 !important;
}
#entityModal[data-entity-type="income"] .field-row > .field {
  min-width: 0 !important;
  width: auto !important;
  max-width: 100% !important;
  contain: inline-size;
  overflow: hidden;
}
#entityModal[data-entity-type="income"] .field-row input {
  display: block !important;
  inline-size: 100% !important;
  width: 100% !important;
  min-inline-size: 0 !important;
  min-width: 0 !important;
  max-inline-size: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}
#entityModal[data-entity-type="income"] input[type="date"] {
  -webkit-appearance: none !important;
  appearance: none !important;
  overflow: hidden !important;
  white-space: nowrap;
  padding-right: 10px !important;
}
#entityModal[data-entity-type="income"] input[type="date"]::-webkit-date-and-time-value {
  min-width: 0 !important;
  width: 100% !important;
  text-align: left !important;
}

'''
if '/* INCOME-AMOUNT-DATE-ROW-V1 */' in text:
    raise SystemExit('Already patched')
if marker not in text:
    raise SystemExit('CSS insertion marker not found')
text = text.replace(marker, css + marker, 1)
p.write_text(text, encoding='utf-8')
