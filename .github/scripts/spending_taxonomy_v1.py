from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Build marker
text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-spending-taxonomy-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

# Replace the flat expense category list with the new category > subcategory taxonomy.
pattern = r'''    const EXPENSE_CATEGORIES = \[.*?\n    \];\n\n    const INCOME_CATEGORIES = \['''
replacement = '''    // SPENDING-TAXONOMY-V1
    const EXPENSE_CATEGORY_TREE = Object.freeze({
      "Alimentation": [
        "Supermarchés & hypermarchés", "Supérettes & épiceries", "Marchés & primeurs", "Boulangerie", "Pâtisserie",
        "Boucherie & charcuterie", "Poissonnerie", "Fromagerie", "Traiteur", "Plat préparé", "Restaurant",
        "Fast-food & snack", "Livraison de repas", "Café & boissons", "Chocolaterie & confiserie", "Épicerie fine"
      ],
      "Voiture": [
        "Crédit & financement", "Assurance auto", "Carburant", "Recharge électrique", "Entretien & révision", "Réparations",
        "Pneus", "Contrôle technique", "Lavage & nettoyage", "Parking & stationnement", "Péages", "Amendes",
        "Carte grise & démarches", "Accessoires & équipements", "Pièces automobiles", "Dépannage & remorquage",
        "Location de voiture", "Achat de véhicule"
      ],
      "Transports en commun": [
        "Abonnement", "Métro", "Bus", "Tramway", "RER", "Train", "TGV", "TER", "Billet occasionnel",
        "Transport aéroport", "Transport international", "Vélo en libre-service", "Trottinette en libre-service", "Autre transport en commun"
      ],
      "VTC & Taxi": ["VTC", "Taxi", "Moto-taxi", "Navette privée", "Chauffeur privé", "Transport médical assis", "Autre VTC & Taxi"],
      "Maison": [
        "Loyer", "Charges de copropriété", "Électricité", "Gaz", "Eau", "Internet", "Assurance habitation", "Entretien maison",
        "Produits ménagers", "Mobilier", "Décoration", "Électroménager", "Cuisine & vaisselle", "Linge de maison", "Literie",
        "Bricolage", "Réparations", "Jardin & extérieur", "Déménagement", "Stockage", "Sécurité & alarmes", "Autre maison"
      ],
      "Santé": [
        "Médecin généraliste", "Médecin spécialiste", "Kiné / physiothérapie", "Pharmacie", "Dentiste", "Optique", "Ophtalmologie",
        "Analyses & laboratoire", "Imagerie médicale", "Examens médicaux", "Hospitalisation", "Urgences", "Psychologue / santé mentale",
        "Ostéopathe", "Podologue", "Audiologie", "Orthopédie & matériel médical", "Vaccins", "Médecine préventive / check-up",
        "Soins non remboursés", "Autre santé"
      ],
      "Personnel": ["Vêtements", "Chaussures", "Coiffure", "Beauté & soins", "Hygiène corporelle", "Accessoires", "Bijoux & montres", "Parfumerie", "Autre personnel"],
      "Loisirs & sorties": ["Cinéma", "Musée & exposition", "Spectacle & concert", "Activité & sortie", "Jeux vidéo", "Jeux & loisirs", "Sport & activité", "Livres & presse", "Bar & vie nocturne", "Autre loisirs & sorties"],
      "Abonnements & services numériques": ["Streaming vidéo", "Musique & audio", "Cloud & stockage", "IA & logiciels", "Applications", "Jeux & gaming", "Presse & lecture numérique", "Téléphonie mobile", "Autre abonnement numérique"],
      "Banque & crédits": ["Frais bancaires", "Cotisations bancaires", "Agios", "Intérêts", "Prêt personnel", "Crédit à la consommation", "Crédit immobilier", "Paiement fractionné", "Frais de change", "Retrait d'espèces", "Autre banque & crédits"],
      "Voyages": ["Avion", "Train longue distance", "Hôtel", "Hébergement", "Location de voiture", "Transports sur place", "Activités & visites", "Visa & formalités", "Assurance voyage", "Bagages", "Frais de change", "Autre voyage"],
      "Cadeaux & événements": ["Cadeau", "Anniversaire", "Mariage", "Fleurs", "Fête & réception", "Décoration événementielle", "Participation & cagnotte", "Autre cadeau & événement"],
      "Administratif & impôts": ["Impôt sur le revenu", "Taxe foncière", "Taxe d'habitation", "Documents officiels", "Frais administratifs", "Timbres fiscaux", "Frais de justice", "Démarches & titres", "Autre administratif & impôts"],
      "Animaux": ["Alimentation", "Vétérinaire", "Médicaments", "Assurance", "Toilettage", "Accessoires", "Garde & pension", "Adoption & démarches", "Autre animaux"],
      "Autre": ["Autre"]
    });
    const EXPENSE_CATEGORIES = Object.keys(EXPENSE_CATEGORY_TREE);

    function spendingCategoryOptions(selected) {
      const current = String(selected || "");
      const options = [...EXPENSE_CATEGORIES];
      if (current && !options.includes(current)) options.push({ value: current, label: `${current} (ancienne catégorie)` });
      return options;
    }

    function spendingSubcategoryOptions(category, selected) {
      const current = String(selected || "");
      const options = [...(EXPENSE_CATEGORY_TREE[String(category || "")] || [])];
      if (current && !options.includes(current)) options.push({ value: current, label: `${current} (ancienne sous-catégorie)` });
      if (!options.length) return [{ value: "", label: "À reclasser avec le prochain JSON" }];
      return options;
    }

    function envelopeCategoryOptions(selected) {
      const current = String(selected || "");
      const options = ["Toutes", ...EXPENSE_CATEGORIES];
      if (current && !options.includes(current)) options.push({ value: current, label: `${current} (ancienne catégorie)` });
      return options;
    }

    function spendingTitle(item, fallback = "Dépense") {
      return String(item?.subcategory || item?.label || item?.category || fallback);
    }

    const INCOME_CATEGORIES = ['''
