from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

css = r'''

    /* PERSISTENT-VOICE-COMPOSER-V2 */
    .voice-hud {
      bottom: calc(var(--nav-height) + max(8px, var(--safe-bottom)) + 12px) !important;
      width: min(calc(100% - 20px), 560px) !important;
    }
    .voice-hud-card {
      grid-template-columns: 48px minmax(0, 1fr) auto !important;
      align-items: start !important;
      gap: 10px 12px !important;
      padding: 13px !important;
      border-radius: 26px !important;
    }
    .voice-mic { width: 48px !important; height: 48px !important; }
    .voice-copy { min-width: 0; padding-top: 1px; }
    .voice-title { font-size: 14px; line-height: 1.25; }
    .voice-transcript {
      margin-top: 5px !important;
      color: var(--on-surface) !important;
      font-size: 13px !important;
      line-height: 1.4 !important;
      white-space: normal !important;
      overflow: visible !important;
      text-overflow: clip !important;
      overflow-wrap: anywhere !important;
      max-height: 112px;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch;
    }
    .voice-preview {
      display: none;
      margin-top: 8px;
      padding: 8px 10px;
      border-radius: 14px;
      background: var(--surface-container-lowest);
      color: var(--on-surface-variant);
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }
    .voice-preview.ready { display: block; }
    .voice-bars { align-self: center; }
    .voice-actions {
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: 1fr 1.25fr;
      gap: 8px;
      width: 100%;
    }
    .voice-action-btn {
      min-height: 42px;
      border-radius: var(--pill);
      border: 0;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      padding: 8px 12px;
      font-weight: 700;
      cursor: pointer;
    }
    .voice-action-btn.cancel { background: var(--surface-container-highest); color: var(--on-surface); }
    .voice-action-btn.validate { background: var(--primary); color: var(--on-primary); }
    .voice-action-btn:disabled { opacity: .42; cursor: default; }
    .voice-action-btn .material-symbols-outlined { font-size: 20px; }
'''
if 'PERSISTENT-VOICE-COMPOSER-V2' not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)

old_hud = '''  <div class="voice-hud" id="voiceHud" role="status" aria-live="polite" aria-hidden="true">
    <div class="voice-hud-card">
      <div class="voice-mic"><span class="material-symbols-outlined">mic</span></div>
      <div class="voice-copy">
        <div class="voice-title" id="voiceHudTitle">Je vous écoute…</div>
        <div class="voice-transcript" id="voiceHudText">Parlez naturellement, par exemple « 25 € d’alimentation chez Auchan aujourd’hui ».</div>
      </div>
      <div class="voice-bars" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div>
      <button class="voice-cancel-btn" id="voiceCancelBtn" type="button" aria-label="Annuler la saisie vocale"><span class="material-symbols-outlined">close</span></button>
    </div>
  </div>'''
new_hud = '''  <div class="voice-hud" id="voiceHud" role="status" aria-live="polite" aria-hidden="true">
    <div class="voice-hud-card">
      <div class="voice-mic"><span class="material-symbols-outlined">mic</span></div>
      <div class="voice-copy">
        <div class="voice-title" id="voiceHudTitle">Je vous écoute…</div>
        <div class="voice-transcript" id="voiceHudText">Parlez naturellement. Votre phrase complète restera affichée ici.</div>
        <div class="voice-preview" id="voiceHudPreview"></div>
      </div>
      <div class="voice-bars" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div>
      <div class="voice-actions">
        <button class="voice-action-btn cancel" id="voiceCancelBtn" type="button"><span class="material-symbols-outlined">close</span>Annuler</button>
        <button class="voice-action-btn validate" id="voiceValidateBtn" type="button" disabled><span class="material-symbols-outlined">check</span>Valider</button>
      </div>
    </div>
  </div>'''
if old_hud not in text:
    raise SystemExit('voice HUD block not found')
text = text.replace(old_hud, new_hud, 1)

globals_old = '''    let snackbarTimer = null;
    let recognition = null;
    let cloud = null;'''
