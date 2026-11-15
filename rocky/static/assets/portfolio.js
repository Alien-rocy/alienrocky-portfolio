/* AlienR portfolio — progressive enhancement. No dependencies. */
(function () {
  'use strict';
  var doc = document;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function getCookie(name) {
    var v = null;
    doc.cookie.split(';').forEach(function (c) {
      c = c.trim();
      if (c.indexOf(name + '=') === 0) v = decodeURIComponent(c.substring(name.length + 1));
    });
    return v;
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function setHidden(el, v) { if (v) el.setAttribute('hidden', ''); else el.removeAttribute('hidden'); }

  /* NAV: mobile menu ------------------------------------------------------ */
  var nav = $('#nav'), toggle = $('#nav-toggle'), links = $('#nav-links');
  function setMenu(open) {
    if (!toggle) return;
    links.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    setHidden($('.menu-open', toggle), open);
    setHidden($('.menu-close', toggle), !open);
  }
  if (toggle) {
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    $$('a', links).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setMenu(false); } });
    doc.addEventListener('click', function (e) {
      if (toggle.getAttribute('aria-expanded') === 'true' && !links.contains(e.target) && !toggle.contains(e.target)) setMenu(false);
    });
    window.matchMedia('(min-width: 960px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* NAV: scroll-spy ------------------------------------------------------- */
  var spyLinks = $$('[data-spy]');
  var sections = spyLinks.map(function (a) { return doc.getElementById(a.getAttribute('data-spy')); }).filter(Boolean);
  if (sections.length && 'IntersectionObserver' in window) {
    var current = null;
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) current = en.target.id; });
      spyLinks.forEach(function (a) {
        if (a.getAttribute('data-spy') === current) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* THEME ----------------------------------------------------------------- */
  var themeBtn = $('#theme-toggle');
  function paintTheme() {
    var dark = doc.documentElement.getAttribute('data-theme') === 'dark';
    if (!themeBtn) return;
    setHidden($('.theme-moon', themeBtn), dark);
    setHidden($('.theme-sun', themeBtn), !dark);
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    var meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', dark ? '#0b0f17' : '#ffffff');
  }
  if (themeBtn) {
    paintTheme();
    themeBtn.addEventListener('click', function () {
      var next = doc.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      doc.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      paintTheme();
    });
  }

  /* REVEAL ---------------------------------------------------------------- */
  var revealEls = $$('.reveal');
  if (revealEls.length) {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      revealEls.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -5% 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
    }
  }

  /* TECH ICON FALLBACK: if the logo CDN is unreachable, swap in the built-in icon */
  doc.addEventListener('error', function (e) {
    var t = e.target;
    if (t && t.tagName === 'IMG' && t.hasAttribute('data-fallback-icon')) {
      var ns = 'http://www.w3.org/2000/svg';
      var svg = doc.createElementNS(ns, 'svg'), use = doc.createElementNS(ns, 'use');
      use.setAttribute('href', '#' + t.getAttribute('data-fallback-icon'));
      svg.appendChild(use); t.replaceWith(svg);
    }
  }, true);

  /* PROJECT DETAIL DIALOGS ------------------------------------------------- */
  $$('[data-open]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var d = doc.getElementById(btn.getAttribute('data-open'));
      if (d && d.showModal) { d.showModal(); }
    });
  });
  $$('dialog.modal').forEach(function (d) {
    d.addEventListener('click', function (e) { if (e.target === d || e.target.closest('[data-close]')) d.close(); });
  });

  /* FORMS ------------------------------------------------------------------ */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function setError(input, msg) {
    var err = doc.getElementById(input.getAttribute('aria-describedby'));
    if (err) err.textContent = msg || '';
    if (msg) input.setAttribute('aria-invalid', 'true'); else input.removeAttribute('aria-invalid');
  }
  function validate(form) {
    var name = form.elements.name, email = form.elements.email, message = form.elements.message;
    var ok = true, first = null;
    function fail(el, msg) { setError(el, msg); ok = false; if (!first) first = el; }
    var n = name.value.trim(), em = email.value.trim(), m = message.value.trim();
    if (n.length < 2) fail(name, 'Please enter your name.'); else setError(name, '');
    if (!em) { if (email.required) fail(email, 'Please enter your email address.'); else setError(email, ''); }
    else if (!EMAIL_RE.test(em)) fail(email, 'That email address doesn’t look right.');
    else setError(email, '');
    if (m.length < 10) fail(message, 'Please write at least 10 characters so I know how to help.');
    else if (m.length > 3000) fail(message, 'Please keep the message under 3,000 characters.');
    else setError(message, '');
    if (first) first.focus();
    return ok;
  }

  var cform = $('#contact-form');
  if (cform) {
    var status = $('#contact-status'), submit = $('#contact-submit');
    ['name', 'email', 'message'].forEach(function (k) {
      cform.elements[k].addEventListener('input', function () { if (this.getAttribute('aria-invalid')) setError(this, ''); });
    });
    cform.addEventListener('submit', function (e) {
      e.preventDefault();
      status.textContent = ''; status.removeAttribute('data-state');
      if (!validate(cform)) { status.textContent = 'Please fix the highlighted fields.'; status.setAttribute('data-state', 'error'); return; }
      submit.disabled = true;
      status.textContent = 'Sending…'; status.setAttribute('data-state', 'pending');
      fetch(cform.action, {
        method: 'POST',
        body: new FormData(cform),
        credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCookie('csrftoken') || cform.elements.csrfmiddlewaretoken.value, 'X-Requested-With': 'XMLHttpRequest' }
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (data) { return { ok: r.ok, data: data }; });
      }).then(function (res) {
        if (res.ok && res.data.ok !== false) {
          cform.reset();
          status.textContent = 'Thanks! Your message was sent. I’ll reply by email.';
          status.setAttribute('data-state', 'ok');
        } else {
          var errs = (res.data && res.data.errors) || {};
          Object.keys(errs).forEach(function (k) { if (cform.elements[k]) setError(cform.elements[k], errs[k]); });
          status.textContent = (res.data && res.data.message) ? res.data.message.replace(/^[^\w]+/, '') : 'Something went wrong. Please try again.';
          status.setAttribute('data-state', 'error');
        }
      }).catch(function () {
        status.textContent = 'Network error. Please try again, or email me directly.';
        status.setAttribute('data-state', 'error');
      }).then(function () { submit.disabled = false; });
    });
  }

  var sform = $('#subscribe-form');
  if (sform) {
    var smsg = $('#subscribe-msg');
    sform.addEventListener('submit', function (e) {
      e.preventDefault();
      var em = sform.elements.email.value.trim();
      if (!EMAIL_RE.test(em)) { smsg.textContent = 'Please enter a valid email address.'; return; }
      smsg.textContent = 'Subscribing…';
      fetch(sform.action, {
        method: 'POST', body: new FormData(sform), credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCookie('csrftoken') || sform.elements.csrfmiddlewaretoken.value, 'X-Requested-With': 'XMLHttpRequest' }
      }).then(function (r) { if (!r.ok) throw new Error(); return r.json(); })
        .then(function (d) { smsg.textContent = (d.message || 'Subscribed.').replace(/^[^\w]+/, ''); if (d.message && d.message.indexOf('✅') > -1) sform.reset(); })
        .catch(function () { smsg.textContent = 'Could not subscribe right now. Please try again later.'; });
    });
  }

  /* PROJECTS PAGE: category filter, testimonials ---------------------------- */
  $$('.filter').forEach(function (btn) {
    btn.addEventListener('click', function () {
      $$('.filter').forEach(function (b) { b.classList.remove('is-active'); b.setAttribute('aria-pressed', 'false'); });
      btn.classList.add('is-active'); btn.setAttribute('aria-pressed', 'true');
      var f = btn.getAttribute('data-filter');
      $$('[data-category]').forEach(function (c) { c.hidden = !(f === 'all' || c.getAttribute('data-category') === f); });
    });
  });

  var more = $('#load-more');
  if (more) {
    more.addEventListener('click', function () {
      var page = parseInt(more.getAttribute('data-page'), 10);
      more.disabled = true; more.textContent = 'Loading…';
      fetch(more.getAttribute('data-url') + '?page=' + page, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var grid = $('#reviews');
          data.testimonials.forEach(function (t) {
            grid.insertAdjacentHTML('beforeend',
              '<article class="review"><blockquote>' + esc(t.message) + '</blockquote><footer><span class="avatar" aria-hidden="true">' +
              esc(t.name.substring(0, 2).toUpperCase()) + '</span><div><strong>' + esc(t.name) + '</strong><small>' + esc(t.created_at) + '</small></div></footer></article>');
          });
          if (data.has_next) { more.setAttribute('data-page', page + 1); more.disabled = false; more.textContent = 'Load more'; }
          else more.parentElement.remove();
        })
        .catch(function () { more.disabled = false; more.textContent = 'Try again'; });
    });
  }

  var tform = $('#testimonial-form');
  if (tform) {
    var tmsg = $('#testimonial-status');
    tform.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(tform)) { tmsg.textContent = 'Please fix the highlighted fields.'; tmsg.setAttribute('data-state', 'error'); return; }
      tmsg.textContent = 'Submitting…'; tmsg.setAttribute('data-state', 'pending');
      fetch(tform.action, {
        method: 'POST', body: new FormData(tform), credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCookie('csrftoken') || tform.elements.csrfmiddlewaretoken.value, 'X-Requested-With': 'XMLHttpRequest' }
      }).then(function (r) { if (!r.ok) throw new Error(); return r.json(); })
        .then(function (d) {
          tmsg.textContent = d.status === 'Approved' ? 'Thanks! Your testimonial has been published.' : 'Thanks! Your testimonial is pending review.';
          tmsg.setAttribute('data-state', 'ok'); tform.reset();
        })
        .catch(function () { tmsg.textContent = 'Something went wrong. Please try again.'; tmsg.setAttribute('data-state', 'error'); });
    });
  }
})();