text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit('expense category block not found')

# Preserve subcategory through imports/migrations without automatically rewriting old data yet.
old = 'expenses: Array.isArray(input.expenses) ? input.expenses.map(item => ({ ...item, category: item.category === "Hygiène" ? "Hygiène corporelle" : item.category, healthReimbursement: normalizeHealthReimbursement(item.healthReimbursement) })) : [],'
new = 'expenses: Array.isArray(input.expenses) ? input.expenses.map(item => ({ ...item, category: item.category === "Hygiène" ? "Hygiène corporelle" : item.category, subcategory: String(item.subcategory || ""), healthReimbursement: normalizeHealthReimbursement(item.healthReimbursement) })) : [],'
if text.count(old) != 1:
    raise SystemExit('expense migration anchor not found')
text = text.replace(old, new, 1)

old = 'fixedCharges: Array.isArray(input.fixedCharges) ? input.fixedCharges : [],'
new = 'fixedCharges: Array.isArray(input.fixedCharges) ? input.fixedCharges.map(item => ({ ...item, subcategory: String(item.subcategory || "") })) : [],'
if text.count(old) != 1:
    raise SystemExit('fixed migration anchor not found')
text = text.replace(old, new, 1)

# Health reimbursement linked row title.
text = text.replace('meta:`Lié à ${expense.label || "dépense santé"}`', 'meta:`Lié à ${spendingTitle(expense, "dépense santé")}`')

# Global search: category/subcategory first, legacy label remains searchable during migration.
old = '''        rows.push({ type:"expense", id:item.id, icon:categoryIcon(item.category), kind:"Dépense", title:item.label,
          subtitle:`${item.category} · ${formatDate(item.date)}`, amount:-safeNumber(item.amount),
          haystack:[item.label,item.category,item.date,"dépense","depense",...amountTokens(item.amount)].join(" ") });'''
