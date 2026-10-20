// 그림 확대. 넓은 화면에서 누르면 화면에 맞춰 크게 보이는 그림에만 돋보기 커서를 달고, 누르면 화면 가득 띄운다.
// - 원본보다 크게 늘리지 않는다. 띄운 폭이 지금 폭의 1.25배가 안 되면 확대하지 않는다
// - 닫기: 아무 데나 누르기, Esc, 뒤로 가기. 뒤로 가기가 이전 페이지로 나가지 않게 열 때 기록을 하나 쌓는다
// - 좁은 화면(모바일)에서는 아무것도 하지 않는다. 화면 폭이 그림 폭과 거의 같아 띄워도 커지지 않고, 두 손가락 확대가 이미 된다
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll(".post-figure img"));
  if (!imgs.length || !window.HTMLDialogElement) return;
  var wide = window.matchMedia("(min-width: 1100px) and (pointer: fine)");

  var dlg = document.createElement("dialog");
  dlg.className = "zoom";
  var big = document.createElement("img");
  var cap = document.createElement("p");
  dlg.appendChild(big);
  dlg.appendChild(cap);
  document.body.appendChild(dlg);

  // 띄웠을 때의 폭. 그림 파일의 크기는 render-image.html이 적은 width·height로 안다(늦게 불러오는 그림도 바로 잴 수 있다).
  function fit(img) {
    var w = +img.getAttribute("width"), h = +img.getAttribute("height");
    if (!w || !h) return 0;
    return Math.min(w, window.innerWidth - 64, (window.innerHeight - 120) * w / h);
  }

  function grows(img) {
    return wide.matches && fit(img) >= img.clientWidth * 1.25;
  }

  function mark() {
    imgs.forEach(function (img) { img.classList.toggle("can-zoom", grows(img)); });
  }

  imgs.forEach(function (img) {
    img.addEventListener("click", function () {
      if (!grows(img)) return;
      big.src = img.currentSrc || img.src;
      big.alt = img.alt;
      big.style.width = Math.floor(fit(img)) + "px";
      var fc = img.closest("figure").querySelector("figcaption");
      cap.innerHTML = fc ? fc.innerHTML : ""; // 보고서형 캡션의 "그림 N."과 출처 줄을 그대로 옮긴다
      cap.hidden = !fc;
      dlg.showModal();
      history.pushState({ zoom: 1 }, "");
    });
  });

  dlg.addEventListener("click", function () { dlg.close(); });
  dlg.addEventListener("close", function () {
    if (history.state && history.state.zoom) history.back();
  });
  window.addEventListener("popstate", function () {
    if (dlg.open) dlg.close();
  });

  mark();
  window.addEventListener("resize", mark);
  if (wide.addEventListener) wide.addEventListener("change", mark);
})();
