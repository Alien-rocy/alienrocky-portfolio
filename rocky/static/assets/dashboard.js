/* Dashboard behaviour: drawer, confirm-before-delete. Theme toggle comes from portfolio.js. */
(function () {
  'use strict';
  var side = document.getElementById('dash-side'), scrim = document.getElementById('dash-scrim'), btn = document.getElementById('dash-menu');
  function set(open) {
    if (!side) return;
    side.classList.toggle('is-open', open); scrim.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (btn) {
    btn.addEventListener('click', function () { set(!side.classList.contains('is-open')); });
    scrim.addEventListener('click', function () { set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-confirm]');
    if (a && !window.confirm(a.getAttribute('data-confirm'))) e.preventDefault();
  });

  /* Overview charts (data comes from data-* attributes; no inline template JS) */
  var el = document.getElementById('dash-charts');
  if (el && !window.Chart) {
    var d0 = el.dataset;
    [['chart-testimonials', d0.approved + ' approved, ' + d0.pending + ' pending'], ['chart-activity', d0.projects + ' projects, ' + d0.messages + ' messages, ' + d0.subs + ' subscribers, ' + d0.testimonials + ' testimonials']].forEach(function (x) {
      var c = document.getElementById(x[0]); if (c) c.parentNode.innerHTML = '<p class="label">' + x[1] + '</p>';
    });
  }
  if (el && window.Chart) {
    var css = getComputedStyle(document.documentElement);
    var v = function (n) { return css.getPropertyValue(n).trim(); };
    var blue = v('--blue'), border = v('--border'), muted = v('--text-2');
    var d = el.dataset;
    new Chart(document.getElementById('chart-testimonials'), {
      type: 'doughnut',
      data: { labels: ['Approved', 'Pending'], datasets: [{ data: [+d.approved, +d.pending], backgroundColor: [blue, border], borderWidth: 0 }] },
      options: { maintainAspectRatio: false, cutout: '68%', plugins: { legend: { position: 'bottom', labels: { color: muted, boxWidth: 10, font: { family: 'IBM Plex Mono', size: 11 } } } } }
    });
    new Chart(document.getElementById('chart-activity'), {
      type: 'bar',
      data: { labels: ['Projects', 'Subscriptions', 'Messages', 'Testimonials'], datasets: [{ data: [+d.projects, +d.subs, +d.messages, +d.testimonials], backgroundColor: blue, borderRadius: 4, maxBarThickness: 36 }] },
      options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0, color: muted }, grid: { color: border } }, x: { ticks: { color: muted }, grid: { display: false } } } }
    });
  }
})();
