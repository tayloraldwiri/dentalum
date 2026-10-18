'use strict';
(() => {
  const lab = document.querySelector('#smile-lab');
  if (!lab) return;
  const $ = selector => lab.querySelector(selector);
  const viewport = $('#lab-viewport');
  const deposits = [...lab.querySelectorAll('.lab-deposit')];
  const palettes = { warm: [216, 190, 151], natural: [232, 219, 194], light: [243, 235, 215] };
  let mode = 'whiten', revealed = false, drawing = false, surface = 'all', lastPoint = null;
  const cleaned = new Set();
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  const rgb = values => `rgb(${values.join(',')})`;
  function shade(base, level) { return mix(base, [251, 249, 241], level / 3 * .9); }
  function paintModel(selector, color) {
    for (const stop of lab.querySelectorAll(`${selector} [data-tone]`)) {
      const tone = stop.dataset.tone;
      stop.setAttribute('stop-color', rgb(tone === 'light' ? mix(color, [255, 255, 255], .3) : tone === 'edge' ? mix(color, [145, 144, 133], .24) : color));
    }
  }
  function updateShade() {
    const base = palettes[$('#lab-start-shade').value], level = Number($('#lab-whiten-level').value);
    paintModel('.lab-before', base); paintModel('.lab-after', shade(base, level));
    $('#lab-shade-output').textContent = `Nivå ${level + 1} av 4`;
    for (const swatch of lab.querySelectorAll('[data-shade]')) {
      const index = Number(swatch.dataset.shade);
      swatch.style.background = rgb(shade(base, index));
      swatch.classList.toggle('active', index === level);
    }
    $('#lab-whiten-level').setAttribute('aria-valuetext', `Illustrativ nyansnivå ${level + 1} av 4`);
  }
  function compare(value) {
    const split = Math.min(100, Math.max(0, Number(value)));
    viewport.style.setProperty('--split', `${split}%`); $('#lab-compare').value = String(Math.round(split));
    $('#lab-compare').setAttribute('aria-valuetext', `${Math.round(split)} procent utgångsnyans`);
  }
  function relevantDeposits() { return deposits.filter(d => surface === 'all' || d.dataset.site === surface); }
  function updateCoverage() {
    const relevant = relevantDeposits(), count = relevant.filter(d => cleaned.has(d)).length;
    const value = Math.round(count / relevant.length * 100);
    if ($('#lab-coverage-value').textContent !== `${value} %`) $('#lab-coverage-value').textContent = `${value} %`; $('#lab-coverage-bar').value = value;
    const allDone = cleaned.size === deposits.length;
    $('#lab-clean-status').textContent = !revealed ? 'Avslöja beläggningarna för att börja.' : allDone ? 'Alla synliga punkter är rengjorda. Glöm inte att verklig rengöring också omfattar tändernas baksidor och mellanrum.' : `${count} av ${relevant.length} punkter på vald yta är rengjorda.`;
    $('#lab-clean-surface').disabled = !revealed || value === 100;
    for (const d of deposits) d.classList.toggle('muted', surface !== 'all' && d.dataset.site !== surface);
  }
  function clean(deposit) {
    if (cleaned.has(deposit)) return;
    cleaned.add(deposit); deposit.classList.add('cleaned', 'just-cleaned');
    setTimeout(() => deposit.classList.remove('just-cleaned'), 700);
  }
  function setMode(next) {
    mode = next; drawing = false; lastPoint = null; lab.dataset.mode = mode;
    for (const button of lab.querySelectorAll('.lab-modes button')) button.setAttribute('aria-pressed', String(button.dataset.mode === mode));
    $('#lab-whitening-panel').hidden = mode !== 'whiten'; $('#lab-cleaning-panel').hidden = mode !== 'clean';
    $('.lab-compare-control').hidden = mode !== 'whiten'; $('.lab-clean-caption').hidden = mode !== 'clean';
    $('#lab-view-name').textContent = mode === 'whiten' ? 'Illustrativ nyansjämförelse' : 'Plackkarta · övningsmodell';
    $('.lab-brush').hidden = true;
  }
  function reveal() {
    revealed = true; lab.classList.add('lab-revealed'); $('#lab-reveal').textContent = 'Beläggningar avslöjade ✓'; $('#lab-reveal').disabled = true;
    updateCoverage();
  }
  function reset() {
    cleaned.clear(); revealed = false; drawing = false; lastPoint = null; lab.classList.remove('lab-revealed');
    for (const d of deposits) d.classList.remove('cleaned', 'just-cleaned');
    $('#lab-reveal').textContent = 'Avslöja beläggningar ✧'; $('#lab-reveal').disabled = false; $('.lab-brush').hidden = true; updateCoverage();
  }
  function point(event) { const r = viewport.getBoundingClientRect(); return { x: (event.clientX - r.left) / r.width * 800, y: (event.clientY - r.top) / r.height * 420 }; }
  function brush(pointNow) {
    $('.lab-brush').hidden = false; $('.lab-brush').setAttribute('transform', `translate(${pointNow.x},${pointNow.y})`);
    const previous = lastPoint || pointNow, dx = pointNow.x - previous.x, dy = pointNow.y - previous.y;
    for (const d of relevantDeposits()) {
      const x = Number(d.dataset.x), y = Number(d.dataset.y);
      const t = dx || dy ? Math.min(1, Math.max(0, ((x - previous.x) * dx + (y - previous.y) * dy) / (dx * dx + dy * dy))) : 0;
      if (Math.hypot(x - previous.x - t * dx, y - previous.y - t * dy) < 25) clean(d);
    }
    lastPoint = pointNow; updateCoverage();
  }
  viewport.addEventListener('pointerdown', event => {
    if (event.button !== 0 || mode === 'clean' && !revealed) return;
    drawing = true; lastPoint = null; viewport.setPointerCapture(event.pointerId);
    if (mode === 'whiten') compare(point(event).x / 8); else brush(point(event));
  });
  viewport.addEventListener('pointermove', event => {
    if (!drawing) return;
    if (mode === 'whiten') compare(point(event).x / 8); else brush(point(event));
  });
  function finish(event) { drawing = false; lastPoint = null; $('.lab-brush').hidden = true; if (viewport.hasPointerCapture(event.pointerId)) viewport.releasePointerCapture(event.pointerId); }
  viewport.addEventListener('pointerup', finish); viewport.addEventListener('pointercancel', finish);
  for (const button of lab.querySelectorAll('.lab-modes button')) button.addEventListener('click', () => setMode(button.dataset.mode));
  $('#lab-start-shade').addEventListener('change', updateShade); $('#lab-whiten-level').addEventListener('input', updateShade); $('#lab-compare').addEventListener('input', event => compare(event.target.value));
  $('#lab-reveal').addEventListener('click', reveal); $('#lab-clean-reset').addEventListener('click', reset);
  $('#lab-surface').addEventListener('change', event => { surface = event.target.value; updateCoverage(); });
  $('#lab-clean-surface').addEventListener('click', () => { if (!revealed) return; relevantDeposits().forEach(clean); updateCoverage(); });
  updateShade(); compare(50); updateCoverage(); setMode('whiten');
  for (const selector of ['.lab-modes', '.lab-whitening-controls', '.lab-cleaning-controls']) $(selector).hidden = false;
})();
