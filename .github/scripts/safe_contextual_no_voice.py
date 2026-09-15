from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")

replacements = [
    (
        '    function openEntityModal(type = "expense", id = null, prefill = null) {',
        '    function openEntityModal(type = "expense", id = null, prefill = null, contextual = false) {'
    ),
    (
        '      document.getElementById("entityModalTitle").textContent = editing ? `Modifier · ${entityLabel(type)}` : "Ajouter";',
        '      document.getElementById("entityModalTitle").textContent = editing ? `Modifier · ${entityLabel(type)}` : (contextual ? `Ajouter · ${entityLabel(type)}` : "Ajouter");'
    ),
    (
        '      const typeSelector = editing ? `<input type="hidden" name="entityType" value="${type}">` : `',
        '      const typeSelector = (editing || contextual) ? `<input type="hidden" name="entityType" value="${type}">` : `'
    ),
    (
        '          </div>\n          <label class="checkbox-row"><input name="active" type="checkbox" ${data.active !== false ? "checked" : ""}><span>Charge active</span></label>`;',
        '          </div>`;'
    ),
    (
        '          day: clamp(Math.round(safeNumber(fd.get("day"), 1)), 1, 31), bucket: "needs", active: fd.get("active") === "on",',
        '          day: clamp(Math.round(safeNumber(fd.get("day"), 1)), 1, 31), bucket: "needs", active: true,'
    ),
    (
        '      if (add) openEntityModal(add.dataset.addType);',
        '      if (add) openEntityModal(add.dataset.addType, null, null, true);'
    ),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"Target not found: {old[:120]}")
    text = text.replace(old, new, 1)

fab_start = text.find('    const fabAdd = document.getElementById("fabAdd");')
form_listener = '    document.getElementById("entityForm").addEventListener("submit", handleEntitySubmit);'
fab_end = text.find(form_listener, fab_start)
if fab_start < 0 or fab_end < 0:
    raise SystemExit("FAB block not found")

fab_replacement = '''    const fabAdd = document.getElementById("fabAdd");
    fabAdd?.addEventListener("click", () => {
      if (currentScreen === "income") openEntityModal("income", null, null, true);
      else if (currentScreen === "expenses" || currentScreen === "home") openEntityModal("expense", null, null, true);
      else openEntityModal("expense");
    });
'''
text = text[:fab_start] + fab_replacement + text[fab_end:]

if '/* VOICE-DISABLED-SAFELY */' not in text:
    text = text.replace('</style>', '    /* VOICE-DISABLED-SAFELY */\n    #voiceHud { display: none !important; }\n\n</style>', 1)

p.write_text(text, encoding="utf-8")
