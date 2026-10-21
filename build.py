#!/usr/bin/env python3
"""Build the Create the Cut static site from data/site.json + data/gallery.json.

    python3 build.py        # writes *.html next to this file

Everything editable (2027 date/venue, winners, rosters, videos, news, form URL)
lives in data/site.json — change it there and rebuild; don't hand-edit the HTML.
"""
import json, os
from html import escape as e

ROOT = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(ROOT, 'data/site.json')))
G = json.load(open(os.path.join(ROOT, 'data/gallery.json')))
EV = S['event_2027']
YEARS = S['years']
REGION = 'Cleveland-Akron-Canton'
V = str(int(max(os.path.getmtime(os.path.join(ROOT, p)) for p in ('assets/css/site.css', 'assets/js/site.js'))))
SITE_NAME = 'Create the Cut 2027'

def money(n): return '${:,.0f}'.format(n)

AWARDED = sum(y['prize_total'] or 0 for y in YEARS)
COMPETITORS = sum(y['competitors'] or 0 for y in YEARS)
PRIZE_TOP = S['prizes'][0]['student']
PRIZE_YEAR = sum(p['student'] + p['school'] for p in S['prizes'])
SCHOOLS = sorted({s for y in YEARS for _, s in y['participants']} | {w['school'] for y in YEARS for w in y['winners']})

NAV = [('index.html', 'Home'), ('event.html', '2027 Event'), ('past-events.html', 'Past Winners'),
       ('gallery.html', 'Photos & Video'), ('news.html', 'In the News'), ('faq.html', 'FAQs')]

TRI = ('<svg class="tri" viewBox="0 0 400 300" preserveAspectRatio="xMaxYMid slice" aria-hidden="true">'
       '<polygon points="160,0 400,0 400,300" fill="#048667" opacity=".55"/>'
       '<polygon points="250,0 400,0 400,190" fill="#089f45" opacity=".55"/>'
       '<polygon points="330,0 400,0 400,90" fill="#9acb3a" opacity=".8"/></svg>')


def lockup(cls=''):
    return (f'<a class="lockup {cls}" href="index.html" aria-label="Great Clips franchisees of {REGION} — home">'
            f'<img src="assets/logo/gc-logo-tag-white.png" alt="Great Clips" width="276" height="26">'
            f'<span>Franchisees of {REGION}</span></a>')


def page(fname, title, desc, body, hero_img=None):
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == fname else ""}>{t}</a>' for h, t in NAV)
    endpoint_note = ''
    contact = S.get('contact_email')
    contact_li = f'<li><a href="mailto:{e(contact)}">{e(contact)}</a></li>' if contact else ''
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="assets/img/gallery/2025/ctc2025-01.jpg">
<meta name="theme-color" content="#073b3a">
<link rel="icon" href="assets/icons/shears.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={V}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    {lockup()}
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}<a class="cta" href="signup.html">Sign Up</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="cols">
      <div>
        {lockup()}
        <p style="margin-top:16px;max-width:30rem">Create the Cut is a haircutting competition for Northeast Ohio cosmetology and barbering students, hosted and funded by the independently owned and operated Great Clips<sup>®</sup> salons of {REGION}.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}<li><a href="signup.html">Sign up for 2027</a></li></ul>
      </div>
      <div>
        <h4>Get involved</h4>
        <ul>
          <li><a href="signup.html?role=student">Students</a></li>
          <li><a href="signup.html?role=instructor">Instructors &amp; schools</a></li>
          <li><a href="https://jobs.greatclips.com" target="_blank" rel="noopener">Great Clips careers</a></li>
          {contact_li}
        </ul>
      </div>
    </div>
    <p class="fine">Great Clips<sup>®</sup> salons are independently owned and operated. Create the Cut is sponsored by the Great Clips franchisees of {REGION}. Great Clips and the Great Clips logo are trademarks of Great Clips, Inc.</p>
  </div>
</footer>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="x" aria-label="Close">×</button><button class="prev" aria-label="Previous photo">‹</button>
  <img alt=""><button class="next" aria-label="Next photo">›</button>