new = '''        rows.push({ type:"expense", id:item.id, icon:categoryIcon(item.category), kind:"Dépense", title:spendingTitle(item),
          subtitle:`${item.category}${item.subcategory ? ` · ${item.subcategory}` : ""} · ${formatDate(item.date)}`, amount:-safeNumber(item.amount),
          haystack:[item.label,item.category,item.subcategory,item.date,"dépense","depense",...amountTokens(item.amount)].join(" ") });'''
if text.count(old) != 1:
    raise SystemExit('global expense search anchor not found')
text = text.replace(old, new, 1)

old = '''      state.fixedCharges.forEach(item => rows.push({
        type: "fixed", id: item.id, icon: "event_repeat", kind: "Charge fixe", title: item.label,
        subtitle: `Jour ${safeNumber(item.day, 1)}`, amount: -safeNumber(item.amount),
        haystack: [item.label, "charge fixe", "charges fixes", item.day, ...amountTokens(item.amount)].join(" ")
      }));'''
new = '''      state.fixedCharges.forEach(item => rows.push({
        type: "fixed", id: item.id, icon: categoryIcon(item.category), kind: "Charge fixe", title: spendingTitle(item, "Charge fixe"),
        subtitle: `${item.category || "Charge fixe"}${item.subcategory ? ` · ${item.subcategory}` : ""} · Jour ${safeNumber(item.day, 1)}`, amount: -safeNumber(item.amount),
        haystack: [item.label, item.category, item.subcategory, "charge fixe", "charges fixes", item.day, ...amountTokens(item.amount)].join(" ")
      }));'''
if text.count(old) != 1:
    raise SystemExit('global fixed search anchor not found')
text = text.replace(old, new, 1)

text = text.replace('Essaie un libellé, une catégorie ou un montant.', 'Essaie une catégorie, une sous-catégorie ou un montant.')

# Fixed charge display/sort uses subcategory; legacy labels remain fallback.
text = text.replace('<div class="list-title">${escapeHtml(charge.label)}</div>', '<div class="list-title">${escapeHtml(spendingTitle(charge, "Charge fixe"))}</div>')
text = text.replace('if (fixedSort === "alpha") return String(a.label || "").localeCompare(String(b.label || ""), "fr", { sensitivity: "base" });', 'if (fixedSort === "alpha") return spendingTitle(a, "Charge fixe").localeCompare(spendingTitle(b, "Charge fixe"), "fr", { sensitivity: "base" });')

# Unified operations: display subcategory instead of requiring a merchant label.
old = 'rows.push({ type:"expense", group:"expense", id:item.id, title:item.label, category:item.category||"Dépense", amount:-safeNumber(item.amount), sortDate:String(item.date||""), meta:`${item.category || "Dépense"} · ${formatOperationDate(item.date)}`, icon:categoryIcon(item.category) });'
new = 'rows.push({ type:"expense", group:"expense", id:item.id, title:spendingTitle(item), category:item.category||"Dépense", amount:-safeNumber(item.amount), sortDate:String(item.date||""), meta:`${item.category || "Dépense"}${item.subcategory ? ` · ${item.subcategory}` : ""} · ${formatOperationDate(item.date)}`, icon:categoryIcon(item.category) });'
if text.count(old) != 1:
    raise SystemExit('operation expense row anchor not found')
text = text.replace(old, new, 1)

text = text.replace('title: item.label,\n          category: item.category || "Charge fixe",', 'title: spendingTitle(item, "Charge fixe"),\n          category: item.category || "Charge fixe",', 1)
text = text.replace('meta: `${item.category || "Charge fixe"} · ${formatOperationDate(operationDate)}`,\n          icon: "event_repeat"', 'meta: `${item.category || "Charge fixe"}${item.subcategory ? ` · ${item.subcategory}` : ""} · ${formatOperationDate(operationDate)}`,\n          icon: categoryIcon(item.category)', 1)

