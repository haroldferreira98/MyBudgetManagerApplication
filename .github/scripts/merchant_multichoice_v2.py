from pathlib import Path
import json, re

html_path = Path('index.html')
json_path = Path('merchants.json')
text = html_path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label} anchor count={count}')
    text = text.replace(old, new, 1)

# Build marker
text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-merchant-multichoice-v2" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

# Allow merchants.json to define multiple category/subcategory choices.
replace_once(
'''              aliases: Array.isArray(item.aliases) ? item.aliases.map(String) : [],
              ambiguous: item.ambiguous === true,
              kind: String(item.kind || "merchant"),
              learned: false''',
'''              aliases: Array.isArray(item.aliases) ? item.aliases.map(String) : [],
              ambiguous: item.ambiguous === true,
              choices: Array.isArray(item.choices)
                ? item.choices
                    .map(choice => ({
                      category: String(choice?.category || ""),
                      subcategory: String(choice?.subcategory || "")
                    }))
                    .filter(choice => choice.category && choice.subcategory)
                : [],
              kind: String(item.kind || "merchant"),
              learned: false''',
'loader choices',
)

# Replace candidate generation so one ambiguous merchant can render several choices.
pattern = re.compile(
    r'    function merchantCandidates\(query = "", limit = 14\) \{.*?\n    \}\n\n(?=    function findMerchantRule)',
    re.S,
)
replacement = '''    function merchantCandidates(query = "", limit = 18) {
      const q = normalizeSearch(query);
      const seen = new Set();
      const combined = [...merchantLearnedRules(), ...merchantDictionary];
      const matched = combined
        .filter(rule => {
          if (!q) return true;
          return merchantSearchValues(rule).some(value => value.includes(q));
        })
        .sort((a, b) => {
          if (!q) return a.name.localeCompare(b.name, "fr", { sensitivity: "base" });
          const aValues = merchantSearchValues(a);
          const bValues = merchantSearchValues(b);
          const aExact = aValues.includes(q) ? 0 : 1;
          const bExact = bValues.includes(q) ? 0 : 1;
          if (aExact !== bExact) return aExact - bExact;
          const aPrefix = aValues.some(value => value.startsWith(q)) ? 0 : 1;
          const bPrefix = bValues.some(value => value.startsWith(q)) ? 0 : 1;
          if (aPrefix !== bPrefix) return aPrefix - bPrefix;
          return a.name.localeCompare(b.name, "fr", { sensitivity: "base" });
        });

      const rows = [];
      matched.forEach(rule => {
        const choices = rule.ambiguous && Array.isArray(rule.choices) && rule.choices.length
          ? rule.choices.map(choice => ({
              ...rule,
              category: choice.category,
              subcategory: choice.subcategory,
              choice: true
            }))
          : [rule];
        choices.forEach(choice => {
          const key = `${normalizeSearch(choice.name)}|${choice.category || ""}|${choice.subcategory || ""}`;
          if (seen.has(key)) return;
          seen.add(key);
          rows.push(choice);
        });
      });
      return rows.slice(0, limit);
    }

'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'merchantCandidates replacement count={count}')

# Render category choice in each suggestion and carry it in data attributes.
pattern = re.compile(
    r'    function merchantSuggestionMarkup\(rule\) \{.*?\n    \}\n\n(?=    function setupMerchantAutocompleteFields)',
    re.S,
)
replacement = '''    function merchantSuggestionMarkup(rule) {
      const classification = rule.category && rule.subcategory
        ? `${rule.category} › ${rule.subcategory}${rule.choice ? " · choix ponctuel" : ""}`
        : rule.ambiguous
          ? "Choisir la catégorie manuellement"
          : "Catégorie à choisir";
      return `<button type="button" class="merchant-suggestion"
        data-merchant-choice="${escapeHtml(rule.name)}"
        data-merchant-category="${escapeHtml(rule.category || "")}"
        data-merchant-subcategory="${escapeHtml(rule.subcategory || "")}"
        data-merchant-ambiguous="${rule.ambiguous ? "true" : "false"}">
        <span class="merchant-suggestion-main">
          <span class="merchant-suggestion-name">${escapeHtml(rule.name)}</span>
          <span class="merchant-suggestion-meta">${escapeHtml(classification)}${rule.learned ? " · mémorisé" : ""}</span>
        </span>
        <span class="material-symbols-outlined merchant-suggestion-arrow">chevron_right</span>
      </button>`;
    }

