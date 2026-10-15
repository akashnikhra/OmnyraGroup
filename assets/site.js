/* OMNyra Group - shared behaviour for program, hub and legal pages.
   Theme key matches the homepage: localStorage "omnyra-theme" = "dark" | "light".
   The <head> of each page applies the saved theme before paint; this file
   wires the toggle, the mobile menu and the scroll reveals. */
(function () {
  var root = document.documentElement;
  var KEY = 'omnyra-theme';

  function setLogos(theme) {
    var src = theme === 'light' ? '/Website/img/primary-logo-transparent.png' : '/Website/img/Monochrome_white-transparent.png';
    document.querySelectorAll('img[data-logo]').forEach(function (img) { img.src = src; });
  }

  function applyTheme(theme) {
    if (theme === 'light') root.setAttribute('data-theme', 'light');
    else root.removeAttribute('data-theme');
    setLogos(theme);
    try { localStorage.setItem(KEY, theme); } catch (e) {}
  }

  var current = 'dark';
  try { current = localStorage.getItem(KEY) === 'light' ? 'light' : 'dark'; } catch (e) {}
  setLogos(current);

  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      current = current === 'light' ? 'dark' : 'light';
      applyTheme(current);
    });
  });

  // Mobile menu
  var menuBtn = document.querySelector('[data-menu-btn]');
  var panel = document.getElementById('mobile-panel');
  if (menuBtn && panel) {
    function setOpen(open) {
      panel.setAttribute('data-open', open ? 'true' : 'false');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    }
    menuBtn.addEventListener('click', function () {
      setOpen(panel.getAttribute('data-open') !== 'true');
    });
    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  // Scroll reveal: content is visible by default; only hidden once JS runs.
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  items.forEach(function (el) { io.observe(el); });
})();