# Expense screen remains compatible, but now displays the subcategory as the operation name.
text = text.replace('.filter(item => !normalizedSearch || `${item.label} ${item.category}`.toLowerCase().includes(normalizedSearch))', '.filter(item => !normalizedSearch || [item.label, item.category, item.subcategory].join(" ").toLowerCase().includes(normalizedSearch))')
text = text.replace('if (expenseSort === "alpha") return String(a.label || "").localeCompare(String(b.label || ""), "fr", { sensitivity: "base" });', 'if (expenseSort === "alpha") return spendingTitle(a).localeCompare(spendingTitle(b), "fr", { sensitivity: "base" });')
text = text.replace('<div class="list-title">${escapeHtml(item.label)}</div>', '<div class="list-title">${escapeHtml(spendingTitle(item))}</div>', 1)
text = text.replace('placeholder="Rechercher un libellé ou une catégorie"', 'placeholder="Rechercher catégorie ou sous-catégorie"')

# Main category icons + legacy icons while the JSON has not yet been migrated.
pattern = r'''    function categoryIcon\(category\) \{\n      return \{.*?\n      \}\[category\] \|\| "receipt_long";\n    \}'''
replacement = '''    function categoryIcon(category) {
      return {
        "Alimentation": "restaurant",
        "Voiture": "directions_car",
        "Transports en commun": "train",
        "VTC & Taxi": "local_taxi",
        "Maison": "home",
        "Santé": "medical_services",
        "Personnel": "person",
        "Loisirs & sorties": "theater_comedy",
        "Abonnements & services numériques": "subscriptions",
        "Banque & crédits": "account_balance",
        "Voyages": "flight_takeoff",
        "Cadeaux & événements": "redeem",
        "Administratif & impôts": "description",
        "Animaux": "pets",
        "Autre": "category",
        "Courses": "shopping_cart",
        "Carburant": "local_gas_station",
        "Beauté & soins": "spa",
        "Entretien maison": "cleaning_services",
        "Hygiène corporelle": "soap",
        "Loisirs": "sports_esports",
        "Restaurant": "restaurant",
        "Plat préparé": "lunch_dining"
      }[category] || "receipt_long";
    }'''
text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit('categoryIcon block not found')

# Reimbursement cards use the health subcategory; legacy labels remain fallback.
text = text.replace('.sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")) || String(a.label || "").localeCompare(String(b.label || ""), "fr", { sensitivity: "base" }));', '.sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")) || spendingTitle(a).localeCompare(spendingTitle(b), "fr", { sensitivity: "base" }));')
text = text.replace('${escapeHtml(item.label || "Dépense Santé")}', '${escapeHtml(spendingTitle(item, "Dépense Santé"))}')

# Generic linked category/subcategory selector setup for expenses and fixed charges.
anchor = '''    function setupHealthReimbursementFields(target) {'''
insert = '''    function setupSpendingSubcategoryFields(target) {
      const category = target.querySelector('[name="category"]');
      const subcategory = target.querySelector('[name="subcategory"]');
      const field = target.querySelector('[data-spending-subcategory-field]');
      if (!category || !subcategory || !field) return;

      const sync = (preserveCurrent = false) => {
        const values = EXPENSE_CATEGORY_TREE[category.value] || [];
        const current = preserveCurrent ? String(subcategory.value || "") : "";
        if (!values.length) {
          subcategory.innerHTML = '<option value="">À reclasser avec le prochain JSON</option>';
          subcategory.required = false;
          subcategory.disabled = true;
          field.classList.add("legacy-subcategory-field");
          return;
        }
        subcategory.disabled = false;
        subcategory.required = true;
        field.classList.remove("legacy-subcategory-field");
        subcategory.innerHTML = optionTags(values, values.includes(current) ? current : values[0]);
      };

      category.addEventListener("change", () => sync(false));
      sync(true);
    }

'''
if text.count(anchor) != 1:
    raise SystemExit('subcategory setup insertion anchor not found')
