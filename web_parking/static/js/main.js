// Main JS for dark mode, animated counters
(function(){
  // Dark mode toggle
  const btn = document.getElementById('dark-toggle');
  function setDark(enabled){
    if(enabled){
      document.documentElement.classList.add('dark-mode');
      btn.textContent = 'Light';
    } else {
      document.documentElement.classList.remove('dark-mode');
      btn.textContent = 'Dark';
    }
    localStorage.setItem('smartpark-dark', enabled? '1':'0');
  }
  if(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      const enabled = !document.documentElement.classList.contains('dark-mode');
      setDark(enabled);
    });
    const pref = localStorage.getItem('smartpark-dark');
    if(pref === '1') setDark(true);
    else setDark(false);
  }

  // Animated counters (elements with data-target)
  function animateCounter(el){
    const target = parseInt(el.getAttribute('data-target')||'0',10);
    let cur = 0;
    const step = Math.max(1, Math.floor(target/60));
    const id = setInterval(()=>{
      cur += step;
      if(cur>=target){ el.textContent = target; clearInterval(id); }
      else el.textContent = cur;
    }, 16);
  }
  document.addEventListener('DOMContentLoaded', ()=>{
    document.querySelectorAll('[data-target]').forEach(animateCounter);
  });
})();
