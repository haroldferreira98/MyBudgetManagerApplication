from pathlib import Path
import re, gzip, base64, json

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
    '<meta name="app-build" content="20260918-merchant-autocomplete-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit("app build marker not found")

merchant_payload = gzip.decompress(base64.b64decode('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')).decode("utf-8")
merchant_data = json.loads(merchant_payload)
if not isinstance(merchant_data.get("merchants"), list) or len(merchant_data["merchants"]) < 200:
    raise SystemExit("merchant dictionary invalid")
Path("merchants.json").write_text(json.dumps(merchant_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

replace_once(
'''    function spendingTitle(item, fallback = "Dépense") {
      return String(item?.subcategory || item?.label || item?.category || fallback);
    }''',
'''    function spendingTitle(item, fallback = "Dépense") {
      return String(item?.label || item?.subcategory || item?.category || fallback);
    }''',
"spendingTitle"
)

replace_once(
'''      settings: { theme: "auto", privacy: false },
      incomes: [],''',
'''      settings: { theme: "auto", privacy: false },
      merchantPreferences: {},
      incomes: [],''',
"empty state merchant preferences"
)
replace_once(
'''        settings: { ...base.settings, ...(input.settings || {}) },
        incomes: Array.isArray(input.incomes) ? input.incomes.map(item => ({ ...item, category: item.category || "Salaire" })) : [],''',
'''        settings: { ...base.settings, ...(input.settings || {}) },
        merchantPreferences: input.merchantPreferences && typeof input.merchantPreferences === "object" && !Array.isArray(input.merchantPreferences) ? input.merchantPreferences : {},
        incomes: Array.isArray(input.incomes) ? input.incomes.map(item => ({ ...item, category: item.category || "Salaire" })) : [],''',
"migrate merchant preferences"
)

css = r'''
    /* MERCHANT-AUTOCOMPLETE-V1 */
    .merchant-field { position: relative; }
    .merchant-input-wrap { position: relative; }
    .merchant-suggestions {
      display: grid;
      max-height: 178px;
      overflow-y: auto;
      margin-top: 5px;
      border: 1px solid var(--outline-variant);
      border-radius: var(--radius-small);
      background: var(--surface-container-lowest);
      box-shadow: 0 8px 22px color-mix(in srgb, var(--shadow) 35%, transparent);
      overscroll-behavior: contain;
    }
    .merchant-suggestions[hidden] { display: none !important; }
    .merchant-suggestion {
      width: 100%;
      min-height: 46px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      align-items: center;
      gap: 10px;
      padding: 7px 10px;
      border: 0;
      border-bottom: 1px solid color-mix(in srgb, var(--outline-variant) 58%, transparent);
      background: transparent;
      color: var(--on-surface);
      text-align: left;
      cursor: pointer;
    }
    .merchant-suggestion:last-child { border-bottom: 0; }
    .merchant-suggestion:active,
    .merchant-suggestion:hover { background: var(--surface-container-low); }
    .merchant-suggestion-main { min-width: 0; }
    .merchant-suggestion-name {
      display: block;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 13px;
      font-weight: 680;
    }
    .merchant-suggestion-meta {
      display: block;
      margin-top: 2px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      color: var(--on-surface-variant);
      font-size: 10.5px;
    }
    .merchant-suggestion-arrow { color: var(--on-surface-variant); font-size: 18px; }
    .merchant-field-hint {
      min-height: 15px;
      padding-inline: 1px;
      color: var(--on-surface-variant);
      font-size: 10px;
      line-height: 1.25;
    }
    .merchant-field-hint.auto { color: var(--success); }
    #entityModal.merchant-suggestions-open .sheet {
      max-height: min(78dvh, 760px) !important;
    }
'''
replace_once("  </style>", css + "\n  </style>", "merchant css")

normalize_block = '''    function normalizeSearch(value) {
      return String(value ?? "")
        .normalize("NFD")
        .replace(/[\\u0300-\\u036f]/g, "")
        .toLowerCase()
        .trim();
    }
'''
merchant_js = r'''
    // MERCHANT-AUTOCOMPLETE-V1
    let merchantDictionary = [];
    let merchantDictionaryLoaded = false;
    let merchantDictionaryPromise = null;

    async function loadMerchantDictionary() {
      if (merchantDictionaryLoaded) return merchantDictionary;
      if (merchantDictionaryPromise) return merchantDictionaryPromise;
      merchantDictionaryPromise = fetch(`./merchants.json?build=${encodeURIComponent(APP_BUILD || "current")}`, { cache: "no-store" })
        .then(response => {
          if (!response.ok) throw new Error(`merchants.json ${response.status}`);
          return response.json();
        })
        .then(payload => {
          const merchants = Array.isArray(payload?.merchants) ? payload.merchants : [];
          merchantDictionary = merchants
            .filter(item => item && item.name)
            .map(item => ({
              name: String(item.name),
              category: item.category ? String(item.category) : "",
              subcategory: item.subcategory ? String(item.subcategory) : "",
              aliases: Array.isArray(item.aliases) ? item.aliases.map(String) : [],
              ambiguous: item.ambiguous === true,
              kind: String(item.kind || "merchant"),
              learned: false
            }))
            .sort((a, b) => a.name.localeCompare(b.name, "fr", { sensitivity: "base" }));
          merchantDictionaryLoaded = true;
          return merchantDictionary;
        })
        .catch(error => {
          console.error("Chargement du dictionnaire d’enseignes impossible", error);
          merchantDictionaryLoaded = false;
          return [];
        })
        .finally(() => {
          merchantDictionaryPromise = null;
        });
      return merchantDictionaryPromise;
    }

    function merchantLearnedRules() {
      const preferences = state.merchantPreferences && typeof state.merchantPreferences === "object" ? state.merchantPreferences : {};
      return Object.values(preferences)
        .filter(item => item && item.name)
        .map(item => ({
          name: String(item.name),
          category: String(item.category || ""),
          subcategory: String(item.subcategory || ""),
          aliases: [],
          ambiguous: false,
          kind: "learned",
          learned: true
        }));
    }

    function merchantSearchValues(rule) {
      return [rule.name, ...(Array.isArray(rule.aliases) ? rule.aliases : [])]
        .map(value => normalizeSearch(value))
        .filter(Boolean);
    }

    function merchantCandidates(query = "", limit = 14) {
      const q = normalizeSearch(query);
      const seen = new Set();
      const combined = [...merchantLearnedRules(), ...merchantDictionary];
      return combined
        .map(rule => {
          const values = merchantSearchValues(rule);
          let rank = 3;
          if (q) {
            if (values.some(value => value === q)) rank = 0;
            else if (values.some(value => value.startsWith(q))) rank = 1;
            else if (values.some(value => value.includes(q))) rank = 2;
            else return null;
          }
          return { rule, rank };
        })
        .filter(Boolean)
        .sort((a, b) => a.rank - b.rank || a.rule.name.localeCompare(b.rule.name, "fr", { sensitivity: "base" }))
        .filter(({ rule }) => {
          const key = normalizeSearch(rule.name);
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        })
        .slice(0, limit)
        .map(entry => entry.rule);
    }

    function findMerchantRule(value) {
      const q = normalizeSearch(value);
      if (!q) return null;
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
      return merchantDictionary.find(rule => merchantSearchValues(rule).includes(q)) || null;
    }

    function rememberMerchantPreference(label, category, subcategory) {
      const name = String(label || "").trim();
      const key = normalizeSearch(name);
      if (!key || !category || !subcategory) return;
      state.merchantPreferences = state.merchantPreferences && typeof state.merchantPreferences === "object" ? state.merchantPreferences : {};
      state.merchantPreferences[key] = {
        name,
        category: String(category),
        subcategory: String(subcategory),
        updatedAt: new Date().toISOString()
      };
    }

    function merchantSuggestionMarkup(rule) {
      const classification = rule.category && rule.subcategory
        ? `${rule.category} › ${rule.subcategory}`
        : "Catégorie à choisir";
      return `<button type="button" class="merchant-suggestion" data-merchant-choice="${escapeHtml(rule.name)}">
        <span class="merchant-suggestion-main">
          <span class="merchant-suggestion-name">${escapeHtml(rule.name)}</span>
          <span class="merchant-suggestion-meta">${escapeHtml(classification)}${rule.learned ? " · mémorisé" : ""}</span>
        </span>
        <span class="material-symbols-outlined merchant-suggestion-arrow">chevron_right</span>
      </button>`;
    }

    function setupMerchantAutocompleteFields(target) {
      const input = target.querySelector('[name="label"][data-merchant-input]');
      const suggestions = target.querySelector("[data-merchant-suggestions]");
      const note = target.querySelector("[data-merchant-auto-note]");
      const category = target.querySelector('[name="category"]');
      const subcategory = target.querySelector('[name="subcategory"]');
      const modal = document.getElementById("entityModal");
      if (!input || !suggestions || !category || !subcategory) return;

      const setNote = (message = "", automatic = false) => {
        if (!note) return;
        note.textContent = message;
        note.classList.toggle("auto", automatic);
      };

      const applyRule = rule => {
        if (!rule) return false;
        if (!rule.category || !rule.subcategory || !EXPENSE_CATEGORY_TREE[rule.category]?.includes(rule.subcategory)) {
          setNote("Enseigne multi-catégories : choisis la catégorie une fois, l’app la mémorisera.", false);
          return false;
        }
        if ([...category.options].some(option => option.value === rule.category)) {
          category.value = rule.category;
          category.dispatchEvent(new Event("change", { bubbles: true }));
          if ([...subcategory.options].some(option => option.value === rule.subcategory)) {
            subcategory.value = rule.subcategory;
          }
          setNote(`${rule.category} › ${rule.subcategory}${rule.learned ? " · mémorisé" : ""}`, true);
          return true;
        }
        return false;
      };

      const closeSuggestions = () => {
        suggestions.hidden = true;
        input.setAttribute("aria-expanded", "false");
        modal?.classList.remove("merchant-suggestions-open");
      };

      const renderSuggestions = async () => {
        if (!merchantDictionaryLoaded) await loadMerchantDictionary();
        if (document.activeElement !== input) return;
        const rows = merchantCandidates(input.value);
        if (!rows.length) {
          suggestions.innerHTML = `<div class="merchant-suggestion" aria-disabled="true"><span class="merchant-suggestion-main"><span class="merchant-suggestion-name">Aucune enseigne trouvée</span><span class="merchant-suggestion-meta">Tu peux garder ton libellé et choisir la catégorie manuellement.</span></span></div>`;
        } else {
          suggestions.innerHTML = rows.map(merchantSuggestionMarkup).join("");
        }
        suggestions.hidden = false;
        input.setAttribute("aria-expanded", "true");
        modal?.classList.add("merchant-suggestions-open");
      };

      input.addEventListener("focus", () => {
        renderSuggestions();
        const exact = findMerchantRule(input.value);
        if (exact) applyRule(exact);
      });

      input.addEventListener("input", () => {
        const exact = findMerchantRule(input.value);
        if (exact) applyRule(exact);
        else setNote("Tape librement ou choisis une enseigne dans la liste.", false);
        renderSuggestions();
      });

      input.addEventListener("blur", () => setTimeout(closeSuggestions, 140));

      suggestions.addEventListener("pointerdown", event => {
        const button = event.target.closest?.("[data-merchant-choice]");
        if (button) event.preventDefault();
      });

      suggestions.addEventListener("click", event => {
        const button = event.target.closest?.("[data-merchant-choice]");
        if (!button) return;
        const rule = findMerchantRule(button.dataset.merchantChoice) || merchantCandidates(button.dataset.merchantChoice, 1)[0];
        if (!rule) return;
        input.value = rule.name;
        applyRule(rule);
        closeSuggestions();
        input.focus({ preventScroll: true });
        input.setSelectionRange(input.value.length, input.value.length);
      });

      category.addEventListener("change", () => {
        const rule = findMerchantRule(input.value);
        if (rule && rule.category === category.value && rule.subcategory === subcategory.value) {
          setNote(`${rule.category} › ${rule.subcategory}${rule.learned ? " · mémorisé" : ""}`, true);
        } else if (input.value.trim()) {
          setNote("Catégorie personnalisée : elle sera mémorisée pour ce libellé.", false);
        }
      });
      subcategory.addEventListener("change", () => {
        if (input.value.trim()) setNote("Catégorie personnalisée : elle sera mémorisée pour ce libellé.", false);
      });

      const initialRule = findMerchantRule(input.value);
      if (initialRule) applyRule(initialRule);
      else if (input.value.trim()) setNote("Libellé libre : la catégorie actuelle sera mémorisée à l’enregistrement.", false);
      else setNote("Tape librement ou choisis une enseigne dans la liste.", false);
    }
'''
replace_once(normalize_block, normalize_block + merchant_js + "\n", "normalizeSearch merchant helpers")

replace_once(
'''      if (type === "expense") {
        fields = `
          <div class="field-row">''',
'''      if (type === "expense") {
        fields = `
          <div class="field merchant-field">
            <label>Libellé</label>
            <div class="merchant-input-wrap"><input name="label" data-merchant-input required maxlength="80" autocomplete="off" aria-autocomplete="list" aria-expanded="false" value="${escapeHtml(data.label || "")}" placeholder="Ex. Intermarché"><div class="merchant-suggestions" data-merchant-suggestions hidden></div></div>
            <div class="merchant-field-hint" data-merchant-auto-note></div>
          </div>
          <div class="field-row">''',
"expense label field"
)
replace_once(
'''      } else if (type === "fixed") {
        fields = `
          <div class="field-row">''',
'''      } else if (type === "fixed") {
        fields = `
          <div class="field merchant-field">
            <label>Libellé</label>
            <div class="merchant-input-wrap"><input name="label" data-merchant-input required maxlength="80" autocomplete="off" aria-autocomplete="list" aria-expanded="false" value="${escapeHtml(data.label || "")}" placeholder="Ex. Netflix"><div class="merchant-suggestions" data-merchant-suggestions hidden></div></div>
            <div class="merchant-field-hint" data-merchant-auto-note></div>
          </div>
          <div class="field-row">''',
"fixed label field"
)

replace_once(
'''      if (type === "expense") {
        setupSpendingSubcategoryFields(target);
        setupHealthReimbursementFields(target);
        requestAnimationFrame(() => target.querySelector('[name="amount"]')?.focus());
      } else {
        if (type === "fixed") setupSpendingSubcategoryFields(target);
        healthModal?.classList.remove("health-reimbursement-available", "health-reimbursement-open");
      }''',
'''      if (type === "expense") {
        setupSpendingSubcategoryFields(target);
        setupHealthReimbursementFields(target);
        setupMerchantAutocompleteFields(target);
        requestAnimationFrame(() => target.querySelector('[name="label"]')?.focus());
      } else {
        if (type === "fixed") {
          setupSpendingSubcategoryFields(target);
          setupMerchantAutocompleteFields(target);
        }
        healthModal?.classList.remove("health-reimbursement-available", "health-reimbursement-open");
      }''',
"wire merchant autocomplete"
)

replace_once(
'label:String(current?.label||""), amount:moneyInputValue(form,"amount")',
'label:String(fd.get("label")||"").trim(), amount:moneyInputValue(form,"amount")',
"expense submit label"
)
replace_once(
'id: id || uid("fix"), label: String(current?.label || ""), amount: moneyInputValue(form, "amount"),',
'id: id || uid("fix"), label: String(fd.get("label") || "").trim(), amount: moneyInputValue(form, "amount"),',
"fixed submit label"
)

replace_once(
'''      } else return;

      const collection = collectionForType(type);''',
'''      } else return;

      if ((type === "expense" || type === "fixed") && item?.label && item?.category && item?.subcategory) {
        rememberMerchantPreference(item.label, item.category, item.subcategory);
      }

      const collection = collectionForType(type);''',
"remember merchant preference"
)

replace_once(
'<div class="list-title">${escapeHtml(item.label)}</div>',
'<div class="list-title">${escapeHtml(spendingTitle(item))}</div>',
"expense row title"
)
replace_once(
'placeholder="Rechercher catégorie ou sous-catégorie"',
'placeholder="Rechercher libellé, catégorie ou sous-catégorie"',
"expense search placeholder"
)
replace_once(
'Essaie une catégorie, une sous-catégorie ou un montant.',
'Essaie un libellé, une catégorie, une sous-catégorie ou un montant.',
"global empty search copy"
)

replace_once(
'''    renderAll();
    initCloudSync();''',
'''    renderAll();
    loadMerchantDictionary();
    initCloudSync();''',
"startup dictionary load"
)

replace_once(
'item.subcategory || item.label || item.name || item.category || entityLabel(type)',
'item.label || item.subcategory || item.name || item.category || entityLabel(type)',
"delete confirm label first"
)

text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
path.write_text(text, encoding="utf-8")
