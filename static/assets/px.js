(function () {
  var btn = document.querySelector('.menu'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  var fb = document.querySelectorAll('.filters button'), cards = document.querySelectorAll('#grid .card'), empty = document.querySelector('.empty');
  function apply(cat) {
    var shown = 0;
    fb.forEach(function (b) { var on = b.getAttribute('data-cat') === cat; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    cards.forEach(function (c, i) {
      var show = cat === 'all' ? ((document.getElementById("main").dataset.limit) ? i < +document.getElementById("main").dataset.limit : true) : c.getAttribute('data-cat') === cat;
      c.hidden = !show; if (show) shown++;
    });
    if (empty) empty.hidden = shown > 0;
  }
  if (fb.length) {
    fb.forEach(function (b) { b.addEventListener('click', function () {
      apply(b.getAttribute('data-cat'));
      var g = document.getElementById('grid'); if (g && window.scrollY < g.offsetTop - 200) g.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    }); });
    apply('all');
  }
})();