globals_new = '''    let snackbarTimer = null;
    let recognition = null;
    let voiceSessionActive = false;
    let voiceFinalTranscript = "";
    let voiceInterimTranscript = "";
    let voicePendingParsed = null;
    let voiceRestartTimer = null;
    let cloud = null;'''
if globals_old not in text:
    raise SystemExit('voice globals insertion point not found')
text = text.replace(globals_old, globals_new, 1)

voice_pattern = re.compile(r'''    function setVoiceHud\(active, title = "Je vous écoute…", text = "Parlez naturellement"\) \{.*?\n    \}\n\n    function exportJSON\(\) \{''', re.S)
voice_replacement = r'''    function voiceCombinedTranscript() {
      return `${voiceFinalTranscript} ${voiceInterimTranscript}`.replace(/\s+/g, " ").trim();
    }

    function setVoiceHud(active, title = "Je vous écoute…", value = "") {
      const hud = document.getElementById("voiceHud");
      if (!hud) return;
      const fullText = value || voiceCombinedTranscript() || "Parlez naturellement. Votre phrase complète restera affichée ici.";
      document.getElementById("voiceHudTitle").textContent = title;
      const transcript = document.getElementById("voiceHudText");
      transcript.textContent = fullText;
      transcript.scrollTop = transcript.scrollHeight;
      hud.classList.toggle("active", !!active);
      hud.setAttribute("aria-hidden", active ? "false" : "true");
    }

    function updateVoiceCandidate() {
      const fullText = voiceCombinedTranscript();
      voicePendingParsed = fullText ? parseVoiceCommand(fullText) : null;
      const preview = document.getElementById("voiceHudPreview");
      const validate = document.getElementById("voiceValidateBtn");
      const ready = !!voicePendingParsed?.ok;
      if (validate) validate.disabled = !ready;
      if (preview) {
        preview.classList.toggle("ready", ready);
        preview.textContent = ready ? voicePendingParsed.message : "";
      }
    }

    function clearVoiceRestartTimer() {
      if (voiceRestartTimer) clearTimeout(voiceRestartTimer);
      voiceRestartTimer = null;
    }

    function finishVoiceSession({ hide = true } = {}) {
      voiceSessionActive = false;
      clearVoiceRestartTimer();
      const activeRecognition = recognition;
      recognition = null;
      try { activeRecognition?.abort(); } catch (_) {}
      document.getElementById("micBtn")?.classList.remove("listening");
      if (hide) setVoiceHud(false);
    }

    function cancelVoiceRecognition() {
      finishVoiceSession({ hide: true });
      voiceFinalTranscript = "";
      voiceInterimTranscript = "";
      voicePendingParsed = null;
      updateVoiceCandidate();
    }

    function validateVoiceRecognition() {
      const fullText = voiceCombinedTranscript();
      const parsed = fullText ? parseVoiceCommand(fullText) : null;
      if (!parsed?.ok) {
        updateVoiceCandidate();
        return;
      }
      const collection = collectionForType(parsed.type);
      if (!collection) return;
      finishVoiceSession({ hide: true });
      state[collection].push(parsed.item);
      saveState(parsed.message);
      voiceFinalTranscript = "";
      voiceInterimTranscript = "";
      voicePendingParsed = null;
      updateVoiceCandidate();
    }

    function startRecognitionCycle(SpeechRecognition) {
      if (!voiceSessionActive || recognition) return;
      clearVoiceRestartTimer();
      const cycle = new SpeechRecognition();
      recognition = cycle;
      cycle.lang = "fr-FR";
      cycle.interimResults = true;
      cycle.continuous = true;
      cycle.maxAlternatives = 1;

      cycle.onstart = () => {
        if (!voiceSessionActive || recognition !== cycle) return;
        document.getElementById("micBtn")?.classList.add("listening");
        setVoiceHud(true, "Je vous écoute…");
      };

      cycle.onresult = event => {
        if (!voiceSessionActive || recognition !== cycle) return;
        let interim = "";
        for (let i = event.resultIndex; i < event.results.length; i += 1) {
          const chunk = String(event.results[i]?.[0]?.transcript || "").trim();
          if (!chunk) continue;
          if (event.results[i].isFinal) {
            voiceFinalTranscript = `${voiceFinalTranscript} ${chunk}`.replace(/\s+/g, " ").trim();
          } else {
            interim += `${interim ? " " : ""}${chunk}`;
          }
        }
        voiceInterimTranscript = interim.trim();
        setVoiceHud(true, "Je vous écoute…");
        updateVoiceCandidate();
      };

      cycle.onerror = event => {
        if (!voiceSessionActive || recognition !== cycle) return;
        if (event.error === "not-allowed" || event.error === "service-not-allowed") {
          voiceSessionActive = false;
          clearVoiceRestartTimer();
          recognition = null;
          document.getElementById("micBtn")?.classList.remove("listening");
          setVoiceHud(true, "Accès au micro requis", voiceCombinedTranscript() || "Autorisez le micro dans Safari pour continuer.");
          return;
        }
        setVoiceHud(true, "Je vous écoute…");
      };

      cycle.onend = () => {
        if (recognition === cycle) recognition = null;
        document.getElementById("micBtn")?.classList.remove("listening");
        if (!voiceSessionActive) return;
        if (voiceInterimTranscript) {
          voiceFinalTranscript = `${voiceFinalTranscript} ${voiceInterimTranscript}`.replace(/\s+/g, " ").trim();
          voiceInterimTranscript = "";
          setVoiceHud(true, "Je vous écoute…");
          updateVoiceCandidate();
        }
        voiceRestartTimer = setTimeout(() => {
          voiceRestartTimer = null;
          if (voiceSessionActive && !recognition) startRecognitionCycle(SpeechRecognition);
        }, 180);
      };

      try {
        cycle.start();
      } catch (error) {
        if (recognition === cycle) recognition = null;
        if (!voiceSessionActive) return;
        console.warn("Redémarrage de la reconnaissance vocale", error);
        voiceRestartTimer = setTimeout(() => {
          voiceRestartTimer = null;
          if (voiceSessionActive && !recognition) startRecognitionCycle(SpeechRecognition);
        }, 450);
      }
    }

    function startVoiceRecognition(options = {}) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        setVoiceHud(false);
        showSnackbar("La reconnaissance vocale n’est pas disponible dans ce navigateur.");
        return;
      }
      if (voiceSessionActive) {
        setVoiceHud(true, "Je vous écoute…");
        return;
      }
      try { recognition?.abort(); } catch (_) {}
      recognition = null;
      clearVoiceRestartTimer();
      voiceSessionActive = true;
      voiceFinalTranscript = "";
      voiceInterimTranscript = "";
      voicePendingParsed = null;
      updateVoiceCandidate();
      setVoiceHud(true, "Je vous écoute…", "Parlez naturellement. Le micro restera actif jusqu’à Valider ou Annuler.");
      startRecognitionCycle(SpeechRecognition);
    }

    function exportJSON() {'''
text, count = voice_pattern.subn(voice_replacement, text, count=1)
if count != 1:
    raise SystemExit(f'voice function block replacement failed: {count}')

old_listener = '''    document.getElementById("entityForm").addEventListener("submit", handleEntitySubmit);
    document.getElementById("voiceCancelBtn")?.addEventListener("click", event => { event.preventDefault(); event.stopPropagation(); cancelVoiceRecognition(); });'''
new_listener = '''    document.getElementById("entityForm").addEventListener("submit", handleEntitySubmit);
    document.getElementById("voiceCancelBtn")?.addEventListener("click", event => { event.preventDefault(); event.stopPropagation(); cancelVoiceRecognition(); });
    document.getElementById("voiceValidateBtn")?.addEventListener("click", event => { event.preventDefault(); event.stopPropagation(); validateVoiceRecognition(); });'''
if old_listener not in text:
    raise SystemExit('voice listener block not found')
text = text.replace(old_listener, new_listener, 1)

p.write_text(text, encoding='utf-8')
