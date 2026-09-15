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
