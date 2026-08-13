/* Page helpers: COMP state, snackbar, dialog, AD tabs/menu/date/confirm. */
(function (global) {
  "use strict";

  var WEEK = ["日", "一", "二", "三", "四", "五", "六"];

  function applyCompState(compId, state) {
    var nodes = document.querySelectorAll('[data-comp="' + compId + '"]');
    nodes.forEach(function (n) {
      n.setAttribute("data-state", state);
    });
    var empties = document.querySelectorAll('[data-empty-for="' + compId + '"]');
    empties.forEach(function (n) {
      var hide = state !== "empty" && state !== "error";
      n.classList.toggle("is-hidden", hide);
      var msg = "";
      if (state === "empty") msg = n.getAttribute("data-empty-text") || "暂无数据";
      if (state === "error") msg = n.getAttribute("data-error-text") || "加载失败";
      if (msg) {
        var slot = n.querySelector(".md-empty__text");
        if (slot) slot.textContent = msg;
        else if (!n.querySelector(".md-empty__art")) n.textContent = msg;
      }
    });
    var skels = document.querySelectorAll('[data-skel-for="' + compId + '"]');
    skels.forEach(function (n) {
      n.classList.toggle("is-hidden", state !== "loading");
    });
    var page = document.documentElement;
    page.setAttribute("data-comp-" + compId, state);
  }

  function snackbar(text, msOrOpts) {
    var opts = typeof msOrOpts === "object" && msOrOpts ? msOrOpts : {};
    var ms = typeof msOrOpts === "number" ? msOrOpts : opts.ms || 2400;
    var bar = document.getElementById("mdSnackbar");
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "mdSnackbar";
      bar.className = "md-snackbar";
      document.body.appendChild(bar);
    }
    bar.className = "md-snackbar" + (opts.severity ? " md-snackbar--" + opts.severity : "");
    bar.textContent = text;
    bar.classList.add("is-open");
    clearTimeout(bar._t);
    bar._t = setTimeout(function () {
      bar.classList.remove("is-open");
    }, ms);
  }

  function syncDialogLock() {
    var open = document.querySelector(".md-dialog.is-open, .md-backdrop.is-open");
    document.body.classList.toggle("md-dialog-open", !!open);
  }

  function closeDialog(id) {
    var dlg = document.getElementById(id);
    var mask = document.getElementById(id + "Backdrop");
    if (dlg) {
      dlg.classList.remove("is-open");
      dlg.setAttribute("aria-hidden", "true");
    }
    if (mask) mask.classList.remove("is-open");
    syncDialogLock();
  }

  function openDialog(id) {
    var dlg = document.getElementById(id);
    var mask = document.getElementById(id + "Backdrop");
    if (mask) mask.classList.add("is-open");
    if (dlg) {
      dlg.classList.add("is-open");
      dlg.setAttribute("aria-hidden", "false");
    }
    syncDialogLock();
  }

  function closeDrawer(id) {
    var el = document.getElementById(id);
    var mask = document.getElementById(id + "Backdrop");
    if (el) el.classList.remove("is-open");
    if (mask) mask.classList.remove("is-open");
  }

  function openDrawer(id) {
    var el = document.getElementById(id);
    var mask = document.getElementById(id + "Backdrop");
    if (mask) mask.classList.add("is-open");
    if (el) el.classList.add("is-open");
  }

  function ensureConfirm() {
    if (document.getElementById("mdConfirmDlg")) return;
    var mask = document.createElement("div");
    mask.id = "mdConfirmDlgBackdrop";
    mask.className = "md-backdrop";
    var dlg = document.createElement("div");
    dlg.id = "mdConfirmDlg";
    dlg.className = "md-dialog md-dialog--sm";
    dlg.innerHTML =
      '<h2 class="md-dialog__title" id="mdConfirmTitle">确认</h2>' +
      '<div class="md-dialog__body" id="mdConfirmBody"></div>' +
      '<div class="md-dialog__actions">' +
      '<button type="button" class="md-btn md-btn--text" id="mdConfirmCancel">取消</button>' +
      '<button type="button" class="md-btn md-btn--contained" id="mdConfirmOk">确定</button>' +
      "</div>";
    document.body.appendChild(mask);
    document.body.appendChild(dlg);
    mask.addEventListener("click", function () {
      closeDialog("mdConfirmDlg");
    });
    document.getElementById("mdConfirmCancel").addEventListener("click", function () {
      closeDialog("mdConfirmDlg");
    });
  }

  function confirm(opts) {
    opts = opts || {};
    ensureConfirm();
    document.getElementById("mdConfirmTitle").textContent = opts.title || "确认";
    document.getElementById("mdConfirmBody").textContent = opts.body || "";
    var okBtn = document.getElementById("mdConfirmOk");
    okBtn.textContent = opts.ok || "确定";
    document.getElementById("mdConfirmCancel").textContent = opts.cancel || "取消";
    okBtn.onclick = function () {
      closeDialog("mdConfirmDlg");
      if (typeof opts.onOk === "function") opts.onOk();
    };
    openDialog("mdConfirmDlg");
  }

  function closeMenus(except) {
    document.querySelectorAll(".md-menu.is-open").forEach(function (m) {
      if (m !== except) m.classList.remove("is-open");
    });
    document.querySelectorAll(".md-cal-pop.is-open").forEach(function (m) {
      if (m !== except) m.classList.remove("is-open");
    });
  }

  function bindTabs() {
    document.querySelectorAll(".md-tabs").forEach(function (bar) {
      bar.addEventListener("click", function (ev) {
        var tab = ev.target.closest(".md-tab");
        if (!tab || !bar.contains(tab)) return;
        var panelId = tab.getAttribute("data-panel");
        bar.querySelectorAll(".md-tab").forEach(function (t) {
          t.classList.toggle("is-active", t === tab);
        });
        if (!panelId) return;
        var root = bar.parentElement || document;
        root.querySelectorAll(".md-tab-panel").forEach(function (p) {
          p.classList.toggle("is-active", p.id === panelId);
        });
      });
    });
  }

  function bindMenus() {
    document.addEventListener("click", function (ev) {
      var btn = ev.target.closest("[data-menu]");
      if (btn) {
        var id = btn.getAttribute("data-menu");
        var menu = document.getElementById(id);
        if (menu) {
          var open = !menu.classList.contains("is-open");
          closeMenus(menu);
          menu.classList.toggle("is-open", open);
        }
        ev.stopPropagation();
        return;
      }
      if (
        !ev.target.closest(".md-menu") &&
        !ev.target.closest(".md-cal-pop") &&
        !ev.target.closest(".md-field--date")
      ) {
        closeMenus();
      }
    });
  }

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function ymd(y, m, d) {
    return y + "-" + pad(m + 1) + "-" + pad(d);
  }

  function renderCal(pop, input, view) {
    var y = view.getFullYear();
    var m = view.getMonth();
    var first = new Date(y, m, 1);
    var start = first.getDay();
    var days = new Date(y, m + 1, 0).getDate();
    var prevDays = new Date(y, m, 0).getDate();
    var selected = (input.value || "").split("-");
    var html =
      '<div class="md-cal"><div class="md-cal__head">' +
      '<button type="button" class="md-icon-btn" data-cal="prev">‹</button>' +
      "<span>" +
      y +
      "年" +
      (m + 1) +
      "月</span>" +
      '<button type="button" class="md-icon-btn" data-cal="next">›</button></div>' +
      '<div class="md-cal__week">' +
      WEEK.map(function (w) {
        return "<span>" + w + "</span>";
      }).join("") +
      "</div><div class=\"md-cal__grid\">";
    var i;
    for (i = 0; i < start; i += 1) {
      html +=
        '<button type="button" class="md-cal__day is-muted" data-day="' +
        ymd(y, m - 1, prevDays - start + i + 1) +
        '">' +
        (prevDays - start + i + 1) +
        "</button>";
    }
    var today = new Date();
    var todayStr = ymd(today.getFullYear(), today.getMonth(), today.getDate());
    for (i = 1; i <= days; i += 1) {
      var val = ymd(y, m, i);
      var cls = "md-cal__day";
      if (val === todayStr) cls += " is-today";
      if (
        selected.length === 3 &&
        Number(selected[0]) === y &&
        Number(selected[1]) === m + 1 &&
        Number(selected[2]) === i
      ) {
        cls += " is-active";
      }
      html +=
        '<button type="button" class="' + cls + '" data-day="' + val + '">' + i + "</button>";
    }
    html += "</div></div>";
    pop.innerHTML = html;
    pop._view = view;
  }

  function bindCals() {
    document.querySelectorAll(".md-field--date").forEach(function (field) {
      var input = field.querySelector('input[type="date"], input.md-field__input');
      if (!input) return;
      var pop = field.querySelector(".md-cal-pop");
      if (!pop) {
        pop = document.createElement("div");
        pop.className = "md-cal-pop";
        field.appendChild(pop);
      }
      function openPop() {
        closeMenus(pop);
        if (pop.classList.contains("is-open")) return;
        var base = input.value ? new Date(input.value + "T00:00:00") : new Date();
        if (isNaN(base.getTime())) base = new Date();
        renderCal(pop, input, base);
        pop.classList.add("is-open");
      }
      field.addEventListener("click", function (ev) {
        ev.stopPropagation();
      });
      input.addEventListener("focus", openPop);
      input.addEventListener("click", openPop);
      pop.addEventListener("mousedown", function (ev) {
        ev.preventDefault();
      });
      pop.addEventListener("click", function (ev) {
        var nav = ev.target.closest("[data-cal]");
        if (nav) {
          var view = pop._view || new Date();
          view = new Date(view.getFullYear(), view.getMonth() + (nav.getAttribute("data-cal") === "next" ? 1 : -1), 1);
          renderCal(pop, input, view);
          ev.preventDefault();
          return;
        }
        var day = ev.target.closest("[data-day]");
        if (day) {
          input.value = day.getAttribute("data-day");
          pop.classList.remove("is-open");
          input.dispatchEvent(new Event("change", { bubbles: true }));
        }
      });
    });
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

  function bindUi() {
    bindTabs();
    bindMenus();
    bindCals();
  }

  global.ProtoPage = {
    applyCompState: applyCompState,
    snackbar: snackbar,
    openDialog: openDialog,
    closeDialog: closeDialog,
    openDrawer: openDrawer,
    closeDrawer: closeDrawer,
    confirm: confirm,
    closeMenus: closeMenus,
  };

  window.addEventListener("message", onMessage);
  window.addEventListener("hashchange", onHash);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      onHash();
      bindUi();
    });
  } else {
    onHash();
    bindUi();
  }
})(window);