'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'merchantSuggestionMarkup replacement count={count}')

# Mark both taxonomy fields so they can disappear for recognized merchants.
old = '''          <div class="field"><label>Catégorie</label><select name="category" required>${optionTags(spendingCategoryOptions(data.category), data.category || "Alimentation")}</select></div>
          <div class="field" data-spending-subcategory-field><label>Sous-catégorie</label><select name="subcategory">${optionTags(spendingSubcategoryOptions(data.category || "Alimentation", data.subcategory), data.subcategory || "")}</select></div>'''
new = '''          <div class="field" data-spending-category-field><label>Catégorie</label><select name="category" required>${optionTags(spendingCategoryOptions(data.category), data.category || "Alimentation")}</select></div>
          <div class="field" data-spending-subcategory-field><label>Sous-catégorie</label><select name="subcategory">${optionTags(spendingSubcategoryOptions(data.category || "Alimentation", data.subcategory), data.subcategory || "")}</select></div>'''
count = text.count(old)
if count != 2:
    raise SystemExit(f'taxonomy field markup count={count}')
text = text.replace(old, new)

# Add references to taxonomy fields in autocomplete setup.
replace_once(
'''      const category = target.querySelector('[name="category"]');
      const subcategory = target.querySelector('[name="subcategory"]');
      const modal = document.getElementById("entityModal");
      if (!input || !suggestions || !category || !subcategory) return;''',
'''      const category = target.querySelector('[name="category"]');
      const subcategory = target.querySelector('[name="subcategory"]');
      const categoryField = target.querySelector('[data-spending-category-field]');
      const subcategoryField = target.querySelector('[data-spending-subcategory-field]');
      const modal = document.getElementById("entityModal");
      if (!input || !suggestions || !category || !subcategory) return;''',
'autocomplete taxonomy refs',
)

# Add show/hide helper after the note helper.
replace_once(
'''      const setNote = (message = "", automatic = false) => {
        if (!note) return;
        note.textContent = message;
        note.classList.toggle("auto", automatic);
      };

      const customCategoryNote = () => {''',
'''      const setNote = (message = "", automatic = false) => {
        if (!note) return;
        note.textContent = message;
        note.classList.toggle("auto", automatic);
      };

      const setTaxonomyFieldsVisible = visible => {
        if (categoryField) categoryField.hidden = !visible;
        if (subcategoryField) subcategoryField.hidden = !visible;
      };

      const customCategoryNote = () => {''',
'taxonomy visibility helper',
)

# For base ambiguous merchants keep manual fields visible; recognized choices hide them.
replace_once(
'''        if (!rule.category || !rule.subcategory || !EXPENSE_CATEGORY_TREE[rule.category]?.includes(rule.subcategory)) {
          setNote("Enseigne multi-catégories : choisis librement pour cette opération. Ce choix ne sera pas mémorisé.", false);
          return false;
        }''',
'''        if (!rule.category || !rule.subcategory || !EXPENSE_CATEGORY_TREE[rule.category]?.includes(rule.subcategory)) {
          setTaxonomyFieldsVisible(true);
          setNote("Enseigne multi-catégories : choisis une proposition ci-dessus ou classe-la manuellement.", false);
          return false;
        }''',
'apply invalid rule',
)

replace_once(
'''          if ([...subcategory.options].some(option => option.value === rule.subcategory)) {
            subcategory.value = rule.subcategory;
          }
          setNote(`${rule.category} › ${rule.subcategory}${rule.learned ? " · mémorisé" : ""}`, true);''',
'''          if ([...subcategory.options].some(option => option.value === rule.subcategory)) {
            subcategory.value = rule.subcategory;
          }
          setTaxonomyFieldsVisible(false);
          setNote(`${rule.category} › ${rule.subcategory}${rule.choice ? " · choix ponctuel" : rule.learned ? " · mémorisé" : ""}`, true);''',
'apply valid rule',
)

