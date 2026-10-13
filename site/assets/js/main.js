/* Encon Engineering Solutions — main.js (no dependencies) */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- header: shadow on scroll + back-to-top ---------- */
  var header = $('.header'), toTop = $('.to-top');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (toTop) toTop.classList.toggle('show', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }); });

  /* ---------- mobile nav ---------- */
  var burger = $('.burger');
  if (burger) {
    var setNav = function (open) {
      document.body.classList.toggle('nav-open', open);
      burger.setAttribute('aria-expanded', open);
    };
    burger.addEventListener('click', function () { setNav(!document.body.classList.contains('nav-open')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
    document.addEventListener('click', function (e) {
      if (document.body.classList.contains('nav-open') && !e.target.closest('.nav') && !e.target.closest('.burger')) setNav(false);
    });
    $$('.nav a').forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });
  }

  /* ---------- hero slider ---------- */
  var slides = $$('.slide'), msgs = $$('.hero-msg'), dots = $$('.hero-dots button');
  if (slides.length > 1) {
    var cur = 0, timer;
    var go = function (n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
      msgs.forEach(function (m, i) { m.classList.toggle('active', i === cur); });
      dots.forEach(function (d, i) { d.setAttribute('aria-current', i === cur); });
    };
    var play = function () { clearInterval(timer); if (!reduced) timer = setInterval(function () { go(cur + 1); }, 6500); };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); play(); }); });
    play();
  }

  /* ---------- reveal on scroll ---------- */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else reveals.forEach(function (el) { el.classList.add('in'); });

  /* ---------- counters ---------- */
  var counters = $$('[data-count]');
  var runCount = function (el) {
    var end = +el.getAttribute('data-count'), suf = el.getAttribute('data-suffix') || '', t0 = null;
    if (reduced) { el.textContent = end + suf; return; }
    var tick = function (t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1800, 1), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
      el.textContent = v + suf;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { runCount(e.target); cio.unobserve(e.target); } });
    }, { threshold: .5 });
    counters.forEach(function (c) { cio.observe(c); });
  } else counters.forEach(runCount);

  /* ---------- tabs (technologies) ---------- */
  $$('[role="tablist"]').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    var select = function (tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowUp' || k === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); n.focus(); select(n); }
      });
    });
  });

  /* ---------- filter buttons (gallery + project table) ---------- */
  $$('.filters').forEach(function (bar) {
    var target = $(bar.getAttribute('data-target'));
    if (!target) return;
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      $$('button', bar).forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      target.setAttribute('data-filter', b.getAttribute('data-filter'));
      applyFilter(target);
    });
  });
  var search = $('#project-search');
  if (search) search.addEventListener('input', function () { applyFilter($(search.getAttribute('data-target'))); });

  function applyFilter(target) {
    var f = target.getAttribute('data-filter') || 'all';
    var q = search && search.getAttribute('data-target') === '#' + target.id ? search.value.trim().toLowerCase() : '';
    var shown = 0;
    $$('[data-cat]', target).forEach(function (el) {
      var okCat = f === 'all' || el.getAttribute('data-cat').split(' ').indexOf(f) > -1;
      var okQ = !q || el.textContent.toLowerCase().indexOf(q) > -1;
      el.classList.toggle('hide', !(okCat && okQ));
      if (okCat && okQ) shown++;
    });
    var note = $('[data-count-for="#' + target.id + '"]');
    if (note) note.textContent = shown ? 'Showing ' + shown + ' project' + (shown === 1 ? '' : 's') : 'No projects match that search.';
  }

  /* ---------- lightbox ---------- */
  var zoomables = $$('[data-zoom]');
  if (zoomables.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Image viewer');
    lb.innerHTML = '<button class="lb-btn lb-close" aria-label="Close"><svg class="icon"><use href="#i-x"/></svg></button>' +
      '<button class="lb-btn lb-prev" aria-label="Previous image"><svg class="icon"><use href="#i-left"/></svg></button>' +
      '<figure><img alt=""><figcaption></figcaption></figure>' +
      '<button class="lb-btn lb-next" aria-label="Next image"><svg class="icon"><use href="#i-right"/></svg></button>';
    document.body.appendChild(lb);
    var lbImg = $('img', lb), lbCap = $('figcaption', lb), idx = 0, lastFocus = null;
    var visible = function () { return zoomables.filter(function (z) { return !z.closest('.hide'); }); };
    var show = function (i) {
      var list = visible(); idx = (i + list.length) % list.length;
      var el = list[idx], img = el.tagName === 'IMG' ? el : $('img', el);
      lbImg.src = el.getAttribute('data-zoom') || img.src;
      lbImg.alt = img.alt;
      lbCap.textContent = el.getAttribute('data-caption') || img.alt;
    };
    var open = function (el) { lastFocus = el; show(visible().indexOf(el)); lb.classList.add('open'); $('.lb-close', lb).focus(); };
    var close = function () { lb.classList.remove('open'); if (lastFocus) lastFocus.focus(); };
    zoomables.forEach(function (z) {
      z.tabIndex = 0;
      z.addEventListener('click', function () { open(z); });
      z.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(z); } });
    });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', function () { show(idx - 1); });
    $('.lb-next', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ---------- testimonials ---------- */
  var testis = $$('.testi');
  if (testis.length > 1) {
    var ti = 0, tt;
    var tgo = function (n) { ti = (n + testis.length) % testis.length; testis.forEach(function (t, i) { t.classList.toggle('active', i === ti); }); };
    var tplay = function () { clearInterval(tt); if (!reduced) tt = setInterval(function () { tgo(ti + 1); }, 7000); };
    $('.t-prev').addEventListener('click', function () { tgo(ti - 1); tplay(); });
    $('.t-next').addEventListener('click', function () { tgo(ti + 1); tplay(); });
    tplay();
  }

  /* ---------- services sub-nav highlight ---------- */
  var subLinks = $$('.svc-nav a');
  if (subLinks.length && 'IntersectionObserver' in window) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        subLinks.forEach(function (a) {
          var on = a.getAttribute('href') === '#' + e.target.id;
          a.classList.toggle('on', on);
          if (on && a.scrollIntoView) a.parentNode.parentNode.scrollLeft = a.offsetLeft - 20;
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    subLinks.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) sio.observe(s); });
  }

  /* ---------- enquiry form: honest mailto / WhatsApp composer ---------- */
  var ENQUIRY_TO = 'encon417@gmail.com', WA = '919448111405';
  var form = document.getElementById('enquiry');
  if (form) {
    var compose = function () {
      var v = function (id) { return ($('#' + id, form).value || '').trim(); };
      var name = v('f-name'), org = v('f-org'), phone = v('f-phone'), email = v('f-email'), svc = v('f-service'), msg = v('f-msg');
      var note = $('#form-note');
      if (!name || !msg || (!phone && !email)) {
        note.classList.remove('sent');
        note.textContent = 'Please add your name, a phone number or email, and a line about your requirement.';
        (!name ? $('#f-name', form) : !msg ? $('#f-msg', form) : $('#f-phone', form)).focus();
        return null;
      }
      return {
        subject: 'Enquiry' + (svc ? ': ' + svc : '') + ' from ' + name + (org ? ' (' + org + ')' : ''),
        body: msg + '\n\n' + name + (org ? '\n' + org : '') + (phone ? '\nPhone: ' + phone : '') + (email ? '\nEmail: ' + email : ''),
        note: note
      };
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var c = compose(); if (!c) return;
      window.location.href = 'mailto:' + ENQUIRY_TO + '?subject=' + encodeURIComponent(c.subject) + '&body=' + encodeURIComponent(c.body);
      c.note.textContent = 'Your email app should now open with the enquiry drafted. Press send there and it reaches ' + ENQUIRY_TO + '.';
      c.note.classList.add('sent');
    });
    var waBtn = $('#send-wa');
    if (waBtn) waBtn.addEventListener('click', function () {
      var c = compose(); if (!c) return;
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(c.subject + '\n\n' + c.body), '_blank', 'noopener');
      c.note.textContent = 'WhatsApp opened in a new tab with your message ready to send.';
      c.note.classList.add('sent');
    });
  }

  /* ---------- footer year ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
