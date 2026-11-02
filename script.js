const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];

const menu = $('.desktop-nav');
$('.menu-toggle').addEventListener('click', (e) => {
  const open = menu.classList.toggle('open');
  e.currentTarget.setAttribute('aria-expanded', open);
});
$$('.desktop-nav a').forEach(a => a.addEventListener('click', () => menu.classList.remove('open')));

const calc = () => {
  const length = +$('#length').value;
  const height = +$('#height').value;
  const thickness = +$('#thickness').value;
  const openings = Math.max(0, +$('#openings').value || 0);
  const volume = Math.max(0, (length * height - openings) * thickness);
  $('#lengthOut').value = length;
  $('#heightOut').value = height.toFixed(1);
  $('#volume').value = volume.toFixed(1);
  $('#pallets').value = Math.ceil(volume / 1.5);
};
$$('#calc-form input, #calc-form select').forEach(el => el.addEventListener('input', calc));
calc();

const modal = $('#modal');
const openModal = () => { modal.classList.add('open'); modal.setAttribute('aria-hidden', 'false'); setTimeout(() => $('.modal-card input').focus(), 100); };
const closeModal = () => { modal.classList.remove('open'); modal.setAttribute('aria-hidden', 'true'); };
$('#requestBtn').addEventListener('click', openModal);
$('.modal-close').addEventListener('click', closeModal);
modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

const submitLead = (e) => {
  e.preventDefault();
  closeModal();
  e.target.reset();
  $('.toast').classList.add('show');
  setTimeout(() => $('.toast').classList.remove('show'), 3000);
};
$('#lead-form').addEventListener('submit', submitLead);
$('#modal-form').addEventListener('submit', submitLead);

const observer = new IntersectionObserver(entries => entries.forEach(entry => {
  if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
}), { threshold: .12 });
$$('.reveal').forEach(el => observer.observe(el));
