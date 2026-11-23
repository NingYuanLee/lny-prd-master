/* Prototype shell: sidebar, AppBar, 状态演示, 规格说明, phone scale. */
(function () {
  "use strict";

  var cfg = window.PROTO_SHELL || {};
  var mode = cfg.mode || (cfg.terminal === "PC" || cfg.terminal === "AD" ? "desktop" : "mobile");
  var pages = cfg.pages || [];
  var currentId = cfg.currentId || (pages[0] && pages[0].id) || "";
  var sidebarOpen = cfg.sidebarOpen !== false;
  var statePanelOpen = true;
  var drawerOpen = false;
  var collapsedGroups = {};

  /** Directory URL of current page (always ends with /). Fixes serve cleanUrls → /MP without slash. */
  function dirHref() {
    var path = location.pathname;
    if (/\.html?$/i.test(path)) path = path.replace(/\/[^/]*$/, "/");
    else if (!path.endsWith("/")) path += "/";
    return location.origin + path;
  }

  /** Resolve local relative URLs against the page directory (not the no-slash parent). */
  function relUrl(u) {
    if (!u) return u;
    if (/^(?:#|https?:|mailto:|tel:|javascript:|data:|blob:)/i.test(u)) return u;
    if (u.indexOf("//") === 0) return u;
    try {
      return new URL(u, dirHref()).href;
    } catch (e) {
      if (/^(?:\.\/|\.\.\/|\/)/.test(u)) return u;
      return "./" + u;
    }
  }

  function syncGroup(head, body, open) {
    if (head) {
      head.classList.toggle("is-open", open);
      head.setAttribute("aria-expanded", open ? "true" : "false");
    }
    if (body) body.classList.toggle("is-collapsed", !open);
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (k) {
      if (k === "className") node.className = attrs[k];
      else if (k === "text") node.textContent = attrs[k];
      else if (k === "html") node.innerHTML = attrs[k];
      else if (k === "on") {
        Object.keys(attrs.on).forEach(function (ev) {
          node.addEventListener(ev, attrs.on[ev]);
        });
      } else if (attrs[k] === false || attrs[k] == null) {
        /* skip */
      } else if (attrs[k] === true) {
        node.setAttribute(k, k);
      } else {
        node.setAttribute(k, String(attrs[k]));
      }
    });
    (children || []).forEach(function (c) {
      if (c) node.appendChild(c);
    });
    return node;
  }

  function icon(name) {
    if (window.ProtoIcons && typeof window.ProtoIcons.element === "function") {
      return window.ProtoIcons.element(name);
    }
    return el("span", { className: "md-i md-i-" + name, "aria-hidden": "true" });
  }

  function pageById(id) {
    for (var i = 0; i < pages.length; i++) if (pages[i].id === id) return pages[i];
    return pages[0] || null;
  }

  function groupPages() {
    var groups = [];
    var map = {};
    pages.forEach(function (p) {
      var key = p.module || "页面";
      if (!map[key]) {
        map[key] = { name: key, items: [] };
        groups.push(map[key]);
      }
      map[key].items.push(p);
    });
    return groups;
  }

  function hasStatePanel(page) {
    if (!page) return false;
    /* State demos are opt-out only when the product page owns the state switch. */
    if (page.stateDemo === false) return false;
    return !!(page.comps && page.comps.length);
  }

  window.fitPhoneFrame = function fitPhoneFrame() {
    var area = document.querySelector(".preview-area");
    var host = document.querySelector(".phone-scale-host");
    if (!area || !host) return;
    var pad = 64;
    var bezel = 10;
    var scaleX = (area.clientWidth - pad) / (375 + bezel * 2);
    var scaleY = (area.clientHeight - pad) / (812 + bezel * 2);
    var scale = Math.min(1, scaleX, scaleY);
    if (!isFinite(scale) || scale <= 0) scale = 1;
    host.style.setProperty("--phone-scale", String(scale));
  };

  function postCompState(compId, state) {
    var frame = document.getElementById("previewFrame");
    if (!frame || !frame.contentWindow) return;
    frame.contentWindow.postMessage(
      { type: "comp-state", compId: compId, state: state },
      "*"
    );
  }

  function renderStatePanel(page) {
    var panel = document.getElementById("statePanel");
    var toggle = document.getElementById("statePanelToggle");
    if (!panel) return;
    panel.innerHTML = "";
    var show = hasStatePanel(page);
    if (toggle) toggle.hidden = !show;
    if (!show) {
      panel.classList.remove("show");
      panel.classList.remove("collapsed");
      return;
    }
    panel.classList.add("show");
    if (!statePanelOpen) panel.classList.add("collapsed");
    else panel.classList.remove("collapsed");
    panel.appendChild(el("div", { className: "proto-state__title", text: "状态演示" }));
    (page.comps || []).forEach(function (comp) {
      var group = el("div", { className: "proto-state__group" }, [
        el("div", { className: "proto-state__name", text: comp.name || comp.id }),
      ]);
      var tog = el("div", { className: "md-toggle md-toggle--vert" });
      (comp.states || []).forEach(function (st, idx) {
        var btn = el("button", {
          type: "button",
          className: idx === 0 ? "is-active" : "",
          text: st,
          on: {
            click: function () {
              Array.prototype.forEach.call(tog.querySelectorAll("button"), function (b) {
                b.classList.toggle("is-active", b === btn);
              });
              postCompState(comp.id, st);
            },
          },
        });
        tog.appendChild(btn);
      });
      group.appendChild(tog);
      panel.appendChild(group);
    });
  }

  function fillDrawer(page) {
    var body = document.getElementById("specDrawerBody");
    if (!body) return;
    var spec = (page && page.spec) || {};
    var blocks = [
      ["页面布局说明", spec.layout || "无"],
      ["局部自定义UI组件说明", spec.comps || "无"],
      ["接口交互说明", spec.apis || "无"],
      ["Feature 关联清单", spec.features || "无"],
      ["E. 操作交互说明", spec.actions || "无"],
    ];
    body.innerHTML = "";
    blocks.forEach(function (b) {
      body.appendChild(
        el("section", { className: "proto-drawer__section" }, [
          el("h3", { text: b[0] }),
          el("p", { text: b[1] }),
        ])
      );
    });
  }

  function loadPage(id) {
    var page = pageById(id);
    if (!page) return;
    currentId = page.id;
    var title = document.getElementById("protoTitle");
    if (title) title.textContent = page.name || page.id;
    document.querySelectorAll(".md-list-item[data-page]").forEach(function (a) {
      a.classList.toggle("is-active", a.getAttribute("data-page") === page.id);
    });
    document.querySelectorAll(".proto-nav-group").forEach(function (gEl) {
      var ids = (gEl.getAttribute("data-pages") || "").split(",");
      if (ids.indexOf(page.id) === -1) return;
      var name = gEl.getAttribute("data-group") || "";
      collapsedGroups[name] = false;
      syncGroup(
        gEl.querySelector(".proto-nav-group__head"),
        gEl.querySelector(".proto-nav-group__items"),
        true
      );
    });
    var frame = document.getElementById("previewFrame");
    if (frame) frame.src = relUrl(page.file);
    renderStatePanel(page);
    fillDrawer(page);
    if (mode === "mobile") setTimeout(window.fitPhoneFrame, 0);
  }

  function setSidebar(open) {
    sidebarOpen = open;
    var side = document.getElementById("protoSidebar");
    if (side) side.classList.toggle("collapsed", !open);
    if (mode === "mobile") setTimeout(window.fitPhoneFrame, 220);
  }

  function setStatePanel(open) {
    statePanelOpen = open;
    var panel = document.getElementById("statePanel");
    if (panel && panel.classList.contains("show")) {
      panel.classList.toggle("collapsed", !open);
    }
    if (mode === "mobile") setTimeout(window.fitPhoneFrame, 220);
  }

  function setDrawer(open) {
    drawerOpen = !!open;
    syncSidePanels();
  }

  function syncSidePanels() {
    var spec = document.getElementById("specDrawer");
    var b = document.getElementById("specBackdrop");
    if (spec) spec.classList.toggle("is-open", drawerOpen);
    if (b) b.classList.toggle("is-open", drawerOpen);
  }

  function mountSkillCredit() {
    if (document.getElementById("protoSkillCredit")) return;
    var p = el("p", {
      id: "protoSkillCredit",
      className: "proto-skill-credit",
    });
    p.appendChild(document.createTextNode("该原型使用SKILL地址： "));
    p.appendChild(
      el("a", {
        href: "https://github.com/NingYuanLee/lny-prd-master",
        target: "_blank",
        rel: "noopener noreferrer",
        text: "https://github.com/NingYuanLee/lny-prd-master",
      })
    );
    p.appendChild(document.createTextNode(" 或"));
    p.appendChild(
      el("a", {
        href: "https://gitee.com/ningyuanlee/lny-prd-master",
        target: "_blank",
        rel: "noopener noreferrer",
        text: "https://gitee.com/ningyuanlee/lny-prd-master",
      })
    );
    document.body.appendChild(p);
  }

  function build() {
    var root = document.getElementById("proto-root");
    if (!root) return;
    root.className = "proto-shell";
    root.setAttribute("data-mode", mode);
    root.setAttribute("data-terminal", cfg.terminal || "");

    var nav = el("nav", { className: "proto-sidebar__nav" });
    groupPages().forEach(function (g) {
      var open = collapsedGroups[g.name] !== true;
      var ids = g.items.map(function (p) { return p.id; }).join(",");
      var body = el("div", { className: "proto-nav-group__items" });
      g.items.forEach(function (p) {
        body.appendChild(
          el("button", {
            type: "button",
            className: "md-list-item" + (p.id === currentId ? " is-active" : ""),
            "data-page": p.id,
            on: {
              click: function () {
                loadPage(p.id);
              },
            },
          }, [
            el("span", { className: "proto-nav-item__name", text: p.name || p.id }),
            el("span", { className: "proto-nav-item__id", text: p.id }),
          ])
        );
      });
      var head = el("button", {
        type: "button",
        className: "proto-nav-group__head",
        "aria-expanded": open ? "true" : "false",
        on: {
          click: function () {
            var next = !head.classList.contains("is-open");
            collapsedGroups[g.name] = !next;
            syncGroup(head, body, next);
          },
        },
      }, [
        el("span", { className: "proto-nav-group__title", text: g.name }),
        icon("chevron-right"),
      ]);
      syncGroup(head, body, open);
      nav.appendChild(
        el("div", {
          className: "proto-nav-group",
          "data-group": g.name,
          "data-pages": ids,
        }, [head, body])
      );
    });

    var sidebar = el("aside", { id: "protoSidebar", className: "proto-sidebar" }, [
      el("div", { className: "proto-sidebar__head", text: cfg.title || (cfg.terminal || "") + " 原型" }),
      nav,
    ]);
    if (!sidebarOpen) sidebar.classList.add("collapsed");

    var mapLink =
      mode === "mobile"
        ? el("a", { className: "proto-link", href: "./map.html", text: "关系图" })
        : null;

    var appbar = el("header", { className: "proto-appbar" }, [
      el("button", {
        type: "button",
        className: "md-icon-btn",
        id: "sidebarToggle",
        title: "页单收起",
        "aria-label": "页单收起",
        on: {
          click: function () {
            setSidebar(!sidebarOpen);
          },
        },
      }, [icon("menu")]),
      el("button", {
        type: "button",
        className: "md-icon-btn",
        id: "statePanelToggle",
        title: "状态演示",
        "aria-label": "状态演示",
        on: {
          click: function () {
            setStatePanel(!statePanelOpen);
          },
        },
      }, [icon("tune")]),
      el("div", { className: "proto-appbar__title", id: "protoTitle", text: "" }),
      mapLink,
      el("button", {
        type: "button",
        className: "md-btn md-btn--text",
        text: "规格说明",
        on: {
          click: function () {
            setDrawer(!drawerOpen);
          },
        },
      }),
    ]);

    var previewInner;
    if (mode === "mobile") {
      previewInner = el("div", { className: "phone-scale-host" }, [
        el("div", { className: "phone-frame" }, [
          el("iframe", { id: "previewFrame", title: "页面原型预览" }),
          el("div", { className: "phone-home-bar" }),
        ]),
      ]);
    } else {
      previewInner = el("iframe", {
        id: "previewFrame",
        className: "preview-frame",
        title: "页面原型预览",
      });
    }

    var content = el("div", { className: "proto-content" }, [
      el("aside", { id: "statePanel", className: "proto-state" }),
      el("div", { className: "preview-area" }, [previewInner]),
    ]);

    var main = el("div", { className: "proto-main" }, [appbar, content]);
    var backdrop = el("div", {
      id: "specBackdrop",
      className: "proto-drawer-backdrop",
      on: {
        click: function () {
          setDrawer(false);
        },
      },
    });
    var drawer = el("aside", { id: "specDrawer", className: "proto-drawer" }, [
      el("div", { className: "proto-drawer__head" }, [
        el("h2", { text: "规格说明" }),
        el("button", {
          type: "button",
          className: "md-icon-btn",
          "aria-label": "关闭",
          on: {
            click: function () {
              setDrawer(false);
            },
          },
        }, [icon("close")]),
      ]),
      el("div", { id: "specDrawerBody", className: "proto-drawer__body" }),
    ]);

    root.innerHTML = "";
    root.appendChild(sidebar);
    root.appendChild(main);
    root.appendChild(backdrop);
    root.appendChild(drawer);
    mountSkillCredit();

    loadPage(currentId);
    window.addEventListener("resize", window.fitPhoneFrame);
    if (mode === "mobile") setTimeout(window.fitPhoneFrame, 0);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
