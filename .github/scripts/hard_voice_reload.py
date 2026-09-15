from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")
old = '      const reloadAfterVoiceSave = () => setTimeout(() => window.location.reload(), 180);'
new = '''      const reloadAfterVoiceSave = () => setTimeout(() => {
        // JavaScript cannot trigger Safari's exact Cmd+Shift+R command.
        // A unique navigation URL gives us a fresh document and voice context.
        const url = new URL(window.location.href);
        url.searchParams.set("__voice_hard_reload", Date.now().toString());
        window.location.replace(url.toString());
      }, 220);'''
if old not in text:
    raise SystemExit("reloadAfterVoiceSave target not found")
text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8")