</div>
<script src="assets/js/site.js?v={V}"></script>
</body>
</html>
'''
    open(os.path.join(ROOT, fname), 'w').write(html)
    print('wrote', fname)


def icon(name):
    return f'<div class="ico"><img src="assets/icons/{name}.svg" alt=""></div>'


def prize_cards():
    out = []
    for i, p in enumerate(S['prizes'], 1):
        out.append(f'<div class="prize p{i}"><div class="place">{p["place"]} Place</div>'
                   f'<div class="amt">{money(p["student"])}</div><div class="who">to the student</div><div class="who" style="margin-top:2px">cash <b>or</b> an equal-value tool package</div>'
                   f'<span class="plus">+ {money(p["school"])} to their school<br><small style="font-weight:400;color:var(--muted)">as cash or tools for the program</small></span></div>')
    return '<div class="prizes">' + ''.join(out) + '</div>'


def stats_band():
    return f'''<section class="band-dark"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Investing in the next generation</span>
  <h2>Real money for real talent.</h2>
  <p>Every dollar is funded by local Great Clips franchisees — going straight to student winners and matched, dollar for dollar, to the schools that trained them — as cash or professional tools.</p></div>
  <div class="grid g4">
    <div class="stat"><b>{money(AWARDED)}+</b><span>awarded to students &amp; schools</span></div>
    <div class="stat"><b>{money(PRIZE_YEAR)}</b><span>in prizes up for grabs in 2027</span></div>
    <div class="stat"><b>{COMPETITORS}+</b><span>student competitors</span></div>
    <div class="stat"><b>{len(SCHOOLS)}+</b><span>cosmetology &amp; barber programs</span></div>
  </div>
  <p class="note">Dollar totals reflect the 2025 and 2026 competitions; 2024 winners received professional tool kits plus prizes for their schools.</p>
</div></section>'''


def cta_band(h='Ready to show what you can do?', p='Students: let us know you’re interested. Instructors: sign up to receive the nomination form — all competitors are nominated by their cosmetology school instructors.'):
    return f'''<section class="cta-band">{TRI}<div class="wrap" style="position:relative;z-index:1">
  <h2>{h}</h2><p>{p}</p>
  <div class="btn-row"><a class="btn btn-lime" href="signup.html">Sign up for 2027</a><a class="btn btn-ghost" href="event.html">Event details</a></div>
</div></section>'''


# ---------------------------------------------------------------- home
def save_the_date():
    return f'''<section class="band-mint"><div class="wrap split">
  <a href="{EV["save_the_date_pdf"]}" target="_blank" rel="noopener"><img src="{EV["save_the_date_img"]}" alt="Save the date: Create the Cut, Sunday, March 14, 2027, Don Umerley Civic Center, Rocky River" loading="lazy" style="max-height:none;object-fit:contain;background:#fff"></a>
  <div>
    <span class="eyebrow" style="color:var(--jade)">Save the date</span>
    <h2>{e(EV["headline_date"])}</h2>
    <p style="font-size:1.15rem;margin-bottom:4px"><b>{e(EV["venue"])}</b></p>
    <p><a href="{e(EV["maps_url"])}" target="_blank" rel="noopener">{e(EV["venue_detail"])}</a></p>
    <p>Instructors: start thinking about who you’ll nominate. Students: tell your instructor you want in — all nominations come from instructors. Start time and nomination details are coming soon.</p>
    <div class="btn-row"><a class="btn btn-jade" href="{EV["ics"]}" download>Add to calendar</a><a class="btn btn-outline" href="{EV["save_the_date_pdf"]}" download>Download the flyer</a></div>
  </div>
</div></section>'''


def build_home():
    cd = ''
    if EV.get('countdown_iso'):
        cd = f'<div class="countdown" data-to="{EV["countdown_iso"]}"><div><b data-d>–</b><small>days to go</small></div></div>'
    w25 = next(y for y in YEARS if y['year'] == 2025)['winners']
    body = f'''
<section class="hero"><div class="hero-bg" style="background-image:url('assets/img/gallery/2025/ctc2025-19.jpg')"></div><div class="wrap">
  <span class="eyebrow">Northeast Ohio’s student haircut competition</span>
  <h1>Create the Cut <em>2027</em></h1>
  <p class="lede">Cosmetology and barbering students from across Northeast Ohio go shears-to-shears for cash prizes or career-launching tool packages — with every winner’s school taking home a matching gift. Hosted by the Great Clips franchisees of {REGION}.</p>
  <div class="facts"><span>{e(EV["headline_date"])}</span><span>{e(EV["venue"])}, Rocky River</span><span>{money(PRIZE_TOP)} top prize</span><span>Free to compete</span></div>
  {cd}
  <div class="btn-row"><a class="btn btn-lime" href="signup.html">Join the 2027 interest list</a><a class="btn btn-ghost" href="event.html">See event details</a></div>
</div></section>

{save_the_date()}