# When user manually changes a taxonomy value, make sure both controls remain available.
replace_once(
'''      category.addEventListener("change", () => {
        const rule = findMerchantRule(input.value);''',
'''      category.addEventListener("change", () => {
        setTaxonomyFieldsVisible(true);
        const rule = findMerchantRule(input.value);''',
'category manual visibility',
)
replace_once(
'''      subcategory.addEventListener("change", () => {
        if (input.value.trim()) setNote(customCategoryNote(), false);''',
'''      subcategory.addEventListener("change", () => {
        setTaxonomyFieldsVisible(true);
        if (input.value.trim()) setNote(customCategoryNote(), false);''',
'subcategory manual visibility',
)

# Unknown/free labels should expose manual taxonomy fields.
replace_once(
'''      const initialRule = findMerchantRule(input.value);
      if (initialRule) applyRule(initialRule);
      else if (input.value.trim()) setNote("Libellé libre : la catégorie actuelle sera mémorisée à l’enregistrement.", false);''',
'''      const initialRule = findMerchantRule(input.value);
      if (initialRule) applyRule(initialRule);
      else {
        setTaxonomyFieldsVisible(true);
        if (input.value.trim()) setNote("Libellé libre : choisis la catégorie et la sous-catégorie.", false);
      }''',
'initial unknown rule',
)