text = text.replace(anchor, insert + anchor, 1)

# Expense form: no label. Category + subcategory are the identity of the purchase.
old = '''          <div class="field"><label>Libellé</label><input name="label" required maxlength="80" value="${escapeHtml(data.label || "")}" placeholder="Ex. Auchan"></div>
          <div class="field-row">'''
new = '''          <div class="field-row">'''
if text.count(old) != 1:
    raise SystemExit('expense label field anchor not found')
text = text.replace(old, new, 1)
old = '<div class="field"><label>Catégorie</label><select name="category">${optionTags(EXPENSE_CATEGORIES, data.category || "Autre")}</select></div>'
new = '<div class="field"><label>Catégorie</label><select name="category" required>${optionTags(spendingCategoryOptions(data.category), data.category || "Alimentation")}</select></div>\n          <div class="field" data-spending-subcategory-field><label>Sous-catégorie</label><select name="subcategory">${optionTags(spendingSubcategoryOptions(data.category || "Alimentation", data.subcategory), data.subcategory || "")}</select></div>'
if text.count(old) != 1:
    raise SystemExit('expense category field anchor not found')
text = text.replace(old, new, 1)

# Fixed charge form uses the same taxonomy and no longer requires a custom label for new entries.
old = '''          <div class="field"><label>Libellé</label><input name="label" required maxlength="80" value="${escapeHtml(data.label || "")}" placeholder="Ex. Loyer"></div>
          <div class="field-row">'''
new = '''          <div class="field-row">'''
if text.count(old) != 1:
    raise SystemExit('fixed label field anchor not found')
text = text.replace(old, new, 1)
old = '<div class="field"><label>Catégorie</label><select name="category">${optionTags(FIXED_CHARGE_CATEGORIES, data.category || "Abonnements")}</select></div>'
new = '<div class="field"><label>Catégorie</label><select name="category" required>${optionTags(spendingCategoryOptions(data.category), data.category || "Maison")}</select></div>\n          <div class="field" data-spending-subcategory-field><label>Sous-catégorie</label><select name="subcategory">${optionTags(spendingSubcategoryOptions(data.category || "Maison", data.subcategory), data.subcategory || "")}</select></div>'
if text.count(old) != 1:
    raise SystemExit('fixed category field anchor not found')
text = text.replace(old, new, 1)

# Envelopes follow main categories, while legacy envelope categories remain editable until JSON migration.
old = '${optionTags(["Toutes", ...EXPENSE_CATEGORIES], data.category || "Toutes")}'
new = '${optionTags(envelopeCategoryOptions(data.category), data.category || "Toutes")}'
if text.count(old) != 1:
    raise SystemExit('envelope category options anchor not found')
text = text.replace(old, new, 1)

# Setup linked subcategory selects when rendering forms.
old = '''      if (type === "expense") {
        setupHealthReimbursementFields(target);
        requestAnimationFrame(() => target.querySelector('[name="amount"]')?.focus());
      } else {
        healthModal?.classList.remove("health-reimbursement-available", "health-reimbursement-open");
      }'''
new = '''      if (type === "expense") {
        setupSpendingSubcategoryFields(target);
        setupHealthReimbursementFields(target);
        requestAnimationFrame(() => target.querySelector('[name="amount"]')?.focus());
      } else {
        if (type === "fixed") setupSpendingSubcategoryFields(target);
        healthModal?.classList.remove("health-reimbursement-available", "health-reimbursement-open");
      }'''
if text.count(old) != 1:
    raise SystemExit('form setup anchor not found')
text = text.replace(old, new, 1)

