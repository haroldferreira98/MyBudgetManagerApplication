from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old_globals = '''    let recognition = null;
    let voiceSessionActive = false;
    let voiceFinalTranscript = "";
    let voiceInterimTranscript = "";
    let voicePendingParsed = null;
    let voiceRestartTimer = null;'''
new_globals = '''    let recognition = null;
    let voiceSessionActive = false;
    let voiceFinalTranscript = "";
    let voiceInterimTranscript = "";
    let voicePendingParsed = null;
    let voiceRestartTimer = null;
    let voiceRecorder = null;
    let voiceStream = null;
    let voiceChunks = [];
    let voiceRecorderStopPromise = null;
    let voiceRecorderStopResolve = null;
    let voiceRecordedBlob = null;
    let voiceRecordingStartedAt = 0;
    let voiceTimerId = null;
    let voicePhase = "idle";
    let whisperTranscriberPromise = null;'''
if old_globals not in text:
    raise SystemExit('voice globals block not found')
text = text.replace(old_globals, new_globals, 1)

css = r'''

    /* LOCAL-WHISPER-VOICE-V1 */
    .voice-hud.recording .voice-mic { animation: voicePulse 1.15s ease-out infinite; }
    .voice-hud.transcribing .voice-bars span,
    .voice-hud.review .voice-bars span { animation: none !important; height: 8px !important; opacity: .35; }
    .voice-hud.transcribing .voice-mic { animation: none !important; opacity: .78; }
    .voice-hud.review .voice-mic { animation: none !important; background: var(--success-container); color: var(--success); }
'''
if 'LOCAL-WHISPER-VOICE-V1' not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)

