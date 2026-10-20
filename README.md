# Create the Cut 2027 — event website

Static site for the Great Clips franchisees of Cleveland-Akron-Canton's student haircut competition.
Hosted free on GitHub Pages.

## Editing
All content lives in `data/site.json` (2027 date/venue, winners, rosters, videos, news, form URL).
Edit it, then rebuild and push:

    python3 build.py
    git add -A && git commit -m "Update site" && git push

Photos: `data/gallery.json` lists the gallery images in `assets/img/gallery/<year>/`.
Sign-up form backend: `apps-script/README.md` (Google Sheet + Apps Script, free).

## Preview locally
    python3 -m http.server 8427   # then open http://localhost:8427
