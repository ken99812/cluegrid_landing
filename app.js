// ClueGrid landing page: a small playable arrowword in the app's style, and the app's
// drifting letter tiles behind the page.
(() => {
  'use strict';

  // The puzzle: a 5 x 5 frame (clue row on top, clue column on the left) around a
  // 4 x 4 block of letters. Across: SOLD, AREA, FAST, ELSE. Down: SAFE, ORAL, LESS, DATE.
  const SOLUTION = ['SOLD', 'AREA', 'FAST', 'ELSE'];
  const ACROSS = [
    { text: 'Gone at auction' },
    { text: 'Length times width' },
    { text: 'Very quick' },
    { text: 'Otherwise' },
  ];
  const DOWN = [
    { text: 'Out of danger' },
    { text: 'Spoken, not written' },
    { text: 'Not as much' },
    { text: 'Day on a calendar', picture: 'assets/pictures/emoji_u1f4c5.png' },
  ];
  const N = 4;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const boardEl = document.getElementById('board');
  const statusEl = document.getElementById('status');
  const keysEl = document.getElementById('keys');
  const grid = Array.from({ length: N }, () => Array(N).fill(''));
  const cells = [];
  let cur = { r: 0, c: 0 };
  let dir = 'across';
  let solved = false;
  let introRunning = false;

  // Build the board once.
  for (let r = 0; r <= N; r++) {
    for (let c = 0; c <= N; c++) {
      const el = document.createElement('div');
      el.className = 'cell';
      el.setAttribute('role', 'gridcell');
      if (r === 0 && c === 0) {
        el.className += ' badge';
        el.innerHTML = 'Level<b>1</b>';
        el.setAttribute('aria-label', 'Level 1');
      } else if (r === 0) {
        const clue = DOWN[c - 1];
        el.className += ' clue';
        el.dataset.dir = 'down';
        el.dataset.index = String(c - 1);
        if (clue.picture) {
          el.innerHTML = `<img src="${clue.picture}" alt="">`;
          el.setAttribute('aria-label', `Down clue, picture: ${clue.text}`);
        } else {
          el.textContent = clue.text;
          el.setAttribute('aria-label', `Down clue: ${clue.text}`);
        }
        el.insertAdjacentHTML('beforeend', '<i class="arrow-d"></i>');
      } else if (c === 0) {
        const clue = ACROSS[r - 1];
        el.className += ' clue';
        el.dataset.dir = 'across';
        el.dataset.index = String(r - 1);
        el.textContent = clue.text;
        el.setAttribute('aria-label', `Across clue: ${clue.text}`);
        el.insertAdjacentHTML('beforeend', '<i class="arrow-r"></i>');
      } else {
        el.className += ' letter';
        el.dataset.r = String(r - 1);
        el.dataset.c = String(c - 1);
        cells.push(el);
      }
      boardEl.appendChild(el);
    }
  }
  const cellAt = (r, c) => cells[r * N + c];

  // The on-screen keyboard (phones and tablets).
  const ROWS = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'];
  ROWS.forEach((row, i) => {
    const line = document.createElement('div');
    line.className = 'row';
    for (const ch of row) {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = ch;
      b.setAttribute('aria-label', ch);
      b.addEventListener('click', () => type(ch));
      line.appendChild(b);
    }
    if (i === 2) {
      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'wide';
      del.textContent = '⌫';
      del.setAttribute('aria-label', 'Delete');
      del.addEventListener('click', erase);
      line.appendChild(del);
    }
    keysEl.appendChild(line);
  });

  const inWord = (r, c) => (dir === 'across' ? r === cur.r : c === cur.c);
  const wordRight = (d, i) =>
    Array.from({ length: N }, (_, k) => (d === 'across' ? grid[i][k] === SOLUTION[i][k] : grid[k][i] === SOLUTION[k][i])).every(Boolean);

  function render() {
    for (let r = 0; r < N; r++) {
      for (let c = 0; c < N; c++) {
        const el = cellAt(r, c);
        el.textContent = grid[r][c];
        const good = (wordRight('across', r) || wordRight('down', c)) && grid[r][c] !== '';
        el.classList.toggle('good', good);
        el.classList.toggle('cursor', !solved && r === cur.r && c === cur.c);
        el.classList.toggle('word', !solved && inWord(r, c));
        el.setAttribute('aria-label', `Row ${r + 1}, column ${c + 1}${grid[r][c] ? `, ${grid[r][c]}` : ', empty'}`);
      }
    }
    boardEl.querySelectorAll('.cell.clue').forEach((el) => {
      const on = !solved && el.dataset.dir === dir && Number(el.dataset.index) === (dir === 'across' ? cur.r : cur.c);
      el.classList.toggle('on', on);
    });
  }

  function say(text, win = false) {
    statusEl.textContent = text;
    statusEl.classList.toggle('win', win);
  }

  function clueText() {
    const clue = dir === 'across' ? ACROSS[cur.r] : DOWN[cur.c];
    return `${dir === 'across' ? 'Across' : 'Down'}: ${clue.text}`;
  }

  function checkSolved() {
    if (grid.every((row, r) => row.join('') === SOLUTION[r])) {
      solved = true;
      say('Solved! Hundreds more are waiting in the app.', true);
      render();
      return true;
    }
    return false;
  }

  function step(delta) {
    if (dir === 'across') cur.c = Math.min(N - 1, Math.max(0, cur.c + delta));
    else cur.r = Math.min(N - 1, Math.max(0, cur.r + delta));
  }

  function type(ch) {
    if (solved || introRunning) return;
    grid[cur.r][cur.c] = ch.toUpperCase();
    const el = cellAt(cur.r, cur.c);
    if (!reduced) { el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); }
    if (!checkSolved()) {
      step(1);
      say(clueText());
      render();
    }
  }

  function erase() {
    if (solved || introRunning) return;
    if (grid[cur.r][cur.c] === '') step(-1);
    grid[cur.r][cur.c] = '';
    render();
  }

  function select(r, c) {
    if (solved || introRunning) return;
    if (r === cur.r && c === cur.c) dir = dir === 'across' ? 'down' : 'across';
    cur = { r, c };
    say(clueText());
    render();
  }

  boardEl.addEventListener('click', (e) => {
    const el = e.target.closest('.cell');
    if (!el) return;
    if (el.classList.contains('letter')) select(Number(el.dataset.r), Number(el.dataset.c));
    else if (el.classList.contains('clue') && !solved && !introRunning) {
      dir = el.dataset.dir;
      const i = Number(el.dataset.index);
      cur = dir === 'across' ? { r: i, c: 0 } : { r: 0, c: i };
      say(clueText());
      render();
    }
    boardEl.focus({ preventScroll: true });
  });

  boardEl.addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (/^[a-z]$/i.test(k)) { type(k); e.preventDefault(); }
    else if (k === 'Backspace') { erase(); e.preventDefault(); }
    else if (k === ' ') { dir = dir === 'across' ? 'down' : 'across'; say(clueText()); render(); e.preventDefault(); }
    else if (k.startsWith('Arrow') && !solved && !introRunning) {
      const d = { ArrowRight: [0, 1], ArrowLeft: [0, -1], ArrowDown: [1, 0], ArrowUp: [-1, 0] }[k];
      cur = { r: Math.min(N - 1, Math.max(0, cur.r + d[0])), c: Math.min(N - 1, Math.max(0, cur.c + d[1])) };
      say(clueText());
      render();
      e.preventDefault();
    }
  });

  document.getElementById('hint').addEventListener('click', () => {
    if (solved || introRunning) return;
    // A hint fills the selected square, as Reveal letter does in the app.
    grid[cur.r][cur.c] = SOLUTION[cur.r][cur.c];
    if (!checkSolved()) { step(1); say(clueText()); render(); }
  });
  document.getElementById('reveal').addEventListener('click', () => {
    if (solved || introRunning) return;
    for (let k = 0; k < N; k++) {
      if (dir === 'across') grid[cur.r][k] = SOLUTION[cur.r][k];
      else grid[k][cur.c] = SOLUTION[k][cur.c];
    }
    if (!checkSolved()) { say(clueText()); render(); }
  });
  document.getElementById('restart').addEventListener('click', () => {
    if (introRunning) return;
    for (const row of grid) row.fill('');
    solved = false;
    cur = { r: 0, c: 0 };
    dir = 'across';
    say('Tap a white square and type. Tap it again to switch direction.');
    render();
  });

  // The intro: the first across word types itself in, then it is the visitor's turn.
  function intro() {
    render();
    if (reduced) return;
    introRunning = true;
    say('Across: Gone at auction');
    const word = SOLUTION[0];
    let i = 0;
    const tick = () => {
      if (i < word.length) {
        cur = { r: 0, c: i };
        grid[0][i] = word[i];
        render();
        const el = cellAt(0, i);
        el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');
        i++;
        setTimeout(tick, 380);
      } else {
        introRunning = false;
        cur = { r: 1, c: 0 };
        say('Your turn: Across, Length times width');
        render();
      }
    };
    setTimeout(tick, 700);
  }
  intro();

  // Drifting letter tiles behind the page, like the app's home screen.
  const canvas = document.getElementById('tiles');
  const ctx = canvas.getContext('2d');
  const LETTERS = 'CLUEGRIDWORDSAFETIMEDAILY';
  let tiles = [];
  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = innerWidth * dpr;
    canvas.height = innerHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.round((innerWidth * innerHeight) / 52000) + 6;
    tiles = Array.from({ length: count }, (_, i) => ({
      x: Math.random() * innerWidth,
      y: Math.random() * innerHeight,
      s: 46 + Math.random() * 46,
      a: (Math.random() - 0.5) * 0.5,
      v: 0.12 + Math.random() * 0.22,
      ch: LETTERS[i % LETTERS.length],
    }));
  }
  function draw() {
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    if (!ctx.roundRect) return;
    for (const t of tiles) {
      ctx.save();
      ctx.translate(t.x, t.y);
      ctx.rotate(t.a);
      ctx.fillStyle = 'rgba(255,255,255,0.12)';
      const r = t.s * 0.2;
      ctx.beginPath();
      ctx.roundRect(-t.s / 2, -t.s / 2, t.s, t.s, r);
      ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,0.18)';
      ctx.font = `900 ${t.s * 0.56}px Nunito, sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(t.ch, 0, t.s * 0.04);
      ctx.restore();
    }
  }
  function animate() {
    for (const t of tiles) {
      t.y -= t.v;
      if (t.y < -t.s) { t.y = innerHeight + t.s; t.x = Math.random() * innerWidth; }
    }
    draw();
    requestAnimationFrame(animate);
  }
  resize();
  addEventListener('resize', resize);
  if (reduced || !ctx.roundRect) draw();
  else requestAnimationFrame(animate);

  document.getElementById('year').textContent = String(new Date().getFullYear());
})();
