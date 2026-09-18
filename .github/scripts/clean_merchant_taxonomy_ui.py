from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label} anchor count={count}')
    text = text.replace(old, new, 1)


# Build marker.
text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-merchant-clean-hidden-taxonomy-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

# Keep merchant suggestion rows visually clean: only category + subcategory.
replace_once(
    '? `${rule.category} › ${rule.subcategory}${rule.choice ? " · choix ponctuel" : ""}`',
    '? `${rule.category} › ${rule.subcategory}`',
    'suggestion classification suffix',
)
replace_once(
    '<span class="merchant-suggestion-meta">${escapeHtml(classification)}${rule.learned ? " · mémorisé" : ""}</span>',
    '<span class="merchant-suggestion-meta">${escapeHtml(classification)}</span>',
    'suggestion learned suffix',
)

# Never expose category/subcategory controls below amount/date, even before JS initializes.
replace_once(
    '<div class="field" data-spending-category-field><label>Catégorie</label><select name="category" required>${optionTags(spendingCategoryOptions(data.category), data.category || "Alimentation")}</select></div>',
    '<div class="field" data-spending-category-field hidden><label>Catégorie</label><select name="category" required>${optionTags(spendingCategoryOptions(data.category), data.category || "Alimentation")}</select></div>',
    'hidden category field',
)
replace_once(
    '<div class="field" data-spending-subcategory-field><label>Sous-catégorie</label><select name="subcategory">${optionTags(spendingSubcategoryOptions(data.category || "Alimentation", data.subcategory), data.subcategory || "")}</select></div>',
    '<div class="field" data-spending-subcategory-field hidden><label>Sous-catégorie</label><select name="subcategory">${optionTags(spendingSubcategoryOptions(data.category || "Alimentation", data.subcategory), data.subcategory || "")}</select></div>',
    'hidden subcategory field',
)

# Any existing visibility calls must keep those controls hidden.
replace_once(
'''      const setTaxonomyFieldsVisible = visible => {
        if (categoryField) categoryField.hidden = !visible;
        if (subcategoryField) subcategoryField.hidden = !visible;
      };''',
'''      const setTaxonomyFieldsVisible = () => {
        if (categoryField) categoryField.hidden = true;
        if (subcategoryField) subcategoryField.hidden = true;
      };''',
    'taxonomy visibility helper',
)

# Remove memory/temporary-choice wording from merchant classification UI.
replace_once(
'''      const customCategoryNote = () => {
        const rule = merchantDictionaryRuleForValue(input.value);
        return rule?.ambiguous
          ? "Enseigne multi-catégories : choisis librement pour cette opération. Ce choix ne sera pas mémorisé."
          : "Catégorie personnalisée : elle sera mémorisée pour ce libellé.";
      };''',
'''      const customCategoryNote = () => {
        const rule = merchantDictionaryRuleForValue(input.value);
        return rule?.ambiguous
          ? "Enseigne multi-catégories."
          : "Catégorie personnalisée.";
      };''',
    'custom category note',
)
replace_once(
    'setNote("Enseigne multi-catégories : choisis une proposition ci-dessus ou classe-la manuellement.", false);',
    'setNote("Enseigne multi-catégories : choisis une proposition dans la liste.", false);',
    'ambiguous merchant note',
)
replace_once(
    'setNote(`${rule.category} › ${rule.subcategory}${rule.choice ? " · choix ponctuel" : rule.learned ? " · mémorisé" : ""}`, true);',
    'setNote(`${rule.category} › ${rule.subcategory}`, true);',
    'selected merchant note',
)
replace_once(
    'setNote(`${rule.category} › ${rule.subcategory}${rule.learned ? " · mémorisé" : ""}`, true);',
    'setNote(`${rule.category} › ${rule.subcategory}`, true);',
    'category change note',
)
replace_once(
    'setNote("Libellé libre : choisis la catégorie et la sous-catégorie.", false);',
    'setNote("Libellé libre.", false);',
    'free label note',
)

path.write_text(text, encoding='utf-8')
