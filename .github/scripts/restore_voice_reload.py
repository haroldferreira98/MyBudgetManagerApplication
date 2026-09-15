from pathlib import Path
import subprocess

repo_file = Path("index.html")
old = subprocess.check_output(
    ["git", "show", "d5ce8ab729f56839bc3596a29dc0271cc36ea8bf:index.html"],
    text=True,
)

start = old.find('    function validateVoiceRecognition() {')
if start < 0:
    raise SystemExit('validateVoiceRecognition not found in restored version')
end = old.find('\n    function startRecognitionCycle(', start)
if end < 0:
    raise SystemExit('end of validateVoiceRecognition not found')

block = old[start:end]
target = '      saveState(parsed.message);'
if target not in block:
    raise SystemExit('saveState(parsed.message) not found in validateVoiceRecognition')

replacement = '''      saveState(parsed.message);

      // iOS/WebKit can leave SpeechRecognition unusable after the first session.
      // Persist Firebase first, then reload the page so the next voice operation
      // starts with a fresh browser speech-recognition context.
      const reloadAfterVoiceSave = () => setTimeout(() => window.location.reload(), 180);
      if (cloud && cloudUser) {
        clearTimeout(cloudSaveTimer);
        writeCloudState()
          .then(reloadAfterVoiceSave)
          .catch(error => {
            console.error("Synchronisation avant rechargement impossible", error);
            showSnackbar("Dépense enregistrée localement · recharge manuelle nécessaire.");
          });
      } else {
        reloadAfterVoiceSave();
      }'''

block = block.replace(target, replacement, 1)
old = old[:start] + block + old[end:]
repo_file.write_text(old, encoding="utf-8")
