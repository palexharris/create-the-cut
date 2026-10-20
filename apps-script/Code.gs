/**
 * Create the Cut 2027 — sign-up form backend.
 * Bound to a Google Sheet; the website POSTs each sign-up here and it lands as a new row.
 * Setup steps: see apps-script/README.md.
 */
var NOTIFY_EMAIL = '';          // e.g. 'admin@harrisclips.com' — gets an email per sign-up. Blank = off.
var SEND_CONFIRMATION = true;   // emails the person a short "you're on the list" note

var FIELDS = ['role', 'first_name', 'last_name', 'email', 'phone', 'school', 'program_type',
  'expected_graduation', 'students_to_nominate', 'adult_on_event_day', 'organization',
  'instructor_name', 'city', 'heard_about', 'notes', 'consent', 'submitted_from'];

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.website) return ok_();                       // honeypot hit — silently drop
  if (!p.email || !p.first_name) return ok_();

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = sheet_();
    var row = [new Date()].concat(FIELDS.map(function (f) { return String(p[f] || '').slice(0, 2000); }));
    sh.appendRow(row);
  } finally {
    lock.releaseLock();
  }

  var name = (p.first_name + ' ' + (p.last_name || '')).trim();
  if (NOTIFY_EMAIL) {
    MailApp.sendEmail(NOTIFY_EMAIL, 'Create the Cut sign-up: ' + name + ' (' + p.role + ')',
      FIELDS.map(function (f) { return f + ': ' + (p[f] || ''); }).join('\n'));
  }
  if (SEND_CONFIRMATION) {
    MailApp.sendEmail({
      to: p.email,
      name: 'Create the Cut — Great Clips Franchisees of Cleveland-Akron-Canton',
      subject: "You're on the Create the Cut 2027 list!",
      body: 'Hi ' + p.first_name + ',\n\nThanks for your interest in Create the Cut 2027! ' +
        "We'll email you as soon as the date, venue and nomination details are announced.\n\n" +
        '— The Great Clips franchisees of Cleveland-Akron-Canton'
    });
  }
  return ok_();
}

function doGet() { return ok_(); }

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName('Sign-ups') || ss.insertSheet('Sign-ups');
  if (sh.getLastRow() === 0) {
    sh.appendRow(['timestamp'].concat(FIELDS));
    sh.setFrozenRows(1);
  }
  return sh;
}

function ok_() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
}
