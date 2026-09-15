from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# 1. Remove only the voice overlay markup.
hud_start = text.find('  <div class="voice-hud" id="voiceHud"')
if hud_start >= 0:
    hud_end_marker = '\n  <div class="sheet-backdrop" id="entityModal"'
    hud_end = text.find(hud_end_marker, hud_start)
    if hud_end < 0:
        raise SystemExit('Could not locate end of voice HUD')
    text = text[:hud_start] + text[hud_end:]

# 2. Remove voice-only runtime globals, preserving all cloud/Firebase state.
voice_globals = '''    let recognition = null;\n    let voiceSessionActive = false;\n    let voiceFinalTranscript = "";\n    let voiceInterimTranscript = "";\n    let voicePendingParsed = null;\n    let voiceRestartTimer = null;\n    let voiceStartWatchdog = null;\n    let voiceLastReleaseAt = 0;\n    let voiceCycleSerial = 0;\n'''
text = text.replace(voice_globals, '', 1)

# 3. Remove voice-specific CSS only.
text = text.replace('    .mic-btn.listening { background: var(--error-container); color: var(--error); animation: pulse 1s infinite; }\n    @keyframes pulse { 50% { transform: scale(.92); } }\n', '', 1)
base_voice_start = text.find('    .voice-hud {')
base_voice_end = text.find('    /* SEARCH-BG-LOWER-PILL-V3 */', base_voice_start)
if base_voice_start >= 0 and base_voice_end >= 0:
    text = text[:base_voice_start] + text[base_voice_end:]
text = re.sub(r'\n\s*/\* VOICE-CANCEL-SILENT-V1 \*/\n\s*\.voice-hud-card\{.*?\}\n', '\n', text, count=1)
persistent_start = text.find('    /* PERSISTENT-VOICE-COMPOSER-V2 */')
if persistent_start >= 0:
    disabled = text.find('    /* VOICE-DISABLED-SAFELY */', persistent_start)
    if disabled >= 0:
        disabled_end = text.find('\n', text.find('#voiceHud', disabled))
        if disabled_end < 0:
            disabled_end = text.find('</style>', disabled)
        else:
            disabled_end += 1
        text = text[:persistent_start] + text[disabled_end:]
    else:
        style_end = text.find('</style>', persistent_start)
        if style_end < 0:
            raise SystemExit('Could not locate end of persistent voice CSS')
        text = text[:persistent_start] + text[style_end:]

# 4. Remove microphone from the expense search UI and its listener.
text = text.replace('            <button class="icon-btn mic-btn" id="micBtn" type="button" aria-label="Saisie vocale"><span class="material-symbols-outlined">mic</span></button>\n', '', 1)
text = text.replace('      const micBtn = document.getElementById("micBtn");\n      if (micBtn) micBtn.addEventListener("click", startVoiceRecognition);\n', '', 1)

# 5. Remove voice parser/engine only. In this version it is a contiguous block
#    immediately after credit simulation and immediately before exportJSON.
voice_js_start = text.find('    function normalizeVoice(text) {')
voice_js_end = text.find('    function exportJSON() {', voice_js_start)
if voice_js_start >= 0:
    if voice_js_end < 0:
        raise SystemExit('Could not locate exact end of voice JS block')
    text = text[:voice_js_start] + text[voice_js_end:]

# 6. Remove stale voice action listeners.
text = re.sub(r'\n\s*document\.getElementById\("voiceCancelBtn"\).*?;\n', '\n', text, count=1)
text = re.sub(r'\n\s*document\.getElementById\("voiceValidateBtn"\).*?;\n', '\n', text, count=1)

# 7. Make Firebase web config resilient even if the external config script is
#    temporarily stale/missed by an iOS home-screen web app cache.
text = text.replace('<script src="firebase-config.js"></script>', '<script src="firebase-config.js?v=20260915-profile-repair"></script>', 1)
main_script_marker = '  <script>\n    "use strict";'
fallback = '''  <script>\n    "use strict";\n\n    // Public Firebase Web configuration fallback. This is intentionally not a secret.\n    window.BUDGET_FIREBASE_CONFIG = window.BUDGET_FIREBASE_CONFIG || {\n      apiKey: "AIzaSyDsN9i87GGzx_v_Ci72yt-oDWN77S2Apak",\n      authDomain: "mybudgetmanagerapplication.firebaseapp.com",\n      projectId: "mybudgetmanagerapplication",\n      storageBucket: "mybudgetmanagerapplication.firebasestorage.app",\n      messagingSenderId: "83517729033",\n      appId: "1:83517729033:web:07144c82e6f6bab3984bd8",\n      measurementId: "G-YHNCYY4FYK"\n    };'''
if main_script_marker not in text:
    raise SystemExit('Main script marker not found')
