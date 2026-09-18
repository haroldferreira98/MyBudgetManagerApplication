from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-reimbursement-profile-tracking-v2" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

old_account = '      const account = event.target.closest("#accountBtn");\n      if (account) { renderProfile(); renderAccountModal(); openModal("accountModal"); return; }'
new_account = '      const account = event.target.closest("#accountBtn");\n      if (account) { checkForAppUpdate(); renderProfile(); renderAccountModal(); openModal("accountModal"); return; }'
if text.count(old_account) != 1:
    raise SystemExit(f'account handler anchor count={text.count(old_account)}')
text = text.replace(old_account, new_account, 1)

old_refresh = '''    // APP-AUTO-REFRESH-V1
    const APP_BUILD = document.querySelector('meta[name="app-build"]')?.content || "";
    let appUpdateCheckInFlight = false;
    async function checkForAppUpdate() {
      if (appUpdateCheckInFlight || !navigator.onLine) return;
      appUpdateCheckInFlight = true;
      try {
        const response = await fetch(`/index.html?app-update=${Date.now()}`, { cache: "no-store", headers: { "Cache-Control": "no-cache" } });
        if (!response.ok) return;
        const html = await response.text();
        const match = html.match(/<meta name="app-build" content="([^"]+)"/);
        if (match?.[1] && APP_BUILD && match[1] !== APP_BUILD) window.location.reload();
      } catch (_) {
      } finally {
        appUpdateCheckInFlight = false;
      }
    }
    window.addEventListener("focus", checkForAppUpdate);
    document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") checkForAppUpdate(); });

    renderAll();
    initCloudSync();
    setTimeout(checkForAppUpdate, 1200);'''

new_refresh = '''    // APP-AUTO-REFRESH-V2
    const APP_BUILD = document.querySelector('meta[name="app-build"]')?.content || "";
    let appUpdateCheckInFlight = false;
    async function checkForAppUpdate() {
      if (appUpdateCheckInFlight || !navigator.onLine) return;
      appUpdateCheckInFlight = true;
      try {
        const response = await fetch(`/index.html?app-update=${Date.now()}`, { cache: "no-store", headers: { "Cache-Control": "no-cache" } });
        if (!response.ok) return;
        const html = await response.text();
        const match = html.match(/<meta name="app-build" content="([^"]+)"/);
        if (match?.[1] && APP_BUILD && match[1] !== APP_BUILD) {
          window.location.reload();
          return;
        }
      } catch (_) {
      } finally {
        appUpdateCheckInFlight = false;
      }
    }
    window.addEventListener("focus", checkForAppUpdate);
    window.addEventListener("pageshow", checkForAppUpdate);
    document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") checkForAppUpdate(); });

    renderAll();
    initCloudSync();
    setTimeout(checkForAppUpdate, 1200);
    setInterval(() => { if (document.visibilityState === "visible") checkForAppUpdate(); }, 30000);'''

if text.count(old_refresh) != 1:
    raise SystemExit(f'auto refresh anchor count={text.count(old_refresh)}')
text = text.replace(old_refresh, new_refresh, 1)

path.write_text(text, encoding='utf-8')
