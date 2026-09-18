from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label} anchor count={count}")
    text = text.replace(old, new, 1)


text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-merchant-multicategory-free-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit("app build marker not found")

replace_once(
'''    function merchantLearnedRules() {
      const preferences = state.merchantPreferences && typeof state.merchantPreferences === "object" ? state.merchantPreferences : {};
      return Object.values(preferences)
        .filter(item => item && item.name)''',
'''    function merchantDictionaryRuleForValue(value) {
      const q = normalizeSearch(value);
      if (!q) return null;
      return merchantDictionary.find(rule => merchantSearchValues(rule).includes(q)) || null;
    }

    function merchantLearnedRules() {
      const preferences = state.merchantPreferences && typeof state.merchantPreferences === "object" ? state.merchantPreferences : {};
      return Object.values(preferences)
        .filter(item => item && item.name && !merchantDictionaryRuleForValue(item.name)?.ambiguous)''',
"merchant learned rules",
)

pattern = re.compile(
    r'    function findMerchantRule\(value\) \{.*?\n    \}\n\n(?=    function rememberMerchantPreference)',
    re.S,
)
replacement = '''    function findMerchantRule(value) {
      const q = normalizeSearch(value);
      if (!q) return null;
      const dictionaryRule = merchantDictionaryRuleForValue(value);
      if (dictionaryRule?.ambiguous) return dictionaryRule;
      const preference = state.merchantPreferences?.[q];
      if (preference?.name && preference?.category && preference?.subcategory) {
        return {
          name: String(preference.name),
          category: String(preference.category),
          subcategory: String(preference.subcategory),
          aliases: [],
          ambiguous: false,
          kind: "learned",
          learned: true
        };
      }
      return dictionaryRule;
    }

'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f"findMerchantRule replacement count={count}")

pattern = re.compile(
    r'    function rememberMerchantPreference\(label, category, subcategory\) \{.*?\n    \}\n\n(?=    function )',
    re.S,
)
replacement = '''    function rememberMerchantPreference(label, category, subcategory) {
      const name = String(label || "").trim();
      const key = normalizeSearch(name);
      if (!key || !category || !subcategory) return;
      state.merchantPreferences = state.merchantPreferences && typeof state.merchantPreferences === "object" ? state.merchantPreferences : {};
      const dictionaryRule = merchantDictionaryRuleForValue(name);
      if (dictionaryRule?.ambiguous) {
        delete state.merchantPreferences[key];
        return;
      }
      state.merchantPreferences[key] = {
        name,
        category: String(category),
        subcategory: String(subcategory),
        updatedAt: new Date().toISOString()
      };
    }

'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f"rememberMerchantPreference replacement count={count}")

replace_once(
'''      const classification = rule.category && rule.subcategory
        ? `${rule.category} › ${rule.subcategory}`
        : "Catégorie à choisir";''',
'''      const classification = rule.ambiguous
        ? "Catégorie libre · choix non mémorisé"
        : rule.category && rule.subcategory
          ? `${rule.category} › ${rule.subcategory}`
          : "Catégorie à choisir";''',
"merchant suggestion classification",
)

replace_once(
'''      const setNote = (message = "", automatic = false) => {
        if (!note) return;
        note.textContent = message;
        note.classList.toggle("auto", automatic);
      };''',
'''      const setNote = (message = "", automatic = false) => {
        if (!note) return;
        note.textContent = message;
        note.classList.toggle("auto", automatic);
      };

      const customCategoryNote = () => {
        const rule = merchantDictionaryRuleForValue(input.value);
        return rule?.ambiguous
          ? "Enseigne multi-catégories : choisis librement pour cette opération. Ce choix ne sera pas mémorisé."
          : "Catégorie personnalisée : elle sera mémorisée pour ce libellé.";
      };''',
"merchant note helper",
)

replace_once(
'          setNote("Enseigne multi-catégories : choisis la catégorie une fois, l’app la mémorisera.", false);',
'          setNote("Enseigne multi-catégories : choisis librement pour cette opération. Ce choix ne sera pas mémorisé.", false);',
"ambiguous merchant note",
)

count = text.count('setNote("Catégorie personnalisée : elle sera mémorisée pour ce libellé.", false);')
if count != 2:
    raise SystemExit(f"custom category note count={count}")
text = text.replace('setNote("Catégorie personnalisée : elle sera mémorisée pour ce libellé.", false);', 'setNote(customCategoryNote(), false);')

path.write_text(text, encoding="utf-8")
