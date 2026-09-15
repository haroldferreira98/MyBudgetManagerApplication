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
