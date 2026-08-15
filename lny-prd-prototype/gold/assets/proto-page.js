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

  function isMobilePage() {
    return !!document.querySelector(".md-mobile-page");
  }

  function snackbarIcon(severity) {
    if (severity === "error") return "error";
    if (severity === "warning") return "warning";
    if (severity === "info") return "info";
    return "check";
  }

  function clampPct(pct) {
    var n = Number(pct);
    if (isNaN(n)) n = 0;
    return Math.max(0, Math.min(100, n));
  }

  function setMeterText(el, n, valueText, valueSel) {
    el.setAttribute("aria-valuenow", String(Math.round(n)));
    var val = el.querySelector(valueSel);
    if (val) val.textContent = valueText != null ? valueText : Math.round(n) + "%";
  }

  function setProgress(root, pct, valueText) {
    var el = typeof root === "string" ? document.querySelector(root) : root;
    if (!el) return;
    var n = clampPct(pct);
    var bar = el.querySelector(".md-progress__bar");
    if (bar && el.className.indexOf("md-progress--indeterminate") === -1) {
      bar.style.width = n + "%";
    }
    setMeterText(el, n, valueText, ".md-progress__value");
  }

  function advanceSegCount(el) {
    var n = Number(el.getAttribute("data-segments"));
    if (!n || n < 2) n = 4;
    if (n > 12) n = 12;
    return n;
  }

  function ensureAdvanceSegs(el) {
    var track = el.querySelector(".md-advance__track");
    if (!track) return [];
    var count = advanceSegCount(el);
    var segs = track.querySelectorAll(".md-advance__seg");
    if (segs.length === count) return segs;
    track.innerHTML = "";
    var i;
    for (i = 0; i < count; i += 1) {
      var seg = document.createElement("div");
      seg.className = "md-advance__seg";
      var bar = document.createElement("div");
      bar.className = "md-advance__bar";
      seg.appendChild(bar);
      track.appendChild(seg);
    }
    return track.querySelectorAll(".md-advance__seg");
  }

  function paintAdvance(el, pct) {
    var n = clampPct(pct);
    var segs = ensureAdvanceSegs(el);
    var count = segs.length;
    var units = (n / 100) * count;
    if (Math.abs(units - Math.round(units)) < 0.02) units = Math.round(units);
    segs.forEach(function (seg, i) {
      var bar = seg.querySelector(".md-advance__bar");
      if (!bar) return;
      var fill = 0;
      if (units >= i + 1) fill = 100;
      else if (units > i) fill = (units - i) * 100;
      bar.style.width = fill + "%";
    });
    return n;
  }

  function setAdvance(root, pct, valueText) {
    var el = typeof root === "string" ? document.querySelector(root) : root;
    if (!el) return;
    var n = paintAdvance(el, pct);
    setMeterText(el, n, valueText, ".md-advance__value");
  }

  function bindProgress() {
    document.querySelectorAll(".md-progress").forEach(function (el) {
      var now = el.getAttribute("aria-valuenow");
      setProgress(el, now == null ? 0 : now, (el.querySelector(".md-progress__value") || {}).textContent);
    });
    document.querySelectorAll(".md-advance").forEach(function (el) {
      var now = el.getAttribute("aria-valuenow");
      var val = el.querySelector(".md-advance__value");
      setAdvance(el, now == null ? 0 : now, val ? val.textContent : null);
    });
  }

  function snackbar(text, msOrOpts) {
    var opts = typeof msOrOpts === "object" && msOrOpts ? msOrOpts : {};
    var ms = typeof msOrOpts === "number" ? msOrOpts : opts.ms || 2400;
    var bar = document.getElementById("mdSnackbar");
    var mobile = isMobilePage();
    var sev = opts.severity || "";
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "mdSnackbar";
      document.body.appendChild(bar);
    }
    bar.className = "md-snackbar"
      + (sev ? " md-snackbar--" + sev : "")
      + (mobile ? " md-snackbar--toast" : "");
    if (mobile) {
      bar.innerHTML = '<span class="md-snackbar__icon md-icon" data-icon="'
        + snackbarIcon(sev)
        + '" aria-hidden="true"></span><span class="md-snackbar__text"></span>';
      bar.querySelector(".md-snackbar__text").textContent = text;
      if (global.ProtoIcons && global.ProtoIcons.mount) global.ProtoIcons.mount(bar);
    } else {
      bar.textContent = text;
    }
    bar.classList.add("is-open");
    clearTimeout(bar._t);
    bar._t = setTimeout(function () {
      bar.classList.remove("is-open");
    }, ms);
  }

  function syncDialogLock() {
    var open = document.querySelector(
      ".md-dialog.is-open, .md-backdrop.is-open, .md-lightbox.is-open"
    );
    document.body.classList.toggle("md-dialog-open", !!open);
    document.body.classList.toggle(
      "md-lightbox-open",
      !!document.querySelector(".md-lightbox.is-open")
    );
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
    document.querySelectorAll(".is-menu-host").forEach(function (el) {
      if (except && el.contains(except)) return;
      el.classList.remove("is-menu-host");
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
        var pane = document.getElementById(panelId);
        var root =
          pane && pane.parentElement ? pane.parentElement : document;
        root.querySelectorAll(".md-tab-panel").forEach(function (p) {
          p.classList.toggle("is-active", p.id === panelId);
        });
      });
    });
  }

  function placeFixedMenu(btn, menu) {
    if (!menu.classList.contains("md-menu--fixed")) return;
    var host = btn.closest("tr") || btn.closest(".md-select-wrap") || btn.parentElement;
    if (host) host.classList.add("is-menu-host");
    var r = btn.getBoundingClientRect();
    menu.style.position = "fixed";
    menu.style.top = r.bottom + 4 + "px";
    menu.style.left = "auto";
    menu.style.right = Math.max(8, window.innerWidth - r.right) + "px";
    menu.style.minWidth = "128px";
    menu.style.zIndex = "1300";
  }

  function bindMenus() {
    document.addEventListener("click", function (ev) {
      if (ev.target.closest(".md-menu__item")) {
        closeMenus();
        return;
      }
      var btn = ev.target.closest("[data-menu]");
      if (btn) {
        var id = btn.getAttribute("data-menu");
        var menu = document.getElementById(id);
        if (menu) {
          var open = !menu.classList.contains("is-open");
          closeMenus(menu);
          menu.classList.toggle("is-open", open);
          if (open) placeFixedMenu(btn, menu);
        }
        ev.stopPropagation();
        return;
      }
      if (
        !ev.target.closest(".md-menu") &&
        !ev.target.closest(".md-cal-pop") &&
        !ev.target.closest(".md-field--date") &&
        !ev.target.closest(".md-field--daterange")
      ) {
        closeMenus();
      }
    });
    document.addEventListener(
      "scroll",
      function () {
        closeMenus();
      },
      true
    );
  }

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function ymd(y, m, d) {
    return y + "-" + pad(m + 1) + "-" + pad(d);
  }

  function parseRange(input) {
    var start = (input.getAttribute("data-start") || "").trim();
    var end = (input.getAttribute("data-end") || "").trim();
    if (!start && input.value) {
      var parts = String(input.value).split(/\s*[~～]\s*/);
      start = (parts[0] || "").trim();
      end = (parts[1] || "").trim();
    }
    return { start: start, end: end };
  }

  function writeRange(input, start, end) {
    if (start && end && start > end) {
      var tmp = start;
      start = end;
      end = tmp;
    }
    input.setAttribute("data-start", start || "");
    input.setAttribute("data-end", end || "");
    input.value = start && end ? start + " ~ " + end : start || "";
  }

  function calDayClass(val, todayStr, rangeMode, range, selected) {
    var cls = "md-cal__day";
    if (val === todayStr) cls += " is-today";
    if (rangeMode && range) {
      if (range.start && range.end) {
        if (val === range.start) cls += " is-active is-range-start";
        else if (val === range.end) cls += " is-active is-range-end";
        else if (val > range.start && val < range.end) cls += " is-in-range";
      } else if (range.start && val === range.start) {
        cls += " is-active is-range-start";
      }
    } else if (selected === val) {
      cls += " is-active";
    }
    return cls;
  }

  function renderCal(pop, input, view) {
    var y = view.getFullYear();
    var m = view.getMonth();
    var first = new Date(y, m, 1);
    var start = first.getDay();
    var days = new Date(y, m + 1, 0).getDate();
    var prevDays = new Date(y, m, 0).getDate();
    var rangeMode = !!pop._rangeMode;
    var range = rangeMode ? pop._range || parseRange(input) : null;
    var selected = rangeMode ? "" : (input.value || "").trim();
    var hint = "";
    if (rangeMode) {
      hint = range && range.start && !range.end ? "再点结束日期" : "先点开始日期，再点结束日期";
    }
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
    var today = new Date();
    var todayStr = ymd(today.getFullYear(), today.getMonth(), today.getDate());
    for (i = 0; i < start; i += 1) {
      var prevVal = ymd(y, m - 1, prevDays - start + i + 1);
      html +=
        '<button type="button" class="' +
        calDayClass(prevVal, todayStr, rangeMode, range, selected) +
        ' is-muted" data-day="' +
        prevVal +
        '">' +
        (prevDays - start + i + 1) +
        "</button>";
    }
    for (i = 1; i <= days; i += 1) {
      var val = ymd(y, m, i);
      html +=
        '<button type="button" class="' +
        calDayClass(val, todayStr, rangeMode, range, selected) +
        '" data-day="' +
        val +
        '">' +
        i +
        "</button>";
    }
    html += "</div>";
    if (hint) html += '<p class="md-cal__hint">' + hint + "</p>";
    html += "</div>";
    pop.innerHTML = html;
    pop._view = view;
  }

  function bindCals() {
    document.querySelectorAll(".md-field--date, .md-field--daterange").forEach(function (field) {
      var rangeMode = field.classList.contains("md-field--daterange");
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
        pop._rangeMode = rangeMode;
        var base;
        if (rangeMode) {
          pop._range = parseRange(input);
          base = pop._range.start ? new Date(pop._range.start + "T00:00:00") : new Date();
        } else {
          base = input.value ? new Date(input.value + "T00:00:00") : new Date();
        }
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
        if (!day) return;
        var picked = day.getAttribute("data-day");
        if (rangeMode) {
          var r = pop._range || { start: "", end: "" };
          if (!r.start || r.end) {
            pop._range = { start: picked, end: "" };
            renderCal(pop, input, pop._view || new Date());
            return;
          }
          writeRange(input, r.start, picked);
          pop._range = parseRange(input);
          pop.classList.remove("is-open");
          input.dispatchEvent(new Event("change", { bubbles: true }));
          return;
        }
        input.value = picked;
        pop.classList.remove("is-open");
        input.dispatchEvent(new Event("change", { bubbles: true }));
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

  function bindSwipers() {
    document.querySelectorAll(".md-swiper").forEach(function (root) {
      var track = root.querySelector(".md-swiper__track");
      var slides = root.querySelectorAll(".md-swiper__slide");
      var dotsHost = root.querySelector(".md-swiper__dots");
      if (!track || slides.length < 2) return;
      var i = 0;
      function paintDots() {
        if (!dotsHost) return;
        var dots = dotsHost.querySelectorAll(".md-swiper__dot");
        if (!dots.length) {
          for (var s = 0; s < slides.length; s += 1) {
            var b = document.createElement("button");
            b.type = "button";
            b.className = "md-swiper__dot" + (s === 0 ? " is-active" : "");
            b.setAttribute("aria-label", String(s + 1));
            (function (idx) {
              b.addEventListener("click", function () {
                go(idx);
              });
            })(s);
            dotsHost.appendChild(b);
          }
          dots = dotsHost.querySelectorAll(".md-swiper__dot");
        }
        dots.forEach(function (d, di) {
          d.classList.toggle("is-active", di === i);
        });
      }
      function go(n) {
        i = (n + slides.length) % slides.length;
        track.style.transform = "translateX(" + -i * 100 + "%)";
        paintDots();
      }
      paintDots();
      if (root.getAttribute("data-auto") !== "off") {
        setInterval(function () {
          go(i + 1);
        }, 4000);
      }
    });
  }

  function ensureStatusBar() {
    var page = document.querySelector(".md-mobile-page");
    if (!page) return;
    var bars = document.querySelectorAll(".md-status-bar");
    var bar = bars[0];
    var i;
    for (i = 1; i < bars.length; i++) {
      bars[i].parentNode.removeChild(bars[i]);
    }
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "md-status-bar";
      bar.setAttribute("aria-hidden", "true");
      bar.innerHTML = '<span>9:41</span><span class="md-status-bar__signals"></span>';
    }
    bar.classList.add("md-status-bar--chrome");
    bar.classList.remove("md-status-bar--mp");
    var immersive = page.classList.contains("md-immersive") || page.classList.contains("md-sink");
    bar.classList.toggle("md-status-bar--immersive", immersive);
    bar.classList.toggle("md-status-bar--standard", !immersive);
    if (!page.classList.contains("md-immersive") && !page.classList.contains("md-sink") && !page.classList.contains("md-standard")) {
      page.classList.add("md-standard");
    }
    if (bar.parentNode !== document.body) {
      document.body.insertBefore(bar, document.body.firstChild);
    }
  }

  var REGION = [
    { n: "浙江省", c: [
      { n: "杭州市", d: ["西湖区", "余杭区", "滨江区"] },
      { n: "宁波市", d: ["海曙区", "鄞州区"] }
    ]},
    { n: "广东省", c: [
      { n: "广州市", d: ["天河区", "越秀区"] },
      { n: "深圳市", d: ["南山区", "福田区"] }
    ]},
    { n: "四川省", c: [
      { n: "成都市", d: ["武侯区", "锦江区"] }
    ]}
  ];

  function daysInMonth(y, m) {
    return new Date(y, m, 0).getDate();
  }

  function fillCol(col, items, selected) {
    col.innerHTML = items.map(function (item) {
      var on = item === selected ? " is-active" : "";
      return '<div class="md-wheel__opt' + on + '" data-val="' + item + '">' + item + "</div>";
    }).join("");
  }

  function fmtDateParts(sel) {
    return sel[0] + "-" + pad(Number(sel[1])) + "-" + pad(Number(sel[2]));
  }

  function parseDateParts(s, fallback) {
    var cur = (s || "").split("-");
    return [
      cur[0] || fallback[0],
      String(Number(cur[1]) || fallback[1]),
      String(Number(cur[2]) || fallback[2])
    ];
  }

  function ensureWheel() {
    if (document.getElementById("mdWheelSheet")) return;
    var mask = document.createElement("div");
    mask.id = "mdWheelSheetBackdrop";
    mask.className = "md-backdrop";
    var sheet = document.createElement("aside");
    sheet.id = "mdWheelSheet";
    sheet.className = "md-drawer md-drawer--bottom md-wheel";
    sheet.setAttribute("aria-hidden", "true");
    sheet.innerHTML =
      '<div class="md-wheel__bar">' +
      '<button type="button" class="md-btn md-btn--text" data-wheel-cancel>取消</button>' +
      '<h2 class="md-wheel__title" id="mdWheelTitle">请选择</h2>' +
      '<button type="button" class="md-btn md-btn--text" data-wheel-ok>确定</button>' +
      "</div>" +
      '<div class="md-wheel__tabs" hidden>' +
      '<button type="button" class="md-wheel__tab is-active" data-range-tab="start">开始日期</button>' +
      '<button type="button" class="md-wheel__tab" data-range-tab="end">结束日期</button>' +
      "</div>" +
      '<div class="md-wheel__cols">' +
      '<div class="md-wheel__col" data-col="0"></div>' +
      '<div class="md-wheel__col" data-col="1"></div>' +
      '<div class="md-wheel__col" data-col="2"></div>' +
      "</div>";
    document.body.appendChild(mask);
    document.body.appendChild(sheet);
    mask.addEventListener("click", function () {
      closeDrawer("mdWheelSheet");
    });
    sheet.querySelector("[data-wheel-cancel]").addEventListener("click", function () {
      closeDrawer("mdWheelSheet");
    });
    sheet.querySelector("[data-wheel-ok]").addEventListener("click", function () {
      var trig = sheet._trigger;
      if (trig) {
        var text;
        if (sheet._kind === "daterange") {
          var a = fmtDateParts(sheet._start);
          var b = fmtDateParts(sheet._end);
          if (a > b) {
            var swap = a;
            a = b;
            b = swap;
          }
          text = a + " ~ " + b;
          trig.setAttribute("data-start", a);
          trig.setAttribute("data-end", b);
          trig.setAttribute("data-value", a + "~" + b);
        } else if (sheet._kind === "date") {
          text = fmtDateParts(sheet._sel);
          trig.setAttribute("data-value", sheet._sel.join("-"));
        } else {
          text = sheet._sel.join(" ");
          trig.setAttribute("data-value", sheet._sel.join("-"));
        }
        trig.textContent = text;
        trig.classList.add("has-value");
        trig.dispatchEvent(new Event("change", { bubbles: true }));
      }
      closeDrawer("mdWheelSheet");
    });
    sheet.querySelectorAll("[data-range-tab]").forEach(function (tab) {
      tab.addEventListener("click", function () {
        var next = tab.getAttribute("data-range-tab");
        sheet._rangeTab = next;
        sheet._sel = next === "start" ? sheet._start : sheet._end;
        sheet.querySelectorAll("[data-range-tab]").forEach(function (t) {
          t.classList.toggle("is-active", t === tab);
        });
        paintWheel(sheet);
      });
    });
    sheet.querySelectorAll(".md-wheel__col").forEach(function (col) {
      col.addEventListener("click", function (ev) {
        var opt = ev.target.closest(".md-wheel__opt");
        if (!opt) return;
        var idx = Number(col.getAttribute("data-col"));
        sheet._sel[idx] = opt.getAttribute("data-val");
        paintWheel(sheet);
      });
    });
  }

  function dateCols(sel) {
    var y = Number(sel[0]);
    var m = Number(sel[1]);
    var years = [];
    var i;
    for (i = 2025; i <= 2028; i += 1) years.push(String(i));
    var months = [];
    for (i = 1; i <= 12; i += 1) months.push(String(i));
    if (years.indexOf(sel[0]) < 0) sel[0] = "2026";
    if (months.indexOf(sel[1]) < 0) sel[1] = "8";
    y = Number(sel[0]);
    m = Number(sel[1]);
    var maxd = daysInMonth(y, m);
    var days = [];
    for (i = 1; i <= maxd; i += 1) days.push(String(i));
    if (days.indexOf(sel[2]) < 0) sel[2] = String(Math.min(Number(sel[2]) || 14, maxd));
    return [years, months, days];
  }

  function regionCols(sel) {
    var p = REGION.filter(function (x) { return x.n === sel[0]; })[0] || REGION[0];
    sel[0] = p.n;
    var c = p.c.filter(function (x) { return x.n === sel[1]; })[0] || p.c[0];
    sel[1] = c.n;
    if (c.d.indexOf(sel[2]) < 0) sel[2] = c.d[0];
    return [
      REGION.map(function (x) { return x.n; }),
      p.c.map(function (x) { return x.n; }),
      c.d.slice()
    ];
  }

  function paintWheel(sheet) {
    var kind = sheet._kind;
    var cols = kind === "region" ? regionCols(sheet._sel) : dateCols(sheet._sel);
    sheet._labels = sheet._sel.slice();
    sheet.querySelectorAll(".md-wheel__col").forEach(function (col, i) {
      fillCol(col, cols[i], sheet._sel[i]);
      var on = col.querySelector(".is-active");
      if (on) on.scrollIntoView({ block: "center" });
    });
  }

  function openWheel(trigger) {
    ensureWheel();
    var sheet = document.getElementById("mdWheelSheet");
    var kind = trigger.getAttribute("data-wheel");
    var tabs = sheet.querySelector(".md-wheel__tabs");
    sheet._kind = kind;
    sheet._trigger = trigger;
    if (kind === "daterange") {
      document.getElementById("mdWheelTitle").textContent = "选择日期段";
      var start = trigger.getAttribute("data-start") || "";
      var end = trigger.getAttribute("data-end") || "";
      if (!start && trigger.getAttribute("data-value")) {
        var pair = trigger.getAttribute("data-value").split("~");
        start = pair[0] || "";
        end = pair[1] || "";
      }
      sheet._start = parseDateParts(start, ["2026", "8", "1"]);
      sheet._end = parseDateParts(end || start, ["2026", "8", "14"]);
      sheet._rangeTab = "start";
      sheet._sel = sheet._start;
      tabs.hidden = false;
      sheet.querySelectorAll("[data-range-tab]").forEach(function (t) {
        t.classList.toggle("is-active", t.getAttribute("data-range-tab") === "start");
      });
    } else {
      tabs.hidden = true;
      var cur = (trigger.getAttribute("data-value") || "").split("-");
      if (kind === "region") {
        document.getElementById("mdWheelTitle").textContent = "选择地区";
        sheet._sel = [cur[0] || "浙江省", cur[1] || "杭州市", cur[2] || "西湖区"];
      } else {
        document.getElementById("mdWheelTitle").textContent = "选择日期";
        sheet._sel = [cur[0] || "2026", cur[1] || "8", cur[2] || "14"];
      }
    }
    paintWheel(sheet);
    openDrawer("mdWheelSheet");
  }

  function bindWheels() {
    document.querySelectorAll("[data-wheel]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        openWheel(btn);
      });
    });
  }

  function bindSliders() {
    document.querySelectorAll(".md-slider input[type=range]").forEach(function (el) {
      var box = el.closest(".md-slider");
      var out = box.querySelector(".md-slider__value");
      var labels = box.getAttribute("data-labels");
      var suffix = el.getAttribute("data-suffix") || "";
      function paint() {
        if (!out) return;
        if (labels) {
          var arr = labels.split(",");
          var i = Number(el.value) - Number(el.min || 1);
          out.textContent = arr[i] || el.value;
        } else {
          out.textContent = el.value + suffix;
        }
      }
      el.addEventListener("input", paint);
      paint();
    });
  }

  function phClass(n) {
    return "md-media-ph md-media-ph--" + ((n % 6) + 1);
  }

  function bindUploads() {
    document.querySelectorAll('[data-upload="single"]').forEach(function (box) {
      var input = box.querySelector('input[type="file"]');
      var empty = box.querySelector(".md-upload__empty");
      var filled = box.querySelector(".md-upload__filled");
      var preview = box.querySelector(".md-upload__preview");
      var replace = box.querySelector(".md-upload__replace");
      function pick() {
        if (input) input.click();
      }
      if (empty) empty.addEventListener("click", pick);
      if (replace) replace.addEventListener("click", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        pick();
      });
      if (input) {
        input.addEventListener("change", function () {
          var file = input.files && input.files[0];
          box.classList.add("is-filled");
          if (empty) empty.classList.add("is-hidden");
          if (filled) filled.classList.remove("is-hidden");
          if (!file || !preview) return;
          if (file.type.indexOf("image/") === 0) {
            var url = URL.createObjectURL(file);
            preview.style.backgroundImage = "url(" + url + ")";
            preview.className = "md-upload__preview";
          } else {
            preview.style.backgroundImage = "";
            preview.className = "md-upload__preview " + phClass(2);
          }
          markPreviewables();
        });
      }
    });
    document.querySelectorAll('[data-upload="multi"]').forEach(function (grid) {
      var add = grid.querySelector(".md-upload-grid__add");
      var input = add && add.querySelector('input[type="file"]');
      var n = grid.querySelectorAll(".md-upload-grid__item").length;
      function bindDel(item) {
        var del = item.querySelector(".md-upload-grid__del");
        if (del) {
          del.addEventListener("click", function () {
            item.parentNode.removeChild(item);
          });
        }
      }
      grid.querySelectorAll(".md-upload-grid__item").forEach(bindDel);
      if (input) {
        input.addEventListener("change", function () {
          var file = input.files && input.files[0];
          var item = document.createElement("div");
          item.className = "md-upload-grid__item";
          var thumb = document.createElement("div");
          n += 1;
          if (file && file.type.indexOf("image/") === 0) {
            thumb.className = "md-upload-grid__thumb";
            thumb.style.backgroundImage = "url(" + URL.createObjectURL(file) + ")";
          } else {
            thumb.className = "md-upload-grid__thumb " + phClass(n);
          }
          var del = document.createElement("button");
          del.type = "button";
          del.className = "md-icon-btn md-upload-grid__del";
          del.setAttribute("aria-label", "删除");
          del.innerHTML = '<span class="md-icon" data-icon="close" aria-hidden="true"></span>';
          item.appendChild(thumb);
          item.appendChild(del);
          grid.insertBefore(item, add);
          bindDel(item);
          if (global.ProtoIcons && global.ProtoIcons.mount) global.ProtoIcons.mount(item);
          markPreviewables();
          input.value = "";
        });
      }
    });
    document.querySelectorAll(".md-upload--file input[type=file]").forEach(function (input) {
      input.addEventListener("change", function () {
        var name = input.files && input.files[0] ? input.files[0].name : "";
        var slot = input.closest(".md-upload").querySelector(".md-upload__name");
        if (slot) slot.textContent = name;
      });
    });
  }

  var SELECT_CENTER_MAX = 6;

  function closeSelectSheet() {
    var sheet = document.getElementById("mdSelectSheet");
    var mask = document.getElementById("mdSelectSheetBackdrop");
    if (sheet) {
      sheet.classList.remove("is-open");
      sheet.setAttribute("aria-hidden", "true");
    }
    if (mask) mask.classList.remove("is-open");
    syncDialogLock();
  }

  function selectSheetTitle(sel) {
    var field = sel.closest(".md-field");
    var label = field && field.querySelector(".md-field__label");
    if (label && label.textContent) return label.textContent.replace(/\s+/g, " ").trim();
    return sel.getAttribute("aria-label") || "请选择";
  }

  function selectSheetMode(sel) {
    var forced = sel.getAttribute("data-sheet");
    if (forced === "center" || forced === "bottom") return forced;
    return sel.querySelectorAll("option:not([disabled])").length <= SELECT_CENTER_MAX
      ? "center"
      : "bottom";
  }

  function ensureSelectSheet() {
    if (document.getElementById("mdSelectSheet")) return;
    var mask = document.createElement("div");
    mask.id = "mdSelectSheetBackdrop";
    mask.className = "md-backdrop md-select-sheet-backdrop";
    var sheet = document.createElement("div");
    sheet.id = "mdSelectSheet";
    sheet.className = "md-select-sheet";
    sheet.setAttribute("role", "dialog");
    sheet.setAttribute("aria-hidden", "true");
    sheet.innerHTML =
      '<div class="md-select-sheet__handle" aria-hidden="true"></div>' +
      '<h2 class="md-select-sheet__title" id="mdSelectSheetTitle">请选择</h2>' +
      '<div class="md-select-sheet__list" role="listbox"></div>' +
      '<button type="button" class="md-btn md-btn--text md-select-sheet__cancel">取消</button>';
    document.body.appendChild(mask);
    document.body.appendChild(sheet);
    mask.addEventListener("click", closeSelectSheet);
    sheet.querySelector(".md-select-sheet__cancel").addEventListener("click", closeSelectSheet);
    sheet.querySelector(".md-select-sheet__list").addEventListener("click", function (ev) {
      var opt = ev.target.closest("[data-opt]");
      if (!opt || opt.disabled) return;
      var sel = sheet._select;
      if (!sel) return;
      sel.value = opt.getAttribute("data-opt");
      sel.dispatchEvent(new Event("change", { bubbles: true }));
      closeSelectSheet();
    });
  }

  function openSelectSheet(sel) {
    ensureSelectSheet();
    var sheet = document.getElementById("mdSelectSheet");
    var mask = document.getElementById("mdSelectSheetBackdrop");
    var list = sheet.querySelector(".md-select-sheet__list");
    var mode = selectSheetMode(sel);
    sheet._select = sel;
    sheet.className = "md-select-sheet md-select-sheet--" + mode;
    sheet.setAttribute("aria-labelledby", "mdSelectSheetTitle");
    document.getElementById("mdSelectSheetTitle").textContent = selectSheetTitle(sel);
    list.innerHTML = "";
    Array.prototype.forEach.call(sel.options, function (opt) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "md-select-sheet__opt";
      btn.setAttribute("data-opt", opt.value);
      btn.setAttribute("role", "option");
      btn.textContent = opt.text;
      if (opt.disabled) {
        btn.disabled = true;
        btn.classList.add("is-disabled");
      }
      if (opt.selected) {
        btn.classList.add("is-active");
        btn.setAttribute("aria-selected", "true");
      }
      list.appendChild(btn);
    });
    mask.classList.add("is-open");
    sheet.classList.add("is-open");
    sheet.setAttribute("aria-hidden", "false");
    syncDialogLock();
    var on = list.querySelector(".is-active");
    if (on) on.scrollIntoView({ block: "nearest" });
  }

  function bindMobileSelects() {
    if (!isMobilePage()) return;
    document.querySelectorAll("select.md-select").forEach(function (sel) {
      if (sel.getAttribute("data-native") === "1") return;
      if (sel.getAttribute("data-md-bound") === "1") return;
      sel.setAttribute("data-md-bound", "1");
      sel.setAttribute("tabindex", "-1");
      var field = sel.closest(".md-field") || sel.parentElement;
      var trigger = field.querySelector(".md-select-trigger");
      if (!trigger) {
        trigger = document.createElement("button");
        trigger.type = "button";
        trigger.className = "md-select md-select-trigger";
        trigger.setAttribute("aria-haspopup", "listbox");
        sel.insertAdjacentElement("afterend", trigger);
      }
      function paint() {
        var opt = sel.options[sel.selectedIndex];
        trigger.textContent = opt ? opt.text : "请选择";
      }
      paint();
      sel.addEventListener("change", paint);
      sel.addEventListener("mousedown", function (ev) {
        ev.preventDefault();
      });
      sel.addEventListener("focus", function () {
        sel.blur();
        openSelectSheet(sel);
      });
      trigger.addEventListener("click", function () {
        openSelectSheet(sel);
      });
    });
  }

  function bindTimelines() {
    document.querySelectorAll(".md-timeline").forEach(function (tl) {
      if (tl.getAttribute("data-md-bound") === "1") return;
      tl.setAttribute("data-md-bound", "1");
      tl.addEventListener("click", function (ev) {
        var item = ev.target.closest(".md-timeline__item");
        if (!item || !tl.contains(item)) return;
        tl.querySelectorAll(".md-timeline__item.is-active").forEach(function (n) {
          n.classList.remove("is-active");
        });
        item.classList.add("is-active");
        tl.dispatchEvent(
          new CustomEvent("md-timeline-select", {
            bubbles: true,
            detail: { item: item },
          })
        );
      });
    });
  }

  function bindTrees() {
    document.querySelectorAll(".md-tree").forEach(function (tree) {
      if (tree.getAttribute("data-md-bound") === "1") return;
      tree.setAttribute("data-md-bound", "1");
      tree.addEventListener("click", function (ev) {
        var toggle = ev.target.closest(".md-tree__toggle");
        var item = ev.target.closest(".md-tree__item");
        if (toggle && tree.contains(toggle)) {
          ev.preventDefault();
          ev.stopPropagation();
          var branch = toggle.closest("li");
          if (branch && branch.querySelector(":scope > ul")) {
            branch.classList.toggle("is-open");
          }
          return;
        }
        if (!item || !tree.contains(item)) return;
        tree.querySelectorAll(".md-tree__item.is-active").forEach(function (n) {
          n.classList.remove("is-active");
        });
        item.classList.add("is-active");
        var li = item.closest("li");
        if (li && li.querySelector(":scope > ul")) li.classList.add("is-open");
        var cat = item.getAttribute("data-cat") || "";
        var title = document.getElementById("catTitle");
        if (title && cat) title.textContent = cat;
        tree.dispatchEvent(
          new CustomEvent("md-tree-select", {
            bubbles: true,
            detail: { item: item, cat: cat },
          })
        );
      });
    });
  }

  function previewSkip(el) {
    if (!el || !el.closest) return true;
    if (el.closest(".md-lightbox")) return true;
    if (el.getAttribute("data-preview") === "off") return true;
    if (el.closest("[data-preview=off]")) return true;
    if (
      el.closest(
        ".md-appbar__cover, .md-card__leading, .md-empty__art, .md-chart-ph, .md-upload-grid__add, .md-upload-grid__del, .md-upload-grid__thumb, .md-upload__preview"
      )
    ) {
      return true;
    }
    if (el.closest(".is-hidden")) return true;
    return false;
  }

  function isMediaLike(el) {
    if (el.tagName === "IMG" && !el.closest(".md-icon, svg")) return true;
    var cls = el.className && String(el.className);
    return !!(cls && /\bmd-media-ph--[1-6]\b/.test(cls));
  }

  function isPreviewable(el) {
    if (!el || previewSkip(el) || !isMediaLike(el)) return false;
    if (el.getAttribute("data-preview") === "on" || el.closest("[data-preview=on]")) {
      return true;
    }
    if (el.closest(".md-card--row")) return true;
    if (el.closest("[data-lightbox]")) return true;
    return false;
  }

  var lightboxRoot = null;

  function previewGroupRoot(el) {
    if (!el) return lightboxRoot || document;
    var row = el.closest(".md-card--row");
    if (row) return row;
    var page = el.closest("[data-lightbox]");
    if (page) return page;
    return document;
  }

  function collectPreviewables(root) {
    root = root || lightboxRoot || document;
    var nodes = root.querySelectorAll('[class*="md-media-ph--"], img');
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (!isPreviewable(el)) continue;
      var nested = false;
      for (var j = 0; j < out.length; j++) {
        if (out[j].contains(el)) {
          nested = true;
          break;
        }
      }
      if (nested) continue;
      out.push(el);
    }
    return out;
  }

  function markPreviewables() {
    collectPreviewables(document).forEach(function (el) {
      el.classList.add("md-previewable");
    });
  }

  function mediaUrl(el) {
    if (!el) return "";
    if (el.tagName === "IMG") return el.currentSrc || el.src || "";
    var bg = (el.style && el.style.backgroundImage) || "";
    var m = bg.match(/url\(["']?([^"')]+)["']?\)/);
    return m ? m[1] : "";
  }

  function ensureLightbox() {
    var box = document.getElementById("mdLightbox");
    if (box) return box;
    box = document.createElement("div");
    box.id = "mdLightbox";
    box.className = "md-lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-hidden", "true");
    box.setAttribute("aria-label", "图片预览");
    box.innerHTML =
      '<div class="md-lightbox__mask" data-lightbox-close="1"></div>' +
      '<div class="md-lightbox__stage">' +
      '<div class="md-lightbox__frame"></div>' +
      "</div>" +
      '<button type="button" class="md-lightbox__close" aria-label="关闭">' +
      '<span class="md-icon" data-icon="close" aria-hidden="true"></span>' +
      "</button>" +
      '<button type="button" class="md-lightbox__nav md-lightbox__prev" aria-label="上一张">' +
      '<span class="md-icon" data-icon="chevron-left" aria-hidden="true"></span>' +
      "</button>" +
      '<button type="button" class="md-lightbox__nav md-lightbox__next" aria-label="下一张">' +
      '<span class="md-icon" data-icon="chevron-right" aria-hidden="true"></span>' +
      "</button>" +
      '<p class="md-lightbox__count"></p>';
    document.body.appendChild(box);
    if (global.ProtoIcons && global.ProtoIcons.mount) global.ProtoIcons.mount(box);
    return box;
  }

  var lightboxIndex = 0;
  var lightboxTouch = null;

  function renderLightboxFrame(el) {
    var frame = document.querySelector("#mdLightbox .md-lightbox__frame");
    if (!frame) return;
    frame.innerHTML = "";
    var src = mediaUrl(el);
    if (src) {
      var img = document.createElement("img");
      img.src = src;
      img.alt = (el.getAttribute && el.getAttribute("alt")) || "";
      frame.appendChild(img);
      return;
    }
    var ph = document.createElement("div");
    ph.className = "md-lightbox__ph md-media-ph";
    var cls = el && el.className ? String(el.className) : "";
    var m = cls.match(/\bmd-media-ph--[1-6]\b/);
    ph.classList.add(m ? m[0] : "md-media-ph--1");
    frame.appendChild(ph);
  }

  function paintLightbox() {
    var box = ensureLightbox();
    var items = collectPreviewables();
    if (!items.length) {
      closeLightbox();
      return;
    }
    if (lightboxIndex < 0) lightboxIndex = 0;
    if (lightboxIndex > items.length - 1) lightboxIndex = items.length - 1;
    renderLightboxFrame(items[lightboxIndex]);
    var count = box.querySelector(".md-lightbox__count");
    if (count) count.textContent = lightboxIndex + 1 + " / " + items.length;
    var prev = box.querySelector(".md-lightbox__prev");
    var next = box.querySelector(".md-lightbox__next");
    if (prev) prev.disabled = lightboxIndex <= 0;
    if (next) next.disabled = lightboxIndex >= items.length - 1;
  }

  function openLightbox(el) {
    lightboxRoot = previewGroupRoot(el);
    markPreviewables();
    var items = collectPreviewables();
    var idx = -1;
    for (var i = 0; i < items.length; i++) {
      if (items[i] === el) {
        idx = i;
        break;
      }
    }
    if (idx < 0) return;
    lightboxIndex = idx;
    var box = ensureLightbox();
    box.classList.add("is-open");
    box.setAttribute("aria-hidden", "false");
    paintLightbox();
    syncDialogLock();
    var closeBtn = box.querySelector(".md-lightbox__close");
    if (closeBtn && closeBtn.focus) closeBtn.focus();
  }

  function closeLightbox() {
    var box = document.getElementById("mdLightbox");
    if (!box) return;
    box.classList.remove("is-open");
    box.setAttribute("aria-hidden", "true");
    syncDialogLock();
  }

  function stepLightbox(delta) {
    var items = collectPreviewables();
    var next = lightboxIndex + delta;
    if (next < 0 || next >= items.length) return;
    lightboxIndex = next;
    paintLightbox();
  }

  function previewHostFromEvent(ev) {
    var t = ev.target;
    if (!t || !t.closest) return null;
    if (t.closest(".md-lightbox")) return null;
    if (
      t.closest(
        "button, input, textarea, select, label.md-upload-grid__add, .md-upload-grid__del, .md-icon-btn, a.md-btn"
      )
    ) {
      return null;
    }
    var el = t.closest(
      '[class*="md-media-ph--"], .md-upload-grid__thumb, .md-upload__preview, img'
    );
    if (!el || !isPreviewable(el)) return null;
    return el;
  }

  // Default: detail pages ([data-lightbox]) and md-card--row images only.
  function bindLightbox() {
    if (document.documentElement.getAttribute("data-md-lightbox") === "1") {
      markPreviewables();
      return;
    }
    document.documentElement.setAttribute("data-md-lightbox", "1");
    ensureLightbox();
    markPreviewables();
    document.addEventListener(
      "click",
      function (ev) {
        var el = previewHostFromEvent(ev);
        if (!el) return;
        ev.preventDefault();
        ev.stopPropagation();
        openLightbox(el);
      },
      true
    );
    document.addEventListener("click", function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var box = t.closest("#mdLightbox");
      if (!box || !box.classList.contains("is-open")) return;
      if (t.closest("[data-lightbox-close], .md-lightbox__close")) {
        closeLightbox();
        return;
      }
      if (t.closest(".md-lightbox__prev")) {
        stepLightbox(-1);
        return;
      }
      if (t.closest(".md-lightbox__next")) {
        stepLightbox(1);
        return;
      }
      if (t.classList && t.classList.contains("md-lightbox__stage")) {
        closeLightbox();
      }
    });
    document.addEventListener("keydown", function (ev) {
      var box = document.getElementById("mdLightbox");
      if (!box || !box.classList.contains("is-open")) return;
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeLightbox();
      } else if (ev.key === "ArrowLeft") {
        ev.preventDefault();
        stepLightbox(-1);
      } else if (ev.key === "ArrowRight") {
        ev.preventDefault();
        stepLightbox(1);
      }
    });
    var stage = document.querySelector("#mdLightbox .md-lightbox__stage");
    if (stage) {
      stage.addEventListener(
        "touchstart",
        function (ev) {
          var t = ev.changedTouches && ev.changedTouches[0];
          if (!t) return;
          lightboxTouch = { x: t.clientX, y: t.clientY };
        },
        { passive: true }
      );
      stage.addEventListener("touchend", function (ev) {
        if (!lightboxTouch) return;
        var t = ev.changedTouches && ev.changedTouches[0];
        var dx = t ? t.clientX - lightboxTouch.x : 0;
        var dy = t ? t.clientY - lightboxTouch.y : 0;
        lightboxTouch = null;
        if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy)) return;
        stepLightbox(dx > 0 ? -1 : 1);
      });
    }
  }

  function hoistPods() {
    var page = document.querySelector(".md-mobile-page") || document.querySelector(".md-d1");
    if (!page) return;
    page.querySelectorAll(".md-pod:not(.md-pod--static)").forEach(function (pod) {
      if (pod.parentNode !== page) page.appendChild(pod);
    });
  }

  function paintIcon(host) {
    if (global.ProtoIcons && typeof global.ProtoIcons.mount === "function") {
      global.ProtoIcons.mount(host);
    }
  }

  function bindDeskPods() {
    var pods = document.querySelectorAll(".md-d1 .md-pod, .md-pod--desk");
    pods.forEach(function (pod) {
      pod.classList.add("md-pod--desk", "md-pod--br");
      pod.classList.remove("md-pod--tl", "md-pod--bl");
      var items = pod.querySelectorAll(".md-pod__item:not(.md-pod__toggle)");
      var foldAt = Number(pod.getAttribute("data-fold"));
      if (!foldAt && foldAt !== 0) foldAt = 4;
      if (foldAt <= 0 || items.length < foldAt) return;
      pod.classList.add("md-pod--fold");
      pod.style.setProperty("--pod-n", String(items.length));
      items.forEach(function (item, i) {
        item.style.setProperty("--pod-i", String(items.length - i));
      });
      var toggle = pod.querySelector(".md-pod__toggle");
      if (!toggle) {
        toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "md-pod__item md-pod__toggle";
        toggle.setAttribute("aria-label", "展开快捷操作");
        toggle.setAttribute("aria-expanded", "false");
        toggle.innerHTML = '<span class="md-icon" data-icon="add" aria-hidden="true"></span>';
        pod.appendChild(toggle);
        paintIcon(toggle);
      }
      if (toggle.getAttribute("data-bound") === "1") return;
      if (toggle.getAttribute("onclick")) {
        toggle.setAttribute("data-bound", "1");
        return;
      }
      toggle.setAttribute("data-bound", "1");
      toggle.addEventListener("click", function () {
        var open = pod.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        toggle.setAttribute("aria-label", open ? "收起快捷操作" : "展开快捷操作");
      });
    });
  }

  function bindDeskWizards() {
    var host = document.querySelector(".md-d1");
    if (!host || host.getAttribute("data-wizard") === "off") return;
    var stepper = host.querySelector(".md-stepper");
    if (!stepper || stepper.getAttribute("data-wizard") === "off") return;
    if (stepper.getAttribute("data-bound") === "1") return;
    var steps = stepper.querySelectorAll(".md-step");
    if (!steps.length) return;
    var form = host.querySelector(".md-d1__form") || host.querySelector("form");
    if (!form) return;
    var panels = Array.prototype.filter.call(form.children, function (el) {
      return el.hasAttribute("data-step");
    });
    if (!panels.length) return;
    stepper.setAttribute("data-bound", "1");
    var btnPrev = host.querySelector("#btnPrev, [data-wizard-prev]");
    var btnNext = host.querySelector("#btnNext, [data-wizard-next]");
    var advance = host.querySelector(".md-advance");
    var progress = host.querySelector(".md-progress");
    var total = steps.length;
    var step = 0;

    function paint() {
      panels.forEach(function (el) {
        el.hidden = Number(el.getAttribute("data-step")) !== step;
      });
      steps.forEach(function (el, i) {
        el.classList.toggle("is-active", i === step);
        el.classList.toggle("is-done", i < step);
      });
      if (btnPrev) btnPrev.disabled = step === 0;
      if (btnNext) btnNext.textContent = step === total - 1 ? "提交" : "下一步";
      var pct = ((step + 1) / total) * 100;
      var label = (step + 1) + " / " + total;
      if (advance) setAdvance(advance, pct, label);
      if (progress) setProgress(progress, pct);
    }

    function go(i) {
      if (i < 0 || i >= total) return;
      step = i;
      paint();
    }

    steps.forEach(function (el, i) {
      el.setAttribute("role", "button");
      el.setAttribute("tabindex", "0");
      el.addEventListener("click", function () {
        go(i);
      });
      el.addEventListener("keydown", function (e) {
        if (e.key !== "Enter" && e.key !== " ") return;
        e.preventDefault();
        go(i);
      });
    });
    if (btnPrev) {
      btnPrev.addEventListener("click", function () {
        go(step - 1);
      });
    }
    if (btnNext) {
      btnNext.addEventListener("click", function () {
        if (step < total - 1) {
          go(step + 1);
          return;
        }
        snackbar("已提交");
      });
    }
    paint();
  }

  function bindUi() {
    ensureStatusBar();
    hoistPods();
    bindDeskPods();
    bindDeskWizards();
    bindTabs();
    bindMenus();
    bindCals();
    bindSwipers();
    bindWheels();
    bindSliders();
    bindTrees();
    bindTimelines();
    bindUploads();
    bindMobileSelects();
    bindProgress();
    bindLightbox();
  }

  global.ProtoPage = {
    applyCompState: applyCompState,
    snackbar: snackbar,
    setProgress: setProgress,
    setAdvance: setAdvance,
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