<section><div class="wrap split">
  <div>
    <span class="eyebrow" style="color:var(--jade)">What is Create the Cut?</span>
    <h2>Two cuts. One clock. Real stakes.</h2>
    <p>Create the Cut gives the region’s most promising stylists a stage. Instructors nominate their top students, who then compete on mannequins through two timed rounds — a haircut and style, then a second haircut — while a panel of judges scores their technique and finished looks.</p>
    <p>Family, friends and instructors pack the room to cheer them on, and the top three walk away with oversized checks, bragging rights and a head start on their careers.</p>
    <a class="btn btn-jade" href="event.html">How it works</a>
  </div>
  <img src="assets/img/gallery/2025/ctc2025-14.jpg" alt="A student competitor cutting a mannequin's hair at Create the Cut 2025" loading="lazy">
</div></section>

<section class="band-gray"><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--jade)">Prizes</span><h2>Win for yourself. Win for your school.</h2>
  <p>Winners choose a cash prize <b>or</b> a professional tool package of equal value to jump-start their careers — and each school’s matching gift can come as cash or as tools for the program.</p></div>
  {prize_cards()}
</div></section>

{stats_band()}

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--jade)">Get involved</span><h2>There’s a spot for everyone.</h2></div>
  <div class="grid g3">
    <div class="card">{icon("shears")}<h3>Students</h3><p>Enrolled in (or recently graduated from) a Northeast Ohio cosmetology or barbering program? Submit your interest, then ask your instructor to nominate you — only instructors can enter students.</p><a href="signup.html?role=student">Submit student interest →</a></div>
    <div class="card">{icon("trophy")}<h3>Instructors &amp; schools</h3><p>All competitors are nominated by their instructors. Sign up to receive the nomination form, then put your program on the board. Every winning school receives a matching gift.</p><a href="signup.html?role=instructor">Sign up your program →</a></div>
    <div class="card">{icon("party")}<h3>Family &amp; fans</h3><p>Come cheer! Create the Cut is a high-energy afternoon and spectators are welcome — no sign-up needed, and light refreshments are provided.</p><a href="event.html">See event details →</a></div>
  </div>
</div></section>

<section class="band-mint"><div class="wrap split">
  <img src="{w25[0]["photo"]}" alt="{e(w25[0]["name"])} holding the first-place check at Create the Cut 2025" loading="lazy">
  <div>
    <span class="eyebrow" style="color:var(--jade)">2025 Champion</span>
    <h2>{e(w25[0]["name"])}</h2>
    <p style="font-size:1.1rem">{e(w25[0]["school"])} — {money(w25[0]["amount"])} to the student and {money(w25[0]["amount"])} to the school.</p>
    <p>“We’ve had winners who jump up and down, laughing and crying, in total disbelief they have won.” — Alex Harris, Great Clips franchisee</p>
    <a class="btn btn-jade" href="past-events.html">Meet every winner</a>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--jade)">As seen on FOX 8</span><h2>In the news</h2></div>
  <div class="feature-video">
    <iframe class="yt" src="https://www.youtube.com/embed/{S["news"]["youtube"][0]["id"]}" title="{e(S["news"]["youtube"][0]["title"])}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    <div><h3>{e(S["news"]["youtube"][0]["title"])}</h3><p>Fox 8 Cleveland has covered Create the Cut as students from public and private programs across the region competed for scholarships and school gifts.</p><a class="btn btn-outline" href="news.html">More coverage</a></div>
  </div>
</div></section>

{cta_band()}
'''
    page('index.html', f'{SITE_NAME} | Great Clips Franchisees of {REGION}',
         f'Create the Cut is a haircutting competition for Northeast Ohio cosmetology and barbering students — cash or tool-package prizes plus matching school gifts, hosted by the Great Clips franchisees of {REGION}.',
         body)


# ---------------------------------------------------------------- event
def build_event():
    body = f'''
<section class="page-hero">{TRI}<div class="wrap"><span class="eyebrow">Create the Cut 2027</span><h1>Event details</h1>
<p>Save the date: <b>{e(EV["headline_date"])}</b> at the {e(EV["venue"])} in Rocky River. Everything competitors, instructors and spectators need to know — <a href="signup.html" style="color:var(--lime)">join the list</a> for nomination details.</p></div></section>

<section><div class="wrap">
  <div class="glance">
    <div><small>When</small><strong>{e(EV["headline_date"])}</strong><span>{e(EV["date_detail"])} · <a href="{EV["ics"]}" download>Add to calendar</a></span></div>
    <div><small>Time</small><strong>Afternoon</strong><span>{e(EV["time"])}</span></div>
    <div><small>Where</small><strong>{e(EV["venue"])}</strong><span><a href="{e(EV["maps_url"])}" target="_blank" rel="noopener">{e(EV["venue_detail"])}</a></span></div>
    <div><small>Who competes</small><strong>Instructor-nominated students</strong><span>Cosmetology &amp; barbering programs</span></div>
    <div><small>Nominations due</small><strong>{e(EV["nomination_deadline"])}</strong><span>Last year’s deadline was Jan. 15</span></div>
    <div><small>Cost</small><strong>Free</strong><span>To compete and to watch</span></div>
  </div>
