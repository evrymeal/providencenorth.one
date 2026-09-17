(function(){
  var b=document.getElementById('burger'), m=document.getElementById('mnav');
  if(!b||!m) return;
  b.addEventListener('click',function(){
    var open=m.classList.toggle('open');
    b.setAttribute('aria-expanded', open?'true':'false');
  });
  m.addEventListener('click',function(e){ if(e.target.tagName==='A'){ m.classList.remove('open'); b.setAttribute('aria-expanded','false'); }});
})();
