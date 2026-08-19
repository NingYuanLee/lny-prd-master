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

  function ensureBottomDrawerClose(el) {
    if (!el || !el.classList.contains("md-drawer--bottom")) return;
    if (el.classList.contains("md-wheel")) return;
    if (el.querySelector(":scope > .md-drawer__close")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "md-drawer__close";
    btn.setAttribute("aria-label", "关闭");
    btn.innerHTML = '<span class="md-icon" data-icon="close" aria-hidden="true"></span>';
    btn.addEventListener("click", function () {
      if (el.id) closeDrawer(el.id);
    });
    el.insertBefore(btn, el.firstChild);
    if (global.ProtoIcons && global.ProtoIcons.mount) global.ProtoIcons.mount(btn);
  }

  function openDrawer(id) {
    var el = document.getElementById(id);
    var mask = document.getElementById(id + "Backdrop");
    if (mask) mask.classList.add("is-open");
    if (el) {
      ensureBottomDrawerClose(el);
      el.classList.add("is-open");
    }
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
    var cancelBtn = document.getElementById("mdConfirmCancel");
    cancelBtn.hidden = false;
    document.getElementById("mdConfirmTitle").textContent = opts.title || "确认";
    document.getElementById("mdConfirmBody").textContent = opts.body || "";
    var okBtn = document.getElementById("mdConfirmOk");
    okBtn.textContent = opts.ok || "确定";
    cancelBtn.textContent = opts.cancel || "取消";
    okBtn.onclick = function () {
      closeDialog("mdConfirmDlg");
      if (typeof opts.onOk === "function") opts.onOk();
    };
    openDialog("mdConfirmDlg");
  }

  function alertInfo(opts) {
    opts = opts || {};
    ensureConfirm();
    var cancelBtn = document.getElementById("mdConfirmCancel");
    document.getElementById("mdConfirmTitle").textContent = opts.title || "说明";
    document.getElementById("mdConfirmBody").textContent = opts.body || "";
    var okBtn = document.getElementById("mdConfirmOk");
    okBtn.textContent = opts.ok || "知道了";
    cancelBtn.hidden = true;
    okBtn.onclick = function () {
      closeDialog("mdConfirmDlg");
      cancelBtn.hidden = false;
      if (typeof opts.onOk === "function") opts.onOk();
    };
    openDialog("mdConfirmDlg");
  }

  function closeCombos(except) {
    document.querySelectorAll(".md-combo.is-open").forEach(function (el) {
      if (el !== except) {
        el.classList.remove("is-open");
        var trig = el.querySelector(".md-combo__trigger");
        if (trig) trig.setAttribute("aria-expanded", "false");
      }
    });
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
    if (!except || !except.closest || !except.closest(".md-combo")) closeCombos();
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
        Array.prototype.forEach.call(root.children, function (p) {
          if (!p.classList || !p.classList.contains("md-tab-panel")) return;
          p.classList.toggle("is-active", p.id === panelId);
        });
        syncLocatorSpies();
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            syncLocatorSpies();
          });
        });
        scheduleActionColWidths();
      });
    });
  }

  function placeFixedMenu(btn, menu) {
    if (!menu.classList.contains("md-menu--fixed")) return;
    var host = btn.closest("tr") || btn.closest(".md-select-wrap") || btn.parentElement;
    if (host) host.classList.add("is-menu-host");
    var r = btn.getBoundingClientRect();
    var pad = 8;
    var maxW = window.innerWidth - pad * 2;
    menu.style.position = "fixed";
    menu.style.minWidth = "128px";
    menu.style.maxWidth = maxW + "px";
    menu.style.zIndex = "1300";
    menu.style.left = "0";
    menu.style.top = "0";
    menu.style.right = "auto";
    var mw = menu.offsetWidth;
    var mh = menu.offsetHeight;
    var left;
    var top = r.bottom + 4;
    if (r.left + r.width / 2 < window.innerWidth / 2) {
      left = r.left;
    } else {
      left = r.right - mw;
    }
    if (left + mw > window.innerWidth - pad) {
      left = window.innerWidth - pad - mw;
    }
    if (left < pad) {
      left = pad;
    }
    if (top + mh > window.innerHeight - pad) {
      top = r.top - 4 - mh;
    }
    if (top < pad) {
      top = pad;
    }
    menu.style.left = left + "px";
    menu.style.top = top + "px";
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
        !ev.target.closest(".md-field--daterange") &&
        !ev.target.closest(".md-combo")
      ) {
        closeMenus();
        closeCombos();
      }
    });
    document.addEventListener(
      "scroll",
      function (ev) {
        var t = ev.target;
        if (t && t.closest && t.closest(".md-combo__panel")) return;
        closeMenus();
        closeCombos();
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
      var isSteps = box.classList.contains("md-slider--steps");
      var slots = isSteps ? box.querySelectorAll(".md-slider__slot") : null;
      if (isSteps && slots && slots.length) {
        box.style.setProperty("--md-slider-steps", String(slots.length));
      }
      function paint() {
        if (isSteps && slots && slots.length) {
          var min = Number(el.min);
          if (isNaN(min)) min = 0;
          var idx = Number(el.value) - min;
          slots.forEach(function (slot, i) {
            slot.classList.toggle("is-active", i === idx);
          });
          return;
        }
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

  function ensureAvatarPickSheet() {
    if (document.getElementById("mdAvatarPickSheet")) return;
    var mask = document.createElement("div");
    mask.id = "mdAvatarPickSheetBackdrop";
    mask.className = "md-backdrop md-select-sheet-backdrop";
    var sheet = document.createElement("div");
    sheet.id = "mdAvatarPickSheet";
    sheet.className = "md-select-sheet md-select-sheet--bottom";
    sheet.setAttribute("role", "dialog");
    sheet.setAttribute("aria-hidden", "true");
    sheet.innerHTML =
      '<div class="md-select-sheet__handle" aria-hidden="true"></div>' +
      '<h2 class="md-select-sheet__title">更换头像</h2>' +
      '<div class="md-select-sheet__list" role="listbox">' +
      '<button type="button" class="md-select-sheet__opt" data-avatar-pick="wx">微信头像授权</button>' +
      '<button type="button" class="md-select-sheet__opt" data-avatar-pick="album">从相册选择</button>' +
      "</div>" +
      '<button type="button" class="md-btn md-btn--text md-select-sheet__cancel">取消</button>';
    document.body.appendChild(mask);
    document.body.appendChild(sheet);
    mask.addEventListener("click", closeAvatarPickSheet);
    sheet.querySelector(".md-select-sheet__cancel").addEventListener("click", closeAvatarPickSheet);
    sheet.querySelector(".md-select-sheet__list").addEventListener("click", function (ev) {
      var opt = ev.target.closest("[data-avatar-pick]");
      if (!opt) return;
      var cb = sheet._onPick;
      closeAvatarPickSheet();
      if (typeof cb === "function") cb(opt.getAttribute("data-avatar-pick"));
    });
  }

  function closeAvatarPickSheet() {
    var sheet = document.getElementById("mdAvatarPickSheet");
    var mask = document.getElementById("mdAvatarPickSheetBackdrop");
    if (sheet) {
      sheet.classList.remove("is-open");
      sheet.setAttribute("aria-hidden", "true");
      sheet._onPick = null;
    }
    if (mask) mask.classList.remove("is-open");
    syncDialogLock();
  }

  function openAvatarPickSheet(onPick) {
    ensureAvatarPickSheet();
    var sheet = document.getElementById("mdAvatarPickSheet");
    var mask = document.getElementById("mdAvatarPickSheetBackdrop");
    if (!sheet || !mask) return;
    sheet._onPick = onPick;
    mask.classList.add("is-open");
    sheet.classList.add("is-open");
    sheet.setAttribute("aria-hidden", "false");
    syncDialogLock();
  }

  function ensureNickPickSheet() {
    if (document.getElementById("mdNickPickSheet")) return;
    var mask = document.createElement("div");
    mask.id = "mdNickPickSheetBackdrop";
    mask.className = "md-backdrop md-select-sheet-backdrop";
    var sheet = document.createElement("div");
    sheet.id = "mdNickPickSheet";
    sheet.className = "md-select-sheet md-select-sheet--bottom";
    sheet.setAttribute("role", "dialog");
    sheet.setAttribute("aria-hidden", "true");
    sheet.innerHTML =
      '<div class="md-select-sheet__handle" aria-hidden="true"></div>' +
      '<h2 class="md-select-sheet__title">修改昵称</h2>' +
      '<div class="md-select-sheet__list" role="listbox">' +
      '<button type="button" class="md-select-sheet__opt" data-nick-pick="wx">微信昵称授权</button>' +
      "</div>" +
      '<div class="md-select-sheet__form">' +
      '<label class="md-field md-field--sm">' +
      '<span class="md-field__label">手动输入</span>' +
      '<input type="text" class="md-field__input" data-nick-input maxlength="32" placeholder="请输入昵称" autocomplete="nickname">' +
      "</label>" +
      '<button type="button" class="md-btn md-btn--contained" data-nick-save>保存</button>' +
      "</div>" +
      '<button type="button" class="md-btn md-btn--text md-select-sheet__cancel">取消</button>';
    document.body.appendChild(mask);
    document.body.appendChild(sheet);
    mask.addEventListener("click", closeNickPickSheet);
    sheet.querySelector(".md-select-sheet__cancel").addEventListener("click", closeNickPickSheet);
    sheet.querySelector("[data-nick-pick]").addEventListener("click", function () {
      var btn = sheet._nickBtn;
      closeNickPickSheet();
      if (!btn) return;
      btn.textContent = "微信昵称";
      snackbar("已授权微信昵称");
    });
    sheet.querySelector("[data-nick-save]").addEventListener("click", function () {
      applyNickPickManual();
    });
    sheet.querySelector("[data-nick-input]").addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") {
        ev.preventDefault();
        applyNickPickManual();
      }
    });
  }

  function closeNickPickSheet() {
    var sheet = document.getElementById("mdNickPickSheet");
    var mask = document.getElementById("mdNickPickSheetBackdrop");
    if (sheet) {
      sheet.classList.remove("is-open");
      sheet.setAttribute("aria-hidden", "true");
      sheet._nickBtn = null;
    }
    if (mask) mask.classList.remove("is-open");
    syncDialogLock();
  }

  function applyNickPickManual() {
    var sheet = document.getElementById("mdNickPickSheet");
    if (!sheet || !sheet._nickBtn) return;
    var input = sheet.querySelector("[data-nick-input]");
    var nickBtn = sheet._nickBtn;
    var current = nickBtn.textContent.replace(/\s+/g, " ").trim();
    var val = input ? input.value.replace(/\s+/g, " ").trim() : "";
    if (!val) val = current;
    closeNickPickSheet();
    nickBtn.textContent = val;
    if (val !== current) snackbar("昵称已保存");
  }

  function openNickPickSheet(nickBtn) {
    ensureNickPickSheet();
    var sheet = document.getElementById("mdNickPickSheet");
    var mask = document.getElementById("mdNickPickSheetBackdrop");
    var input = sheet && sheet.querySelector("[data-nick-input]");
    if (!sheet || !mask || !nickBtn) return;
    sheet._nickBtn = nickBtn;
    if (input) {
      input.value = nickBtn.textContent.replace(/\s+/g, " ").trim();
    }
    mask.classList.add("is-open");
    sheet.classList.add("is-open");
    sheet.setAttribute("aria-hidden", "false");
    syncDialogLock();
    if (input) {
      window.setTimeout(function () {
        input.focus();
        input.select();
      }, 320);
    }
  }

  function bindProfileNameEdit(nickBtn) {
    if (!nickBtn || nickBtn.getAttribute("data-name-bound") === "1") return;
    nickBtn.setAttribute("data-name-bound", "1");
    nickBtn.addEventListener("click", function () {
      if (nickBtn.tagName !== "BUTTON") return;
      openNickPickSheet(nickBtn);
    });
  }

  function bindMeProfiles() {
    document.querySelectorAll(".md-profile--me").forEach(function (root) {
      if (root.getAttribute("data-md-bound") === "1") return;
      root.setAttribute("data-md-bound", "1");
      var avatar = root.querySelector("[data-profile-avatar]");
      var fileInput = root.querySelector('input[type="file"][data-profile-avatar-file]');
      root.querySelectorAll("[data-copy]").forEach(function (btn) {
        btn.addEventListener("click", function (ev) {
          ev.preventDefault();
          ev.stopPropagation();
          var text = btn.getAttribute("data-copy") || "";
          copyPlainText(text).then(
            function () {
              snackbar("已复制");
            },
            function () {
              snackbar("复制失败", { severity: "error" });
            }
          );
        });
      });
      if (avatar) {
        avatar.addEventListener("click", function () {
          openAvatarPickSheet(function (pick) {
            if (pick === "wx") snackbar("已授权微信头像");
            else if (pick === "album" && fileInput) fileInput.click();
          });
        });
      }
      if (fileInput && avatar) {
        fileInput.addEventListener("change", function () {
          var file = fileInput.files && fileInput.files[0];
          if (file && file.type.indexOf("image/") === 0) {
            avatar.style.backgroundImage = "url(" + URL.createObjectURL(file) + ")";
            snackbar("头像已更新");
          }
          fileInput.value = "";
        });
      }
      bindProfileNameEdit(root.querySelector(".md-profile__name"));
    });
  }

  function bindSvcStrips() {
    document.querySelectorAll(".md-svc-strip__help[data-svc-help]").forEach(function (btn) {
      if (btn.getAttribute("data-md-bound") === "1") return;
      btn.setAttribute("data-md-bound", "1");
      btn.addEventListener("click", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        alertInfo({
          title: btn.getAttribute("data-svc-help-title") || "说明",
          body: btn.getAttribute("data-svc-help") || "",
        });
      });
    });
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
          preview.removeAttribute("data-preview-kind");
          preview.removeAttribute("data-preview-src");
          if (file.type.indexOf("image/") === 0) {
            var url = URL.createObjectURL(file);
            preview.style.backgroundImage = "url(" + url + ")";
            preview.className = "md-upload__preview";
            preview.setAttribute("data-preview-src", url);
          } else if (file.type.indexOf("video/") === 0) {
            var vurl = URL.createObjectURL(file);
            preview.style.backgroundImage = "";
            preview.className = "md-upload__preview " + phClass(3);
            preview.setAttribute("data-preview-kind", "video");
            preview.setAttribute("data-preview-src", vurl);
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
            var iurl = URL.createObjectURL(file);
            thumb.style.backgroundImage = "url(" + iurl + ")";
            thumb.setAttribute("data-preview-src", iurl);
          } else if (file && file.type.indexOf("video/") === 0) {
            thumb.className = "md-upload-grid__thumb " + phClass(n);
            var mvurl = URL.createObjectURL(file);
            thumb.setAttribute("data-preview-kind", "video");
            thumb.setAttribute("data-preview-src", mvurl);
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
    function uploadProgressEl(upload) {
      if (!upload) return null;
      var next = upload.nextElementSibling;
      if (next && next.classList.contains("md-progress")) return next;
      var nested = upload.querySelector(".md-progress");
      if (nested) return nested;
      var box = document.createElement("div");
      box.className = "md-progress is-hidden md-upload__progress";
      box.setAttribute("role", "progressbar");
      box.setAttribute("aria-valuemin", "0");
      box.setAttribute("aria-valuemax", "100");
      box.setAttribute("aria-valuenow", "0");
      box.innerHTML =
        '<div class="md-progress__head">' +
        '<span class="md-progress__label">文件上传进度</span>' +
        '<span class="md-progress__value">0%</span>' +
        "</div>" +
        '<div class="md-progress__track"><div class="md-progress__bar"></div></div>';
      upload.insertAdjacentElement("afterend", box);
      return box;
    }

    function simulateFileUploadProgress(progressEl) {
      if (!progressEl) return;
      progressEl.classList.remove("is-hidden");
      var p = 0;
      setProgress(progressEl, 0);
      var t = setInterval(function () {
        p += 25;
        setProgress(progressEl, Math.min(p, 100));
        if (p >= 100) clearInterval(t);
      }, 120);
    }

    document.querySelectorAll(".md-upload--file input[type=file]").forEach(function (input) {
      input.addEventListener("change", function () {
        var upload = input.closest(".md-upload");
        var name = input.files && input.files[0] ? input.files[0].name : "";
        var slot = upload && upload.querySelector(".md-upload__name");
        if (slot) slot.textContent = name;
        simulateFileUploadProgress(uploadProgressEl(upload));
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
      if (tl.classList.contains("md-timeline--static") || tl.getAttribute("data-timeline") === "static") {
        return;
      }
      tl.setAttribute("data-md-bound", "1");
      tl.addEventListener("click", function (ev) {
        var item = ev.target.closest(".md-timeline__item");
        if (!item || !tl.contains(item)) return;
        tl.querySelectorAll(".md-timeline__item.is-active").forEach(function (n) {
          n.classList.remove("is-active");
        });
        item.classList.add("is-active");
        var target =
          item.getAttribute("data-target") ||
          item.getAttribute("data-section") ||
          "";
        var host = tl.closest(".md-tab-panel") || tl.closest(".md-d1") || document;
        if (target) scrollToSectionTarget(host, target);
        tl.dispatchEvent(
          new CustomEvent("md-timeline-select", {
            bubbles: true,
            detail: { item: item, target: target },
          })
        );
      });
    });
  }

  function scrollToSectionTarget(root, sectionId) {
    if (!sectionId) return;
    var scope = root || document;
    var el =
      scope.querySelector('[data-section="' + sectionId + '"]') ||
      document.getElementById(sectionId) ||
      document.querySelector('[data-section="' + sectionId + '"]');
    if (!el) return;
    var scrollRoot =
      el.closest(".md-doc-scroll") ||
      el.closest(".md-article") ||
      el.closest(".md-split__main") ||
      el.closest(".md-layout__pane") ||
      el.closest(".md-d1") ||
      document.scrollingElement ||
      document.documentElement;
    if (scrollRoot === document.scrollingElement || scrollRoot === document.documentElement) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    var rootRect = scrollRoot.getBoundingClientRect();
    var elRect = el.getBoundingClientRect();
    var top = scrollRoot.scrollTop + (elRect.top - rootRect.top) - 8;
    if (scrollRoot.scrollTo) scrollRoot.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
    else scrollRoot.scrollTop = Math.max(0, top);
  }

  function locatorScope(nav) {
    return (
      nav.closest(".md-tab-panel") ||
      nav.closest(".md-article-host") ||
      nav.closest(".md-d1") ||
      document
    );
  }

  function locatorScrollRoot(nav) {
    var floatHost = nav.closest(".md-article-host");
    if (floatHost) {
      return floatHost.querySelector(".md-doc-scroll") || floatHost.querySelector(".md-article") || floatHost;
    }
    var scope = locatorScope(nav);
    return (
      scope.querySelector(".md-doc-scroll") ||
      scope.querySelector(".md-split__main") ||
      scope.querySelector(".md-article")
    );
  }

  function locatorSectionEl(scope, id) {
    if (!id) return null;
    return (
      scope.querySelector('[data-section="' + id + '"]') ||
      document.getElementById(id)
    );
  }

  function setLocatorActive(nav, btn) {
    if (!nav || !btn) return;
    nav.querySelectorAll(".md-locator__item.is-active").forEach(function (n) {
      n.classList.remove("is-active");
    });
    btn.classList.add("is-active");
    var navRect = nav.getBoundingClientRect();
    var btnRect = btn.getBoundingClientRect();
    if (btnRect.top < navRect.top) nav.scrollTop += btnRect.top - navRect.top;
    else if (btnRect.bottom > navRect.bottom) nav.scrollTop += btnRect.bottom - navRect.bottom;
  }

  function syncLocatorSpy(nav) {
    if (!nav || nav.getAttribute("data-locator-lock") === "1") return;
    var pane = nav.closest(".md-tab-panel");
    if (pane && !pane.classList.contains("is-active")) return;
    var scope = locatorScope(nav);
    var scrollRoot = locatorScrollRoot(nav);
    if (!scrollRoot) return;
    var pairs = [];
    nav.querySelectorAll(".md-locator__item").forEach(function (btn) {
      var id = btn.getAttribute("data-target") || btn.getAttribute("data-section") || "";
      var el = locatorSectionEl(scope, id);
      if (el) pairs.push({ btn: btn, el: el });
    });
    if (!pairs.length) return;
    var rootRect = scrollRoot.getBoundingClientRect();
    var marker = rootRect.top + Math.min(48, Math.max(16, rootRect.height * 0.18));
    var atBottom =
      scrollRoot.scrollHeight - (scrollRoot.scrollTop + scrollRoot.clientHeight) <= 4;
    var current = atBottom ? pairs[pairs.length - 1].btn : pairs[0].btn;
    if (!atBottom) {
      pairs.forEach(function (it) {
        if (it.el.getBoundingClientRect().top <= marker) current = it.btn;
      });
    }
    if (!current.classList.contains("is-active")) setLocatorActive(nav, current);
  }

  function syncLocatorSpies() {
    document.querySelectorAll(".md-locator").forEach(function (nav) {
      if (nav.getAttribute("data-md-bound") === "1") syncLocatorSpy(nav);
    });
  }

  function lockLocatorSpy(nav) {
    nav.setAttribute("data-locator-lock", "1");
    if (nav._locatorUnlock) clearTimeout(nav._locatorUnlock);
    nav._locatorUnlock = setTimeout(function () {
      nav.removeAttribute("data-locator-lock");
      syncLocatorSpy(nav);
    }, 640);
  }

  function bindLocators() {
    document.querySelectorAll(".md-locator").forEach(function (nav) {
      if (nav.getAttribute("data-md-bound") === "1") return;
      nav.setAttribute("data-md-bound", "1");
      nav.addEventListener("click", function (ev) {
        var btn = ev.target.closest(".md-locator__item");
        if (!btn || !nav.contains(btn)) return;
        ev.preventDefault();
        setLocatorActive(nav, btn);
        var target =
          btn.getAttribute("data-target") ||
          btn.getAttribute("data-section") ||
          "";
        var host = locatorScope(nav);
        lockLocatorSpy(nav);
        scrollToSectionTarget(host, target);
        nav.dispatchEvent(
          new CustomEvent("md-locator-select", {
            bubbles: true,
            detail: { item: btn, target: target },
          })
        );
      });
      var scrollRoot = locatorScrollRoot(nav);
      if (scrollRoot && scrollRoot.getAttribute("data-locator-scroll") !== "1") {
        scrollRoot.setAttribute("data-locator-scroll", "1");
        scrollRoot.addEventListener(
          "scroll",
          function () {
            if (scrollRoot._locatorTick) return;
            scrollRoot._locatorTick = true;
            requestAnimationFrame(function () {
              scrollRoot._locatorTick = false;
              document.querySelectorAll(".md-locator").forEach(function (other) {
                if (locatorScrollRoot(other) === scrollRoot) syncLocatorSpy(other);
              });
            });
          },
          { passive: true }
        );
      }
      syncLocatorSpy(nav);
    });
  }

  function setOutlineOpen(host, open) {
    if (!host) return;
    if (host.classList.contains("md-locator-float")) {
      host.classList.toggle("is-collapsed", !open);
    } else {
      host.classList.toggle("is-side-collapsed", !open);
    }
    host.querySelectorAll("[data-outline-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "收起大纲" : "展开大纲");
    });
  }

  function bindOutlineCollapse() {
    document.querySelectorAll(".md-split--outline, .md-locator-float").forEach(function (host) {
      if (host.getAttribute("data-md-bound") === "1") return;
      host.setAttribute("data-md-bound", "1");
      host.addEventListener("click", function (ev) {
        var btn = ev.target.closest("[data-outline-toggle]");
        if (!btn || !host.contains(btn)) return;
        ev.preventDefault();
        var collapsed = host.classList.contains("md-locator-float")
          ? host.classList.contains("is-collapsed")
          : host.classList.contains("is-side-collapsed");
        setOutlineOpen(host, collapsed);
      });
    });
  }

  function bindNestTables() {
    document.querySelectorAll(".md-table--nest").forEach(function (table) {
      if (table.getAttribute("data-md-bound") === "1") return;
      table.setAttribute("data-md-bound", "1");
      table.addEventListener("click", function (ev) {
        var toggle = ev.target.closest(".md-nest-toggle");
        if (!toggle || !table.contains(toggle)) return;
        ev.preventDefault();
        var row = toggle.closest("tr");
        if (!row) return;
        var id = row.getAttribute("data-row-id");
        if (!id) return;
        var willCollapse = !row.classList.contains("is-collapsed-branch");
        row.classList.toggle("is-collapsed-branch", willCollapse);
        toggle.setAttribute("aria-expanded", willCollapse ? "false" : "true");
        toggle.setAttribute("aria-label", willCollapse ? "展开" : "收起");
        table.querySelectorAll('.md-row--child[data-parent="' + id + '"]').forEach(function (child) {
          child.hidden = willCollapse;
        });
      });
    });
  }

  function bindTrees() {
    document.querySelectorAll(".md-tree").forEach(function (tree) {
      if (tree.getAttribute("data-md-bound") === "1") return;
      tree.setAttribute("data-md-bound", "1");
      enhanceTree(tree);
      tree.addEventListener("click", function (ev) {
        if (handleTreeAction(tree, ev)) return;
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
        if (ev.target.closest(".md-tree__rename")) return;
        selectTreeItem(tree, item);
      });
      bindTreeDrag(tree);
    });
  }

  function treeEditOn(tree) {
    return tree.getAttribute("data-tree-edit") !== "off";
  }

  function treeLeafLocked(tree, li) {
    if (!li) return true;
    if (li.hasAttribute("data-leaf")) return true;
    if (tree.getAttribute("data-leaf-add") === "off" && !li.querySelector(":scope > ul")) {
      return true;
    }
    return false;
  }

  function treeItemOf(li) {
    return li ? li.querySelector(":scope > .md-tree__row > .md-tree__item, :scope > .md-tree__item") : null;
  }

  function treeRowOf(li) {
    if (!li) return null;
    var row = li.querySelector(":scope > .md-tree__row");
    if (row) return row;
    var item = li.querySelector(":scope > .md-tree__item");
    return item ? ensureTreeRow(item) : null;
  }

  function treeLabelOf(item) {
    return item ? item.querySelector(".md-tree__label") : null;
  }

  function treeNotify(tree, action, detail) {
    var payload = detail || {};
    payload.action = action;
    tree.dispatchEvent(new CustomEvent("md-tree-change", { bubbles: true, detail: payload }));
  }

  function pruneEmptyBranch(li) {
    if (!li) return;
    var ul = li.querySelector(":scope > ul");
    if (ul && !ul.children.length) ul.remove();
  }

  function childListOf(li, create) {
    var ul = li.querySelector(":scope > ul");
    if (!ul && create) {
      ul = document.createElement("ul");
      li.appendChild(ul);
    }
    return ul;
  }

  function ensureTreeRow(item) {
    if (item.parentElement && item.parentElement.classList.contains("md-tree__row")) {
      return item.parentElement;
    }
    var row = document.createElement("div");
    row.className = "md-tree__row";
    item.parentNode.insertBefore(row, item);
    row.appendChild(item);
    return row;
  }

  function ensureTreeOps(row) {
    if (row.querySelector(".md-tree__ops")) return;
    var ops = document.createElement("div");
    ops.className = "md-tree__ops";
    ops.innerHTML =
      '<button type="button" class="md-icon-btn" data-tree-act="add" title="增子节点" aria-label="增子节点">' +
      '<span class="md-icon" data-icon="add" aria-hidden="true"></span></button>' +
      '<button type="button" class="md-icon-btn" data-tree-act="rename" title="重命名" aria-label="重命名">' +
      '<span class="md-icon" data-icon="edit" aria-hidden="true"></span></button>' +
      '<button type="button" class="md-icon-btn" data-tree-act="delete" title="删除" aria-label="删除">' +
      '<span class="md-icon md-icon--danger" data-icon="delete" aria-hidden="true"></span></button>';
    row.appendChild(ops);
    paintIcon(ops);
  }

  function ensureTreeBar(tree) {
    var prev = tree.previousElementSibling;
    if (prev && prev.classList.contains("md-tree-bar")) return prev;
    var bar = document.createElement("div");
    bar.className = "md-tree-bar";
    bar.innerHTML =
      '<button type="button" class="md-icon-btn" data-tree-act="expand" title="全部展开" aria-label="全部展开">' +
      '<span class="md-icon" data-icon="unfold" aria-hidden="true"></span></button>' +
      '<button type="button" class="md-icon-btn" data-tree-act="collapse" title="全部收起" aria-label="全部收起">' +
      '<span class="md-icon" data-icon="fold" aria-hidden="true"></span></button>' +
      '<button type="button" class="md-btn md-btn--contained md-btn--sm" data-tree-act="add-root">' +
      '<span class="md-icon" data-icon="add" aria-hidden="true"></span>根节点</button>';
    tree.parentNode.insertBefore(bar, tree);
    paintIcon(bar);
    return bar;
  }

  function enhanceTree(tree) {
    if (!treeEditOn(tree)) return;
    var bar = ensureTreeBar(tree);
    if (bar.getAttribute("data-md-bound") !== "1") {
      bar.setAttribute("data-md-bound", "1");
      bar.addEventListener("click", function (ev) {
        handleTreeAction(tree, ev);
      });
    }
    tree.querySelectorAll(".md-tree__item").forEach(function (item) {
      var row = ensureTreeRow(item);
      ensureTreeOps(row);
    });
  }

  function uniqueTreeName(tree, base) {
    var names = {};
    tree.querySelectorAll(".md-tree__label").forEach(function (el) {
      names[el.textContent.trim()] = true;
    });
    if (!names[base]) return base;
    var i = 2;
    while (names[base + " " + i]) i += 1;
    return base + " " + i;
  }

  function createTreeLi(tree, name) {
    var li = document.createElement("li");
    var row = document.createElement("div");
    row.className = "md-tree__row";
    var item = document.createElement("button");
    item.type = "button";
    item.className = "md-tree__item";
    item.setAttribute("data-cat", name);
    item.innerHTML =
      '<span class="md-icon md-tree__toggle" data-icon="chevron-right" aria-hidden="true"></span>' +
      '<span class="md-tree__label"></span>';
    item.querySelector(".md-tree__label").textContent = name;
    row.appendChild(item);
    ensureTreeOps(row);
    li.appendChild(row);
    paintIcon(li);
    return li;
  }

  function selectTreeItem(tree, item) {
    if (!item) return;
    tree.querySelectorAll(".md-tree__item.is-active").forEach(function (n) {
      n.classList.remove("is-active");
    });
    item.classList.add("is-active");
    var li = item.closest("li");
    if (li && li.querySelector(":scope > ul")) li.classList.add("is-open");
    var cat = item.getAttribute("data-cat") || (treeLabelOf(item) ? treeLabelOf(item).textContent.trim() : "");
    if (treeLabelOf(item) && !item.getAttribute("data-cat")) item.setAttribute("data-cat", cat);
    var title = document.getElementById("catTitle");
    if (title && cat) title.textContent = cat;
    tree.dispatchEvent(
      new CustomEvent("md-tree-select", {
        bubbles: true,
        detail: { item: item, cat: cat, li: li },
      })
    );
  }

  function startTreeRename(tree, item) {
    var label = treeLabelOf(item);
    if (!label || item.querySelector(".md-tree__rename")) return;
    var input = document.createElement("input");
    input.type = "text";
    input.className = "md-field__input md-tree__rename";
    input.value = label.textContent.trim();
    label.replaceWith(input);
    input.focus();
    input.select();
    var done = false;
    function commit(ok) {
      if (done) return;
      done = true;
      var next = document.createElement("span");
      next.className = "md-tree__label";
      var val = input.value.replace(/^\s+|\s+$/g, "");
      if (!ok || !val) val = item.getAttribute("data-cat") || "未命名";
      next.textContent = val;
      item.setAttribute("data-cat", val);
      input.replaceWith(next);
      if (item.classList.contains("is-active")) {
        var title = document.getElementById("catTitle");
        if (title) title.textContent = val;
      }
      treeNotify(tree, "rename", { item: item, cat: val });
    }
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") {
        ev.preventDefault();
        commit(true);
      } else if (ev.key === "Escape") {
        ev.preventDefault();
        commit(false);
      }
    });
    input.addEventListener("blur", function () { commit(true); });
  }

  function addTreeChild(tree, parentLi) {
    if (treeLeafLocked(tree, parentLi)) {
      snackbar("末级节点不可新增子节点");
      return;
    }
    var name = uniqueTreeName(tree, "新节点");
    var li = createTreeLi(tree, name);
    childListOf(parentLi, true).appendChild(li);
    parentLi.classList.add("is-open");
    var item = treeItemOf(li);
    selectTreeItem(tree, item);
    startTreeRename(tree, item);
    treeNotify(tree, "add-child", { item: item, parent: parentLi });
  }

  function addTreeRoot(tree) {
    var name = uniqueTreeName(tree, "新节点");
    var li = createTreeLi(tree, name);
    tree.appendChild(li);
    var item = treeItemOf(li);
    selectTreeItem(tree, item);
    startTreeRename(tree, item);
    treeNotify(tree, "add-root", { item: item });
  }

  function deleteTreeLi(tree, li) {
    var item = treeItemOf(li);
    var label = item ? (treeLabelOf(item) ? treeLabelOf(item).textContent.trim() : "") : "";
    confirm({
      title: "删除节点",
      body: "确定删除「" + (label || "该节点") + "」？子节点将一并删除。",
      ok: "删除",
      onOk: function () {
        var parentLi = li.parentElement && li.parentElement.closest("li");
        var wasActive = !!(item && item.classList.contains("is-active"));
        li.remove();
        pruneEmptyBranch(parentLi);
        if (wasActive) {
          var next = parentLi ? treeItemOf(parentLi) : tree.querySelector(".md-tree__item");
          if (next) selectTreeItem(tree, next);
        }
        treeNotify(tree, "delete", { cat: label });
      },
    });
  }

  function setTreeOpenAll(tree, open) {
    tree.querySelectorAll("li").forEach(function (li) {
      if (li.querySelector(":scope > ul")) {
        li.classList.toggle("is-open", open);
      }
    });
  }

  function handleTreeAction(tree, ev) {
    var btn = ev.target.closest("[data-tree-act]");
    if (!btn) return false;
    var bar = tree.previousElementSibling;
    var inBar = bar && bar.classList.contains("md-tree-bar") && bar.contains(btn);
    var inOps = tree.contains(btn) && btn.closest(".md-tree__ops");
    if (!inBar && !inOps) return false;
    ev.preventDefault();
    ev.stopPropagation();
    var act = btn.getAttribute("data-tree-act");
    if (act === "expand") setTreeOpenAll(tree, true);
    else if (act === "collapse") setTreeOpenAll(tree, false);
    else if (act === "add-root") addTreeRoot(tree);
    else if (act === "add") addTreeChild(tree, btn.closest("li"));
    else if (act === "rename") startTreeRename(tree, treeItemOf(btn.closest("li")));
    else if (act === "delete") deleteTreeLi(tree, btn.closest("li"));
    return true;
  }

  function clearTreeDrop(tree) {
    tree.querySelectorAll(".is-drop-before, .is-drop-into, .is-drop-after").forEach(function (el) {
      el.classList.remove("is-drop-before", "is-drop-into", "is-drop-after");
    });
  }

  function treeDropZone(row, clientY, tree, targetLi) {
    var rect = row.getBoundingClientRect();
    var y = (clientY - rect.top) / (rect.height || 1);
    if (y < 0.28) return "before";
    if (y > 0.72) return "after";
    if (treeLeafLocked(tree, targetLi)) return y < 0.5 ? "before" : "after";
    return "into";
  }

  function applyTreeMove(tree, dragLi, targetLi, zone) {
    if (!dragLi || !targetLi || dragLi === targetLi || dragLi.contains(targetLi)) return false;
    var oldParent = dragLi.parentElement && dragLi.parentElement.closest("li");
    if (zone === "into") {
      childListOf(targetLi, true).appendChild(dragLi);
      targetLi.classList.add("is-open");
    } else if (zone === "before") {
      targetLi.parentNode.insertBefore(dragLi, targetLi);
    } else {
      targetLi.parentNode.insertBefore(dragLi, targetLi.nextSibling);
    }
    pruneEmptyBranch(oldParent);
    treeNotify(tree, "move", { li: dragLi, target: targetLi, zone: zone });
    return true;
  }

  function bindTreeDrag(tree) {
    if (!treeEditOn(tree)) return;
    var dragLi = null;
    var dragging = false;
    var startX = 0;
    var startY = 0;
    var suppressClick = false;

    function endDrag(apply, ev) {
      var clientY = ev && ev.clientY;
      var clientX = ev && ev.clientX;
      var hit = clientX != null ? document.elementFromPoint(clientX, clientY) : null;
      var row = hit && hit.closest ? hit.closest(".md-tree__row") : null;
      var targetLi = row && tree.contains(row) ? row.closest("li") : null;
      var zone = row && targetLi ? treeDropZone(row, clientY, tree, targetLi) : "";
      if (apply && dragging) applyTreeMove(tree, dragLi, targetLi, zone);
      if (dragging) suppressClick = true;
      clearTreeDrop(tree);
      if (dragLi) dragLi.classList.remove("is-dragging");
      dragLi = null;
      dragging = false;
      document.removeEventListener("pointermove", onMove);
      document.removeEventListener("pointerup", onUp);
      document.removeEventListener("pointercancel", onCancel);
    }

    function onMove(ev) {
      if (!dragLi) return;
      if (!dragging) {
        if (Math.abs(ev.clientX - startX) < 6 && Math.abs(ev.clientY - startY) < 6) return;
        dragging = true;
        dragLi.classList.add("is-dragging");
      }
      ev.preventDefault();
      var hit = document.elementFromPoint(ev.clientX, ev.clientY);
      var row = hit && hit.closest ? hit.closest(".md-tree__row") : null;
      clearTreeDrop(tree);
      if (!row || !tree.contains(row)) return;
      var targetLi = row.closest("li");
      if (!targetLi || dragLi === targetLi || dragLi.contains(targetLi)) return;
      row.classList.add("is-drop-" + treeDropZone(row, ev.clientY, tree, targetLi));
    }

    function onUp(ev) { endDrag(true, ev); }
    function onCancel(ev) { endDrag(false, ev); }

    tree.addEventListener("pointerdown", function (ev) {
      if (ev.button) return;
      if (ev.target.closest(".md-tree__ops, .md-tree__rename, .md-tree__toggle")) return;
      var row = ev.target.closest(".md-tree__row");
      if (!row || !tree.contains(row)) return;
      dragLi = row.closest("li");
      if (!dragLi) return;
      startX = ev.clientX;
      startY = ev.clientY;
      dragging = false;
      document.addEventListener("pointermove", onMove);
      document.addEventListener("pointerup", onUp);
      document.addEventListener("pointercancel", onCancel);
    });
    tree.addEventListener("click", function (ev) {
      if (!suppressClick) return;
      suppressClick = false;
      ev.preventDefault();
      ev.stopPropagation();
    }, true);
  }

  function previewSkip(el) {
    if (!el || !el.closest) return true;
    if (el.closest(".md-lightbox")) return true;
    if (el.getAttribute("data-preview") === "off") return true;
    if (el.closest("[data-preview=off]")) return true;
    if (el.closest(".md-upload--file")) return true;
    if (
      el.closest(
        ".md-appbar__cover, .md-card__leading, .md-profile__media, .md-set-row__thumb, .md-empty__art, .md-chart-ph, .md-upload-grid__add, .md-upload-grid__del, .md-upload__replace"
      )
    ) {
      return true;
    }
    if (el.closest(".is-hidden")) return true;
    return false;
  }

  function isMediaLike(el) {
    if (el.tagName === "IMG" && !el.closest(".md-icon, svg")) return true;
    if (
      el.classList &&
      (el.classList.contains("md-upload__preview") ||
        el.classList.contains("md-upload-grid__thumb"))
    ) {
      return true;
    }
    var cls = el.className && String(el.className);
    return !!(cls && /\bmd-media-ph--[1-6]\b/.test(cls));
  }

  function isPreviewable(el) {
    if (!el || previewSkip(el) || !isMediaLike(el)) return false;
    if (el.getAttribute("data-preview") === "on" || el.closest("[data-preview=on]")) {
      return true;
    }
    /* 单图 / 多图 / 视频上传：已选缩略默认可点大图预览 */
    if (
      el.classList &&
      (el.classList.contains("md-upload__preview") ||
        el.classList.contains("md-upload-grid__thumb")) &&
      el.closest(".md-upload--single, .md-upload-grid, [data-upload]")
    ) {
      return true;
    }
    if (el.closest(".md-card--row")) return true;
    if (el.closest("[data-lightbox]")) return true;
    return false;
  }

  var lightboxRoot = null;

  /**
   * Preview groups stay separate by zone:
   * - md-card--row: one group per card
   * - upload multi: one group per md-upload-grid; single: one per md-upload--single
   * - detail [data-lightbox]: swiper / article / comment-list each their own group
   * - optional [data-lightbox-group] overrides the container
   */
  function previewGroupRoot(el) {
    if (!el) return lightboxRoot || document;
    var row = el.closest(".md-card--row");
    if (row) return row;
    var uploadGrid = el.closest(".md-upload-grid");
    if (uploadGrid) return uploadGrid;
    var uploadSingle = el.closest(".md-upload--single, [data-upload=single]");
    if (uploadSingle) return uploadSingle;
    var named = el.closest("[data-lightbox-group]");
    if (named) return named;
    var page = el.closest("[data-lightbox]");
    if (page) {
      var swiper = el.closest(".md-swiper");
      if (swiper) return swiper;
      var hero = el.closest(".md-hero, .md-detail-hero");
      if (hero) return hero;
      var article = el.closest(".md-article, .md-article-block");
      if (article) return article;
      var comments = el.closest(".md-comment-list");
      if (comments) return comments;
      var comment = el.closest(".md-comment");
      if (comment) return comment;
      var mod = el.closest(".md-module");
      if (mod) return mod;
      return page;
    }
    return document;
  }

  function collectPreviewables(root) {
    root = root || lightboxRoot || document;
    var nodes = root.querySelectorAll(
      '[class*="md-media-ph--"], img, .md-upload__preview, .md-upload-grid__thumb'
    );
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
    document.querySelectorAll(".md-previewable").forEach(function (el) {
      el.classList.remove("md-previewable");
    });
    collectPreviewables(document).forEach(function (el) {
      el.classList.add("md-previewable");
    });
  }

  function mediaUrl(el) {
    if (!el) return "";
    var dataSrc = el.getAttribute && el.getAttribute("data-preview-src");
    if (dataSrc) return dataSrc;
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
    var kind = el && el.getAttribute && el.getAttribute("data-preview-kind");
    if (src && kind === "video") {
      var video = document.createElement("video");
      video.src = src;
      video.controls = true;
      video.playsInline = true;
      video.setAttribute("playsinline", "");
      frame.appendChild(video);
      return;
    }
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

  // Default: detail ([data-lightbox]), md-card--row, and image/video uploads.
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

  function detailScrollRoot(page) {
    if (!page) return document.scrollingElement || document.documentElement;
    if (page.classList.contains("md-mobile-page")) {
      return page.querySelector(".md-mobile-body") || page;
    }
    return document.scrollingElement || document.documentElement;
  }

  function scrollDetailTop(page) {
    var root = detailScrollRoot(page);
    if (root === document.scrollingElement || root === document.documentElement || root === document.body) {
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    if (root.scrollTo) root.scrollTo({ top: 0, behavior: "smooth" });
    else root.scrollTop = 0;
  }

  function scrollDetailTo(page, el) {
    if (!el) return;
    var root = detailScrollRoot(page);
    if (root === document.scrollingElement || root === document.documentElement || root === document.body) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    var rootRect = root.getBoundingClientRect();
    var elRect = el.getBoundingClientRect();
    var top = root.scrollTop + (elRect.top - rootRect.top) - 8;
    if (root.scrollTo) root.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
    else root.scrollTop = Math.max(0, top);
  }

  function detailSectionTitle(el) {
    if (!el) return "";
    var named = el.getAttribute("data-section");
    if (named) return named.trim();
    var head =
      el.querySelector(".md-section-head__title") ||
      el.querySelector(".md-detail-head__title") ||
      el.querySelector(".md-article__h2") ||
      el.querySelector("h1, h2");
    return head ? String(head.textContent || "").trim() : "";
  }

  function collectDetailSections(page) {
    var out = [];
    var seen = [];
    function push(el) {
      if (!el || seen.indexOf(el) >= 0) return;
      var pane = el.closest(".md-tab-panel");
      if (pane && !pane.classList.contains("is-active")) return;
      var title = detailSectionTitle(el);
      if (!title) return;
      seen.push(el);
      if (!el.id) {
        el.id = "detail-sec-" + out.length;
      }
      out.push({ el: el, title: title });
    }
    page.querySelectorAll(".md-hero[data-section]").forEach(push);
    page.querySelectorAll(".md-detail-hero[data-section], .md-detail-hero").forEach(push);
    page.querySelectorAll(".md-module[data-section], .md-module").forEach(push);
    return out;
  }

  function ensureDetailTocDrawer() {
    var id = "mdDetailToc";
    if (document.getElementById(id)) return id;
    var mask = document.createElement("div");
    mask.id = id + "Backdrop";
    mask.className = "md-backdrop";
    mask.addEventListener("click", function () {
      closeDrawer(id);
    });
    var sheet = document.createElement("aside");
    sheet.id = id;
    sheet.className = "md-drawer md-drawer--bottom";
    sheet.setAttribute("aria-hidden", "true");
    sheet.innerHTML =
      '<h2 class="md-drawer__title">目录</h2>' +
      '<div class="md-drawer__body" id="mdDetailTocBody"></div>';
    document.body.appendChild(mask);
    document.body.appendChild(sheet);
    ensureBottomDrawerClose(sheet);
    paintIcon(sheet);
    return id;
  }

  function openDetailToc(page) {
    var id = ensureDetailTocDrawer();
    var body = document.getElementById("mdDetailTocBody");
    if (!body) return;
    var sections = collectDetailSections(page);
    body.innerHTML = "";
    if (!sections.length) {
      var empty = document.createElement("p");
      empty.className = "md-body2";
      empty.textContent = "本页暂无区块标题";
      body.appendChild(empty);
    } else {
      sections.forEach(function (sec) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "md-drawer__opt";
        btn.textContent = sec.title;
        btn.addEventListener("click", function () {
          closeDrawer(id);
          scrollDetailTo(page, sec.el);
        });
        body.appendChild(btn);
      });
    }
    openDrawer(id);
  }

  function ensureDetailNav() {
    document.querySelectorAll(".md-detail-page").forEach(function (page) {
      var mode = page.getAttribute("data-detail-nav");
      if (mode === "off" || mode === "0" || mode === "false") return;
      if (page.querySelector(".md-pod--detail-nav")) return;
      var wantToc = true;
      var wantTop = true;
      if (mode === "toc") wantTop = false;
      else if (mode === "top") wantToc = false;
      else if (mode && mode !== "on") {
        wantToc = mode.indexOf("toc") >= 0;
        wantTop = mode.indexOf("top") >= 0;
      }
      if (!wantToc && !wantTop) return;

      var isDesk = page.classList.contains("md-d1");
      var pod = document.createElement("nav");
      pod.className = isDesk
        ? "md-pod md-pod--desk md-pod--br md-pod--detail-nav"
        : "md-pod md-pod--br md-pod--detail-nav";
      pod.setAttribute("aria-label", "页面导航");
      if (wantToc) {
        var tocBtn = document.createElement("button");
        tocBtn.type = "button";
        tocBtn.className = "md-pod__item";
        tocBtn.setAttribute("aria-label", "目录");
        tocBtn.setAttribute("data-detail-nav", "toc");
        tocBtn.innerHTML = '<span class="md-icon" data-icon="list" aria-hidden="true"></span>';
        tocBtn.addEventListener("click", function () {
          openDetailToc(page);
        });
        pod.appendChild(tocBtn);
      }
      if (wantTop) {
        var topBtn = document.createElement("button");
        topBtn.type = "button";
        topBtn.className = "md-pod__item";
        topBtn.setAttribute("aria-label", "返回顶部");
        topBtn.setAttribute("data-detail-nav", "top");
        topBtn.innerHTML = '<span class="md-icon" data-icon="arrow-up" aria-hidden="true"></span>';
        topBtn.addEventListener("click", function () {
          scrollDetailTop(page);
        });
        pod.appendChild(topBtn);
      }
      page.appendChild(pod);
      paintIcon(pod);
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

  function copyPlainText(text) {
    if (!text) return Promise.reject();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      try {
        if (document.execCommand("copy")) resolve();
        else reject();
      } catch (err) {
        reject(err);
      }
      document.body.removeChild(ta);
    });
  }

  function overflowCellText(cell) {
    if (!cell) return "";
    var clone = cell.cloneNode(true);
    clone
      .querySelectorAll(
        "button, .md-menu, .md-check, .md-radio, input, select, textarea, .md-icon, .md-thumb, .md-actions, a.md-btn, .md-btn"
      )
      .forEach(function (n) {
        if (n.parentNode) n.parentNode.removeChild(n);
      });
    return String(clone.textContent || "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function isOverflowCell(el) {
    if (!el || !el.getBoundingClientRect) return false;
    if (el.closest(".md-col-check, .md-col-actions, .md-actions")) return false;
    return el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1;
  }

  function ensureOverflowTip() {
    var tip = document.getElementById("mdOverflowTip");
    if (tip) return tip;
    tip = document.createElement("div");
    tip.id = "mdOverflowTip";
    tip.className = "md-overflow-tip";
    tip.setAttribute("role", "tooltip");
    document.body.appendChild(tip);
    return tip;
  }

  function placeOverflowTip(tip, ev) {
    var pad = 12;
    var x = (ev && ev.clientX != null ? ev.clientX : 0) + 14;
    var y = (ev && ev.clientY != null ? ev.clientY : 0) + 16;
    tip.style.left = "0px";
    tip.style.top = "0px";
    var rect = tip.getBoundingClientRect();
    var maxX = window.innerWidth - rect.width - pad;
    var maxY = window.innerHeight - rect.height - pad;
    tip.style.left = Math.max(pad, Math.min(x, maxX)) + "px";
    tip.style.top = Math.max(pad, Math.min(y, maxY)) + "px";
  }

  /** AD 列表：表头/单元格文字溢出省略时，悬停看全文，点击复制 */
  function bindOverflowTips() {
    if (document.documentElement.getAttribute("data-md-overflow-tip") === "1") return;
    var hosts = document.querySelectorAll(".md-d1 .md-table");
    if (!hosts.length) return;
    document.documentElement.setAttribute("data-md-overflow-tip", "1");
    var tip = ensureOverflowTip();
    var active = null;

    function hide() {
      if (active) active.classList.remove("is-overflow");
      active = null;
      tip.classList.remove("is-open");
      tip.textContent = "";
    }

    function cellFromEvent(ev) {
      var t = ev.target;
      if (!t || !t.closest) return null;
      if (
        t.closest(
          "button, a.md-btn, .md-btn, input, select, textarea, .md-menu, .md-check, .md-radio, .md-actions, label.md-check, label.md-radio"
        )
      ) {
        return null;
      }
      var cell = t.closest(".md-d1 .md-table th, .md-d1 .md-table td");
      if (!cell || cell.closest(".md-col-check, .md-col-actions")) return null;
      return cell;
    }

    document.addEventListener(
      "pointerover",
      function (ev) {
        var cell = cellFromEvent(ev);
        if (!cell) {
          if (active && (!ev.relatedTarget || !active.contains(ev.relatedTarget))) hide();
          return;
        }
        if (!isOverflowCell(cell)) {
          if (active === cell) hide();
          return;
        }
        var text = overflowCellText(cell);
        if (!text) return;
        if (active && active !== cell) active.classList.remove("is-overflow");
        active = cell;
        cell.classList.add("is-overflow");
        tip.textContent = text;
        tip.classList.add("is-open");
        placeOverflowTip(tip, ev);
      },
      true
    );

    document.addEventListener(
      "pointermove",
      function (ev) {
        if (!active || !tip.classList.contains("is-open")) return;
        placeOverflowTip(tip, ev);
      },
      true
    );

    document.addEventListener(
      "pointerout",
      function (ev) {
        if (!active) return;
        var to = ev.relatedTarget;
        if (to && active.contains(to)) return;
        hide();
      },
      true
    );

    document.addEventListener(
      "click",
      function (ev) {
        var cell = cellFromEvent(ev);
        if (!cell || !isOverflowCell(cell)) return;
        var text = overflowCellText(cell);
        if (!text) return;
        ev.preventDefault();
        ev.stopPropagation();
        copyPlainText(text).then(
          function () {
            snackbar("已复制");
          },
          function () {
            snackbar("复制失败", { severity: "error" });
          }
        );
      },
      true
    );

    window.addEventListener("scroll", hide, true);
    window.addEventListener("resize", hide);
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

  var _actionTextCanvas;

  function actionColPadding(cell) {
    if (!cell) return 8;
    var cs = window.getComputedStyle(cell);
    return (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0);
  }

  function measureTextPx(text, refEl) {
    _actionTextCanvas = _actionTextCanvas || document.createElement("canvas");
    var ctx = _actionTextCanvas.getContext("2d");
    if (!ctx) return (text || "").length * 14;
    var cs = refEl ? window.getComputedStyle(refEl) : null;
    ctx.font = cs && cs.font ? cs.font : "400 14px sans-serif";
    return Math.ceil(ctx.measureText(text || "").width);
  }

  /** 按直出控件计数/文案算宽（28px 图标钮；文字钮按 font 测字宽+padding），与视口无关 */
  function calcActionsContentWidth(pack, refCell) {
    if (!pack) return 0;
    var total = 0;
    var iconW = 28;
    var textRef =
      pack.querySelector(".md-btn:not(.md-icon-btn)") ||
      (refCell && refCell.querySelector(".md-actions .md-btn:not(.md-icon-btn)"));
    Array.prototype.forEach.call(pack.children, function (child) {
      if (child.classList.contains("md-icon-btn")) {
        total += iconW;
        return;
      }
      if (child.classList.contains("md-select-wrap")) {
        if (child.querySelector(".md-icon-btn")) total += iconW;
        return;
      }
      if (child.classList.contains("md-btn")) {
        var label = (child.textContent || "").replace(/\s+/g, " ").trim();
        var cs = window.getComputedStyle(child);
        var pad =
          (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0);
        var border =
          (parseFloat(cs.borderLeftWidth) || 0) +
          (parseFloat(cs.borderRightWidth) || 0);
        total += pad + border + measureTextPx(label, textRef || child);
      }
    });
    return total;
  }

  function ensureTableColgroup(table) {
    var cg = table.querySelector("colgroup");
    if (cg) return cg;
    var row = table.tHead && table.tHead.rows[0];
    if (!row || !row.cells.length) return null;
    cg = document.createElement("colgroup");
    Array.prototype.forEach.call(row.cells, function (th) {
      var col = document.createElement("col");
      Array.prototype.forEach.call(th.classList, function (cls) {
        if (cls.indexOf("md-col-") === 0) col.classList.add(cls);
      });
      cg.appendChild(col);
    });
    table.insertBefore(cg, table.firstChild);
    return cg;
  }

  function applyActionColWidth(table, widthPx) {
    var col = Math.max(36, Math.ceil(widthPx));
    var key = String(col);
    if (table.dataset.mdActionsColW === key) return;
    table.dataset.mdActionsColW = key;
    table.style.setProperty("--md-col-actions-w", key + "px");
    var cg = ensureTableColgroup(table);
    if (cg) {
      var actionCol = cg.querySelector("col.md-col-actions");
      if (actionCol) actionCol.style.width = key + "px";
    }
  }

  function syncActionColWidths() {
    document.querySelectorAll("table.md-table").forEach(function (table) {
      var cells = table.querySelectorAll("td.md-col-actions");
      var head = table.querySelector("th.md-col-actions");
      if (!cells.length && !head) return;

      var max = 0;
      cells.forEach(function (cell) {
        var pack = cell.querySelector(".md-actions");
        max = Math.max(max, calcActionsContentWidth(pack, cell));
      });

      if (head) {
        var headCs = window.getComputedStyle(head);
        var headFont = headCs.font || "500 14px sans-serif";
        _actionTextCanvas = _actionTextCanvas || document.createElement("canvas");
        var hctx = _actionTextCanvas.getContext("2d");
        if (hctx) {
          hctx.font = headFont;
          max = Math.max(max, Math.ceil(hctx.measureText(head.textContent || "").width));
        }
      }

      if (!max) return;

      var pad = Math.max(
        actionColPadding(cells[0] || head),
        actionColPadding(head)
      );
      applyActionColWidth(table, max + pad);
    });
  }

  function scheduleActionColWidths() {
    requestAnimationFrame(function () {
      syncActionColWidths();
    });
  }

  function bindActionColObservers() {
    document.querySelectorAll("table.md-table").forEach(function (table) {
      if (table.__mdActionsObs) return;
      var tbody = table.querySelector("tbody");
      if (!tbody) return;
      table.__mdActionsObs = true;
      var timer = 0;
      new MutationObserver(function () {
        clearTimeout(timer);
        timer = setTimeout(scheduleActionColWidths, 16);
      }).observe(tbody, { childList: true, subtree: true });
    });
  }

  function comboIsMulti(root) {
    return root.getAttribute("data-mode") === "multi";
  }

  function comboLeafOnly(root) {
    return root.getAttribute("data-tree") === "leaf";
  }

  function comboOpts(root) {
    return root.querySelectorAll(".md-combo__opt");
  }

  function comboOptLabel(opt) {
    return (opt.getAttribute("data-label") || opt.textContent || "").replace(/\s+/g, " ").trim();
  }

  function comboOptValue(opt) {
    return opt.getAttribute("data-value") || comboOptLabel(opt);
  }

  function comboPaintTrigger(root) {
    var trigger = root.querySelector(".md-combo__trigger");
    if (!trigger) return;
    var ph = root.getAttribute("data-placeholder") || "请选择";
    var vals = [];
    var labels = [];
    comboOpts(root).forEach(function (opt) {
      if (!opt.classList.contains("is-active")) return;
      vals.push(comboOptValue(opt));
      labels.push(comboOptLabel(opt));
    });
    trigger.querySelectorAll(".md-combo__tag, .md-combo__ph, .md-combo__text").forEach(function (n) {
      n.parentNode.removeChild(n);
    });
    var caret = trigger.querySelector(".md-combo__caret");
    function insert(node) {
      if (caret) trigger.insertBefore(node, caret);
      else trigger.appendChild(node);
    }
    if (!vals.length) {
      var phEl = document.createElement("span");
      phEl.className = "md-combo__ph";
      phEl.textContent = ph;
      insert(phEl);
    } else if (comboIsMulti(root)) {
      labels.forEach(function (lab, i) {
        var tag = document.createElement("span");
        tag.className = "md-combo__tag";
        var labEl = document.createElement("span");
        labEl.textContent = lab;
        tag.appendChild(labEl);
        var x = document.createElement("button");
        x.type = "button";
        x.className = "md-combo__tag-x";
        x.setAttribute("data-combo-remove", vals[i]);
        x.setAttribute("aria-label", "移除");
        x.textContent = "×";
        tag.appendChild(x);
        insert(tag);
      });
    } else {
      var t = document.createElement("span");
      t.className = "md-combo__text";
      t.textContent = labels[0];
      insert(t);
    }
    var hidden = root.querySelector(".md-combo__value");
    if (hidden) hidden.value = vals.join(",");
  }

  function comboFilter(root, q) {
    q = (q || "").trim().toLowerCase();
    var empty = root.querySelector(".md-combo__empty");
    var shown = 0;
    comboOpts(root).forEach(function (opt) {
      var hit =
        !q ||
        comboOptLabel(opt).toLowerCase().indexOf(q) >= 0 ||
        comboOptValue(opt).toLowerCase().indexOf(q) >= 0;
      opt.classList.toggle("is-filtered", !hit);
      if (hit) shown += 1;
    });
    root.querySelectorAll(".md-combo__tree li").forEach(function (li) {
      var any = li.querySelector(".md-combo__opt:not(.is-filtered)");
      li.classList.toggle("is-hidden", !any);
      if (q && any) li.classList.add("is-open");
    });
    if (empty) empty.classList.toggle("is-hidden", shown > 0);
  }

  function comboClearFilter(root) {
    var search = root.querySelector(".md-combo__search");
    if (search) search.value = "";
    comboFilter(root, "");
  }

  function comboSetOpt(root, opt, on) {
    if (!opt) return;
    opt.classList.toggle("is-active", on);
    if (comboIsMulti(root) && root.querySelector(".md-combo__tree")) {
      var li = opt.closest("li");
      if (li && on) {
        li.querySelectorAll(".md-combo__opt").forEach(function (child) {
          child.classList.add("is-active");
        });
      }
      if (li && !on) {
        li.querySelectorAll(".md-combo__opt").forEach(function (child) {
          child.classList.remove("is-active");
        });
        var walk = li.parentElement;
        while (walk && walk !== root) {
          if (walk.tagName === "LI") {
            var parentOpt = walk.querySelector(":scope > .md-combo__node .md-combo__opt");
            if (parentOpt) parentOpt.classList.remove("is-active");
          }
          walk = walk.parentElement;
        }
      }
    }
    comboPaintTrigger(root);
  }

  function comboToggleOpt(root, opt) {
    if (!opt || opt.classList.contains("is-disabled")) return;
    if (comboLeafOnly(root) && opt.getAttribute("data-branch") === "1") return;
    if (!comboIsMulti(root)) {
      comboOpts(root).forEach(function (o) {
        o.classList.remove("is-active");
      });
      opt.classList.add("is-active");
      comboPaintTrigger(root);
      root.classList.remove("is-open");
      var trig = root.querySelector(".md-combo__trigger");
      if (trig) trig.setAttribute("aria-expanded", "false");
      return;
    }
    comboSetOpt(root, opt, !opt.classList.contains("is-active"));
  }

  function bindCombos() {
    document.querySelectorAll(".md-combo").forEach(function (root) {
      if (root.getAttribute("data-md-bound") === "1") return;
      root.setAttribute("data-md-bound", "1");
      comboPaintTrigger(root);
      var trigger = root.querySelector(".md-combo__trigger");
      var search = root.querySelector(".md-combo__search");
      if (trigger) {
        trigger.addEventListener("click", function (ev) {
          if (ev.target.closest("[data-combo-remove]")) return;
          ev.preventDefault();
          var open = !root.classList.contains("is-open");
          closeMenus();
          closeCombos(open ? root : null);
          root.classList.toggle("is-open", open);
          trigger.setAttribute("aria-expanded", open ? "true" : "false");
          if (open && search) {
            comboClearFilter(root);
            setTimeout(function () {
              search.focus();
            }, 0);
          }
        });
      }
      root.addEventListener("click", function (ev) {
        var rm = ev.target.closest("[data-combo-remove]");
        if (rm && root.contains(rm)) {
          ev.preventDefault();
          ev.stopPropagation();
          var val = rm.getAttribute("data-combo-remove") || "";
          comboOpts(root).forEach(function (opt) {
            if (comboOptValue(opt) === val) comboSetOpt(root, opt, false);
          });
          return;
        }
        var twist = ev.target.closest("[data-combo-twist]");
        if (twist && root.contains(twist)) {
          ev.preventDefault();
          ev.stopPropagation();
          var li = twist.closest("li");
          if (li) li.classList.toggle("is-open");
          return;
        }
        var opt = ev.target.closest(".md-combo__opt");
        if (opt && root.contains(opt)) {
          ev.preventDefault();
          comboToggleOpt(root, opt);
        }
      });
      if (search) {
        search.addEventListener("input", function () {
          comboFilter(root, search.value);
        });
        search.addEventListener("click", function (ev) {
          ev.stopPropagation();
        });
      }
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key !== "Escape") return;
      closeCombos();
    });
  }

  function filterDrawerDirty(drawer) {
    if (!drawer) return false;
    var dirty = false;
    drawer.querySelectorAll(".md-check input[type=checkbox]").forEach(function (cb) {
      if (cb.checked !== cb.hasAttribute("data-default-checked")) dirty = true;
    });
    drawer.querySelectorAll("select").forEach(function (sel) {
      var def = sel.querySelector("option[data-default]");
      var defVal = def ? def.value : (sel.options[0] ? sel.options[0].value : "");
      if (sel.value !== defVal) dirty = true;
    });
    drawer.querySelectorAll("[data-wheel]").forEach(function (trigger) {
      if (trigger.classList.contains("has-value") || trigger.getAttribute("data-start") || trigger.getAttribute("data-value")) {
        dirty = true;
      }
    });
    return dirty;
  }

  function syncFilterTrigger(btn) {
    var drawerId = btn.getAttribute("data-filter-drawer");
    var drawer = drawerId ? document.getElementById(drawerId) : null;
    btn.classList.toggle("is-active", filterDrawerDirty(drawer));
  }

  function bindFilterTriggers() {
    document.querySelectorAll(".md-search-row__filter[data-filter-drawer]").forEach(function (btn) {
      if (btn.getAttribute("data-filter-bound") === "1") return;
      btn.setAttribute("data-filter-bound", "1");
      var drawerId = btn.getAttribute("data-filter-drawer");
      var drawer = drawerId ? document.getElementById(drawerId) : null;
      if (!drawer) return;
      function sync() {
        syncFilterTrigger(btn);
      }
      drawer.addEventListener("change", sync);
      drawer.addEventListener("input", sync);
      drawer.querySelectorAll("[data-wheel]").forEach(function (trigger) {
        var obs = new MutationObserver(sync);
        obs.observe(trigger, {
          attributes: true,
          attributeFilter: ["class", "data-start", "data-end", "data-value"],
          childList: true,
          characterData: true,
          subtree: true
        });
      });
      sync();
    });
  }

  function bindOverlayAppbars() {
    document.querySelectorAll(".md-mobile-page:has(.md-appbar--overlay)").forEach(function (page) {
      if (page.getAttribute("data-overlay-bound") === "1") return;
      page.setAttribute("data-overlay-bound", "1");
      var bar = page.querySelector(".md-appbar--overlay");
      var body = page.querySelector(".md-mobile-body");
      if (!bar || !body) return;
      var statusBar = document.querySelector(".md-status-bar");
      var immersive = page.classList.contains("md-immersive");
      function sync() {
        var solid = body.scrollTop > 24;
        bar.classList.toggle("is-solid", solid);
        if (statusBar && immersive) {
          statusBar.classList.toggle("md-status-bar--immersive", !solid);
          statusBar.classList.toggle("md-status-bar--standard", solid);
        }
      }
      body.addEventListener("scroll", sync, { passive: true });
      sync();
    });
  }

  function bindUi() {
    ensureStatusBar();
    ensureDetailNav();
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
    bindLocators();
    bindOutlineCollapse();
    bindNestTables();
    bindUploads();
    bindMeProfiles();
    bindSvcStrips();
    bindCombos();
    bindMobileSelects();
    bindProgress();
    bindLightbox();
    bindOverflowTips();
    bindFilterTriggers();
    bindOverlayAppbars();
    document.querySelectorAll(".md-drawer.md-drawer--bottom").forEach(ensureBottomDrawerClose);
    bindActionColObservers();
    scheduleActionColWidths();
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
    alertInfo: alertInfo,
    closeMenus: closeMenus,
    syncActionColWidths: syncActionColWidths,
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