</div></section>

<section class="band-gray"><div class="wrap split" style="align-items:start">
  <div>
    <span class="eyebrow" style="color:var(--jade)">The competition</span>
    <h2>How it works</h2>
    <p>Competitors work on mannequins through two timed rounds of about 40 minutes each — <b>Round 1: a haircut and style</b>, then <b>Round 2: a second haircut</b>. Judges score each round as soon as the clock stops.</p>
    <p>The highest combined scores take 1st, 2nd and 3rd place, and winners are announced and presented with their checks at the end of the afternoon.</p>
    <div class="steps" style="margin-top:26px">
      <div class="step"><h3>Students submit interest</h3><p>Students let us know they’re interested on this site — this is not an entry. Instructors sign up to receive the nomination form.</p></div>
      <div class="step"><h3>Instructors nominate</h3><p><b>All competitors must be nominated by their cosmetology school instructor</b> — students can’t enter themselves. Past events allowed up to two nominees per program.</p></div>
      <div class="step"><h3>Confirm &amp; sign the release</h3><p>Nominees complete the Affidavit of Eligibility &amp; Release (parent/guardian signs if under 18).</p></div>
      <div class="step"><h3>Compete on event day</h3><p>Check in, set up your station and cut against the clock — two rounds, about 40 minutes each.</p></div>
      <div class="step"><h3>Awards</h3><p>Top three choose a cash prize or an equal-value tool package — plus matching gifts for their schools.</p></div>
    </div>
  </div>
  <div>
    <img src="assets/img/gallery/2025/ctc2025-21.jpg" alt="Competitor working on a haircut" loading="lazy" style="margin-bottom:22px">
    <div class="card">
      <h3>Event-day schedule</h3>
      <p style="color:var(--muted);font-size:.92rem">Based on the 2026 run of show — the 2027 schedule is sent to confirmed competitors.</p>
      <ul class="sched">
        <li><b>12:00 p.m.</b><span>Competitor &amp; educator check-in, swag bags, station setup</span></li>
        <li><b>12:30 p.m.</b><span>Competitor orientation</span></li>
        <li><b>1:00 p.m.</b><span>Welcome from the emcees</span></li>
        <li><b>1:10 p.m.</b><span>Round 1: haircut &amp; style (40 min), then judging</span></li>
        <li><b>2:15 p.m.</b><span>Round 2: haircut (40 min)</span></li>
        <li><b>3:00 p.m.</b><span>Final judging</span></li>
        <li><b>3:20 p.m.</b><span>Winners announced &amp; prizes presented</span></li>
      </ul>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--jade)">Prizes</span><h2>{money(PRIZE_YEAR)} in prizes</h2>
  <p>Each winner chooses a cash prize <b>or</b> a professional tool package of the same value to help start their career. Every student prize is matched by an equal gift to the winner’s school program — as cash or as tools for the classroom.</p></div>
  {prize_cards()}
</div></section>

<section class="band-gray"><div class="wrap grid g2">
  <div class="card">{icon("checkmark")}<h3>Eligibility</h3>
    <ul>
      <li>Currently enrolled in, or recently graduated from, a cosmetology or barbering program in Northeast Ohio.</li>
      <li>Nominated by a cosmetology instructor at your school — students cannot nominate themselves.</li>
      <li>Signed Affidavit of Eligibility &amp; Release — a parent or guardian also signs if you’re under 18.</li>
    </ul></div>
  <div class="card">{icon("chat")}<h3>Spectators &amp; media</h3>
    <p>Family, friends, instructors and classmates are welcome to come cheer — the energy in the room is a big part of the day. No sign-up needed, and light refreshments are provided.</p>
    <p>The event is photographed and filmed, and local media including FOX 8 Cleveland have covered past competitions.</p></div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--jade)">Hosted by</span><h2>Your local Great Clips franchisees</h2>
  <p>Create the Cut is planned, staffed and funded by the independently owned and operated Great Clips salons of {REGION} — not by Great Clips corporate. Franchisees {", ".join(S["hosts"][:-1])} and {S["hosts"][-1]} and their salon teams make it happen every year.</p>
  <p>“This is a growth opportunity for students. It’s also a chance for us to demonstrate to the next generation of stylists that Great Clips is not simply a large haircut chain, but a network of locally owned and operated businesses that invest in their communities, support local students, and hire local talent.” — Alex Harris</p>
  <a class="btn btn-outline" href="https://jobs.greatclips.com" target="_blank" rel="noopener">Explore Great Clips careers</a></div>