# Save category + subcategory. Existing legacy label is retained silently only until the JSON migration.
old = '''        const category=fd.get("category")||"Autre", tracked=category==="Santé"&&fd.get("healthReimbursementTracked")==="on";'''
new = '''        const category=fd.get("category")||"Autre", subcategory=String(fd.get("subcategory")||"").trim(), tracked=category==="Santé"&&fd.get("healthReimbursementTracked")==="on";
        if (EXPENSE_CATEGORY_TREE[category] && !subcategory) { showSnackbar("Choisis une sous-catégorie."); form.querySelector('[name="subcategory"]')?.focus(); return; }'''
if text.count(old) != 1:
    raise SystemExit('expense submit category anchor not found')
text = text.replace(old, new, 1)
old = 'item={ id:id||uid("exp"), label:String(fd.get("label")||"").trim(), amount:moneyInputValue(form,"amount"), date:fd.get("date")||todayISO(), category, bucket:"wants", healthReimbursement:{ tracked, completed:tracked?previousHealth.completed:false, completedAt:tracked?previousHealth.completedAt:"", socialSecurity:{amount:ss,date:ss>0?ssDate:""}, mutual:{amount:mutual,date:mutual>0?mutualDate:""} } };'
new = 'item={ id:id||uid("exp"), label:String(current?.label||""), amount:moneyInputValue(form,"amount"), date:fd.get("date")||todayISO(), category, subcategory, bucket:"wants", healthReimbursement:{ tracked, completed:tracked?previousHealth.completed:false, completedAt:tracked?previousHealth.completedAt:"", socialSecurity:{amount:ss,date:ss>0?ssDate:""}, mutual:{amount:mutual,date:mutual>0?mutualDate:""} } };'
if text.count(old) != 1:
    raise SystemExit('expense item anchor not found')
text = text.replace(old, new, 1)

old = '''          id: id || uid("fix"), label: String(fd.get("label") || "").trim(), amount: moneyInputValue(form, "amount"),
          day: clamp(Math.round(safeNumber(fd.get("day"), 1)), 1, 31), category: String(fd.get("category") || current?.category || "Abonnements"), bucket: "needs", active: true,
          paidMonths: current?.paidMonths || []'''
new = '''          id: id || uid("fix"), label: String(current?.label || ""), amount: moneyInputValue(form, "amount"),
          day: clamp(Math.round(safeNumber(fd.get("day"), 1)), 1, 31), category: String(fd.get("category") || current?.category || "Maison"), subcategory: String(fd.get("subcategory") || ""), bucket: "needs", active: true,
          paidMonths: current?.paidMonths || []'''
if text.count(old) != 1:
    raise SystemExit('fixed item anchor not found')
text = text.replace(old, new, 1)

# Delete confirmation works without a label.
text = text.replace('item.label || item.name || entityLabel(type)', 'item.subcategory || item.label || item.name || item.category || entityLabel(type)')

# CSV includes the new field.
text = text.replace('"date","categorie","affectation"', '"date","categorie","sous_categorie","affectation"')
text = text.replace('["depense",x.id,x.label,x.amount,x.date,x.category,x.bucket,', '["depense",x.id,x.label,x.amount,x.date,x.category,x.subcategory || "",x.bucket,')
text = text.replace('["revenu",x.id,x.label,x.amount,x.date,x.category || "Salaire","","",', '["revenu",x.id,x.label,x.amount,x.date,x.category || "Salaire","","","",')
text = text.replace('["charge_fixe",x.id,x.label,x.amount,"","",x.bucket,', '["charge_fixe",x.id,x.label,x.amount,"",x.category || "",x.subcategory || "",x.bucket,')
text = text.replace('["credit",x.id,x.name,"","","","savings",', '["credit",x.id,x.name,"","","","","savings",')
text = text.replace('["projet_epargne",x.id,x.name,"","","","savings",', '["projet_epargne",x.id,x.name,"","","","","savings",')
text = text.replace('["enveloppe",x.id,x.name,"","",x.category,"","",', '["enveloppe",x.id,x.name,"","",x.category,"","","",')

path.write_text(text, encoding='utf-8')
