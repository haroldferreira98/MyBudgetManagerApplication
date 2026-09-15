from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")

repls = [
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
        '    fabAdd?.addEventListener("click", () => openEntityModal("expense"));',
        '    fabAdd?.addEventListener("click", () => {\n      if (currentScreen === "income") openEntityModal("income", null, null, true);\n      else if (currentScreen === "expenses" || currentScreen === "home") openEntityModal("expense", null, null, true);\n      else openEntityModal("expense");\n    });'
    ),
    (
        '      if (add) openEntityModal(add.dataset.addType);',
        '      if (add) openEntityModal(add.dataset.addType, null, null, true);'
    ),
]

for old, new in repls:
    if old not in text:
        raise SystemExit(f"Target not found: {old[:90]}")
    text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")