</div></section>
{cta_band()}
'''
    page('event.html', f'Event Details | {SITE_NAME}',
         'Date, format, prizes, eligibility and schedule for Create the Cut 2027, the Northeast Ohio student haircut competition.', body)


# ---------------------------------------------------------------- past events
def build_past():
    blocks = []
    for y in YEARS:
        meta = [y['date'], ', '.join(x for x in (y['venue'], y['city']) if x)]
        if y['competitors']: meta.append(f'{y["competitors"]} competitors')
        if y['prize_total']: meta.append(f'{money(y["prize_total"])} awarded')
        tags = ''.join(f'<span class="tag">{e(m)}</span>' for m in meta if m)
        if y['winners']:
            pod = '<div class="podium">' + ''.join(
                f'<div class="winner p{i}">'
                + (f'<img src="{w["photo"]}" data-full="{w["photo"]}" alt="{e(w["name"])}, {w["place"]} place {y["year"]}" loading="lazy" style="border-radius:10px;margin:-6px -6px 16px;width:calc(100% + 12px);aspect-ratio:4/3;object-fit:cover;cursor:zoom-in">' if w.get('photo') else '')
                + f'<div class="medal">{w["place"]}</div><div class="nm">{e(w["name"])}</div><div class="sc">{e(w["school"])}</div>'
                + (f'<div class="amt"><b>{money(w["amount"])}</b> to the student{" (" + ("tool package" if w["choice"] == "tools" else "cash") + ")" if w.get("choice") else ""} + <b>{money(w["amount"])}</b> to the school</div>' if w.get('amount') else '')
                + (f'<div class="amt">{e(w["prize_text"])}</div>' if w.get('prize_text') else '')
                + '</div>' for i, w in enumerate(y['winners'], 1)) + '</div>'
        else:
            pod = f'<div class="pending"><b>{y["year"]} winners</b> — names and schools coming soon.</div>'
        roster = ''
        if y['participants']:
            by_school = {}
            for n, s in y['participants']: by_school.setdefault(s, []).append(n)
            roster = (f'<details class="roster"><summary>All {len(y["participants"])} {y["year"]} competitors</summary><div class="roster-grid">'
                      + ''.join(f'<div><b>{e(n)}</b><span>{e(s)}</span></div>' for n, s in sorted(y['participants'], key=lambda p: p[0].split()[-1]))
                      + '</div></details>'
                      + f'<details class="roster"><summary>{len(by_school)} participating schools</summary><ul class="schools">'
                      + ''.join(f'<li><b>{e(s)}</b> <span>· {len(ns)} student{"s" if len(ns) > 1 else ""}</span></li>' for s, ns in sorted(by_school.items()))
                      + '</ul></details>')
        strip = ''
        if y['gallery'] and y['gallery'] in G:
            pics = G[y['gallery']][:8]
            strip = ('<div class="strip">' + ''.join(f'<img src="{p["thumb"]}" data-full="{p["src"]}" alt="Create the Cut {y["year"]}" loading="lazy">' for p in pics)
                     + f'</div><p style="margin-top:12px"><a href="gallery.html#y{y["year"]}">See all {y["year"]} photos →</a></p>')
        blocks.append(f'''<div class="year" id="y{y["year"]}">
  <div class="year-head"><h2>{y["year"]}</h2><div class="meta">{tags}</div></div>
  <p style="max-width:52rem;font-size:1.08rem">{e(y["summary"])}</p>
  {pod}{roster}{strip}
</div>''')
    ynav = ''.join(f'<a href="#y{y["year"]}">{y["year"]}</a>' for y in YEARS)
    body = f'''
<section class="page-hero">{TRI}<div class="wrap"><span class="eyebrow">Hall of fame</span><h1>Past winners &amp; competitors</h1>
<p>Every year, the region’s best student stylists — and the schools behind them — earn their place here.</p></div></section>
<section><div class="wrap">
  <div class="year-nav">{ynav}</div>
  {'<div class="divider"></div>'.join(blocks)}