# Change the click handler so a particular multi-choice row applies its own classification.
pattern = re.compile(
    r'      suggestions\.addEventListener\("click", event => \{\n        const button = event\.target\.closest\?\.\("\[data-merchant-choice\]"\);\n        if \(!button\) return;\n        const rule = findMerchantRule\(button\.dataset\.merchantChoice\) \|\| merchantCandidates\(button\.dataset\.merchantChoice, 1\)\[0\];\n        if \(!rule\) return;\n        input\.value = rule\.name;\n        applyRule\(rule\);\n        closeSuggestions\(\);\n        input\.focus\(\);\n        input\.setSelectionRange\(input\.value\.length, input\.value\.length\);\n      \}\);',
    re.S,
)
replacement = '''      suggestions.addEventListener("click", event => {
        const button = event.target.closest?.("[data-merchant-choice]");
        if (!button) return;
        const name = button.dataset.merchantChoice || "";
        const chosenCategory = button.dataset.merchantCategory || "";
        const chosenSubcategory = button.dataset.merchantSubcategory || "";
        const baseRule = findMerchantRule(name) || merchantCandidates(name, 1)[0];
        if (!baseRule) return;
        const rule = chosenCategory && chosenSubcategory
          ? {
              ...baseRule,
              name,
              category: chosenCategory,
              subcategory: chosenSubcategory,
              ambiguous: button.dataset.merchantAmbiguous === "true",
              choice: button.dataset.merchantAmbiguous === "true"
            }
          : baseRule;
        input.value = rule.name;
        applyRule(rule);
        closeSuggestions();
        input.focus();
        input.setSelectionRange(input.value.length, input.value.length);
      });'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'suggestion click replacement count={count}')

# When typing away from a known exact merchant, reveal manual taxonomy fields again.
old = '''      input.addEventListener("input", () => {
        const exact = findMerchantRule(input.value);'''
new = '''      input.addEventListener("input", () => {
        setTaxonomyFieldsVisible(true);
        const exact = findMerchantRule(input.value);'''
replace_once(old, new, 'input reveals fields')

html_path.write_text(text, encoding='utf-8')

# Curated choices for common multi-category merchants. Keep choices in JSON, not HTML.
data = json.loads(json_path.read_text(encoding='utf-8'))
choice_map = {
    'Action': [
        ('Maison', 'Produits ménagers'), ('Maison', 'Décoration'), ('Maison', 'Cuisine & vaisselle'),
        ('Maison', 'Bricolage'), ('Personnel', 'Hygiène corporelle'), ('Personnel', 'Accessoires')
    ],
    'Amazon': [
        ('Maison', 'Électroménager'), ('Maison', 'Cuisine & vaisselle'), ('Maison', 'Produits ménagers'),
        ('Maison', 'Décoration'), ('Personnel', 'Vêtements'), ('Personnel', 'Accessoires'),
        ('Loisirs & sorties', 'Livres & presse'), ('Loisirs & sorties', 'Jeux & loisirs'),
        ('Animaux', 'Accessoires')
    ],
    'AliExpress': [
        ('Maison', 'Électroménager'), ('Maison', 'Décoration'), ('Maison', 'Bricolage'),
        ('Personnel', 'Vêtements'), ('Personnel', 'Accessoires'), ('Animaux', 'Accessoires')
    ],
    'Back Market': [('Maison', 'Électroménager'), ('Personnel', 'Accessoires')],
    'Bazarland': [
        ('Maison', 'Produits ménagers'), ('Maison', 'Décoration'), ('Maison', 'Cuisine & vaisselle'),
        ('Maison', 'Bricolage'), ('Personnel', 'Accessoires')
    ],
    'Cdiscount': [
        ('Maison', 'Électroménager'), ('Maison', 'Cuisine & vaisselle'), ('Maison', 'Décoration'),
        ('Personnel', 'Vêtements'), ('Personnel', 'Accessoires'), ('Loisirs & sorties', 'Jeux & loisirs')
    ],
    'Fnac': [
        ('Maison', 'Électroménager'), ('Loisirs & sorties', 'Livres & presse'),
        ('Loisirs & sorties', 'Jeux & loisirs'), ('Personnel', 'Accessoires')
    ],
    'Galeries Lafayette': [
        ('Personnel', 'Vêtements'), ('Personnel', 'Chaussures'), ('Personnel', 'Accessoires'),
        ('Personnel', 'Beauté & soins'), ('Maison', 'Décoration')
    ],
    'Gifi': [
        ('Maison', 'Produits ménagers'), ('Maison', 'Décoration'), ('Maison', 'Cuisine & vaisselle'),
        ('Maison', 'Bricolage'), ('Personnel', 'Accessoires')
    ],
    'Greenweez': [
        ('Alimentation', 'Supérettes & épiceries'), ('Personnel', 'Hygiène corporelle'),
        ('Maison', 'Produits ménagers')
    ],
    'La Redoute': [
        ('Personnel', 'Vêtements'), ('Personnel', 'Chaussures'), ('Maison', 'Mobilier'),
        ('Maison', 'Décoration'), ('Maison', 'Linge de maison'), ('Maison', 'Literie')
    ],
    'Materiel.net': [('Maison', 'Électroménager'), ('Personnel', 'Accessoires')],
    'Printemps': [
        ('Personnel', 'Vêtements'), ('Personnel', 'Chaussures'), ('Personnel', 'Accessoires'),
        ('Personnel', 'Beauté & soins'), ('Maison', 'Décoration')
    ],
    'Temu': [
        ('Maison', 'Électroménager'), ('Maison', 'Décoration'), ('Maison', 'Cuisine & vaisselle'),
        ('Personnel', 'Vêtements'), ('Personnel', 'Accessoires'), ('Animaux', 'Accessoires')
    ],
    'Veepee': [
        ('Personnel', 'Vêtements'), ('Personnel', 'Chaussures'), ('Personnel', 'Accessoires'),
        ('Maison', 'Décoration'), ('Maison', 'Électroménager')
    ],
    'Xiaomi': [('Maison', 'Électroménager'), ('Personnel', 'Accessoires')],
}

updated = 0
for merchant in data.get('merchants', []):
    name = str(merchant.get('name', ''))
    if name in choice_map and merchant.get('ambiguous') is True:
        merchant['choices'] = [
            {'category': category, 'subcategory': subcategory}
            for category, subcategory in choice_map[name]
        ]
        updated += 1

if updated < 10:
    raise SystemExit(f'only {updated} ambiguous merchants received choices')

json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'updated {updated} multi-category merchants')