pattern = re.compile(r'''    function voiceCombinedTranscript\(\) \{.*?\n    function exportJSON\(\) \{''', re.S)
replacement = r'''    function voiceCombinedTranscript() {
      return `${voiceFinalTranscript} ${voiceInterimTranscript}`.replace(/\s+/g, " ").trim();
    }

    function setVoiceHud(active, title = "Je vous écoute…", value = "") {
      const hud = document.getElementById("voiceHud");
      if (!hud) return;
      const fullText = value || voiceCombinedTranscript() || "Parlez naturellement.";
      document.getElementById("voiceHudTitle").textContent = title;
      const transcript = document.getElementById("voiceHudText");
      transcript.textContent = fullText;
      transcript.scrollTop = transcript.scrollHeight;
      hud.classList.toggle("active", !!active);
      hud.setAttribute("aria-hidden", active ? "false" : "true");
    }

    function setVoicePhase(phase) {
      voicePhase = phase;
      const hud = document.getElementById("voiceHud");
      if (!hud) return;
      hud.classList.remove("recording", "transcribing", "review");
      if (["recording", "transcribing", "review"].includes(phase)) hud.classList.add(phase);
      const validate = document.getElementById("voiceValidateBtn");
      if (!validate) return;
      const label = validate.querySelector("span:last-child");
      if (phase === "recording") {
        validate.disabled = false;
        if (label) label.textContent = "Valider";
      } else if (phase === "transcribing") {
        validate.disabled = true;
        if (label) label.textContent = "Transcription…";
      } else if (phase === "review") {
        validate.disabled = !voicePendingParsed?.ok;
        if (label) label.textContent = voicePendingParsed?.ok ? "Ajouter" : "Recommencer";
      } else {
        validate.disabled = true;
        if (label) label.textContent = "Valider";
      }
    }

    function updateVoiceCandidate() {
      const fullText = voiceCombinedTranscript();
      voicePendingParsed = fullText ? parseVoiceCommand(fullText) : null;
      const preview = document.getElementById("voiceHudPreview");
      const ready = !!voicePendingParsed?.ok;
      if (preview) {
        preview.classList.toggle("ready", ready);
        preview.textContent = ready ? voicePendingParsed.message : "";
      }
      if (voicePhase === "review") setVoicePhase("review");
    }

    function stopVoiceTimer() {
      if (voiceTimerId) clearInterval(voiceTimerId);
      voiceTimerId = null;
    }

    function voiceDurationLabel() {
      const seconds = Math.max(0, Math.floor((Date.now() - voiceRecordingStartedAt) / 1000));
      const mm = String(Math.floor(seconds / 60)).padStart(2, "0");
      const ss = String(seconds % 60).padStart(2, "0");
      return `${mm}:${ss}`;
    }

    function releaseVoiceStream() {
      try { voiceStream?.getTracks()?.forEach(track => track.stop()); } catch (_) {}
      voiceStream = null;
    }

    function recorderMimeType() {
      const candidates = ["audio/mp4", "audio/webm;codecs=opus", "audio/webm", "audio/ogg;codecs=opus"];
      return candidates.find(type => window.MediaRecorder?.isTypeSupported?.(type)) || "";
    }

    async function stopRecorderAndGetBlob() {
      stopVoiceTimer();
      if (!voiceRecorder) return voiceRecordedBlob;
      if (voiceRecorder.state === "inactive") {
        releaseVoiceStream();
        return voiceRecordedBlob;
      }
      if (!voiceRecorderStopPromise) {
        voiceRecorderStopPromise = new Promise(resolve => { voiceRecorderStopResolve = resolve; });
      }
      try { voiceRecorder.requestData?.(); } catch (_) {}
      try { voiceRecorder.stop(); } catch (_) {}
      const blob = await voiceRecorderStopPromise;
      releaseVoiceStream();
      return blob;
    }

    function cleanupVoiceRecorder() {
      stopVoiceTimer();
      try {
        if (voiceRecorder && voiceRecorder.state !== "inactive") voiceRecorder.stop();
      } catch (_) {}
      voiceRecorder = null;
      voiceRecorderStopPromise = null;
      voiceRecorderStopResolve = null;
      voiceChunks = [];
      voiceRecordedBlob = null;
      releaseVoiceStream();
    }

    async function decodeVoiceBlobTo16kMono(blob) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) throw new Error("AudioContext indisponible");
      const context = new AudioCtx();
      try {
        const buffer = await blob.arrayBuffer();
        const decoded = await context.decodeAudioData(buffer.slice(0));
        const channels = decoded.numberOfChannels;
        const mono = new Float32Array(decoded.length);
        for (let c = 0; c < channels; c += 1) {
          const data = decoded.getChannelData(c);
          for (let i = 0; i < data.length; i += 1) mono[i] += data[i] / channels;
        }
        if (decoded.sampleRate === 16000) return mono;
        const ratio = decoded.sampleRate / 16000;
        const outLength = Math.max(1, Math.round(mono.length / ratio));
        const out = new Float32Array(outLength);
        for (let i = 0; i < outLength; i += 1) {
          const sourcePos = i * ratio;
          const left = Math.floor(sourcePos);
          const right = Math.min(mono.length - 1, left + 1);
          const mix = sourcePos - left;
          out[i] = mono[left] * (1 - mix) + mono[right] * mix;
        }
        return out;
      } finally {
        try { await context.close(); } catch (_) {}
      }
    }

    async function getLocalWhisperTranscriber() {
      if (!whisperTranscriberPromise) {
        whisperTranscriberPromise = (async () => {
          setVoiceHud(true, "Préparation du modèle local…", "Premier chargement uniquement. Le modèle sera ensuite mis en cache sur cet appareil.");
          const { pipeline, env } = await import("https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1");
          env.allowLocalModels = false;
          return pipeline(
            "automatic-speech-recognition",
            "onnx-community/whisper-tiny",
            {
              device: "wasm",
              dtype: "q8",
              progress_callback: progress => {
                if (voicePhase !== "transcribing") return;
                let pct = null;
                if (typeof progress?.progress === "number") pct = progress.progress;
                else if (progress?.loaded && progress?.total) pct = (progress.loaded / progress.total) * 100;
                const suffix = pct == null ? "" : ` · ${Math.max(0, Math.min(100, pct)).toFixed(0)} %`;
                setVoiceHud(true, "Préparation du modèle local…", `Téléchargement et mise en cache${suffix}`);
              }
            }
          );
        })().catch(error => {
          whisperTranscriberPromise = null;
          throw error;
        });
      }
      return whisperTranscriberPromise;
    }

    async function transcribeVoiceBlob(blob) {
      const audio = await decodeVoiceBlobTo16kMono(blob);
      const transcriber = await getLocalWhisperTranscriber();
      const output = await transcriber(audio, { language: "french", task: "transcribe" });
      return String(output?.text || "").trim();
    }

    async function startVoiceRecognition(options = {}) {
      if (voiceSessionActive || voicePhase === "transcribing") {
        setVoiceHud(true, voicePhase === "transcribing" ? "Transcription locale…" : "Je vous écoute…");
        return;
      }
      if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) {
        showSnackbar("L’enregistrement audio n’est pas disponible dans ce navigateur.");
        return;
      }
      cleanupVoiceRecorder();
      voiceFinalTranscript = "";
      voiceInterimTranscript = "";
      voicePendingParsed = null;
      updateVoiceCandidate();
      try {
        voiceStream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } });
        const mimeType = recorderMimeType();
        voiceChunks = [];
        voiceRecorderStopPromise = new Promise(resolve => { voiceRecorderStopResolve = resolve; });
        voiceRecorder = mimeType ? new MediaRecorder(voiceStream, { mimeType }) : new MediaRecorder(voiceStream);
        voiceRecorder.ondataavailable = event => { if (event.data && event.data.size > 0) voiceChunks.push(event.data); };
        voiceRecorder.onerror = event => { console.error("MediaRecorder", event.error || event); };
        voiceRecorder.onstop = () => {
          const type = voiceRecorder?.mimeType || mimeType || "audio/mp4";
          voiceRecordedBlob = new Blob(voiceChunks, { type });
          const resolve = voiceRecorderStopResolve;
          voiceRecorderStopResolve = null;
          resolve?.(voiceRecordedBlob);
        };
        voiceSessionActive = true;
        voiceRecordingStartedAt = Date.now();
        voiceRecorder.start(250);
        setVoicePhase("recording");
        setVoiceHud(true, "Je vous écoute…", `Enregistrement local · ${voiceDurationLabel()}`);
        voiceTimerId = setInterval(() => {
          if (voicePhase === "recording") setVoiceHud(true, "Je vous écoute…", `Enregistrement local · ${voiceDurationLabel()}`);
        }, 500);
      } catch (error) {
        console.error("Microphone", error);
        cleanupVoiceRecorder();
        voiceSessionActive = false;
        voicePhase = "idle";
        setVoiceHud(false);
        showSnackbar("Impossible d’accéder au microphone.");
      }
    }

    async function cancelVoiceRecognition() {
      voiceSessionActive = false;
      stopVoiceTimer();
      try { if (voiceRecorder && voiceRecorder.state !== "inactive") voiceRecorder.stop(); } catch (_) {}
      releaseVoiceStream();
      cleanupVoiceRecorder();
      voiceFinalTranscript = "";
      voiceInterimTranscript = "";
      voicePendingParsed = null;
      setVoicePhase("idle");
      setVoiceHud(false);
    }

    async function validateVoiceRecognition() {
      if (voicePhase === "recording") {
        voiceSessionActive = false;
        setVoicePhase("transcribing");
        setVoiceHud(true, "Transcription locale…", "Traitement sur votre iPhone, sans API payante.");
        try {
          const blob = await stopRecorderAndGetBlob();
          if (!blob || blob.size < 100) throw new Error("Enregistrement vide");
          const transcript = await transcribeVoiceBlob(blob);
          voiceFinalTranscript = transcript;
          voiceInterimTranscript = "";
          updateVoiceCandidate();
          setVoicePhase("review");
          setVoiceHud(true, transcript ? "Vérifiez la transcription" : "Aucune parole détectée", transcript || "Annulez puis recommencez.");
        } catch (error) {
          console.error("Transcription locale", error);
          voiceFinalTranscript = "";
          voicePendingParsed = null;
          setVoicePhase("review");
          setVoiceHud(true, "Transcription impossible", "Annulez puis réessayez. Le premier chargement du modèle nécessite Internet.");
        } finally {
          releaseVoiceStream();
          voiceRecorder = null;
        }
        return;
      }
      if (voicePhase === "review") {
        if (!voicePendingParsed?.ok) {
          await cancelVoiceRecognition();
          await startVoiceRecognition({ source: "retry" });
          return;
        }
        const collection = collectionForType(voicePendingParsed.type);
        if (!collection) return;
        const parsed = voicePendingParsed;
        state[collection].push(parsed.item);
        saveState(parsed.message);
        await cancelVoiceRecognition();
      }
    }

    function exportJSON() {'''
text, count = pattern.subn(lambda m: replacement, text, count=1)
if count != 1:
    raise SystemExit(f'voice block replacement failed: {count}')

text = text.replace(
    '<button class="voice-action-btn validate" id="voiceValidateBtn" type="button" disabled><span class="material-symbols-outlined">check</span>Valider</button>',
    '<button class="voice-action-btn validate" id="voiceValidateBtn" type="button" disabled><span class="material-symbols-outlined">check</span><span>Valider</span></button>',
    1
)

p.write_text(text, encoding='utf-8')
