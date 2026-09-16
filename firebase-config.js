// Configuration publique de l'application Web Firebase.
window.BUDGET_FIREBASE_CONFIG = {
  apiKey: "AIzaSyDsN9i87GGzx_v_Ci72yt-oDWN77S2Apak",
  authDomain: "mybudgetmanagerapplication.firebaseapp.com",
  projectId: "mybudgetmanagerapplication",
  storageBucket: "mybudgetmanagerapplication.firebasestorage.app",
  messagingSenderId: "83517729033",
  appId: "1:83517729033:web:07144c82e6f6bab3984bd8",
  measurementId: "G-YHNCYY4FYK"
};

// UI patch: on iPhone, keep Montant and Date on the same row in Revenu sheets.
(() => {
  if (document.getElementById("incomeAmountDateRowPatch")) return;
  const style = document.createElement("style");
  style.id = "incomeAmountDateRowPatch";
  style.textContent = `
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
  `;
  document.head.appendChild(style);
})();

// Fixed charge categories.
(() => {
  const FIXED_CHARGE_CATEGORIES = [
    "Loyer",
    "Assurances",
    "Abonnements",
    "Forfait mobile",
    "Forfait internet",
    "Cotisations bancaires",
    "Électricité",
    "Gaz",
    "Eau",
    "Mutuelle",
    "Transport",
    "Parking",
    "Charges de copropriété",
    "Taxe foncière",
    "Frais de garde",
    "Pension alimentaire"
  ];

  function categoryOptions(selected = "") {
    return FIXED_CHARGE_CATEGORIES.map(category =>
      `<option value="${escapeHtml(category)}" ${category === selected ? "selected" : ""}>${escapeHtml(category)}</option>`
    ).join("");
  }

  function decorateFixedChargeRows() {
    if (typeof state === "undefined") return;
    document.querySelectorAll('#screen-home [data-edit-type="fixed"]').forEach(editButton => {
      const charge = state.fixedCharges.find(item => item.id === editButton.dataset.editId);
      if (!charge?.category) return;
      const subtitle = editButton.closest(".list-item")?.querySelector(".list-sub");
      if (!subtitle || subtitle.dataset.fixedCategoryApplied === "1") return;
      subtitle.textContent = `${charge.category} · ${subtitle.textContent}`;
      subtitle.dataset.fixedCategoryApplied = "1";
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (typeof renderEntityFields === "function" && !window.__fixedCategoryFieldsPatched) {
      window.__fixedCategoryFieldsPatched = true;
      const originalRenderEntityFields = renderEntityFields;
      renderEntityFields = function(type, data = {}, editing = false) {
        const result = originalRenderEntityFields(type, data, editing);
        if (type !== "fixed") return result;

        const target = document.getElementById("dynamicFields");
        const actions = target?.querySelector(".modal-actions");
        if (!target || !actions || target.querySelector('[name="category"]')) return result;

        const field = document.createElement("div");
        field.className = "field";
        field.innerHTML = `
          <label>Catégorie</label>
          <select name="category" required>
            <option value="" disabled ${data.category ? "" : "selected"}>Choisir une catégorie</option>
            ${categoryOptions(data.category || "")}
          </select>`;
        target.insertBefore(field, actions);
        return result;
      };
    }

    // Fixed charges need a dedicated submit path so the chosen category is saved too.
    document.addEventListener("submit", event => {
      const form = event.target;
      if (!(form instanceof HTMLFormElement) || form.id !== "entityForm") return;

      const fd = new FormData(form);
      if (fd.get("entityType") !== "fixed") return;

      event.preventDefault();
      event.stopImmediatePropagation();

      const id = form.dataset.editId || null;
      const current = id ? state.fixedCharges.find(item => item.id === id) : null;
      const item = {
        ...(current || {}),
        id: id || uid("fix"),
        label: String(fd.get("label") || "").trim(),
        amount: safeNumber(fd.get("amount")),
        category: String(fd.get("category") || "").trim(),
        day: clamp(Math.round(safeNumber(fd.get("day"), 1)), 1, 31),
        bucket: "needs",
        active: true,
        paidMonths: current?.paidMonths || []
      };

      if (id) {
        const index = state.fixedCharges.findIndex(existing => existing.id === id);
        if (index >= 0) state.fixedCharges[index] = item;
      } else {
        state.fixedCharges.push(item);
      }

      closeModal("entityModal");
      saveState(`Charge fixe ${id ? "modifiée" : "ajoutée"}.`);
    }, true);

    if (typeof renderHome === "function" && !window.__fixedCategoryHomePatched) {
      window.__fixedCategoryHomePatched = true;
      const originalRenderHome = renderHome;
      renderHome = function(...args) {
        const result = originalRenderHome(...args);
        decorateFixedChargeRows();
        return result;
      };
    }

    decorateFixedChargeRows();
  }, { once: true });
})();
