(function(){
  var lb=document.getElementById('lb'), img=document.getElementById('lb-img'), cnt=document.getElementById('lb-count');
  var list=[], idx=0, last=null;
  function show(){ var b=list[idx], i=b.querySelector('img'); img.src=i.currentSrc||i.src; img.alt=i.alt; cnt.textContent=(idx+1)+' / '+list.length; }
  function open(btn){
    last=btn; list=[].slice.call(document.querySelectorAll('.g-item[data-group="'+btn.dataset.group+'"]'));
    idx=list.indexOf(btn); show(); lb.hidden=false; document.body.style.overflow='hidden'; lb.querySelector('.lb-x').focus();
  }
  function close(){ lb.hidden=true; document.body.style.overflow=''; if(last) last.focus(); }
  function step(d){ idx=(idx+d+list.length)%list.length; show(); }
  document.querySelectorAll('.g-item').forEach(function(b){ b.addEventListener('click',function(){ open(b); }); });
  lb.querySelector('.lb-x').addEventListener('click',close);
  lb.querySelector('.prev').addEventListener('click',function(e){ e.stopPropagation(); step(-1); });
  lb.querySelector('.next').addEventListener('click',function(e){ e.stopPropagation(); step(1); });
  lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown',function(e){
    if(lb.hidden) return;
    if(e.key==='Escape') close(); else if(e.key==='ArrowLeft') step(-1); else if(e.key==='ArrowRight') step(1);
  });
  var sx=null;
  lb.addEventListener('touchstart',function(e){ sx=e.touches[0].clientX; },{passive:true});
  lb.addEventListener('touchend',function(e){ if(sx===null) return; var dx=e.changedTouches[0].clientX-sx; if(Math.abs(dx)>50) step(dx<0?1:-1); sx=null; });
  document.querySelectorAll('img').forEach(function(i){ i.addEventListener('error',function(){ i.style.visibility='hidden'; }); });
})();