</div></section>
{stats_band()}
{cta_band('Your name could be next.', 'Submit your interest, then ask your cosmetology instructor to nominate you.')}
'''
    page('past-events.html', f'Past Winners | {SITE_NAME}',
         'Create the Cut winners, their schools and every student competitor from past Northeast Ohio competitions.', body)


# ---------------------------------------------------------------- gallery
def build_gallery():
    years = [k for k in sorted(G, reverse=True)]
    figs = ''.join(f'<figure data-year="{yr}" id="{"y"+yr if i == 0 else ""}"><img src="{p["thumb"]}" data-full="{p["src"]}" width="{p["w"]}" height="{p["h"]}" alt="Create the Cut {yr}" loading="lazy"><figcaption>{yr}</figcaption></figure>'
                   for yr in years for i, p in enumerate(G[yr]))
    btns = '<button data-year="all" aria-pressed="true">All years</button>' + ''.join(f'<button data-year="{y}" aria-pressed="false">{y}</button>' for y in years)
    vids = ''.join(f'<div class="vid"><video controls preload="none" playsinline poster="{v["poster"]}"><source src="{v["src"]}" type="video/mp4"></video><div class="cap"><b>{e(v["title"])}</b><span>Create the Cut {v["year"]}</span></div></div>' for v in S['videos'])
    vids += ''.join(f'<div class="vid"><iframe class="yt" src="https://www.youtube.com/embed/{v["id"]}" title="{e(v["title"])}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe><div class="cap"><b>{e(v["title"])}</b><span>{e(v["outlet"])} · {e(v["date"])}</span></div></div>' for v in S['news']['youtube'])
    body = f'''
<section class="page-hero">{TRI}<div class="wrap"><span class="eyebrow">Photos &amp; video</span><h1>Relive the action</h1>
<p>The focus, the nerves, the big checks — scenes from past Create the Cut competitions.</p></div></section>
<section><div class="wrap">
  <div class="section-head"><h2>Video</h2></div>
  <div class="videos">{vids}</div>
</div></section>
<section class="band-gray"><div class="wrap">
  <div class="section-head"><h2>Photos</h2><p>Tap any photo to view it full size.</p></div>
  <div class="filters" role="group" aria-label="Filter photos by year">{btns}</div>
  <div class="masonry">{figs}</div>
</div></section>
{cta_band()}
'''
    page('gallery.html', f'Photos & Video | {SITE_NAME}', 'Photos and videos from past Create the Cut student haircut competitions in Northeast Ohio.', body)


# ---------------------------------------------------------------- news
def build_news():
    yt = S['news']['youtube']
    feat = yt[0]
    more_yt = ''.join(f'<div class="vid"><iframe class="yt" src="https://www.youtube.com/embed/{v["id"]}" title="{e(v["title"])}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe><div class="cap"><b>{e(v["title"])}</b><span>{e(v["outlet"])} · {e(v["date"])}</span></div></div>' for v in yt[1:])
    arts = ''.join(f'<a class="card article" href="{a["url"]}" target="_blank" rel="noopener"><span class="src">{e(a["outlet"])}</span><h3>{e(a["title"])}</h3><span class="date">{e(a["date"])}</span><p style="margin-top:10px;color:var(--muted)">{e(a["blurb"])}</p><span class="go">Read the story ↗</span></a>' for a in S['news']['articles'])
    body = f'''
<section class="page-hero">{TRI}<div class="wrap"><span class="eyebrow">Press</span><h1>In the news</h1>
<p>Create the Cut on FOX 8 Cleveland and beyond.</p></div></section>
<section><div class="wrap">
  <div class="feature-video">
    <iframe class="yt" src="https://www.youtube.com/embed/{feat["id"]}" title="{e(feat["title"])}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    <div><span class="eyebrow" style="color:var(--jade)">{e(feat["outlet"])}</span><h2>{e(feat["title"])}</h2>
    <p>Dozens of cosmetology students from public and private programs packed the room for Create the Cut 2025, competing for $1,000 toward tuition or professional tools — plus $1,000 for their school’s program.</p></div>
  </div>
  {f'<div class="videos" style="margin-top:32px">{more_yt}</div>' if more_yt else ''}
</div></section>
<section class="band-gray"><div class="wrap">
  <div class="section-head"><h2>Stories</h2></div>
  <div class="grid g3">{arts}</div>
