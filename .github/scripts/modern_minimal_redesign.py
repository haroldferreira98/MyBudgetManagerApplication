from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

text = text.replace('<meta name="app-build" content="20260916-cleanup" />', '<meta name="app-build" content="20260916-minimal-redesign-v1" />', 1)
text = text.replace('    <main>\n      <section class="screen active" id="screen-home"', '    <main class="app-content">\n      <section class="screen active" id="screen-home"', 1)

marker = '  </style>\n</head>'
if marker not in text:
    raise SystemExit('Style closing marker not found')

css = r'''

    /* ============================================================
       MODERN MINIMAL REDESIGN V1
       Flat, legible, information-first. The bottom navigation is the
       only pill-shaped structural element in the interface.
       ============================================================ */

    :root {
      --radius-card: 10px;
      --radius-sheet: 14px;
      --radius-small: 6px;
      --pill: 8px;
      --content-max: 780px;
      --nav-height: 72px;
    }

    body {
      background: var(--surface) !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", system-ui, sans-serif !important;
      letter-spacing: 0;
    }

    .app-shell {
      width: min(100%, var(--content-max));
      padding-bottom: calc(var(--nav-height) + 46px + var(--safe-bottom));
    }

    .app-content { padding: 12px 16px 24px; }

    .topbar {
      min-height: 70px;
      padding: calc(9px + var(--safe-top)) 16px 9px;
      gap: 11px;
      background: color-mix(in srgb, var(--surface) 96%, transparent) !important;
      border-bottom: 1px solid color-mix(in srgb, var(--outline-variant) 72%, transparent);
      box-shadow: none;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    .brand-eyebrow { margin-bottom: 1px; font-size: 10px; font-weight: 650; letter-spacing: .08em; }
    .brand-title { font-size: clamp(22px, 6vw, 27px); line-height: 1.08; font-weight: 720; letter-spacing: -.025em; }
    .top-account-btn { width: 40px; height: 40px; flex-basis: 40px; border-width: 1px; box-shadow: none; }
    .top-actions { gap: 6px; }
    .icon-btn, .mini-btn { border-radius: var(--radius-small) !important; box-shadow: none !important; }
    .icon-btn { width: 40px; height: 40px; background: transparent; border: 1px solid color-mix(in srgb, var(--outline-variant) 78%, transparent); }
    .icon-btn:hover { background: var(--surface-container-low); }

    .screen { animation: screenIn .16s ease; }
    .section { margin: 18px 0 24px; }
    .section-header { margin: 0 0 10px; gap: 10px; align-items: center; }
    .section-title { font-size: 17px; line-height: 1.25; font-weight: 700; letter-spacing: -.015em; }
    .section-subtitle { margin-top: 3px; font-size: 12px; line-height: 1.35; }

    .card, .empty-state, .profile-fold, .expense-category-group, .sim-box, .cloud-status {
      border-radius: var(--radius-card) !important;
      box-shadow: none !important;
    }
    .card { padding: 16px; background: var(--surface-container-lowest); border: 1px solid color-mix(in srgb, var(--outline-variant) 78%, transparent); }
    .card + .card { margin-top: 10px; }

    .hero-card, html[data-theme="dsfr"] .hero-card, html[data-theme="dsfr"] .summary-card {
      padding: 18px;
      background: var(--surface-container-lowest) !important;
      border: 1px solid color-mix(in srgb, var(--outline-variant) 84%, transparent) !important;
      border-top: 3px solid var(--primary) !important;
      overflow: hidden;
    }
    .hero-card::after, html[data-theme="dsfr"] .hero-card::after { display: none !important; }
    .hero-label, html[data-theme="dsfr"] .hero-label {
      color: var(--on-surface-variant) !important;
      font-size: 12px;
      font-weight: 650;
      letter-spacing: .035em;
      text-transform: uppercase;
    }
    .hero-value, html[data-theme="dsfr"] .hero-value {
      margin-top: 7px;
      color: var(--on-surface) !important;
      font-size: clamp(35px, 10.5vw, 48px);
      font-weight: 720;
      letter-spacing: -.04em;
    }
    .hero-meta { justify-content: flex-start; gap: 7px; margin-top: 14px; }
    .hero-privacy-btn { top: 12px; right: 12px; width: 38px; height: 38px; background: var(--surface-container-low) !important; color: var(--on-surface-variant) !important; border-color: transparent; }

    .daily-pill, .status-pill, .chip, .small-pill, .target-badge {
      min-height: 30px;
      padding: 5px 9px;
      border-radius: var(--radius-small) !important;
      font-size: 11.5px;
      font-weight: 650;
    }
    .daily-pill, html[data-theme="dsfr"] .daily-pill { background: var(--surface-container-low) !important; color: var(--on-surface-variant) !important; }

    .home-summary-section { margin-top: 12px; margin-bottom: 20px; }
    .summary-card { padding: 18px; }
    .summary-card .hero-value { margin-top: 5px; font-size: clamp(34px, 9.5vw, 46px); }
    .summary-card .hero-meta { margin-top: 12px; gap: 6px; }
    .summary-bottom { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; margin-top: 15px; padding-top: 12px; border-top: 1px solid var(--outline-variant); }
    .summary-mini, html[data-theme="dsfr"] .summary-mini { min-width: 0; padding: 7px 10px; border-radius: 0 !important; background: transparent !important; }
    .summary-mini:first-child { padding-left: 0; }
    .summary-mini:last-child { padding-right: 0; }
    .summary-mini + .summary-mini { border-left: 1px solid color-mix(in srgb, var(--outline-variant) 72%, transparent); }
    .summary-mini-label { font-size: clamp(9px, 2.7vw, 11px); font-weight: 600; }
    .summary-mini-value, html[data-theme="dsfr"] .summary-mini-value { margin-top: 3px; color: var(--on-surface) !important; font-size: clamp(13px, 3.8vw, 18px); font-weight: 700; }

    .month-switcher, html[data-theme="dsfr"] .month-switcher {
      height: 44px;
      margin: 6px 0 14px;
      padding: 2px 4px;
      border-radius: var(--radius-small) !important;
      background: var(--surface-container-lowest);
      border: 1px solid var(--outline-variant);
    }
    .month-current { height: 36px; border-radius: var(--radius-small) !important; font-size: 13px; font-weight: 680; }
    .month-arrow { width: 36px; height: 36px; border-radius: var(--radius-small) !important; }

    .search-shell, html[data-theme="dsfr"] .search-shell {
      min-height: 46px;
      padding: 6px 9px 6px 12px;
      border-radius: var(--radius-small) !important;
      background: var(--surface-container-lowest);
      border: 1px solid var(--outline-variant);
    }
    .search-shell:focus-within { border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary); }
    .search-shell input { font-size: 14px; }
    .chips { gap: 6px; padding-top: 9px; }
    .chip, html[data-theme="dsfr"] .chip { min-height: 32px; padding: 6px 9px; border-radius: var(--radius-small) !important; background: var(--surface-container-lowest); }
    .chip.active { background: var(--primary-container); color: var(--on-primary-container); border-color: color-mix(in srgb, var(--primary) 34%, var(--outline-variant)); }

    .list { gap: 7px; }
    .list-item, html[data-theme="dsfr"] .list-item {
      min-height: 60px;
      padding: 10px 11px;
      gap: 10px;
      border-radius: var(--radius-small) !important;
      background: var(--surface-container-lowest);
      border: 1px solid color-mix(in srgb, var(--outline-variant) 76%, transparent);
      box-shadow: none;
    }
    .list-item:hover { border-color: color-mix(in srgb, var(--primary) 36%, var(--outline-variant)); }
    .list-icon, html[data-theme="dsfr"] .list-icon { width: 36px; height: 36px; flex: 0 0 36px; border-radius: var(--radius-small) !important; background: var(--surface-container-low); color: var(--primary); }
    .list-icon .material-symbols-outlined { font-size: 20px; }
    .list-title { font-size: 14px; font-weight: 580; }
    .list-sub { margin-top: 2px; font-size: 11px; }
    .list-amount { font-size: 14px; font-weight: 680; font-variant-numeric: tabular-nums; }
    .fixed-charge-row { min-height: 58px; padding: 9px 11px; gap: 10px; border-radius: var(--radius-small) !important; }
    .fixed-charge-row .list-title { font-size: 14px; font-weight: 400; }
    .fixed-charge-row.pending { opacity: .5; background: var(--surface-container-low); }

    .expense-category-group { border: 1px solid var(--outline-variant); background: var(--surface-container-lowest); overflow: hidden; }
    .expense-category-group + .expense-category-group { margin-top: 8px; }
    .expense-category-summary { min-height: 56px; padding: 10px 11px; gap: 9px; }
    .expense-category-group[open] > .expense-category-summary { border-bottom: 1px solid color-mix(in srgb, var(--outline-variant) 72%, transparent); }
    .expense-category-label { font-size: 12px; font-weight: 650; }
    .expense-category-meta { font-size: 10.5px; }
    .expense-category-total { font-size: 13px; font-weight: 680; }
    .expense-category-items { gap: 0; padding: 0 10px 6px; }
    .expense-category-items .list-item { min-height: 52px; padding: 9px 2px; border: 0; border-bottom: 1px solid color-mix(in srgb, var(--outline-variant) 62%, transparent); border-radius: 0 !important; background: transparent; }
    .expense-category-items .list-item:last-child { border-bottom: 0; }
    .expense-category-items .expense-list-item .list-title, .expense-category-items .fixed-charge-row .list-title { font-weight: 400; }

    .btn, html[data-theme="dsfr"] .btn { min-height: 44px; padding: 0 14px; border-radius: var(--radius-small) !important; font-size: 13px; font-weight: 650; box-shadow: none !important; }
    .btn.small { min-height: 36px; padding: 0 11px; font-size: 12px; }
    .btn.primary { background: var(--primary); color: var(--on-primary); }
    .btn.tonal { background: var(--primary-container); color: var(--on-primary-container); }
    .btn.outlined { background: var(--surface-container-lowest); border: 1px solid var(--outline-variant); color: var(--on-surface); }
    .button-row { gap: 7px; flex-wrap: nowrap; }
    .expense-sort-menu { min-width: 184px; padding: 4px; border-radius: var(--radius-small) !important; border-color: var(--outline-variant); box-shadow: 0 12px 28px color-mix(in srgb, var(--shadow) 54%, transparent); }
    .expense-sort-option { min-height: 38px; padding: 7px 9px; border-radius: 4px !important; font-size: 12.5px; }

    .balance-card { padding: 8px 14px !important; background: var(--surface-container-lowest); }
    .balance-card .balance-row { margin: 12px 0; }
    .balance-head { font-size: 12px; }
    .balance-label strong { font-size: 13px; font-weight: 650; }
    .target-badge { min-width: 34px; padding: 3px 6px; }
    .progress-track, html[data-theme="dsfr"] .progress-track { height: 6px; border-radius: 2px !important; }
    .progress-fill, html[data-theme="dsfr"] .progress-fill { border-radius: 2px !important; }

    #screen-settings .settings-page-card { padding: 15px; }
    .segmented, html[data-theme="dsfr"] .segmented { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; padding: 0; border: 0; border-radius: 0 !important; background: transparent; }
    .segmented button, html[data-theme="dsfr"] .segmented button { min-height: 48px; padding: 0 12px; border: 1px solid var(--outline-variant); border-radius: var(--radius-small) !important; background: var(--surface-container-lowest); color: var(--on-surface); font-size: 13px; font-weight: 620; }
    .segmented button.active, html[data-theme="dsfr"] .segmented button.active { background: var(--primary-container); color: var(--on-primary-container); border-color: var(--primary); }

    .sheet, html[data-theme="dsfr"] .sheet { border-radius: var(--radius-sheet) var(--radius-sheet) 0 0 !important; background: var(--surface-container-lowest); border: 1px solid var(--outline-variant); box-shadow: 0 -12px 36px color-mix(in srgb, var(--shadow) 70%, transparent); }
    .sheet-handle, html[data-theme="dsfr"] .sheet-handle { width: 38px; height: 3px; border-radius: 2px !important; opacity: .45; }
    .sheet-head { padding: 9px 14px 7px 18px; }
    .sheet-title { font-size: 20px; font-weight: 710; letter-spacing: -.02em; }
    .sheet-body { padding: 7px 16px 18px; }
    .field { gap: 5px; margin: 11px 0; }
    .field label { padding-left: 0; font-size: 11.5px; font-weight: 650; }
    .field input, .field select, .field textarea, html[data-theme="dsfr"] .field input, html[data-theme="dsfr"] .field select, html[data-theme="dsfr"] .field textarea {
      min-height: 48px;
      padding: 10px 11px;
      border-radius: var(--radius-small) !important;
      background: var(--surface-container-lowest);
      border: 1px solid var(--outline-variant);
      font-size: 15px;
    }
    .field input:focus, .field select:focus, .field textarea:focus { border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary); }
    .checkbox-row, html[data-theme="dsfr"] .checkbox-row { min-height: 46px; padding: 9px 10px; border-radius: var(--radius-small) !important; background: var(--surface-container-low); border: 1px solid color-mix(in srgb, var(--outline-variant) 70%, transparent); }
    .modal-actions { gap: 8px; padding-top: 10px; background: linear-gradient(transparent, var(--surface-container-lowest) 26%); }
    .modal-actions .btn { min-height: 44px; }
    #entityModal[data-entity-type="expense"] .sheet, #entityModal[data-entity-type="income"] .sheet, #entityModal[data-entity-type="fixed"] .sheet { border-radius: var(--radius-sheet) var(--radius-sheet) 0 0 !important; }

    .cloud-status { padding: 10px 11px; border-radius: var(--radius-small) !important; background: var(--surface-container-low); font-size: 12px; }
    .account-profile-content { margin-top: 14px; border-top-color: var(--outline-variant); }
    .profile-fold { border-radius: var(--radius-card) !important; }
    .metric-card { min-height: 104px; }
    .metric-label { font-size: 12px; }
    .metric-value { margin-top: 6px; font-size: 22px; }
    .metric-note { font-size: 11px; }

    .month-picker-year-btn { border-radius: var(--radius-small) !important; background: var(--surface-container-low); }
    .month-picker-option { min-height: 44px; border-radius: var(--radius-small) !important; background: var(--surface-container-lowest); font-size: 13px; }
    .empty-state { padding: 24px 16px; background: var(--surface-container-lowest); border: 1px dashed var(--outline-variant); }
    .snackbar { border-radius: var(--radius-small) !important; font-size: 13px; }

    .nav-wrap { width: min(calc(100% - 20px), 560px); bottom: max(7px, calc(var(--safe-bottom) - 18px)) !important; }
    .bottom-nav, html[data-theme="dsfr"] .bottom-nav {
      height: 66px !important;
      padding: 5px 8px !important;
      border-radius: 9999px !important;
      background: color-mix(in srgb, var(--surface-container-lowest) 96%, transparent) !important;
      border: 1px solid color-mix(in srgb, var(--outline-variant) 82%, transparent) !important;
      box-shadow: 0 8px 26px color-mix(in srgb, var(--shadow) 52%, transparent) !important;
      backdrop-filter: blur(18px) saturate(1.1);
      -webkit-backdrop-filter: blur(18px) saturate(1.1);
    }
    .nav-btn, html[data-theme="dsfr"] .nav-btn { position: relative; height: 54px; border-radius: 8px !important; gap: 3px; background: transparent !important; font-size: 10px; font-weight: 600; }
    .nav-btn > span:last-child { font-size: 9.5px !important; }
    .nav-btn .material-symbols-outlined { font-size: 22px; }
    .nav-btn.active, html[data-theme="dsfr"] .nav-btn.active { color: var(--primary); }
    .nav-btn.active .material-symbols-outlined, html[data-theme="dsfr"] .nav-btn.active .material-symbols-outlined {
      width: auto;
      height: auto;
      border-radius: 0 !important;
      background: transparent !important;
      color: var(--primary);
      font-variation-settings: "FILL" 1, "wght" 600, "GRAD" 0, "opsz" 24;
    }
    .nav-btn.active::after { content: ""; position: absolute; left: 50%; bottom: 1px; width: 18px; height: 2px; transform: translateX(-50%); background: var(--primary); border-radius: 1px; }

    html[data-theme="dsfr"] body { background: var(--surface) !important; }
    html[data-theme="dsfr"] .topbar { background: var(--surface) !important; }

    @media (min-width: 640px) {
      .app-content { padding-left: 22px; padding-right: 22px; }
      .topbar { padding-left: 22px; padding-right: 22px; }
      .sheet { border-radius: var(--radius-sheet) !important; margin-bottom: 18px; }
      #entityModal[data-entity-type="expense"] .sheet, #entityModal[data-entity-type="income"] .sheet, #entityModal[data-entity-type="fixed"] .sheet { border-radius: var(--radius-sheet) !important; }
    }

    @media (max-width: 430px) {
      .app-content { padding-left: 13px; padding-right: 13px; }
      .topbar { padding-left: 13px; padding-right: 13px; }
      .hero-card { padding: 16px; }
      .section { margin-bottom: 21px; }
      .button-row { gap: 5px; }
      .btn.small { padding: 0 9px; }
      .summary-mini { padding-left: 7px; padding-right: 7px; }
      .summary-mini:first-child { padding-left: 0; }
      .summary-mini:last-child { padding-right: 0; }
    }
'''

text = text.replace(marker, css + '\n  </style>\n</head>', 1)
path.write_text(text, encoding='utf-8')
