// 벤치 표(partials/bench/table.html)의 머리글 정렬과 벤치 탭(layouts/bench/list.html).
// 머리글을 누르면 그 열의 좋은 쪽부터 줄을 다시 세운다. 탭은 벤치가 둘 이상일 때만 있다.
(function () {
  document.querySelectorAll('.bench-table').forEach(function (table) {
    var heads = Array.prototype.slice.call(table.querySelectorAll('thead tr.bench-cols th'));
    var body = table.tBodies[0];
    function sortBy(c) {
      var th = heads[c], lower = th.hasAttribute('data-lower');
      var val = function (r) { return parseFloat(r.cells[c].getAttribute('data-v')); };
      var rows = Array.prototype.slice.call(body.rows);
      rows.sort(function (a, b) { return lower ? val(a) - val(b) : val(b) - val(a); });
      rows.forEach(function (r) { body.appendChild(r); });
      heads.forEach(function (h) { h.classList.remove('is-sorted'); h.removeAttribute('aria-sort'); });
      th.classList.add('is-sorted');
      th.setAttribute('aria-sort', lower ? 'ascending' : 'descending');
    }
    heads.forEach(function (th, c) {
      if (!th.hasAttribute('data-sort')) return;
      th.addEventListener('click', function () { sortBy(c); });
      th.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sortBy(c); }
      });
    });
  });

  var tabs = document.querySelectorAll('.bench-tab[data-board]');
  if (!tabs.length) return;
  document.documentElement.classList.add('bench-js');
  function show(id) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-board') === id;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-selected', on);
    });
    document.querySelectorAll('.bench-panel[data-panel]').forEach(function (p) {
      p.classList.toggle('is-on', p.getAttribute('data-panel') === id);
    });
  }
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      var id = t.getAttribute('data-board');
      show(id);
      history.replaceState(null, '', '#' + id);
    });
  });
  var hash = location.hash.slice(1);
  if (hash && document.querySelector('.bench-tab[data-board="' + hash + '"]')) show(hash);
})();
