/* ========== Coinlytics — Vanilla JS ========== */

// Sticky navbar shadow
const nav = document.querySelector('.nav');
const onScroll = () => {
  if (!nav) return;
  nav.classList.toggle('scrolled', window.scrollY > 20);
};
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

// Mobile menu
const burger = document.querySelector('.hamburger');
const links = document.querySelector('.nav-links');
const toggleMenu = () => {
  burger?.classList.toggle('open');
  links?.classList.toggle('mobile-open');
};
burger?.addEventListener('click', toggleMenu);
document.querySelectorAll('.nav-links a').forEach((a) =>
  a.addEventListener('click', () => {
    burger?.classList.remove('open');
    links?.classList.remove('mobile-open');
  })
);

// Reveal on scroll
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  },
  { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// Animate category bars when in view
const bars = document.querySelectorAll('.cat .bar > div');
const barIo = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        const el = e.target;
        el.style.width = el.dataset.w || '0%';
        barIo.unobserve(el);
      }
    });
  },
  { threshold: 0.3 }
);
bars.forEach((b) => barIo.observe(b));

// Feature card cursor glow
document.querySelectorAll('.feature').forEach((card) => {
  card.addEventListener('mousemove', (ev) => {
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', `${ev.clientX - r.left}px`);
    card.style.setProperty('--my', `${ev.clientY - r.top}px`);
  });
});

//toggle
const themeToggle = document.getElementById('themeToggle');

const applyTheme = (theme) => {
  if (theme === 'light') {
    document.body.classList.add('light-mode');
    themeToggle.textContent = '🌙';
  } else {
    document.body.classList.remove('light-mode');
    themeToggle.textContent = '☀️';
  }
};

const savedTheme = localStorage.getItem('coinlytics-theme') || 'dark';
applyTheme(savedTheme);

themeToggle?.addEventListener('click', () => {
  const isLight = document.body.classList.contains('light-mode');
  const newTheme = isLight ? 'dark' : 'light';

  applyTheme(newTheme);
  localStorage.setItem('coinlytics-theme', newTheme);
});