text = text.replace(main_script_marker, fallback, 1)

# 8. Serialize Firebase initialization so tapping Google immediately after launch
#    waits for Firebase instead of incorrectly claiming it is not configured.
cloud_timer = '    let cloudSaveTimer = null;\n'
if cloud_timer in text and 'let cloudInitPromise = null;' not in text:
    text = text.replace(cloud_timer, cloud_timer + '    let cloudInitPromise = null;\n', 1)

init_start = text.find('    async function initCloudSync() {')
init_end = text.find('    function scheduleCloudSave() {', init_start)
if init_start < 0 or init_end < 0:
    raise SystemExit('Firebase init block not found')
new_init = '''    function initCloudSync() {\n      if (cloud) return Promise.resolve(cloud);\n      if (cloudInitPromise) return cloudInitPromise;\n      if (!isFirebaseConfigured()) {\n        renderProfile();\n        return Promise.resolve(null);\n      }\n\n      cloudInitPromise = (async () => {\n        try {\n          const [appMod, authMod, storeMod] = await Promise.all([\n            import("https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js"),\n            import("https://www.gstatic.com/firebasejs/12.19.0/firebase-auth.js"),\n            import("https://www.gstatic.com/firebasejs/12.19.0/firebase-firestore.js")\n          ]);\n          const app = appMod.initializeApp(window.BUDGET_FIREBASE_CONFIG);\n          const auth = authMod.getAuth(app);\n          const db = storeMod.getFirestore(app);\n          const provider = new authMod.GoogleAuthProvider();\n          cloud = { auth, db, provider, authMod, storeMod };\n\n          authMod.onAuthStateChanged(auth, async user => {\n            cloudUser = user || null;\n            renderProfile();\n            updateTopAccountButton();\n            renderAccountModal();\n            if (cloudUser) await reconcileCloudState();\n          });\n          return cloud;\n        } catch (error) {\n          console.error("Initialisation Firebase impossible", error);\n          showSnackbar("Connexion cloud indisponible pour le moment.");\n          return null;\n        } finally {\n          cloudInitPromise = null;\n        }\n      })();\n\n      return cloudInitPromise;\n    }\n\n'''
text = text[:init_start] + new_init + text[init_end:]

old_signin = '''    async function signInWithGoogle() {\n      if (!cloud) {\n        showSnackbar("Firebase doit d'abord être configuré.");\n        return;\n      }\n      try {\n        await cloud.authMod.signInWithPopup(cloud.auth, cloud.provider);\n      } catch (error) {\n        console.error("Connexion Google impossible", error);\n        showSnackbar(firebaseAuthErrorMessage(error));\n      }\n    }'''
new_signin = '''    async function signInWithGoogle() {\n      const readyCloud = cloud || await initCloudSync();\n      if (!readyCloud) {\n        showSnackbar("Connexion Google indisponible pour le moment.");\n        return;\n      }\n      try {\n        await readyCloud.authMod.signInWithPopup(readyCloud.auth, readyCloud.provider);\n      } catch (error) {\n        console.error("Connexion Google impossible", error);\n        showSnackbar(firebaseAuthErrorMessage(error));\n      }\n    }'''
if old_signin not in text:
    raise SystemExit('Google sign-in block not found')
text = text.replace(old_signin, new_signin, 1)

# Safety checks: these are the exact areas that were accidentally removed before.
required = [
    'function renderProfile()',
    'Enveloppes mensuelles',
    'Mes crédits',
    "Projets d'épargne",
    'Sauvegarde & données',
    'function initCloudSync()',
    'function reconcileCloudState()',
    'function signInWithGoogle()',
    'firebase-config.js?v=20260915-profile-repair',
]
for token in required:
    if token not in text:
        raise SystemExit(f'Critical feature missing after patch: {token}')

for forbidden in ['startVoiceRecognition', 'voiceHud', 'voiceCancelBtn', 'voiceValidateBtn', 'id="micBtn"', 'webkitSpeechRecognition']:
    if forbidden in text:
        raise SystemExit(f'Voice residue still present: {forbidden}')

p.write_text(text, encoding='utf-8')
