'use strict';
// In-page anchors should scroll the current document, not reset the page router.
document.addEventListener('click',event=>{
  const link=event.target.closest('a[href="#paths"],a[href="#main"]');
  if(link){
    const target=document.getElementById(link.getAttribute('href').slice(1));
    if(target){
      event.preventDefault();
      target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
      if(target.id==='main')target.focus({preventScroll:true});
    }
  }
  const navLink=event.target.closest('#nav a');
  if(navLink&&navLink.hash===location.hash){
    document.getElementById('nav').classList.remove('open');
    document.getElementById('menuToggle').setAttribute('aria-expanded','false');
  }
});
