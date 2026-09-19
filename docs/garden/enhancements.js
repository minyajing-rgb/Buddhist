'use strict';

(() => {
  const q = (s, root = document) => root.querySelector(s);
  const qa = (s, root = document) => [...root.querySelectorAll(s)];
  const STATE_KEY = 'dharma-atlas-journey-v3';

  const copy = (zh, en) => document.documentElement.lang.toLowerCase().startsWith('en') ? en : zh;
  const todayKey = () => new Date().toISOString().slice(0, 10);

  const stampMeta = {
    text: ['经卷', 'Text', '▤'],
    place: ['圣地', 'Place', '⌖'],
    person: ['人物', 'People', '♙'],
    story: ['故事', 'Story', '✦'],
    timeline: ['时光', 'Time', '◷'],
    library: ['馆藏', 'Library', '▥']
  };

  const levels = [
    { xp: 0, zh: '初见', en: 'First Glimpse' },
    { xp: 40, zh: '漫游者', en: 'Wanderer' },
    { xp: 100, zh: '寻迹者', en: 'Pathfinder' },
    { xp: 180, zh: '连线者', en: 'Connector' },
    { xp: 280, zh: '深读者', en: 'Deep Reader' },
    { xp: 420, zh: '法藏探索者', en: 'Atlas Explorer' }
  ];

  const quests = [
    { type: 'text', zh: '打开一部经典，看看“作品、译本、实物”是不是同一件事。', en: 'Open one text and notice how a work, an edition, and an object differ.', route: 'works' },
    { type: 'place', zh: '在地图上找到一处圣地，看看它和哪些故事或事件相连。', en: 'Find one sacred place on the atlas and follow its links to stories or events.', route: 'places' },
    { type: 'person', zh: '认识一位译者、行旅者或研究者，追一条“人—经卷”的线。', en: 'Meet one translator, traveller, or scholar and trace a person–text connection.', route: 'people' },
    { type: 'timeline', zh: '拖动时间轴，观察“成书、翻译、发现、馆藏”为什么要分开。', en: 'Move through the timeline and separate composition, translation, discovery, and collection.', route: 'timeline' },
    { type: 'library', zh: '打开一件馆藏，记住它的材料、年代或馆藏号中的一个。', en: 'Open one collection object and remember one detail: material, date, or shelfmark.', route: 'library' },
    { type: 'story', zh: '读一段经卷旅程，把它当成今天进入佛典世界的一扇门。', en: 'Read one journey story as today’s doorway into the Buddhist textual world.', route: 'stories' }
  ];

  const cards = [
    { type: 'place', titleZh: '圣地线索', titleEn: 'Sacred Place Trail', textZh: '从鹿野苑、王舍城或舍卫城开始。先看“地点发生了什么”，再追经文。', textEn: 'Begin at Sarnath, Rajgir, or Shravasti. Start with what happened in a place, then follow the texts.', route: 'places' },
    { type: 'text', titleZh: '一卷两看', titleEn: 'Two Ways to Read', textZh: '挑一部经典：先读它关心的问题，再打开版本与证据层。', textEn: 'Choose one text: first read the question it asks, then open the edition and evidence layers.', route: 'works' },
    { type: 'timeline', titleZh: '时间切片', titleEn: 'Time Slice', textZh: '任选一个年代，只看当时已经出现的事件；不要把后来的实物年代倒推成成书年代。', textEn: 'Pick a date and view only events visible by then. Do not back-project an object’s date into a composition date.', route: 'timeline' },
    { type: 'person', titleZh: '人物接力', titleEn: 'People Relay', textZh: '从一个人物出发，找到他关联的经卷，再沿经卷跳到下一位人物。', textEn: 'Start with one person, jump to a connected text, then follow that text to another person.', route: 'people' },
    { type: 'library', titleZh: '实物侦探', titleEn: 'Object Detective', textZh: '找一个具体馆藏号，区分“作品名”和“今天仍能看到的那件东西”。', textEn: 'Find one shelfmark and separate the name of a work from the surviving object you can inspect today.', route: 'library' },
    { type: 'story', titleZh: '故事入口', titleEn: 'Story Door', textZh: '先不背术语。读完一段故事，再问：里面哪些是传统叙事，哪些有可追溯材料？', textEn: 'Skip memorising terms. Read a story, then ask which parts are tradition and which are traceable evidence.', route: 'stories' }
  ];

  let state = {
    xp: 0,
    seen: {},
    stamps: {},
    dailyDone: {},
    drawn: null,
    drawnDate: null
  };

  try {
    state = { ...state, ...(JSON.parse(localStorage.getItem(STATE_KEY) || '{}') || {}) };
  } catch (_) {}

  const save = () => {
    try { localStorage.setItem(STATE_KEY, JSON.stringify(state)); } catch (_) {}
  };

  const currentLevelIndex = () => {
    let idx = 0;
    levels.forEach((l, i) => { if (state.xp >= l.xp) idx = i; });
    return idx;
  };

  const levelName = () => {
    const l = levels[currentLevelIndex()];
    return copy(l.zh, l.en);
  };

  const dailyQuest = () => {
    const seed = todayKey().replaceAll('-', '').split('').reduce((a, b) => a + Number(b), 0);
    return quests[seed % quests.length];
  };

  const burst = () => {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const host = document.createElement('div');
    host.className = 'lotus-burst';
    host.setAttribute('aria-hidden', 'true');
    for (let i = 0; i < 10; i += 1) {
      const p = document.createElement('i');
      p.style.setProperty('--x', `${(Math.random() - .5) * 220}px`);
      p.style.setProperty('--y', `${-60 - Math.random() * 180}px`);
      p.style.setProperty('--r', `${Math.round(Math.random() * 180 - 90)}deg`);
      p.style.setProperty('--d', `${Math.random() * .18}s`);
      host.appendChild(p);
    }
    document.body.appendChild(host);
    setTimeout(() => host.remove(), 1600);
  };

  const maybeCompleteDaily = (type) => {
    const day = todayKey();
    const quest = dailyQuest();
    if (quest.type !== type || state.dailyDone?.[day]) return;
    state.dailyDone = { ...(state.dailyDone || {}), [day]: true };
    state.xp += 20;
    save();
    burst();
    renderJourney();
  };

  const discover = (type, id, points = 10) => {
    const key = `${type}:${id || 'first'}`;
    if (state.seen?.[key]) {
      maybeCompleteDaily(type);
      return;
    }
    state.seen = { ...(state.seen || {}), [key]: Date.now() };
    state.stamps = { ...(state.stamps || {}), [type]: true };
    state.xp = Math.min(999, (state.xp || 0) + points);
    save();
    maybeCompleteDaily(type);
    renderJourney();
    updateHeaderQuest();
  };

  const route = (name) => {
    closeJourney();
    if (name === 'places' || name === 'timeline') {
      location.hash = 'atlas';
      setTimeout(() => {
        const value = name === 'places' ? 'places' : 'events';
        q(`[data-tab="map"][data-value="${value}"]`)?.click();
      }, 80);
      return;
    }
    location.hash = name;
  };

  const syncBrand = () => {
    const en = document.documentElement.lang.toLowerCase().startsWith('en');
    const brand = q('.brand strong');
    const sub = q('.brand small');
    if (brand) brand.textContent = en ? 'Dharma Atlas' : '佛典世界地图';
    if (sub) sub.textContent = en ? 'EXPLORE · LEARN · BE INSPIRED' : '探索 · 学习 · 得到启发';

    const kicker = q('.hero-copy .kicker');
    const h1a = q('.hero-copy h1 span');
    const h1b = q('.hero-copy h1 em');
    const desc = q('.hero-copy p');
    if (kicker) kicker.textContent = en
      ? 'AN INTERACTIVE JOURNEY THROUGH THE WORLD OF BUDDHA'
      : '一场穿越佛陀世界的互动旅程';
    if (h1a) h1a.textContent = en ? 'Dharma Atlas' : '佛典全球知识地图';
    if (h1b) h1b.textContent = en ? 'Places · People · Wisdom' : '圣地 · 人物 · 智慧';
    if (desc) desc.innerHTML = en
      ? 'Discover the places, people, texts, and surviving objects that shaped Buddhist worlds.<br>Enter through a story. Go deeper through evidence.'
      : '发现塑造佛教世界的圣地、人物、经典与实物。<br>从故事进入，再沿证据一层层走深。';
    document.title = en ? 'Dharma Atlas · Interactive Buddhist World' : 'Dharma Atlas · 佛典全球知识地图';
  };

  const buildHeroSearch = () => {
    const heroCopy = q('.hero-copy');
    if (!heroCopy || q('#heroDiscoverySearch')) return;
    const form = document.createElement('form');
    form.id = 'heroDiscoverySearch';
    form.className = 'hero-discovery-search';
    form.innerHTML = `
      <span class="hero-search-icon" aria-hidden="true">⌕</span>
      <label class="sr-only" for="heroDiscoveryQuery">${copy('搜索经典、地点、人物或概念', 'Search texts, places, people, or concepts')}</label>
      <input id="heroDiscoveryQuery" type="search" autocomplete="off" placeholder="${copy('搜索经典、地点、人物、概念…', 'Search texts, places, people, concepts…')}">
      <button type="submit" aria-label="${copy('开始搜索', 'Search')}">→</button>
    `;
    heroCopy.appendChild(form);

    const chips = document.createElement('div');
    chips.className = 'hero-topic-chips';
    const topics = document.documentElement.lang.toLowerCase().startsWith('en')
      ? ['Buddha', 'Lotus', 'Bodhi Tree', 'Nalanda', 'Prajna', 'Meditation']
      : ['佛陀', '莲花', '菩提树', '那烂陀', '般若', '禅修'];
    chips.innerHTML = topics.map(t => `<button type="button" data-hero-topic="${t}">${t}</button>`).join('');
    heroCopy.appendChild(chips);

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const term = q('#heroDiscoveryQuery')?.value.trim();
      if (!term) return;
      route('works');
      setTimeout(() => {
        const wq = q('#workQuery');
        if (wq) {
          wq.value = term;
          wq.dispatchEvent(new Event('input', { bubbles: true }));
        }
      }, 90);
    });
  };

  const updateHeroSearchLanguage = () => {
    const form = q('#heroDiscoverySearch');
    if (!form) return;
    const input = q('#heroDiscoveryQuery');
    if (input) input.placeholder = copy('搜索经典、地点、人物、概念…', 'Search texts, places, people, concepts…');
    const chips = q('.hero-topic-chips');
    if (chips) {
      const topics = document.documentElement.lang.toLowerCase().startsWith('en')
        ? ['Buddha', 'Lotus', 'Bodhi Tree', 'Nalanda', 'Prajna', 'Meditation']
        : ['佛陀', '莲花', '菩提树', '那烂陀', '般若', '禅修'];
      chips.innerHTML = topics.map(t => `<button type="button" data-hero-topic="${t}">${t}</button>`).join('');
    }
  };

  const portalItems = () => [
    ['atlas', '◫', copy('互动地图', 'Interactive Map'), copy('跟随佛陀与经卷的足迹', 'Follow the Buddha and the texts')],
    ['works', '▤', copy('佛典经文', 'Buddhist Texts'), copy('探索百部经典与版本', 'Explore 100 texts and editions')],
    ['places', '⌖', copy('圣地巡礼', 'Sacred Places'), copy('从蓝毗尼到菩提伽耶', 'From Lumbini to Bodh Gaya')],
    ['people', '♙', copy('人物故事', 'People & Stories'), copy('认识译者、行旅者与传承者', 'Meet translators, travellers, carriers')],
    ['timeline', '◷', copy('时间长河', 'Timeline'), copy('穿越两千多年流转史', 'Travel through 2,000+ years')],
    ['library', '▥', copy('图书馆与博物馆', 'Libraries & Museums'), copy('寻找原件、馆藏与数字影像', 'Find objects, collections, digital images')]
  ];

  const renderPortalDeck = () => {
    let deck = q('#heroPortalDeck');
    const hero = q('.garden-hero');
    if (!hero) return;
    if (!deck) {
      deck = document.createElement('section');
      deck.id = 'heroPortalDeck';
      deck.className = 'hero-portal-deck';
      deck.setAttribute('aria-label', copy('探索入口', 'Explore the atlas'));
      hero.insertAdjacentElement('afterend', deck);
    }
    deck.innerHTML = portalItems().map(([routeName, icon, title, text], i) => `
      <button class="portal-card portal-${i + 1}" type="button" data-portal="${routeName}">
        <span class="portal-art" aria-hidden="true"><b>${icon}</b></span>
        <span class="portal-copy"><strong>${title}</strong><small>${text}</small></span>
        <span class="portal-arrow" aria-hidden="true">→</span>
      </button>
    `).join('');
  };

  const renderWorldValues = () => {
    let rail = q('#worldValues');
    const hero = q('.garden-hero');
    if (!hero) return;
    if (!rail) {
      rail = document.createElement('div');
      rail.id = 'worldValues';
      rail.className = 'world-values';
      hero.appendChild(rail);
    }
    rail.innerHTML = `
      <button data-world-action="journey"><span>✺</span><small>${copy('内在安宁', 'Inner Peace')}</small></button>
      <button data-world-action="works"><span>⌂</span><small>${copy('智慧生活', 'Wiser Living')}</small></button>
      <button data-world-action="atlas"><span>◎</span><small>${copy('全球文化', 'Global Cultures')}</small></button>
      <button data-world-action="stories"><span>❧</span><small>${copy('活的智慧', 'Living Wisdom')}</small></button>
    `;
  };

  const buildJourneyButton = () => {
    const tools = q('.header-tools');
    if (!tools || q('#journeyButton')) return;
    const b = document.createElement('button');
    b.id = 'journeyButton';
    b.className = 'journey-button';
    b.type = 'button';
    b.setAttribute('aria-controls', 'journeyDrawer');
    tools.insertBefore(b, tools.firstChild);
    updateHeaderQuest();
  };

  const updateHeaderQuest = () => {
    const b = q('#journeyButton');
    if (!b) return;
    b.innerHTML = `<span aria-hidden="true">✺</span><span class="journey-button-copy">${copy('探索旅程', 'Journey')}</span><b>${state.xp || 0}</b>`;
    b.setAttribute('aria-label', copy(`打开探索旅程，当前 ${state.xp || 0} 点`, `Open journey, ${state.xp || 0} points`));
  };

  const buildJourneyDrawer = () => {
    if (q('#journeyDrawer')) return;
    const backdrop = document.createElement('button');
    backdrop.id = 'journeyBackdrop';
    backdrop.className = 'journey-backdrop';
    backdrop.type = 'button';
    backdrop.hidden = true;
    backdrop.setAttribute('aria-label', copy('关闭探索旅程', 'Close journey'));
    document.body.appendChild(backdrop);

    const drawer = document.createElement('aside');
    drawer.id = 'journeyDrawer';
    drawer.className = 'journey-drawer';
    drawer.setAttribute('aria-hidden', 'true');
    drawer.innerHTML = '<div id="journeyInner"></div>';
    document.body.appendChild(drawer);
    renderJourney();
  };

  const renderJourney = () => {
    const host = q('#journeyInner');
    if (!host) return;
    const idx = currentLevelIndex();
    const now = levels[idx];
    const next = levels[Math.min(idx + 1, levels.length - 1)];
    const maxed = idx === levels.length - 1;
    const span = maxed ? 1 : next.xp - now.xp;
    const pct = maxed ? 100 : Math.max(0, Math.min(100, ((state.xp - now.xp) / span) * 100));
    const dq = dailyQuest();
    const done = Boolean(state.dailyDone?.[todayKey()]);
    const drawn = Number.isInteger(state.drawn) ? cards[state.drawn] : null;

    host.innerHTML = `
      <div class="journey-top">
        <div><span class="journey-kicker">${copy('你的佛典世界探索进度', 'YOUR DHARMA ATLAS JOURNEY')}</span><h2>${levelName()}</h2></div>
        <button class="journey-close" type="button" data-close-journey aria-label="${copy('关闭', 'Close')}">×</button>
      </div>

      <div class="journey-score">
        <div class="lotus-level" style="--p:${pct}%"><span>✺</span></div>
        <div><strong>${state.xp || 0}</strong><small>${copy('探索光点', 'discovery light')}</small></div>
        <div class="journey-progress"><i style="width:${pct}%"></i><small>${maxed ? copy('完整图谱探索中', 'Full atlas exploration') : copy(`距离下一阶段 ${Math.max(0, next.xp - state.xp)} 点`, `${Math.max(0, next.xp - state.xp)} to next level`)}</small></div>
      </div>

      <section class="journey-section">
        <div class="journey-section-head"><b>${copy('六枚探索印章', 'Six exploration stamps')}</b><span>${Object.values(state.stamps || {}).filter(Boolean).length}/6</span></div>
        <div class="stamp-grid">
          ${Object.entries(stampMeta).map(([k, v]) => `
            <div class="stamp ${state.stamps?.[k] ? 'earned' : ''}">
              <span>${v[2]}</span><b>${copy(v[0], v[1])}</b><small>${state.stamps?.[k] ? copy('已点亮', 'Unlocked') : copy('待探索', 'Explore')}</small>
            </div>`).join('')}
        </div>
      </section>

      <section class="daily-quest ${done ? 'done' : ''}">
        <span class="journey-kicker">${copy('今日一小步', 'TODAY’S QUEST')}</span>
        <h3>${done ? copy('今日任务已完成 ✦', 'Quest complete ✦') : copy('今天，只探索一件事', 'Explore just one thing today')}</h3>
        <p>${copy(dq.zh, dq.en)}</p>
        <button class="button primary small" type="button" data-quest-route="${dq.route}">${done ? copy('再走一遍 →', 'Explore again →') : copy('开始任务 +20 →', 'Start quest +20 →')}</button>
      </section>

      <section class="journey-section">
        <div class="journey-section-head"><b>${copy('抽一张探索卡', 'Draw an exploration card')}</b><span>1 / 6</span></div>
        ${drawn ? `
          <article class="explore-card">
            <small>${copy('今日探索卡', 'EXPLORATION CARD')}</small>
            <h3>${copy(drawn.titleZh, drawn.titleEn)}</h3>
            <p>${copy(drawn.textZh, drawn.textEn)}</p>
            <button type="button" data-card-route="${drawn.route}">${copy('沿这条线去探索 →', 'Follow this trail →')}</button>
          </article>
        ` : `<button class="draw-card" type="button" data-draw-card><span>✺</span><b>${copy('翻开一张卡', 'Reveal a card')}</b><small>${copy('不是占卜，是一条今天可以走的知识路线。', 'Not fortune-telling — just a path to explore today.')}</small></button>`}
      </section>

      <p class="journey-privacy">${copy('进度只保存在你的浏览器里，不需要注册。', 'Progress stays in your browser. No account required.')}</p>
    `;
  };

  const openJourney = () => {
    const drawer = q('#journeyDrawer');
    const backdrop = q('#journeyBackdrop');
    if (!drawer || !backdrop) return;
    renderJourney();
    backdrop.hidden = false;
    requestAnimationFrame(() => {
      drawer.classList.add('open');
      backdrop.classList.add('open');
      drawer.setAttribute('aria-hidden', 'false');
      document.body.classList.add('journey-open');
      q('[data-close-journey]', drawer)?.focus({ preventScroll: true });
    });
  };

  const closeJourney = () => {
    const drawer = q('#journeyDrawer');
    const backdrop = q('#journeyBackdrop');
    if (!drawer || !backdrop) return;
    drawer.classList.remove('open');
    backdrop.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('journey-open');
    setTimeout(() => { backdrop.hidden = true; }, 260);
  };

  const drawCard = () => {
    const date = todayKey();
    if (state.drawnDate !== date || !Number.isInteger(state.drawn)) {
      const seed = [...date].reduce((acc, c) => acc + c.charCodeAt(0), 0) + (state.xp || 0);
      state.drawn = seed % cards.length;
      state.drawnDate = date;
      state.xp = Math.min(999, (state.xp || 0) + 4);
      save();
      burst();
    }
    renderJourney();
    updateHeaderQuest();
  };

  const buildBeginJourneyOrb = () => {
    const hero = q('.garden-hero');
    if (!hero || q('#beginJourneyOrb')) return;
    const b = document.createElement('button');
    b.id = 'beginJourneyOrb';
    b.className = 'begin-journey-orb';
    b.type = 'button';
    b.innerHTML = `<span>✦</span><b>${copy('开始旅程', 'Begin Journey')}</b>`;
    hero.appendChild(b);
  };

  const refreshInjectedLanguage = () => {
    syncBrand();
    updateHeroSearchLanguage();
    renderPortalDeck();
    renderWorldValues();
    renderJourney();
    updateHeaderQuest();
    const orb = q('#beginJourneyOrb b');
    if (orb) orb.textContent = copy('开始旅程', 'Begin Journey');
  };

  const markFromAction = (el) => {
    if (!el) return;
    const act = el.dataset.act;
    const id = el.dataset.id || '';
    if (act === 'work') discover('text', id, 10);
    if (act === 'story' || act === 'read') discover('story', id, act === 'read' ? 12 : 8);
    if (act === 'person') discover('person', id, 10);
    if (act === 'place') discover('place', id, 10);
    if (act === 'event') discover('timeline', id, 10);
    if (['object', 'institution', 'figure'].includes(act)) discover('library', id, 10);
    if (act === 'bookmark') discover('text', `bookmark-${id}`, 4);
  };

  const init = () => {
    // Preserve the existing in-page anchor behavior.
    document.addEventListener('click', event => {
      const link = event.target.closest('a[href="#paths"],a[href="#main"]');
      if (link) {
        const target = document.getElementById(link.getAttribute('href').slice(1));
        if (target) {
          event.preventDefault();
          target.scrollIntoView({
            behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
            block: 'start'
          });
          if (target.id === 'main') target.focus({ preventScroll: true });
        }
      }
      const navLink = event.target.closest('#nav a');
      if (navLink && navLink.hash === location.hash) {
        q('#nav')?.classList.remove('open');
        q('#menuToggle')?.setAttribute('aria-expanded', 'false');
      }
    });

    syncBrand();
    buildHeroSearch();
    renderPortalDeck();
    renderWorldValues();
    buildJourneyDrawer();
    buildJourneyButton();
    buildBeginJourneyOrb();

    document.addEventListener('click', event => {
      const topic = event.target.closest('[data-hero-topic]');
      if (topic) {
        const term = topic.dataset.heroTopic;
        const input = q('#heroDiscoveryQuery');
        if (input) input.value = term;
        q('#heroDiscoverySearch')?.requestSubmit();
        return;
      }

      const portal = event.target.closest('[data-portal]');
      if (portal) {
        const name = portal.dataset.portal;
        const type = name === 'works' ? 'text' : name === 'people' ? 'person' : name === 'stories' ? 'story' : name === 'library' ? 'library' : name === 'timeline' ? 'timeline' : 'place';
        discover(type, `portal-${name}`, 5);
        route(name);
        return;
      }

      const world = event.target.closest('[data-world-action]');
      if (world) {
        const name = world.dataset.worldAction;
        if (name === 'journey') openJourney();
        else route(name);
        return;
      }

      if (event.target.closest('#journeyButton') || event.target.closest('#beginJourneyOrb')) {
        openJourney();
        return;
      }

      if (event.target.closest('#journeyBackdrop') || event.target.closest('[data-close-journey]')) {
        closeJourney();
        return;
      }

      const questRoute = event.target.closest('[data-quest-route]');
      if (questRoute) {
        route(questRoute.dataset.questRoute);
        return;
      }

      if (event.target.closest('[data-draw-card]')) {
        drawCard();
        return;
      }

      const cardRoute = event.target.closest('[data-card-route]');
      if (cardRoute) {
        const card = Number.isInteger(state.drawn) ? cards[state.drawn] : null;
        if (card) discover(card.type, `card-${state.drawn}`, 4);
        route(cardRoute.dataset.cardRoute);
        return;
      }

      markFromAction(event.target.closest('[data-act]'));
    });

    q('#langToggle')?.addEventListener('click', () => setTimeout(refreshInjectedLanguage, 0));

    window.addEventListener('hashchange', () => {
      const hash = location.hash.replace('#', '').split('/')[0];
      if (hash === 'library') discover('library', 'section', 3);
      if (hash === 'stories') discover('story', 'section', 3);
    });

    window.addEventListener('keydown', e => {
      if (e.key === 'Escape' && q('#journeyDrawer')?.classList.contains('open')) closeJourney();
    });

    // Small “first light” reward for starting, without forcing an onboarding modal.
    if (!state.seen?.['home:first']) {
      state.seen = { ...(state.seen || {}), 'home:first': Date.now() };
      state.xp = Math.min(999, (state.xp || 0) + 3);
      save();
      updateHeaderQuest();
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
