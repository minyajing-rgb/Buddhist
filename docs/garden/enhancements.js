'use strict';
/* Cinematic visitor layer. Uses the original, allowlisted content and core reader.
   No accounts, analytics, remote image dependencies or repository links. */
(() => {
  const $q=(s,r=document)=>r.querySelector(s), $$q=(s,r=document)=>[...r.querySelectorAll(s)];
  const c=(zh,en)=>document.documentElement.lang.startsWith('en')?en:zh;
  const esc=s=>String(s??'').replace(/[&<>"']/g,a=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[a]));
  const norm=s=>String(s??'').normalize('NFKD').replace(/[\u0300-\u036f\s·_-]/g,'').toLowerCase();
  const text=(o,k)=>o[k+'_'+(document.documentElement.lang.startsWith('en')?'en':'zh')]||o[k]||'';
  const lotus=`<svg viewBox="0 0 52 44" aria-hidden="true"><path d="M26 36C12 30 14 14 26 3c12 11 14 27 0 33Z"/><path d="M25 36C10 38 2 27 2 17c13 0 21 6 23 19ZM27 36c15 2 23-9 23-19-13 0-21 6-23 19Z"/><path d="M24 35C10 29 7 18 11 9c10 4 15 12 13 26ZM28 35c14-6 17-17 13-26-10 4-15 12-13 26Z"/><path d="M26 36C16 42 6 39 2 31c8-1 15 0 24 5Zm0 0c10 6 20 3 24-5-8-1-15 0-24 5Z"/></svg>`;
  const icons={
    globe:`<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="13"/><ellipse cx="16" cy="16" rx="6" ry="13"/><path d="M3 16h26M6 9h20M6 23h20"/></svg>`,
    temple:`<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 12 16 3l13 9H3Zm3 0v14m7-14v14m6-14v14m7-14v14M3 26h26v3H3Z"/></svg>`,
    leaf:`<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M6 26C0 10 17 11 28 3c0 17-9 25-22 23Z"/><path d="M3 30 24 9m-15 13 1-8m5 3 8 0"/></svg>`,
    search:`<svg class="hero-search-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="7.5"/><path d="m16 16 5 5"/></svg>`,
    eye:`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>`,
    expand:`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9V3h6m6 0h6v6M3 15v6h6m6 0h6v-6"/></svg>`
  };
  const KEY='dharma-cinematic-progress-v4';
  let storageOK=true,journey={seen:{},daily:{},cards:{},xp:0},quiet=false,motion=true,guideStep=0,returnTo=null;
  try{const s=JSON.parse(localStorage.getItem(KEY)||'null');if(s&&typeof s==='object'){journey={seen:s.seen&&typeof s.seen==='object'?s.seen:{},daily:s.daily&&typeof s.daily==='object'?s.daily:{},cards:s.cards&&typeof s.cards==='object'?s.cards:{},xp:Number.isFinite(s.xp)?Math.max(0,Math.min(10000,s.xp)):0};}}
  catch{storageOK=false;}
  const day=()=>{const d=new Date();return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};
  const store=()=>{try{localStorage.setItem(KEY,JSON.stringify(journey));storageOK=true;}catch{storageOK=false;}};
  const stamps={text:['经卷','Texts','▤'],place:['圣地','Places','⌖'],person:['人物','People','♙'],story:['故事','Stories','✦'],timeline:['时光','Time','◷'],library:['馆藏','Collections','▥']};
  const levels=[[0,'初见','First Glimpse'],[40,'漫游者','Wanderer'],[100,'寻迹者','Pathfinder'],[180,'连线者','Connector'],[280,'深读者','Deep Reader'],[420,'法藏探索者','Atlas Explorer']];
  const quests=[
    ['text','打开一部经典，读一读它的版本与资料来源。','Open a text and look at its editions and sources.','works'],
    ['place','在地图上打开一个地点，看看它记录了怎样的相遇。','Open a place on the map and explore its connections.','places'],
    ['person','打开一位人物，追寻他与经卷的联系。','Open a person and follow a connection with a text.','people'],
    ['timeline','打开一个带来源的时间事件，分清它是什么日期。','Open a sourced event and identify what its date represents.','timeline'],
    ['library','打开一件馆藏，观察材料、纪年或馆藏号。','Open an object and notice its material, date or shelfmark.','library'],
    ['story','打开一个故事，把一段文字当作今天的旅程。','Open a story and make it today’s journey.','stories']
  ];
  const cards=[
    ['圣地线索','A trail of places','从一处地点进入，再去查它与人物和经卷的联系。','Begin at one place; follow its people and texts.','places'],
    ['一卷两看','Two ways to read','先读一部经典关心什么，再打开版本与证据。','Read a text’s main question, then explore editions and evidence.','works'],
    ['时间切片','A slice of time','拖动时间线，再打开一个事件查看日期的含义。','Move the time slider and inspect the meaning of an event’s date.','timeline'],
    ['人物接力','People carrying words','认识一个人物，再沿着他打开一部经典。','Meet one person, then open a connected text.','people'],
    ['实物侦探','An object’s story','分清一部作品与留存至今的具体物件。','Distinguish a work from a particular surviving object.','library'],
    ['故事之门','A story opens a door','不必先懂术语。从一个完整故事开始。','No terms to memorise first. Begin with one whole story.','stories']
  ];
  const daily=()=>quests[[...day()].reduce((s,k)=>s+(+k||0),0)%6];
  function notice(message){let n=$q('#cinematicToast');if(!n){n=document.createElement('div');n.id='cinematicToast';n.className='cinematic-toast';n.setAttribute('role','status');document.body.append(n);}n.textContent=message;n.hidden=false;clearTimeout(notice.timer);notice.timer=setTimeout(()=>n.hidden=true,2800);}
  function award(type,id){if(!stamps[type]||!id)return;const key=type+':'+id;let extra=0;if(!journey.seen[key]){journey.seen[key]=Date.now();journey.xp+=10;extra=10;}if(daily()[0]===type&&!journey.daily[day()]){journey.daily[day()]=true;journey.xp+=20;extra+=20;}store();updateJourneyHeader();if(extra)notice(c(`记录了一次新探索 +${extra}`,`New discovery recorded +${extra}`));}
  function go(route){closeAux();if($q('#modal').open)closeModal();const mapped=['places','timeline'].includes(route)?'atlas':route;location.hash=mapped;if(location.hash.slice(1)===mapped)navigate(false);if(mapped==='atlas'){mapMode=route==='places'?'places':route==='timeline'?'events':mapMode;renderMap();}window.scrollTo({top:0,behavior:'instant'});$q('#nav').classList.remove('open');$q('#menuToggle').setAttribute('aria-expanded','false');}
  function closeAux(){for(const id of ['journeyDialog','discoveryDialog']){const d=$q('#'+id);if(d?.open)d.close();}}
  function openRecord(type,id){closeAux();const fn={work:showWork,place:showPlace,person:showPerson,story:showStory,event:showEvent,object:showObject,institution:showInstitution}[type];if(fn){fn(id);award({work:'text',place:'place',person:'person',story:'story',event:'timeline',object:'library',institution:'library'}[type],id);}}
  function initScene(){const h=$q('.garden-hero');h.innerHTML=`
    <div class="hero-scene" role="img" aria-label="${c('金色宫殿、莲花、山河、鹿与孔雀组成的艺术想象场景','An imagined world of golden pavilions, lotuses, mountains, deer and a peacock')}"></div><div class="hero-wash"></div>
    <div class="hero-copy"><div class="kicker" id="cinemaKicker"></div><div class="hero-lotus">${lotus}</div><h1><span>Dharma Atlas</span><em id="cinemaSubtitle"></em></h1><p id="cinemaIntro"></p><form class="hero-discovery-search" id="heroDiscoverySearch">${icons.search}<label for="heroDiscoveryQuery" class="sr-only">Search the atlas</label><input id="heroDiscoveryQuery" type="search" autocomplete="off"><button type="submit" id="heroSearchButton" aria-label="Search">→</button></form><div class="hero-topic-chips" id="heroTopics"></div></div>
    <div class="world-values" id="worldValues"></div><div class="hero-note" id="heroNote"></div>
    <div class="scene-hotspots"><button style="left:19%;top:51%" data-record="person" data-id="buddha"><i></i><span></span></button><button style="left:57%;top:55%" data-c-route="places"><i></i><span></span></button><button style="left:39%;top:73%" data-discover="莲花"><i></i><span></span></button></div>
    <div class="scene-petals" aria-hidden="true">${Array.from({length:9},(_,i)=>`<i style="--left:${5+i*11}%;--duration:${13+i%4*3}s;--delay:-${i*2.7}s"></i>`).join('')}</div>
    <div class="hero-controls"><button id="quietButton" type="button" aria-pressed="false">${icons.eye}<span></span></button><button id="fullscreenButton" type="button">${icons.expand}<span></span></button><button class="journey-orb" type="button" data-guide="0"><span>▷</span><small></small></button></div>
    <div class="hero-bottom"><span id="sceneDisclosure"></span><a href="#paths" id="cinemaScroll"></a></div>`;
    const deck=document.createElement('section');deck.className='hero-portal-deck';deck.id='heroPortalDeck';h.after(deck);
    $q('#heroDiscoverySearch').addEventListener('submit',e=>{e.preventDefault();openSearch($q('#heroDiscoveryQuery').value);});
    $q('#quietButton').addEventListener('click',()=>{quiet=!quiet;h.classList.toggle('quiet-view',quiet);$q('#quietButton').setAttribute('aria-pressed',String(quiet));renderSceneLabels();});
    $q('#fullscreenButton').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else if(h.requestFullscreen)await h.requestFullscreen();else notice(c('当前浏览器不支持全屏；可使用纯景模式。','Fullscreen is unavailable; try the quiet view.'));}catch{notice(c('此浏览器未允许全屏。','Fullscreen was not allowed by this browser.'));}});
    if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&matchMedia('(pointer:fine)').matches){h.addEventListener('pointermove',e=>{if(!motion||quiet)return;const r=h.getBoundingClientRect();h.style.setProperty('--scene-x',((e.clientX-r.left)/r.width-.5)*-6+'px');h.style.setProperty('--scene-y',((e.clientY-r.top)/r.height-.5)*-4+'px');});h.addEventListener('pointerleave',()=>{h.style.setProperty('--scene-x','0px');h.style.setProperty('--scene-y','0px');});}
  }
  function renderSceneLabels(){
    $q('#cinemaKicker').textContent=c('一场走入佛陀世界的互动旅程','AN INTERACTIVE JOURNEY THROUGH THE WORLD OF BUDDHA');
    $q('#cinemaSubtitle').textContent=c('探索佛陀的世界 · 走近更美好的自己','Places · People · Wisdom');
    $q('#cinemaIntro').innerHTML=c('沿着圣地、人物与经典的足迹，<br>开启一场关于智慧与善意的探索。','Discover the places, people, and wisdom<br>that shaped a kinder world.');
    $q('#heroDiscoveryQuery').placeholder=c('搜索经典、地点、人物、概念…','Search texts, places, people, concepts…');
    $q('label[for=heroDiscoveryQuery]').textContent=c('搜索佛典世界','Search the Buddhist world');$q('#heroSearchButton').setAttribute('aria-label',c('搜索','Search'));
    const topics=[['佛陀','Buddha'],['莲花','Lotus'],['菩提树','Bodhi tree'],['那烂陀','Nalanda'],['般若','Prajna'],['禅修','Meditation']];
    $q('#heroTopics').innerHTML=topics.map(t=>`<button type="button" data-discover="${t[0]}">${c(...t)}</button>`).join('');
    $q('#worldValues').innerHTML=[[lotus,'内在安宁','Inner peace','quiet'],[icons.temple,'智慧生活','Wiser living','works'],[icons.globe,'多元文化','Global cultures','atlas'],[icons.leaf,'活的智慧','Living wisdom','stories']].map(([i,z,e,r])=>`<button type="button" ${r==='quiet'?'data-quiet':'data-c-route="'+r+'"'}>${i}<small>${c(z,e)}</small></button>`).join('');
    $q('#heroNote').innerHTML=c('带着好奇，<br>让每一次相遇，<br>都成为温柔的开始。','Let curiosity lead.<br>Let every encounter<br>begin with kindness.')+`<small>DHARMA ATLAS · ${c('探索寄语','AN INVITATION')}</small>`;
    $q('#quietButton span').textContent=quiet?c('返回探索','Show interface'):c('静赏此境','Quiet view');$q('#fullscreenButton span').textContent=c('全屏','Fullscreen');
    $q('.journey-orb small').textContent=c('开启旅程','Begin journey');
    $q('#sceneDisclosure').textContent=c('经文启发的艺术想象 · 非历史场景复原','Artistic imagination · Not a historical reconstruction');$q('#cinemaScroll').textContent=c('选择你的旅程 ↓','Choose your path ↓');
    const spots=[[c('认识佛陀','Meet the Buddha')],[c('打开圣地地图','Explore sacred places')],[c('从莲花到经典','From lotus to text')]];
    $$q('.scene-hotspots button').forEach((b,i)=>{b.setAttribute('aria-label',spots[i][0]);b.querySelector('span').textContent=spots[i][0]});
    const portals=[['atlas','互动地图','Interactive Map','跟随地点与经卷，探索彼此相连的世界。','Follow places and texts across an interconnected world.'],['works','佛典经文','Buddhist Texts','从百部经论出发，打开版本与来源。','Explore 100 texts, their editions and sources.'],['places','圣地巡礼','Sacred Places','从菩提伽耶到鹿野苑，沿着地点追寻。','From Bodh Gaya to Sarnath, follow a trail of places.'],['people','人物与故事','People & Stories','认识导师、弟子、译者与行旅者。','Meet teachers, disciples, translators and travellers.'],['timeline','时间长河','Timeline','区分作品、译本与实物的不同时间。','Unfold the dates of works, editions and objects.'],['library','图书馆与博物馆','Libraries & Museums','从馆藏号与数字影像，走近真实经卷。','Discover collections, shelfmarks and digital images.']];
    $q('#heroPortalDeck').setAttribute('aria-label',c('六种探索方式','Six ways to explore'));
    $q('#heroPortalDeck').innerHTML=portals.map(([r,z,e,dz,de],i)=>`<button type="button" class="portal-card portal-${i+1}" data-c-route="${r}"><span class="portal-art" aria-hidden="true"></span><span class="portal-copy"><strong>${c(z,e)}</strong><em>${c(e,{'atlas':'Places & connections','works':'Texts & traditions','places':'Follow the footsteps','people':'A human journey','timeline':'Encounters in time','library':'Objects & collections'}[r])}</em><small>${c(dz,de)}</small></span><span class="portal-arrow" aria-hidden="true">→</span></button>`).join('');
  }
  function renderHeader(){
    $q('.brand-lotus').innerHTML=lotus;$q('.brand strong').textContent='Dharma Atlas';$q('.brand small').textContent='EXPLORE · LEARN · BE INSPIRED';
    const nav=[['home','首页','Home'],['atlas','地图','Map'],['works','经典','Texts'],['places','圣地','Places'],['people','人物','People'],['timeline','时间线','Timeline'],['stories','故事','Stories'],['library','馆藏','Library'],['about','关于','About']];
    $q('#nav').innerHTML=nav.map(([r,z,e])=>`<a href="#${['places','timeline'].includes(r)?'atlas':r}" data-c-route="${r}">${c(z,e)}</a>`).join('');
    if(!$q('#journeyButton')){const b=document.createElement('button');b.type='button';b.id='journeyButton';b.setAttribute('aria-haspopup','dialog');$q('.header-tools').prepend(b);b.addEventListener('click',openJourney);}
    updateJourneyHeader();$$q('.footer-brand strong,.modal-brand').forEach(el=>el.textContent='Dharma Atlas');document.title=c('Dharma Atlas · 佛典世界','Dharma Atlas · Explore a kinder world');
    const current=(location.hash.slice(1)||'home').split('/')[0];$$q('#nav a').forEach(a=>{if(a.dataset.cRoute===current)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  }
  function updateJourneyHeader(){const b=$q('#journeyButton');if(b){b.innerHTML=`<span aria-hidden="true">❁</span><span class="journey-button-copy">${c('我的探索','My journey')}</span><b>${journey.xp}</b>`;b.setAttribute('aria-label',c(`我的探索，${journey.xp}点` ,`My journey, ${journey.xp} points`));}}
  function initDialogs(){
    const d=document.createElement('dialog');d.id='journeyDialog';d.setAttribute('aria-labelledby','journeyTitle');document.body.append(d);d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}});
    const s=document.createElement('dialog');s.id='discoveryDialog';s.setAttribute('aria-labelledby','discoveryTitle');s.innerHTML=`<div class="discovery-head"><div><h2 id="discoveryTitle"></h2><button type="button" class="journey-close" data-close-search aria-label="Close">×</button></div><label for="discoveryInput" class="sr-only">Search</label><input type="search" id="discoveryInput" class="discovery-input" autocomplete="off"></div><div class="discovery-results" id="discoveryResults"></div>`;document.body.append(s);$q('#discoveryInput').addEventListener('input',renderSearch);$q('[data-close-search]').addEventListener('click',()=>s.close());
  }
  function openJourney(){closeAux();renderJourney();returnTo=document.activeElement;$q('#journeyDialog').showModal();$q('#journeyDialog .journey-close').focus({preventScroll:true});}
  function renderJourney(){const unlocked=new Set(Object.keys(journey.seen).map(k=>k.split(':')[0]));let ix=0;levels.forEach((l,i)=>{if(journey.xp>=l[0])ix=i});const lev=levels[ix],nxt=levels[ix+1],p=nxt?Math.min(100,Math.round((journey.xp-lev[0])/(nxt[0]-lev[0])*100)):100;const q=daily(),done=!!journey.daily[day()],card=journey.cards[day()];const drawn=Number.isInteger(card)&&card>=0&&card<6?cards[card]:null;
    $q('#journeyDialog').innerHTML=`<div class="journey-top"><div><span class="journey-kicker">${c('你的佛典世界探索记录','YOUR DHARMA ATLAS JOURNEY')}</span><h2 id="journeyTitle">${c(lev[1],lev[2])}</h2></div><button type="button" class="journey-close" data-close-journey aria-label="${c('关闭','Close')}">×</button></div><div class="journey-body">${storageOK?'':`<p class="journey-storage-warning">${c('浏览器不允许保存。记录仅在本次会话有效。','Storage is blocked. Progress lasts for this session only.')}</p>`}<div class="journey-score"><div class="journey-ring" style="--p:${p}%"><span>❁</span></div><div><strong>${journey.xp}</strong><small>${c('探索光点 · 不用于衡量修行','Discovery points · Not a spiritual ranking')}</small><small>${nxt?c(`距下一阶段还有 ${nxt[0]-journey.xp} 点`,`${nxt[0]-journey.xp} to the next stage`):c('继续随好奇探索','Keep following your curiosity')}</small></div></div><div class="journey-section-head"><span>${c('六枚探索印章','Six exploration stamps')}</span><small>${unlocked.size}/6</small></div><div class="stamp-grid">${Object.entries(stamps).map(([k,v])=>`<div class="stamp ${unlocked.has(k)?'earned':''}"><span>${v[2]}</span><b>${c(v[0],v[1])}</b><small>${unlocked.has(k)?c('已探索','Discovered'):c('尚未探索','Not explored')}</small></div>`).join('')}</div><section class="daily-quest ${done?'done':''}"><span class="journey-kicker">${c('今日一小步','ONE SMALL STEP TODAY')}</span><h3>${done?c('今日探索已完成 ✓','Today’s quest is complete ✓'):c('只探索一件事','Discover one thing')}</h3><p>${c(q[1],q[2])}</p><button type="button" class="button primary small" data-c-route="${q[3]}">${done?c('再次探索 →','Explore again →'):c('开始探索 · 完成 +20 →','Begin · Complete for +20 →')}</button></section><div class="journey-section-head"><span>${c('今日探索卡','Today’s exploration card')}</span></div>${drawn?`<article class="explore-card"><small>${c('一条可以走的知识小径','A PATH TO FOLLOW')}</small><h3>${c(drawn[0],drawn[1])}</h3><p>${c(drawn[2],drawn[3])}</p><button type="button" data-c-route="${drawn[4]}">${c('沿这条路去看看 →','Follow this trail →')}</button></article>`:`<button type="button" class="draw-card" data-draw-card><span>❁</span><b>${c('翻开一张卡','Reveal a card')}</b><small>${c('随机的学习路线，不是占卜。每天一张，无需付费。','A random learning path, not divination. One free card a day.')}</small></button>`}<div class="journey-foot">${c('记录只保存在此浏览器。不注册，不上传。','Stored in this browser only. No account or upload.')}<br><button type="button" data-toggle-motion>${motion?c('关闭场景动效','Pause scene motion'):c('开启场景动效','Enable scene motion')}</button> · <button type="button" data-reset-journey>${c('重置探索记录','Reset journey')}</button></div></div>`;
  }
  function draw(){if(!Number.isInteger(journey.cards[day()])){const a=new Uint32Array(1);if(globalThis.crypto?.getRandomValues)crypto.getRandomValues(a);else a[0]=Math.floor(Math.random()*4294967295);journey.cards[day()]=a[0]%6;store();}renderJourney();}
  function openSearch(query=''){$q('#discoveryTitle').textContent=c('探索佛典世界','Explore the Buddhist world');$q('#discoveryInput').placeholder=c('经名、地点、人物、概念或馆藏号…','Text, place, person, concept or shelfmark…');$q('label[for=discoveryInput]').textContent=c('搜索','Search');$q('[data-close-search]').setAttribute('aria-label',c('关闭','Close'));$q('#discoveryInput').value=query;renderSearch();closeAux();$q('#discoveryDialog').showModal();$q('#discoveryInput').focus();}
  function renderSearch(){const raw=$q('#discoveryInput').value.trim(),syn=[['佛陀','buddha','释迦'],['莲花','lotus','法华'],['菩提树','bodhi','菩提'],['那烂陀','nalanda'],['般若','prajna','prajñā','wisdom'],['禅修','meditation','禅','定']];const v=norm(raw),terms=syn.find(g=>g.some(k=>norm(k)===v))?.map(norm)||[v];const matches=s=>!v||terms.some(t=>norm(s).includes(t));
    const groups=[
      [c('经典','TEXTS'),'work',A.works,w=>c(w.zh,w.en),w=>[w.zh,w.en,w.aliases,w.themes,w.ids?.map(i=>i.value)].join(' '),w=>text(w,'intro')],
      [c('地点','PLACES'),'place',A.places,w=>text(w,'name'),w=>[w.name_zh,w.name_en,w.note].join(' '),w=>c('打开地图中的地点','Open this place on the atlas')],
      [c('人物','PEOPLE'),'person',A.people,w=>text(w,'name'),w=>[w.name_zh,w.name_en,w.intro_zh,w.roles_en].join(' '),w=>text(w,'roles')],
      [c('故事','STORIES'),'story',A.stories.map((s,i)=>({...s,id:i})),w=>text(w,'title'),w=>[w.title_zh,w.title_en,w.teaser_zh,w.teaser_en].join(' '),w=>text(w,'teaser')],
      [c('馆藏','COLLECTIONS'),'object',A.objects,w=>text(w,'title'),w=>[w.title_zh,w.title_en,w.shelfmark,w.holding].join(' '),w=>w.holding]
    ];let count=0,html='';for(const [label,type,items,name,hay,sub] of groups){const all=items.filter(x=>matches(hay(x))),rows=all.slice(0,v?6:3);count+=all.length;if(rows.length)html+=`<div class="discovery-label">${label} · ${all.length}</div>`+rows.map(x=>`<button type="button" data-record="${type}" data-id="${esc(x.id)}"><span>${esc(name(x))}<small>${esc(String(sub(x)||'').slice(0,96))}</small></span><span aria-hidden="true">↗</span></button>`).join('');}
    $q('#discoveryResults').innerHTML=(v?`<p>${c(`找到 ${count} 条相关记录；每类最多展示 6 条。`,`Found ${count} records; up to six shown per category.`)}</p>`:`<p>${c('从一部经典、一个地点或一位人物开始。','Begin with a text, a place or a person.')}</p>`)+(html||`<div class="empty">${c('没有找到匹配记录。试试「心经」「那烂陀」或 “Heart Sutra”。','No matches. Try “Heart Sutra”, “Nalanda”, or another name.')}</div>`);}
  const steps=[
    ['先走进一个世界','Begin with a world','这是一座由佛教文学启发的想象花园，不是古代圣地的复原。你可以点击场景里的光点，认识人物、地点与经典。','This garden is an artistic imagining inspired by Buddhist literature, not a reconstruction. Select its light points to meet people, places and texts.','sacred-world.webp'],
    ['让一卷经打开问题','Let a text open a question','从一部经典的简介开始，再展开版本、人物、实物与资料来源。相似的题名并不自动等于同一部作品。','Begin with an introduction, then explore editions, people, objects and sources. Similar titles do not automatically mean the same work.','texts.webp'],
    ['把时间与证据连起来','Connect dates and evidence','地图上的发现地、制作地与现藏地并不总是同一处；写本的年代也不是作品的成书年代。保留这些区别，探索会更清晰。','A findspot, place of production and present collection may differ. A manuscript date is not a work’s composition date. Keep these distinctions in view.','map.webp'],
    ['留下你的探索足迹','Keep a trace of your journey','打开新的条目，点亮六枚探索印章。今日任务和探索卡只提供学习路线，不给修行打分，也不要求注册。','Open new records to collect six exploration stamps. Quests and cards offer learning paths, not spiritual rankings. No registration is required.','library.webp']
  ];
  function guide(i=0){closeAux();guideStep=Math.max(0,Math.min(3,Number(i)||0));const s=steps[guideStep];openModal(c(s[0],s[1]),`<span class="guide-step">${c('探索导览','GUIDED EXPLORATION')} · ${guideStep+1} / 4</span><div class="guide-progress">${steps.map((_,i)=>`<i class="${i<=guideStep?'active':''}"></i>`).join('')}</div><img class="guide-hero" src="./assets/${s[4]}" alt=""><p class="lead">${c(s[2],s[3])}</p><div class="dialog-actions"><button class="button porcelain small" type="button" data-guide="${guideStep-1}" ${guideStep===0?'disabled':''}>${c('← 上一站','← Previous')}</button>${guideStep<3?`<button class="button primary small" type="button" data-guide="${guideStep+1}">${c('下一站 →','Next →')}</button>`:`<button class="button primary small" type="button" data-open-journey>${c('打开我的探索 →','Open my journey →')}</button>`}</div>`,{type:'cinema-guide',id:guideStep});}
  function refresh(){renderSceneLabels();renderHeader();if($q('#journeyDialog').open)renderJourney();if($q('#discoveryDialog').open){$q('#discoveryTitle').textContent=c('探索佛典世界','Explore the Buddhist world');renderSearch();}if(modalState?.type==='cinema-guide')guide(guideStep);}
  function init(){initScene();initDialogs();renderSceneLabels();renderHeader();
    // Keep localization in the original reader, add UI localization afterwards.
    const originalLanguage=language;language=function(){originalLanguage();refresh();};
    document.addEventListener('click',e=>{const t=e.target.closest('button,a');if(!t)return;
      if(t.hasAttribute('data-c-route')){e.preventDefault();go(t.dataset.cRoute);return;}
      if(t.hasAttribute('data-record')){e.preventDefault();openRecord(t.dataset.record,t.dataset.id);return;}
      if(t.hasAttribute('data-discover')){openSearch(t.dataset.discover);return;}
      if(t.hasAttribute('data-close-journey')){$q('#journeyDialog').close();returnTo?.focus?.({preventScroll:true});return;}
      if(t.hasAttribute('data-open-journey')){if($q('#modal').open)closeModal();openJourney();return;}
      if(t.hasAttribute('data-draw-card')){draw();return;}
      if(t.hasAttribute('data-guide')){guide(t.dataset.guide);return;}
      if(t.hasAttribute('data-quiet')){$q('#quietButton').click();return;}
      if(t.hasAttribute('data-toggle-motion')){motion=!motion;document.body.classList.toggle('no-motion',!motion);renderJourney();return;}
      if(t.hasAttribute('data-reset-journey')){if(confirm(c('只重置探索光点、印章与今日卡。经典收藏和已读记录保留。确定重置？','Reset journey points, stamps and cards? Text bookmarks and reading history will be kept.'))){journey={seen:{},daily:{},cards:{},xp:0};store();renderJourney();updateJourneyHeader();}return;}
      const type={work:'text',person:'person',place:'place',event:'timeline',story:'story',read:'story',object:'library',institution:'library',figure:'library'}[t.dataset.act];
      if(type&&t.dataset.id&&$q('#modal').open)award(type,t.dataset.id);
      if(t.matches('a[href="#paths"],a[href="#main"]')){e.preventDefault();const target=$q(t.hash);target?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});if(t.hash==='#main')target?.focus({preventScroll:true});}
    });
    window.addEventListener('hashchange',()=>{renderHeader();});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&quiet){quiet=false;$q('.garden-hero').classList.remove('quiet-view');$q('#quietButton').setAttribute('aria-pressed','false');renderSceneLabels();}});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