</div></section>
'''
    page('news.html', f'In the News | {SITE_NAME}', 'FOX 8 Cleveland and other news coverage of the Create the Cut student haircut competition.', body)


# ---------------------------------------------------------------- FAQ
FAQ = [
    ('About the event', [
        ('What is Create the Cut?', 'A haircutting competition for Northeast Ohio cosmetology and barbering students. Instructor-nominated students compete through two timed rounds on mannequins, and the top three win cash prizes — with a matching gift to each winner’s school.'),
        ('Who runs it?', f'The independently owned and operated Great Clips salons of {REGION}. Local franchisees and their salon teams plan, staff and fund the entire event.'),
        ('When and where is the 2027 competition?', f'{e(EV["headline_date"])}, at the {e(EV["venue"])}, {e(EV["venue_detail"])}. <a href="{EV["ics"]}" download>Add it to your calendar</a> and <a href="signup.html">join the interest list</a> for nomination details and the start time.'),
        ('How long does it last?', 'Plan on an afternoon. In 2026, check-in opened at noon, the competition started at 1:00 and winners were announced around 3:20.'),
        ('Can family and friends come watch?', 'Yes! Spectators are welcome — no sign-up needed — and light refreshments are provided. The cheering section is a big part of the fun.'),
    ]),
    ('Competing', [
        ('Who is eligible?', 'Students currently enrolled in — or recently graduated from — a cosmetology or barbering program in Northeast Ohio, who are nominated by an instructor at their school.'),
        ('How do I enter?', 'Students can’t enter themselves — <b>all nominations must come from cosmetology school instructors</b>. Fill out the <a href="signup.html?role=student">student interest form</a> so we know you’re interested, then let your instructor know you want to compete. Instructors can sign up <a href="signup.html?role=instructor">here</a> to receive the nomination form.'),
        ('Does the student interest form enter me in the competition?', 'No. The student form only tells us you’re interested so we can keep you posted. To compete, you must be nominated by your cosmetology school instructor.'),
        ('How many students can each school send?', 'In past years each program could nominate up to two students. The 2027 limit will be shared when nominations open.'),
        ('Does it cost anything to compete?', 'No — there is no entry fee.'),
        ('What will I have to cut?', 'Competitors work on mannequins through two timed rounds of about 40 minutes each: a haircut and style, then a second haircut.'),
        ('How is it judged?', 'A panel of judges scores each round right after time is called. Combined scores decide 1st, 2nd and 3rd.'),
        ('What do I need to bring?', 'Confirmed competitors receive a packet with the rules, supply list and check-in details before the event.'),
        ('I’m under 18 — can I still compete?', 'Yes. Every competitor signs an Affidavit of Eligibility & Release, and a parent or guardian also signs if you’re under 18.'),
    ]),
    ('Prizes', [
        ('What are the prizes?', f'1st place: {money(S["prizes"][0]["student"])} · 2nd place: {money(S["prizes"][1]["student"])} · 3rd place: {money(S["prizes"][2]["student"])}. Each winner’s school receives a matching gift of the same amount.'),
        ('Can I take tools instead of cash?', 'Yes. Winners choose either the cash prize or a professional tool package of equal value to help start their career. Schools can likewise take their matching gift as cash or as tools for their program.'),
        ('How much has been awarded so far?', f'More than {money(AWARDED)} has gone to student winners and their schools across recent competitions — all funded by local Great Clips franchisees.'),
    ]),
    ('Schools & more', [
        ('I’m an instructor. How do I get my program involved?', 'Sign up on the <a href="signup.html?role=instructor">interest form</a> and we’ll email you the nomination form as soon as nominations open. Nominations are accepted from instructors only.'),
        ('Will there be photos and video?', 'Yes. The event is professionally photographed and filmed, and local media have covered past competitions. See the <a href="gallery.html">gallery</a> and <a href="news.html">news</a> pages.'),
        ('Does competing lead to a job at Great Clips?', 'There’s no obligation, but many franchisees are hiring and love meeting new talent. Explore openings at <a href="https://jobs.greatclips.com" target="_blank" rel="noopener">jobs.greatclips.com</a>.'),
    ]),
]


def build_faq():
    secs = ''.join(f'<h2>{h}</h2>' + ''.join(f'<details><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in qs) for h, qs in FAQ)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for _, qs in FAQ for q, a in qs]}
    body = f'''
<section class="page-hero">{TRI}<div class="wrap"><span class="eyebrow">FAQs</span><h1>Questions? Answers.</h1>
<p>Can’t find what you need? <a href="signup.html" style="color:var(--lime)">Send us a note</a> on the sign-up form.</p></div></section>
<section><div class="wrap faq">{secs}</div></section>
<script type="application/ld+json">{json.dumps(ld)}</script>
{cta_band()}
'''
    page('faq.html', f'FAQs | {SITE_NAME}', 'Frequently asked questions about Create the Cut — eligibility, nominations, prizes, judging and event day.', body)


# ---------------------------------------------------------------- sign-up
def build_signup():
    endpoint = S.get('form_endpoint', '')
    roles = [('student', 'Student', 'I’m interested in competing'), ('instructor', 'Instructor / school', 'I’ll nominate my students')]
    role_html = ''.join(f'<label><input type="radio" name="role" value="{v}" required><span>{t}<small>{s}</small></span></label>' for v, t, s in roles)
    body = f'''
