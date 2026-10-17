// 글 옆 목차(TREE)의 현재 절 표시와 읽기 진행률. layouts/partials/post-rail.html과 함께 쓴다.
// 목차가 없는 페이지에서는 아무것도 하지 않는다.
(function () {
  var tree = document.getElementById("rail-tree");
  var article = document.querySelector(".post-body");
  if (!tree || !article) return;

  var links = Array.prototype.slice.call(tree.querySelectorAll("a[href^='#']"));
  var heads = links
    .map(function (a) { return document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1))); })
    .filter(Boolean);
  var bar = document.getElementById("rail-progress");
  var top = document.getElementById("top-progress");
  var CELLS = 20;

  function current() {
    // 화면 위에서 30% 지점을 지난 마지막 제목이 지금 읽는 절이다. 첫 제목 전이면 첫 절을 표시한다.
    var line = window.innerHeight * 0.3;
    var on = null;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top <= line) on = heads[i];
    }
    return on || heads[0];
  }

  function mark(head) {
    var id = head ? head.id : null;
    links.forEach(function (a) {
      var hit = id !== null && decodeURIComponent(a.getAttribute("href").slice(1)) === id;
      a.classList.toggle("on", hit);
    });
    // 하위 절 목록은 지금 읽는 절이 속한 항목만 펼친다.
    tree.querySelectorAll("li").forEach(function (li) {
      li.classList.toggle("open", !!li.querySelector("a.on"));
    });
  }

  function progress() {
    var box = article.getBoundingClientRect();
    var total = box.height - window.innerHeight;
    var ratio = total > 0 ? Math.min(1, Math.max(0, -box.top / total)) : 1;
    var pct = Math.round(ratio * 100);
    if (bar) {
      var filled = Math.round(ratio * CELLS);
      bar.querySelector("b").textContent = "▓".repeat(filled);
      bar.querySelector(".rail__rest").textContent = "░".repeat(CELLS - filled);
      bar.querySelector(".rail__pct").textContent = pct + "%";
    }
    if (top) top.style.width = pct + "%";
  }

  var queued = false;
  function update() {
    queued = false;
    mark(current());
    progress();
  }
  window.addEventListener("scroll", function () {
    if (!queued) { queued = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener("resize", update);
  update();
})();
