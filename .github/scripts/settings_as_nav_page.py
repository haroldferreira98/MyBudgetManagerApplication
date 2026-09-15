from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the settings icon from the top bar.
old_top = '''      <div class="top-actions">\n        <button class="icon-btn" id="settingsBtn" type="button" aria-label="Paramètres" title="Paramètres">\n          <span class="material-symbols-outlined">settings</span>\n        </button>\n      </div>'''
if old_top not in s:
    raise SystemExit('top settings button not found')
s = s.replace(old_top, '', 1)

# Add a real Settings screen beside Profile.
old_screens = '''      <section class="screen" id="screen-expenses" data-title="Dépenses"></section>\n      <section class="screen" id="screen-profile" data-title="Profil & patrimoine"></section>'''
new_screens = '''      <section class="screen" id="screen-expenses" data-title="Dépenses"></section>\n      <section class="screen" id="screen-profile" data-title="Profil & patrimoine"></section>\n      <section class="screen" id="screen-settings" data-title="Paramètres"></section>'''
if old_screens not in s:
    raise SystemExit('screen block not found')
s = s.replace(old_screens, new_screens, 1)

# Add Settings as the fifth item in bottom navigation, on the far right.
old_nav = '''      <button class="nav-btn" data-screen="profile" aria-label="Profil">\n        <span class="material-symbols-outlined">person</span><span>Profil</span>\n      </button>'''
new_nav = '''      <button class="nav-btn" data-screen="profile" aria-label="Profil">\n        <span class="material-symbols-outlined">person</span><span>Profil</span>\n      </button>\n      <button class="nav-btn" data-screen="settings" aria-label="Paramètres">\n        <span class="material-symbols-outlined">settings</span><span>Paramètres</span>\n      </button>'''
if old_nav not in s:
    raise SystemExit('profile nav button not found')
s = s.replace(old_nav, new_nav, 1)

# Bottom nav now has five equal destinations.
s = s.replace('grid-template-columns: repeat(4, minmax(0, 1fr));', 'grid-template-columns: repeat(5, minmax(0, 1fr));')

# Render Settings as a normal page, not a sheet.
anchor = '''    function renderAll() {\n      applyTheme();\n      renderHome();\n      renderIncome();\n      renderExpenses();\n      renderProfile();'''
insert = '''    function renderSettings() {\n      const container = document.getElementById("screen-settings");\n      if (!container) return;\n      const selected = state.settings.theme || "auto";\n      container.innerHTML = `\n        <div class="section" style="margin-top:8px">\n          <div class="section-header">\n            <div>\n              <h2 class="section-title">Apparence</h2>\n              <p class="section-subtitle">Le mode Automatique suit le thème de l’iPhone.</p>\n            </div>\n          </div>\n          <div class="card">\n            <div class="segmented" id="settingsThemeSegmentPage">\n              <button data-theme-choice="light" class="${selected === "light" ? "active" : ""}">Clair</button>\n              <button data-theme-choice="dark" class="${selected === "dark" ? "active" : ""}">Sombre</button>\n              <button data-theme-choice="auto" class="${selected === "auto" ? "active" : ""}">Automatique</button>\n            </div>\n          </div>\n        </div>`;\n    }\n\n    function renderAll() {\n      applyTheme();\n      renderHome();\n      renderIncome();\n      renderExpenses();\n      renderProfile();\n      renderSettings();'''
if anchor not in s:
    raise SystemExit('renderAll anchor not found')
s = s.replace(anchor, insert, 1)

# Allow Settings as a normal current screen.
s = s.replace('["home", "income", "expenses", "profile"].includes(screen)', '["home", "income", "expenses", "profile", "settings"].includes(screen)', 1)

# Theme buttons live on the page now; keep the active state in sync globally.
old_update = '''    function updateSettingsUI() {\n      document.querySelectorAll('#settingsModal [data-theme-choice]').forEach(btn => {\n        btn.classList.toggle("active", btn.dataset.themeChoice === (state.settings.theme || "auto"));\n      });\n    }'''
new_update = '''    function updateSettingsUI() {\n      document.querySelectorAll('[data-theme-choice]').forEach(btn => {\n        btn.classList.toggle("active", btn.dataset.themeChoice === (state.settings.theme || "auto"));\n      });\n    }'''
if old_update not in s:
    raise SystemExit('updateSettingsUI not found')
s = s.replace(old_update, new_update, 1)

# When appearance changes, re-render the Settings page as well.
old_theme = '''      if (theme) {\n        state.settings.theme = theme.dataset.themeChoice;\n        saveState("Apparence mise à jour.");\n      }'''
new_theme = '''      if (theme) {\n        state.settings.theme = theme.dataset.themeChoice;\n        saveState("Apparence mise à jour.");\n        renderSettings();\n      }'''
if old_theme not in s:
    raise SystemExit('theme handler not found')
s = s.replace(old_theme, new_theme, 1)

# Remove obsolete top-button behavior. The old sheet may remain in markup but is no longer reachable.
old_settings_click = '''      const settings = event.target.closest("#settingsBtn");\n      if (settings) { updateSettingsUI(); openModal("settingsModal"); return; }\n\n'''
if old_settings_click in s:
    s = s.replace(old_settings_click, '', 1)

# Rename destructive action as requested.
s = s.replace('Tout supprimer du cloud', 'Supprimer toutes les opérations')

# Checks.
for required in ['id="screen-settings"', 'data-screen="settings"', 'Supprimer toutes les opérations', 'renderSettings();']:
    if required not in s:
        raise SystemExit(f'missing {required}')
if 'id="settingsBtn"' in s:
    raise SystemExit('top settings button still present')

p.write_text(s, encoding='utf-8')
