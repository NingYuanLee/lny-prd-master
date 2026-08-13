/* Page helpers: COMP state via postMessage / hash, snackbar, dialog. */
(function (global) {
  "use strict";

  function applyCompState(compId, state) {
    var nodes = document.querySelectorAll('[data-comp="' + compId + '"]');
    nodes.forEach(function (n) {
      n.setAttribute("data-state", state);
    });
    var empties = document.querySelectorAll('[data-empty-for="' + compId + '"]');
    empties.forEach(function (n) {
      var hide = state !== "empty" && state !== "error";
      n.classList.toggle("is-hidden", hide);
      if (state === "empty") n.textContent = n.getAttribute("data-empty-text") || "暂无数据";
      if (state === "error") n.textContent = n.getAttribute("data-error-text") || "加载失败";
    });
    var page = document.documentElement;
    page.setAttribute("data-comp-" + compId, state);
  }

  function snackbar(text, ms) {
    var bar = document.getElementById("mdSnackbar");
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "mdSnackbar";
      bar.className = "md-snackbar";
      document.body.appendChild(bar);
    }
    bar.textContent = text;
    bar.classList.add("is-open");
    clearTimeout(bar._t);
    bar._t = setTimeout(function () {
      bar.classList.remove("is-open");
    }, ms || 2400);
  }

  function closeDialog(id) {
    var dlg = document.getElementById(id);
    var mask = document.getElementById(id + "Backdrop");
    if (dlg) dlg.classList.remove("is-open");
    if (mask) mask.classList.remove("is-open");
  }

  function openDialog(id) {
    var dlg = document.getElementById(id);
    var mask = document.getElementById(id + "Backdrop");
    if (mask) mask.classList.add("is-open");
    if (dlg) dlg.classList.add("is-open");
  }

  function onMessage(ev) {
    var data = ev.data || {};
    if (data.type === "comp-state" && data.compId) {
      applyCompState(data.compId, data.state);
    }
  }

  function onHash() {
    var q = new URLSearchParams(location.hash.replace(/^#/, "").replace(/^\?/, ""));
    q.forEach(function (state, compId) {
      if (compId) applyCompState(compId, state);
    });
  }

  global.ProtoPage = {
    applyCompState: applyCompState,
    snackbar: snackbar,
    openDialog: openDialog,
    closeDialog: closeDialog,
  };

  window.addEventListener("message", onMessage);
  window.addEventListener("hashchange", onHash);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onHash);
  } else {
    onHash();
  }
})(window);
