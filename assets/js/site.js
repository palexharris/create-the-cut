// Create the Cut — nav, lightbox, gallery filter, countdown, sign-up form.
(function () {
  // mobile nav
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });

  // lightbox over any img[data-full]
  var box = document.querySelector('.lightbox');
  if (box) {
    var img = box.querySelector('img'), list = [], idx = 0;
    function visible() { return [].slice.call(document.querySelectorAll('img[data-full]')).filter(function (el) { return el.offsetParent !== null; }); }
    function show(i) { idx = (i + list.length) % list.length; img.src = list[idx].dataset.full; img.alt = list[idx].alt; }
    document.addEventListener('click', function (e) {
      var t = e.target.closest('img[data-full]');
      if (!t) return;
      list = visible(); show(list.indexOf(t));
      box.classList.add('open'); box.querySelector('.x').focus();
    });
    function close() { box.classList.remove('open'); img.src = ''; }
    box.querySelector('.x').onclick = close;
    box.querySelector('.prev').onclick = function () { show(idx - 1); };
    box.querySelector('.next').onclick = function () { show(idx + 1); };
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  // gallery year filter
  var filters = document.querySelectorAll('.filters button');
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      filters.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      var y = b.dataset.year;
      document.querySelectorAll('.masonry figure').forEach(function (f) {
        f.style.display = (y === 'all' || f.dataset.year === y) ? '' : 'none';
      });
    });
  });

  // countdown (only rendered when a date is set in data/site.json)
  var cd = document.querySelector('.countdown');
  if (cd) {
    var end = new Date(cd.dataset.to).getTime();
    var tick = function () {
      var s = Math.max(0, Math.floor((end - Date.now()) / 1000));
      cd.querySelector('[data-d]').textContent = Math.ceil(s / 86400);
      var h = cd.querySelector('[data-h]'), m = cd.querySelector('[data-m]');
      if (h) h.textContent = Math.floor(s % 86400 / 3600);
      if (m) m.textContent = Math.floor(s % 3600 / 60);
    };
    tick(); setInterval(tick, 30000);
  }

  // sign-up form
  var form = document.querySelector('form.signup');
  if (!form) return;
  var msg = form.querySelector('.form-msg');
  function syncRole() {
    var r = (form.querySelector('input[name=role]:checked') || {}).value || '';
    form.querySelectorAll('.role-only').forEach(function (el) {
      var on = el.dataset.roles.split(' ').indexOf(r) > -1;
      el.style.display = on ? 'block' : 'none';
      el.querySelectorAll('input,select').forEach(function (i) { if (i.dataset.req) i.required = on; });
    });
  }
  form.addEventListener('change', function (e) { if (e.target.name === 'role') syncRole(); });
  syncRole();
  var pre = new URLSearchParams(location.search).get('role');
  if (pre) { var r = form.querySelector('input[name=role][value="' + pre + '"]'); if (r) { r.checked = true; syncRole(); } }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    msg.className = 'form-msg';
    if (form.website.value) return; // honeypot
    var endpoint = form.dataset.endpoint;
    if (!endpoint) {
      msg.className = 'form-msg info';
      msg.textContent = 'Thanks! Online sign-up is opening very soon — please check back in a few days.';
      return;
    }
    var data = new URLSearchParams(new FormData(form));
    data.append('submitted_from', location.href);
    var b = form.querySelector('button[type=submit]');
    b.disabled = true; b.textContent = 'Sending…';
    // Apps Script web apps don't send CORS headers; no-cors posts still land in the sheet.
    fetch(endpoint, { method: 'POST', mode: 'no-cors', body: data })
      .then(function () {
        form.reset(); syncRole();
        msg.className = 'form-msg ok';
        msg.textContent = 'You’re on the list! We’ll email you as soon as 2027 details and nominations open.';
        msg.scrollIntoView({ block: 'center', behavior: 'smooth' });
      })
      .catch(function () {
        msg.className = 'form-msg err';
        msg.textContent = 'Something went wrong sending your info. Please check your connection and try again.';
      })
      .finally(function () { b.disabled = false; b.textContent = 'Count me in'; });
  });
})();
