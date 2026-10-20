# Sign-up form → Google Sheet (free)

About 3 minutes, one time:

1. Create a new Google Sheet (e.g. **Create the Cut 2027 Sign-ups**) in the Drive account that should own the data.
2. In the Sheet: **Extensions → Apps Script**. Delete the starter code and paste in everything from `Code.gs`.
   - Optional: set `NOTIFY_EMAIL` at the top to get an email for every sign-up.
3. Click **Deploy → New deployment → Select type: Web app**.
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click **Deploy** and approve the Google permission prompt.
4. Copy the **Web app URL** (ends in `/exec`).
5. Paste it into `data/site.json` → `"form_endpoint": "https://script.google.com/macros/s/…/exec"`, then run `python3 build.py` and publish.

Sign-ups appear on a **Sign-ups** tab, one row per person. If you edit `Code.gs` later, use **Deploy → Manage deployments → Edit → New version**, which keeps the same URL.