<section class="page-hero">{TRI}<div class="wrap"><span class="eyebrow">Create the Cut 2027</span><h1>Join the interest list</h1>
<p><b>Students:</b> this form lets us know you’re interested — it is not an entry. All competitors must be nominated by their cosmetology school instructor.<br><b>Instructors:</b> sign up to receive the nomination form and event details.</p></div></section>
<section class="band-gray"><div class="wrap form-wrap">
<form class="signup" data-endpoint="{e(endpoint)}">
  <fieldset><legend>I am a…</legend><div class="roles">{role_html}</div>
    <p class="role-only role-note" data-roles="student">Submitting this form <b>does not enter you</b> in Create the Cut. It tells us you’re interested so we can keep you posted. To compete, ask your cosmetology instructor to nominate you once nominations open.</p>
    <p class="role-only role-note" data-roles="instructor">We’ll email you the official nomination form as soon as nominations open. Only instructors can nominate students.</p>
  </fieldset>
  <fieldset><legend>About you</legend>
  <div class="fields">
    <div class="field"><label for="f-first">First name</label><input id="f-first" name="first_name" type="text" autocomplete="given-name" required></div>
    <div class="field"><label for="f-last">Last name</label><input id="f-last" name="last_name" type="text" autocomplete="family-name" required></div>
    <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="f-phone">Mobile phone <i>(optional)</i></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field full role-only" data-roles="student instructor"><label for="f-school">School / program name</label><input id="f-school" name="school" type="text" data-req="1" placeholder="e.g. Auburn Career Center"></div>
    <div class="field role-only" data-roles="student instructor"><label for="f-type">Program type</label>
      <select id="f-type" name="program_type"><option value="">Choose…</option><option>Cosmetology — high school</option><option>Cosmetology — adult education</option><option>Cosmetology — private beauty school</option><option>Barbering</option><option>Other</option></select></div>
    <div class="field role-only" data-roles="student"><label for="f-grad">Expected graduation</label><input id="f-grad" name="expected_graduation" type="text" placeholder="e.g. May 2027"></div>
    <div class="field role-only" data-roles="instructor"><label for="f-n">Students you may nominate</label><select id="f-n" name="students_to_nominate"><option value="">Choose…</option><option>1</option><option>2</option><option>Not sure yet</option></select></div>
    <div class="field role-only" data-roles="student"><label for="f-age">Will you be 18+ on event day?</label><select id="f-age" name="adult_on_event_day"><option value="">Choose…</option><option>Yes</option><option>No</option></select></div>
    <div class="field role-only" data-roles="instructor student"><label for="f-instr">Instructor name <i>(optional)</i></label><input id="f-instr" name="instructor_name" type="text"></div>
    <div class="field"><label for="f-city">City</label><input id="f-city" name="city" type="text" autocomplete="address-level2"></div>
    <div class="field full"><label for="f-heard">How did you hear about Create the Cut?</label>
      <select id="f-heard" name="heard_about"><option value="">Choose…</option><option>My instructor / school</option><option>A Great Clips salon</option><option>FOX 8 / news</option><option>Social media</option><option>I competed or attended before</option><option>Friend or family</option><option>Other</option></select></div>
    <div class="field full"><label for="f-notes">Anything else? <i>(optional)</i></label><textarea id="f-notes" name="notes" placeholder="Questions for the organizers, etc."></textarea></div>
  </div></fieldset>
  <label class="check"><input type="checkbox" name="consent" value="yes" required><span>Yes, email me (and text me if I gave a phone number) about Create the Cut. I can opt out anytime.</span></label>
  <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div style="margin-top:22px"><button class="btn btn-jade" type="submit">Submit my interest</button></div>
  <div class="form-msg" role="status" aria-live="polite"></div>
</form>
<aside class="aside-card">
  <h3>Why compete?</h3>
  <div class="big">{money(PRIZE_TOP)}</div><p style="color:#dcebe6">top student prize — take it as cash or an equal-value tool package, plus a matching {money(S["prizes"][0]["school"])} for your school</p>
  <ul><li>Show your skills in front of judges, family and media</li><li>Meet local salon owners who are hiring</li><li>Free to compete</li></ul>
  <p style="color:#fff;font-size:.92rem;margin:0;padding:14px;border-radius:10px;background:rgba(255,255,255,.1)"><b>Students:</b> this form is not an entry. All competitors must be nominated by their cosmetology school instructor.</p>
</aside>
</div></section>
'''
    page('signup.html', f'Sign Up | {SITE_NAME}', 'Join the Create the Cut 2027 interest list — for cosmetology and barbering students and their instructors.', body)


if __name__ == '__main__':
    build_home(); build_event(); build_past(); build_gallery(); build_news(); build_faq(); build_signup()
