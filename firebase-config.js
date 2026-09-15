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

// UI patch: Settings is now a full navigation page, not a bottom sheet.
(() => {
  const style = document.createElement("style");
  style.id = "settingsNavPagePatch";
  style.textContent = `
    .bottom-nav { grid-template-columns: repeat(5, minmax(0, 1fr)) !important; }
    @media (max-width: 560px) {
      .bottom-nav { grid-template-columns: repeat(5, minmax(0, 1fr)) !important; }
      .nav-btn { min-width: 0; }
      .nav-btn span:last-child { font-size: 8.5px; }
    }
    #screen-settings .settings-page-card { margin-top: 8px; }
  `;
  document.head.appendChild(style);

  function syncSettingsButtons() {
    if (typeof state === "undefined") return;
    const selected = state.settings?.theme || "auto";
    document.querySelectorAll('#screen-settings [data-theme-choice]').forEach(btn => {
      btn.classList.toggle("active", btn.dataset.themeChoice === selected);
    });
  }

  function ensureSettingsPage() {
    const main = document.querySelector("main");
    const nav = document.querySelector(".bottom-nav");
    if (!main || !nav) return;

    document.getElementById("settingsBtn")?.closest(".top-actions")?.remove();
    document.getElementById("settingsModal")?.remove();

    let screen = document.getElementById("screen-settings");
    if (!screen) {
      screen = document.createElement("section");
      screen.className = "screen";
      screen.id = "screen-settings";
      screen.dataset.title = "Paramètres";
      screen.innerHTML = `
        <div class="section settings-page-card">
          <div class="section-header">
            <div>
              <h2 class="section-title">Apparence</h2>
              <p class="section-subtitle">Le mode Automatique suit le thème de l’iPhone.</p>
            </div>
          </div>
          <div class="card">
            <div class="segmented" id="settingsThemeSegmentPage">
              <button data-theme-choice="light">Clair</button>
              <button data-theme-choice="dark">Sombre</button>
              <button data-theme-choice="auto">Automatique</button>
            </div>
          </div>
        </div>`;
      main.appendChild(screen);
    }

    if (!nav.querySelector('[data-screen="settings"]')) {
      const button = document.createElement("button");
      button.className = "nav-btn";
      button.dataset.screen = "settings";
      button.setAttribute("aria-label", "Paramètres");
      button.innerHTML = '<span class="material-symbols-outlined">settings</span><span>Paramètres</span>';
      nav.appendChild(button);
    }

    syncSettingsButtons();
  }

  function renameDeleteAction() {
    const button = document.getElementById("deleteCloudDataBtn");
    if (!button || button.disabled) return;
    const icon = button.querySelector(".material-symbols-outlined")?.outerHTML || '<span class="material-symbols-outlined">delete_forever</span>';
    button.innerHTML = `${icon}Supprimer toutes les opérations`;
  }

  document.addEventListener("DOMContentLoaded", () => {
    ensureSettingsPage();
    renameDeleteAction();

    // Extend the app's own screen router so Settings behaves exactly like the other tabs.
    if (typeof setCurrentScreen === "function" && !window.__settingsRouterPatched) {
      window.__settingsRouterPatched = true;
      const originalSetCurrentScreen = setCurrentScreen;
      setCurrentScreen = function(screen, updateNav = true) {
        if (screen !== "settings") return originalSetCurrentScreen(screen, updateNav);
        currentScreen = "settings";
        document.querySelectorAll(".screen").forEach(el => el.classList.toggle("active", el.id === "screen-settings"));
        document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.toggle("active", btn.dataset.screen === "settings"));
        const title = document.getElementById("screenTitle");
        if (title) title.textContent = "Paramètres";
        window.scrollTo({ top: 0, behavior: "smooth" });
        syncSettingsButtons();
      };
    }

    // Keep dynamic Profile content and theme selection in sync after every render.
    if (typeof renderProfile === "function" && !window.__profileDeleteLabelPatched) {
      window.__profileDeleteLabelPatched = true;
      const originalRenderProfile = renderProfile;
      renderProfile = function(...args) {
        const result = originalRenderProfile(...args);
        renameDeleteAction();
        return result;
      };
    }

    if (typeof renderAll === "function" && !window.__settingsRenderPatched) {
      window.__settingsRenderPatched = true;
      const originalRenderAll = renderAll;
      renderAll = function(...args) {
        const result = originalRenderAll(...args);
        ensureSettingsPage();
        renameDeleteAction();
        syncSettingsButtons();
        return result;
      };
    }

    document.addEventListener("click", event => {
      const navButton = event.target.closest('[data-screen="settings"]');
      if (navButton) {
        event.preventDefault();
        event.stopImmediatePropagation();
        setCurrentScreen("settings");
        return;
      }

      if (event.target.closest('#screen-settings [data-theme-choice]')) {
        setTimeout(syncSettingsButtons, 0);
      }
    }, true);
  }, { once: true });
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
