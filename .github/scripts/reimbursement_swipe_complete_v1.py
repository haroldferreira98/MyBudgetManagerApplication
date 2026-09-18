from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Build marker.
text, count = re.subn(
    r'<meta name="app-build" content="[^"]+"\s*/>',
    '<meta name="app-build" content="20260918-reimbursement-swipe-complete-v1" />',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('app build marker not found')

# Persist a manual completion state independently from reimbursement percentage.
old_normalized = '''      return {
        tracked: raw.tracked === true,
        socialSecurity: { amount: Math.max(0, safeNumber(ss.amount)), date: String(ss.date || "") },
        mutual: { amount: Math.max(0, safeNumber(mutual.amount)), date: String(mutual.date || "") }
      };'''
new_normalized = '''      return {
        tracked: raw.tracked === true,
        completed: raw.completed === true,
        completedAt: String(raw.completedAt || ""),
        socialSecurity: { amount: Math.max(0, safeNumber(ss.amount)), date: String(ss.date || "") },
        mutual: { amount: Math.max(0, safeNumber(mutual.amount)), date: String(mutual.date || "") }
      };'''
if text.count(old_normalized) != 1:
    raise SystemExit(f'normalize anchor count={text.count(old_normalized)}')
text = text.replace(old_normalized, new_normalized, 1)

# Keep completion state when the health expense is edited.
old_submit = '''        if(mutual>0&&!mutualDate){showSnackbar("Ajoute la date du remboursement mutuelle.");form.querySelector('[name="healthMutualDate"]')?.focus();return;}
        item={ id:id||uid("exp"), label:String(fd.get("label")||"").trim(), amount:moneyInputValue(form,"amount"), date:fd.get("date")||todayISO(), category, bucket:"wants", healthReimbursement:{ tracked, socialSecurity:{amount:ss,date:ss>0?ssDate:""}, mutual:{amount:mutual,date:mutual>0?mutualDate:""} } };'''
new_submit = '''        if(mutual>0&&!mutualDate){showSnackbar("Ajoute la date du remboursement mutuelle.");form.querySelector('[name="healthMutualDate"]')?.focus();return;}
        const previousHealth=normalizeHealthReimbursement(current?.healthReimbursement);
        item={ id:id||uid("exp"), label:String(fd.get("label")||"").trim(), amount:moneyInputValue(form,"amount"), date:fd.get("date")||todayISO(), category, bucket:"wants", healthReimbursement:{ tracked, completed:tracked?previousHealth.completed:false, completedAt:tracked?previousHealth.completedAt:"", socialSecurity:{amount:ss,date:ss>0?ssDate:""}, mutual:{amount:mutual,date:mutual>0?mutualDate:""} } };'''
if text.count(old_submit) != 1:
    raise SystemExit(f'expense submit anchor count={text.count(old_submit)}')
text = text.replace(old_submit, new_submit, 1)

# Give completed items a reopen action inside the edit sheet.
old_track_row = '''            </label>
            <div class="health-reimbursement-details" data-health-reimbursement-details hidden>'''
new_track_row = '''            </label>
            ${editing && normalizeHealthReimbursement(data.healthReimbursement).completed ? `<div class="health-completed-note"><span><span class="material-symbols-outlined">check_circle</span><strong>Suivi terminé</strong></span><button class="btn outlined small" type="button" data-reimbursement-reopen="${escapeHtml(data.id || "")}">Réouvrir</button></div>` : ""}
            <div class="health-reimbursement-details" data-health-reimbursement-details hidden>'''
if text.count(old_track_row) != 1:
    raise SystemExit(f'health track row anchor count={text.count(old_track_row)}')
text = text.replace(old_track_row, new_track_row, 1)

# Add completion helpers before the profile tracking renderer.
profile_marker = '    // REIMBURSEMENT-PROFILE-TRACKING-V1\n'
if text.count(profile_marker) != 1:
    raise SystemExit(f'profile marker count={text.count(profile_marker)}')
helpers = '''    // REIMBURSEMENT-SWIPE-COMPLETE-V1
    function setHealthReimbursementCompleted(id, completed) {
      const expense = state.expenses.find(item => item.id === id);
      if (!expense) return;
      const reimbursement = normalizeHealthReimbursement(expense.healthReimbursement);
      if (!reimbursement.tracked) return;
      expense.healthReimbursement = {
        ...reimbursement,
        completed: !!completed,
        completedAt: completed ? todayISO() : ""
      };
      saveState(completed ? "Suivi de remboursement terminé." : "Suivi de remboursement rouvert.");
    }

'''
text = text.replace(profile_marker, helpers + profile_marker, 1)

# Render active items with a compact iOS-style slide-to-complete control,
# and completed items as summary-only cards.
start = text.find('      const cards = summaries.map(({ item, summary }) => {')
end_anchor = '      return `${overview}<div class="reimbursement-tracking-list">${cards}</div>`;'
end = text.find(end_anchor, start)
if start < 0 or end < 0:
    raise SystemExit('reimbursement cards block not found')
new_cards = '''      const cards = summaries.map(({ item, summary }) => {
        const reimbursement = summary.reimbursement;
        const displayStatus = summary.gross <= .005 ? "Montant à renseigner" : summary.status;
        if (reimbursement.completed) {
          return `<div class="card reimbursement-tracking-card reimbursement-tracking-card-completed" data-edit-type="expense" data-edit-id="${item.id}" role="button" tabindex="0">
            <div class="reimbursement-completed-main">
              <div class="reimbursement-completed-copy">
                <div class="reimbursement-completed-title-row"><h3>${escapeHtml(item.label || "Dépense Santé")}</h3><span class="reimbursement-completed-badge"><span class="material-symbols-outlined">check</span>Terminé</span></div>
                <p>${escapeHtml(formatOperationGroupDate(item.date))} · <span class="money">${formatMoney(summary.gross)}</span></p>
              </div>
              <span class="reimbursement-percent">${summary.percent.toFixed(0)}%</span>
            </div>
            <div class="reimbursement-completed-summary">
              <span><small>Remboursé</small><strong class="money positive">${formatMoney(summary.total)}</strong></span>
              <span><small>Reste à charge</small><strong class="money">${formatMoney(summary.remaining)}</strong></span>
            </div>
          </div>`;
        }
        return `<div class="card reimbursement-tracking-card" data-edit-type="expense" data-edit-id="${item.id}" role="button" tabindex="0">
          <div class="reimbursement-card-head">
            <div><h3>${escapeHtml(item.label || "Dépense Santé")}</h3><p>${escapeHtml(formatOperationGroupDate(item.date))} · <span class="money">${formatMoney(summary.gross)}</span></p></div>
            <span class="reimbursement-percent">${summary.percent.toFixed(0)}%</span>
          </div>
          <div class="reimbursement-status-row"><span>${escapeHtml(displayStatus)}</span><strong class="money">Reste ${formatMoney(summary.remaining)}</strong></div>
          <div class="progress-track"><div class="progress-fill success" style="width:${clamp(summary.percent,0,100)}%"></div></div>
          <div class="reimbursement-sources">
            ${reimbursementSourceRow("Sécurité sociale", "health_and_safety", reimbursement.socialSecurity)}
            ${reimbursementSourceRow("Mutuelle", "verified_user", reimbursement.mutual)}
          </div>
          <div class="reimbursement-swipe" data-reimbursement-swipe="${item.id}" style="--swipe-x:0px">
            <span class="reimbursement-swipe-label">Glisser pour terminer</span>
            <button class="reimbursement-swipe-handle" type="button" data-reimbursement-swipe-handle aria-label="Glisser pour terminer le suivi" tabindex="-1"><span class="material-symbols-outlined">chevron_right</span></button>
          </div>
        </div>`;
      }).join("");
'''
text = text[:start] + new_cards + text[end:]

# Swipe gesture state alongside other transient UI state.
old_vars = '''    let preservedScrollY = null;
    const expandedProfileItems = new Set();'''
new_vars = '''    let preservedScrollY = null;
    let reimbursementSwipeGesture = null;
    const expandedProfileItems = new Set();'''
if text.count(old_vars) != 1:
    raise SystemExit(f'swipe vars anchor count={text.count(old_vars)}')
text = text.replace(old_vars, new_vars, 1)

# Install pointer-based swipe behavior before the main delegated click handler.
click_anchor = '''    document.addEventListener("click", event => {
      const fixedSortToggle = event.target.closest("[data-fixed-sort-toggle]");'''
if text.count(click_anchor) != 1:
    raise SystemExit(f'main click anchor count={text.count(click_anchor)}')
swipe_js = '''    function resetReimbursementSwipe(track) {
      if (!track) return;
      track.classList.remove("dragging", "ready");
      track.style.setProperty("--swipe-x", "0px");
    }

    document.addEventListener("pointerdown", event => {
      const handle = event.target.closest?.("[data-reimbursement-swipe-handle]");
      if (!handle) return;
      const track = handle.closest("[data-reimbursement-swipe]");
      if (!track) return;
      event.preventDefault();
      event.stopPropagation();
      const trackRect = track.getBoundingClientRect();
      const handleRect = handle.getBoundingClientRect();
      const max = Math.max(0, trackRect.width - handleRect.width - 8);
      reimbursementSwipeGesture = { pointerId:event.pointerId, handle, track, id:track.dataset.reimbursementSwipe, startX:event.clientX, max, x:0 };
      track.classList.add("dragging");
      handle.setPointerCapture?.(event.pointerId);
    }, true);

    document.addEventListener("pointermove", event => {
      const gesture = reimbursementSwipeGesture;
      if (!gesture || gesture.pointerId !== event.pointerId) return;
      event.preventDefault();
      const x = clamp(event.clientX - gesture.startX, 0, gesture.max);
      gesture.x = x;
      gesture.track.style.setProperty("--swipe-x", `${x}px`);
      gesture.track.classList.toggle("ready", gesture.max > 0 && x / gesture.max >= .82);
    }, true);

    const finishReimbursementSwipe = event => {
      const gesture = reimbursementSwipeGesture;
      if (!gesture || gesture.pointerId !== event.pointerId) return;
      event.preventDefault();
      event.stopPropagation();
      reimbursementSwipeGesture = null;
      const completed = gesture.max > 0 && gesture.x / gesture.max >= .82;
      if (completed) {
        gesture.track.classList.add("ready");
        gesture.track.style.setProperty("--swipe-x", `${gesture.max}px`);
        setTimeout(() => setHealthReimbursementCompleted(gesture.id, true), 120);
      } else {
        resetReimbursementSwipe(gesture.track);
      }
    };
    document.addEventListener("pointerup", finishReimbursementSwipe, true);
    document.addEventListener("pointercancel", finishReimbursementSwipe, true);

    document.addEventListener("click", event => {
      const reopen = event.target.closest?.("[data-reimbursement-reopen]");
      if (reopen) {
        event.preventDefault();
        event.stopPropagation();
        setHealthReimbursementCompleted(reopen.dataset.reimbursementReopen, false);
        return;
      }
      const swipe = event.target.closest?.("[data-reimbursement-swipe]");
      if (swipe) {
        event.preventDefault();
        event.stopPropagation();
        return;
      }

      const fixedSortToggle = event.target.closest("[data-fixed-sort-toggle]");'''
text = text.replace(click_anchor, swipe_js, 1)

# Compact swipe + completed summary styles.
style_end = '</style>'
if text.count(style_end) != 1:
    raise SystemExit('style closing tag not unique')
css = r'''
    /* REIMBURSEMENT-SWIPE-COMPLETE-V1 */
    .reimbursement-swipe {
      --swipe-x: 0px;
      position: relative;
      height: 42px;
      margin-top: 11px;
      border: 1px solid color-mix(in srgb, var(--outline-variant) 78%, transparent);
      border-radius: var(--pill);
      overflow: hidden;
      background: color-mix(in srgb, var(--surface-container-high) 74%, var(--surface-container-lowest));
      touch-action: pan-y;
      -webkit-user-select: none;
      user-select: none;
    }
    .reimbursement-swipe::before {
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: calc(var(--swipe-x) + 40px);
      background: color-mix(in srgb, var(--success) 18%, transparent);
      pointer-events: none;
    }
    .reimbursement-swipe-label {
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      padding: 0 48px;
      color: var(--on-surface-variant);
      font-size: 12px;
      line-height: 1;
      font-weight: 700;
      letter-spacing: .01em;
      pointer-events: none;
      transition: opacity .15s ease;
    }
    .reimbursement-swipe.ready .reimbursement-swipe-label { opacity: .35; }
    .reimbursement-swipe-handle {
      position: absolute;
      left: 3px;
      top: 3px;
      width: 34px;
      height: 34px;
      padding: 0;
      border: 0;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: var(--surface-container-lowest);
      color: var(--success);
      box-shadow: 0 1px 5px color-mix(in srgb, var(--shadow) 55%, transparent);
      transform: translateX(var(--swipe-x));
      transition: transform .18s cubic-bezier(.2,.8,.2,1), background .15s ease, color .15s ease;
      touch-action: none;
      cursor: grab;
      z-index: 2;
    }
    .reimbursement-swipe.dragging .reimbursement-swipe-handle { transition: background .15s ease, color .15s ease; cursor: grabbing; }
    .reimbursement-swipe.ready .reimbursement-swipe-handle { background: var(--success); color: var(--on-primary); }
    .reimbursement-swipe-handle .material-symbols-outlined { font-size: 21px; }

    .reimbursement-tracking-card-completed { padding: 12px 14px; }
    .reimbursement-completed-main { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
    .reimbursement-completed-copy { min-width:0; flex:1; }
    .reimbursement-completed-title-row { display:flex; align-items:center; flex-wrap:wrap; gap:7px; min-width:0; }
    .reimbursement-completed-title-row h3 { margin:0; min-width:0; font-size:16px; line-height:1.2; }
    .reimbursement-completed-copy p { margin:4px 0 0; color:var(--on-surface-variant); font-size:12px; }
    .reimbursement-completed-badge {
      display:inline-flex;
      align-items:center;
      gap:3px;
      min-height:22px;
      padding:3px 7px;
      border-radius:var(--pill);
      background:color-mix(in srgb, var(--success-container) 78%, var(--surface-container-lowest));
      color:var(--success);
      font-size:10px;
      font-weight:700;
      white-space:nowrap;
    }
    .reimbursement-completed-badge .material-symbols-outlined { font-size:14px; }
    .reimbursement-tracking-card-completed .reimbursement-percent { font-size:22px; line-height:1; }
    .reimbursement-completed-summary {
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:12px;
      margin-top:9px;
      padding-top:9px;
      border-top:1px solid color-mix(in srgb, var(--outline-variant) 58%, transparent);
    }
    .reimbursement-completed-summary span { display:grid; gap:2px; min-width:0; }
    .reimbursement-completed-summary small { color:var(--on-surface-variant); font-size:10px; }
    .reimbursement-completed-summary strong { font-size:13px; }

    .health-completed-note {
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      margin-top:8px;
      padding:8px 10px;
      border-radius:14px;
      background:color-mix(in srgb, var(--success-container) 44%, var(--surface-container-lowest));
      color:var(--success);
    }
    .health-completed-note > span { display:flex; align-items:center; gap:6px; min-width:0; font-size:12px; }
    .health-completed-note .material-symbols-outlined { font-size:18px; }
    .health-completed-note .btn { min-height:30px; padding:5px 9px; font-size:11px; }
'''
text = text.replace(style_end, css + '\n  ' + style_end, 1)

path.write_text(text, encoding='utf-8')
