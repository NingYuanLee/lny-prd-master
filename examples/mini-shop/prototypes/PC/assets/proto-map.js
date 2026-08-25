/* -*- coding: utf-8 -*- */
/* LNY-PRD map canvas: phone-ratio nodes, localStorage layout, PNG export. */
(function (global) {
  "use strict";

  var PHONE_W = 375;
  var PHONE_H = 812;
  var NODE_W = 200;
  var SAVE_MS = 300;
  var PAD = 48;
  var EDGE_PAD = 28;
  var LANE_GAP = 32;
  var STYLE = {
    forward: { stroke: "#3fb950", dash: "", width: 2, arrow: true, name: "跳转" },
    back: { stroke: "#8b949e", dash: "6 4", width: 1.5, arrow: true, name: "返回" },
    tab: { stroke: "#58a6ff", dash: "8 4", width: 2, arrow: true, name: "TabBar" },
    embed: { stroke: "#d2a8ff", dash: "2 4", width: 1.5, arrow: false, name: "嵌入" }
  };
  var SIDE_NORMAL = {
    left: { x: -1, y: 0 },
    right: { x: 1, y: 0 },
    top: { x: 0, y: -1 },
    bottom: { x: 0, y: 1 }
  };
  var SIDE_TANGENT = {
    left: { x: 0, y: 1 },
    right: { x: 0, y: 1 },
    top: { x: 1, y: 0 },
    bottom: { x: 1, y: 0 }
  };

  /** Directory URL of current page (always ends with /). */
  function dirHref() {
    var path = location.pathname;
    if (/\.html?$/i.test(path)) path = path.replace(/\/[^/]*$/, "/");
    else if (!path.endsWith("/")) path += "/";
    return location.origin + path;
  }

  /** Resolve local relative URLs against the page directory. */
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

  function clonePages(list) {
    return (list || []).map(function (p) {
      return {
        id: p.id,
        name: p.name,
        module: p.module || "",
        file: p.file,
        x: p.x,
        y: p.y
      };
    });
  }

  function thumbH(nodeW, phoneW, phoneH) {
    return Math.round(nodeW * phoneH / phoneW);
  }

  function todayStamp() {
    var d = new Date();
    var m = d.getMonth() + 1;
    var day = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
  }

  function toast(msg) {
    var el = document.getElementById("proto-map-toast");
    if (!el) {
      el = document.createElement("div");
      el.id = "proto-map-toast";
      el.className = "proto-map-toast";
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.classList.add("is-on");
    clearTimeout(toast._t);
    toast._t = setTimeout(function () {
      el.classList.remove("is-on");
    }, 1600);
  }

  function roundRect(ctx, x, y, w, h, r) {
    var rr = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + rr, y);
    ctx.arcTo(x + w, y, x + w, y + h, rr);
    ctx.arcTo(x + w, y + h, x, y + h, rr);
    ctx.arcTo(x, y + h, x, y, rr);
    ctx.arcTo(x, y, x + w, y, rr);
    ctx.closePath();
  }

  function pairKey(a, b) {
    return a < b ? a + ">" + b : b + ">" + a;
  }

  function linkLabel(lk) {
    if (lk.label) return String(lk.label);
    var st = STYLE[lk.type];
    return st ? st.name : "";
  }

  function bezierPoint(p1, c1, c2, p2, t) {
    var u = 1 - t;
    return {
      x: u * u * u * p1.x + 3 * u * u * t * c1.x + 3 * u * t * t * c2.x + t * t * t * p2.x,
      y: u * u * u * p1.y + 3 * u * u * t * c1.y + 3 * u * t * t * c2.y + t * t * t * p2.y
    };
  }

  function bezierTangent(p1, c1, c2, p2, t) {
    var u = 1 - t;
    return {
      x: 3 * u * u * (c1.x - p1.x) + 6 * u * t * (c2.x - c1.x) + 3 * t * t * (p2.x - c2.x),
      y: 3 * u * u * (c1.y - p1.y) + 6 * u * t * (c2.y - c1.y) + 3 * t * t * (p2.y - c2.y)
    };
  }

  function ProtoMap() {}

  ProtoMap.boot = function (opts) {
    opts = opts || {};
    var pages = clonePages(opts.pages || global.PAGES);
    var defaults = clonePages(pages);
    var links = (opts.links || global.LINKS || []).slice();
    var phoneW = opts.phoneW || PHONE_W;
    var phoneH = opts.phoneH || PHONE_H;
    var nodeW = opts.nodeW || NODE_W;
    var previewH = thumbH(nodeW, phoneW, phoneH);
    var terminal = opts.terminal || "MP";
    var project = opts.project || "prd";
    var storageKey = opts.storageKey || project + "-" + terminal + "-map-layout-v1";
    var scale = 1;
    var panX = 40;
    var panY = 20;
    var saveTimer = null;
    var world = document.getElementById("world");
    var svg = document.getElementById("connections");
    var viewport = document.getElementById("viewport");
    var shell = document.getElementById("map-shell");
    if (!world || !svg || !viewport) return;
    document.documentElement.style.height = "100%";
    document.body.style.height = "100%";
    document.body.style.margin = "0";

    document.documentElement.style.setProperty("--map-node-w", nodeW + "px");
    document.documentElement.style.setProperty("--map-phone-w", phoneW + "px");
    document.documentElement.style.setProperty("--map-phone-h", phoneH + "px");
    document.documentElement.style.setProperty("--map-thumb-h", previewH + "px");
    document.documentElement.style.setProperty("--map-thumb-scale", String(nodeW / phoneW));

    function pageMap() {
      var m = {};
      pages.forEach(function (p) {
        m[p.id] = p;
      });
      return m;
    }

    function getNodeBox(p) {
      var n = world.querySelector('.page-node[data-id="' + p.id + '"]');
      if (n) {
        return { x: p.x, y: p.y, w: n.offsetWidth, h: n.offsetHeight };
      }
      return { x: p.x, y: p.y, w: nodeW, h: 64 + previewH };
    }

    function rectCenter(b) {
      return { x: b.x + b.w / 2, y: b.y + b.h / 2 };
    }

    function dominantSide(box, toward) {
      var c = rectCenter(box);
      var dx = toward.x - c.x;
      var dy = toward.y - c.y;
      if (Math.abs(dx) * box.h >= Math.abs(dy) * box.w) {
        return dx >= 0 ? "right" : "left";
      }
      return dy >= 0 ? "bottom" : "top";
    }

    function pointOnSide(box, side, t) {
      var spanV = Math.max(1, box.h - EDGE_PAD * 2);
      var spanH = Math.max(1, box.w - EDGE_PAD * 2);
      t = Math.max(0.08, Math.min(0.92, t));
      if (side === "right") return { x: box.x + box.w, y: box.y + EDGE_PAD + t * spanV };
      if (side === "left") return { x: box.x, y: box.y + EDGE_PAD + t * spanV };
      if (side === "top") return { x: box.x + EDGE_PAD + t * spanH, y: box.y };
      return { x: box.x + EDGE_PAD + t * spanH, y: box.y + box.h };
    }

    function layoutRoutes() {
      var m = pageMap();
      var routes = [];
      links.forEach(function (lk, i) {
        var a = m[lk.from];
        var b = m[lk.to];
        if (!a || !b) return;
        var ba = getNodeBox(a);
        var bb = getNodeBox(b);
        var ca = rectCenter(ba);
        var cb = rectCenter(bb);
        routes.push({
          i: i,
          lk: lk,
          ba: ba,
          bb: bb,
          ca: ca,
          cb: cb,
          sideA: dominantSide(ba, cb),
          sideB: dominantSide(bb, ca)
        });
      });
      var groups = {};
      function addEnd(r, end) {
        var nodeId = end === "a" ? r.lk.from : r.lk.to;
        var side = end === "a" ? r.sideA : r.sideB;
        var k = nodeId + "|" + side;
        (groups[k] = groups[k] || []).push({ r: r, end: end });
      }
      routes.forEach(function (r) {
        addEnd(r, "a");
        addEnd(r, "b");
      });
      Object.keys(groups).forEach(function (k) {
        var side = k.split("|")[1];
        var items = groups[k];
        var vert = side === "left" || side === "right";
        items.sort(function (u, v) {
          var ou = u.end === "a" ? u.r.cb : u.r.ca;
          var ov = v.end === "a" ? v.r.cb : v.r.ca;
          var d = vert ? ou.y - ov.y : ou.x - ov.x;
          if (d) return d;
          var pu = pairKey(u.r.lk.from, u.r.lk.to);
          var pv = pairKey(v.r.lk.from, v.r.lk.to);
          if (pu !== pv) return pu < pv ? -1 : 1;
          return u.r.i - v.r.i;
        });
        items.forEach(function (item, idx) {
          var t = (idx + 1) / (items.length + 1);
          if (item.end === "a") item.r.tA = t;
          else item.r.tB = t;
        });
      });
      var pairCounts = {};
      var pairSeen = {};
      routes.forEach(function (r) {
        var k = pairKey(r.lk.from, r.lk.to);
        pairCounts[k] = (pairCounts[k] || 0) + 1;
      });
      routes.forEach(function (r) {
        var k = pairKey(r.lk.from, r.lk.to);
        pairSeen[k] = (pairSeen[k] || 0) + 1;
        r.lane = pairSeen[k] - 1;
        r.lanes = pairCounts[k];
        r.curve = curveFor(r);
      });
      return routes;
    }

    function curveFor(r) {
      var p1 = pointOnSide(r.ba, r.sideA, r.tA);
      var p2 = pointOnSide(r.bb, r.sideB, r.tB);
      var n1 = SIDE_NORMAL[r.sideA];
      var n2 = SIDE_NORMAL[r.sideB];
      var t1 = SIDE_TANGENT[r.sideA];
      var t2 = SIDE_TANGENT[r.sideB];
      var dist = Math.hypot(p2.x - p1.x, p2.y - p1.y) || 1;
      var reach = Math.min(96, Math.max(40, dist * 0.38));
      var bulge = r.lanes > 1 ? (r.lane - (r.lanes - 1) / 2) * LANE_GAP : 0;
      return {
        p1: p1,
        p2: p2,
        c1: { x: p1.x + n1.x * reach + t1.x * bulge, y: p1.y + n1.y * reach + t1.y * bulge },
        c2: { x: p2.x + n2.x * reach + t2.x * bulge, y: p2.y + n2.y * reach + t2.y * bulge }
      };
    }

    function labelPose(cv) {
      var pt = bezierPoint(cv.p1, cv.c1, cv.c2, cv.p2, 0.5);
      var tg = bezierTangent(cv.p1, cv.c1, cv.c2, cv.p2, 0.5);
      var len = Math.hypot(tg.x, tg.y) || 1;
      var nx = -tg.y / len;
      var ny = tg.x / len;
      if (ny > 0) {
        nx = -nx;
        ny = -ny;
      }
      var ang = (Math.atan2(tg.y, tg.x) * 180) / Math.PI;
      if (ang > 90 || ang < -90) ang += 180;
      return { x: pt.x + nx * 10, y: pt.y + ny * 10, ang: ang };
    }

    function applyTransform() {
      world.style.transform = "translate(" + panX + "px," + panY + "px) scale(" + scale + ")";
    }

    function scheduleSave() {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(persist, SAVE_MS);
    }

    function persist() {
      var payload = {
        v: 1,
        pages: pages.map(function (p) {
          return { id: p.id, x: p.x, y: p.y };
        }),
        viewport: { scale: scale, panX: panX, panY: panY }
      };
      try {
        localStorage.setItem(storageKey, JSON.stringify(payload));
      } catch (err) {}
    }

    function restore() {
      var raw;
      try {
        raw = localStorage.getItem(storageKey);
      } catch (err) {
        return;
      }
      if (!raw) return;
      var data;
      try {
        data = JSON.parse(raw);
      } catch (err2) {
        return;
      }
      var byId = {};
      (data.pages || []).forEach(function (p) {
        if (p && p.id) byId[p.id] = p;
      });
      pages.forEach(function (p) {
        var s = byId[p.id];
        if (!s) return;
        if (typeof s.x === "number") p.x = s.x;
        if (typeof s.y === "number") p.y = s.y;
      });
      if (data.viewport) {
        if (typeof data.viewport.scale === "number") scale = data.viewport.scale;
        if (typeof data.viewport.panX === "number") panX = data.viewport.panX;
        if (typeof data.viewport.panY === "number") panY = data.viewport.panY;
        scale = Math.min(2.5, Math.max(0.15, scale));
      }
    }

    function ensureMarkers() {
      var defs = svg.querySelector("defs");
      if (defs) return;
      defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
      Object.keys(STYLE).forEach(function (k) {
        if (!STYLE[k].arrow) return;
        var mk = document.createElementNS("http://www.w3.org/2000/svg", "marker");
        mk.setAttribute("id", "arr-" + k);
        mk.setAttribute("viewBox", "0 0 10 10");
        mk.setAttribute("refX", "9");
        mk.setAttribute("refY", "5");
        mk.setAttribute("markerWidth", "7");
        mk.setAttribute("markerHeight", "7");
        mk.setAttribute("orient", "auto");
        var p = document.createElementNS("http://www.w3.org/2000/svg", "path");
        p.setAttribute("d", "M0 0 L10 5 L0 10 z");
        p.setAttribute("fill", STYLE[k].stroke);
        mk.appendChild(p);
        defs.appendChild(mk);
      });
      svg.appendChild(defs);
    }

    function drawConnections() {
      svg.innerHTML = "";
      ensureMarkers();
      layoutRoutes().forEach(function (r) {
        var st = STYLE[r.lk.type] || STYLE.forward;
        var cv = r.curve;
        var typeKey = STYLE[r.lk.type] ? r.lk.type : "forward";
        var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute(
          "d",
          "M" + cv.p1.x + " " + cv.p1.y + " C" + cv.c1.x + " " + cv.c1.y + " " + cv.c2.x + " " + cv.c2.y + " " + cv.p2.x + " " + cv.p2.y
        );
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", st.stroke);
        path.setAttribute("stroke-width", st.width);
        if (st.dash) path.setAttribute("stroke-dasharray", st.dash);
        if (st.arrow) path.setAttribute("marker-end", "url(#arr-" + typeKey + ")");
        g.appendChild(path);
        var text = linkLabel(r.lk);
        if (text) {
          var pose = labelPose(cv);
          var el = document.createElementNS("http://www.w3.org/2000/svg", "text");
          el.setAttribute("class", "map-link-label");
          el.setAttribute("fill", st.stroke);
          el.setAttribute("text-anchor", "middle");
          el.setAttribute("dominant-baseline", "central");
          el.setAttribute("transform", "translate(" + pose.x + " " + pose.y + ") rotate(" + pose.ang + ")");
          el.textContent = text;
          g.appendChild(el);
        }
        svg.appendChild(g);
      });
      var bounds = getContentBounds();
      svg.setAttribute("width", String(Math.max(2000, bounds.maxX + 200)));
      svg.setAttribute("height", String(Math.max(2000, bounds.maxY + 200)));
    }

    function sampleLineSvg(type) {
      var st = STYLE[type];
      var dash = st.dash ? ' stroke-dasharray="' + st.dash + '"' : "";
      var arrow = st.arrow
        ? '<polygon points="46,3.5 54,7 46,10.5" fill="' + st.stroke + '"/>'
        : "";
      var x2 = st.arrow ? 46 : 54;
      return (
        '<svg width="56" height="14" viewBox="0 0 56 14" aria-hidden="true">' +
        '<line x1="2" y1="7" x2="' +
        x2 +
        '" y2="7" fill="none" stroke="' +
        st.stroke +
        '" stroke-width="' +
        st.width +
        '"' +
        dash +
        "/>" +
        arrow +
        "</svg>"
      );
    }

    function renderLegend() {
      var stale = document.querySelector(".map-hint");
      if (stale) stale.parentNode.removeChild(stale);
      var host = document.getElementById("map-legend");
      if (!host) {
        host = document.createElement("div");
        host.id = "map-legend";
        (shell || document.body).appendChild(host);
      }
      host.className = "map-legend";
      var used = {};
      links.forEach(function (lk) {
        if (STYLE[lk.type]) used[lk.type] = true;
      });
      var order = ["forward", "back", "tab", "embed"];
      var types = order.filter(function (k) {
        return used[k];
      });
      if (!types.length) types = order.slice();
      var items = types
        .map(function (k) {
          return (
            '<span class="map-legend__item">' +
            sampleLineSvg(k) +
            "<span>" +
            STYLE[k].name +
            "</span></span>"
          );
        })
        .join("");
      host.innerHTML =
        '<div class="map-legend__ops">拖标题栏移动页面块（写入缓存）；拖空白处平移，滚轮缩放。</div>' +
        '<div class="map-legend__items">' +
        items +
        "</div>";
    }

    function createNodes() {
      world.querySelectorAll(".page-node").forEach(function (n) {
        n.parentNode.removeChild(n);
      });
      pages.forEach(function (p) {
        var n = document.createElement("div");
        n.className = "page-node";
        n.dataset.id = p.id;
        n.style.left = p.x + "px";
        n.style.top = p.y + "px";
        n.innerHTML =
          '<div class="node-header">' +
          '<div class="node-id"></div>' +
          '<div class="node-name"></div>' +
          '<div class="md-caption node-mod"></div>' +
          "</div>" +
          '<div class="phone-wrap">' +
          '<iframe loading="lazy"></iframe>' +
          '<div class="phone-overlay"></div>' +
          "</div>";
        n.querySelector(".node-id").textContent = p.id;
        n.querySelector(".node-name").textContent = p.name;
        n.querySelector(".node-mod").textContent = p.module || "";
        var frame = n.querySelector("iframe");
        frame.src = relUrl(p.file);
        frame.title = p.id;
        n.querySelector(".phone-overlay").addEventListener("click", function () {
          window.open(relUrl(p.file), "_blank");
        });
        n.querySelector(".node-header").addEventListener("mousedown", function (ev) {
          ev.preventDefault();
          ev.stopPropagation();
          var sx = ev.clientX;
          var sy = ev.clientY;
          var ox = p.x;
          var oy = p.y;
          function move(e) {
            p.x = ox + (e.clientX - sx) / scale;
            p.y = oy + (e.clientY - sy) / scale;
            n.style.left = p.x + "px";
            n.style.top = p.y + "px";
            drawConnections();
            scheduleSave();
          }
          function up() {
            document.removeEventListener("mousemove", move);
            document.removeEventListener("mouseup", up);
            persist();
          }
          document.addEventListener("mousemove", move);
          document.addEventListener("mouseup", up);
        });
        world.appendChild(n);
      });
    }

    function getContentBounds() {
      var minX = Infinity;
      var minY = Infinity;
      var maxX = -Infinity;
      var maxY = -Infinity;
      pages.forEach(function (p) {
        var b = getNodeBox(p);
        minX = Math.min(minX, b.x);
        minY = Math.min(minY, b.y);
        maxX = Math.max(maxX, b.x + b.w);
        maxY = Math.max(maxY, b.y + b.h);
      });
      if (!isFinite(minX)) {
        return { minX: 0, minY: 0, maxX: 400, maxY: 400 };
      }
      return { minX: minX, minY: minY, maxX: maxX, maxY: maxY };
    }

    function fitAll() {
      var b = getContentBounds();
      var bw = Math.max(1, b.maxX - b.minX);
      var bh = Math.max(1, b.maxY - b.minY);
      var sx = (viewport.clientWidth - PAD * 2) / bw;
      var sy = (viewport.clientHeight - PAD * 2) / bh;
      scale = Math.min(2.5, Math.max(0.15, Math.min(sx, sy, 1)));
      panX = (viewport.clientWidth - bw * scale) / 2 - b.minX * scale;
      panY = (viewport.clientHeight - bh * scale) / 2 - b.minY * scale;
      applyTransform();
      persist();
    }

    function zoomAt(clientX, clientY, next) {
      var rect = viewport.getBoundingClientRect();
      var x = clientX - rect.left;
      var y = clientY - rect.top;
      var wx = (x - panX) / scale;
      var wy = (y - panY) / scale;
      scale = Math.min(2.5, Math.max(0.15, next));
      panX = x - wx * scale;
      panY = y - wy * scale;
      applyTransform();
      scheduleSave();
    }

    function resetLayout() {
      var byId = {};
      defaults.forEach(function (p) {
        byId[p.id] = p;
      });
      pages.forEach(function (p) {
        var d = byId[p.id];
        if (!d) return;
        p.x = d.x;
        p.y = d.y;
      });
      world.querySelectorAll(".page-node").forEach(function (n) {
        var p = pageMap()[n.dataset.id];
        if (!p) return;
        n.style.left = p.x + "px";
        n.style.top = p.y + "px";
      });
      scale = 1;
      panX = 40;
      panY = 20;
      applyTransform();
      drawConnections();
      try {
        localStorage.removeItem(storageKey);
      } catch (err) {}
      toast("已恢复默认布局");
    }

    function exportCanvasImage() {
      toast("正在生成图片…");
      var b = getContentBounds();
      var w = Math.ceil(b.maxX - b.minX + PAD * 2);
      var h = Math.ceil(b.maxY - b.minY + PAD * 2);
      var dpr = 2;
      var canvas = document.createElement("canvas");
      canvas.width = Math.max(1, w * dpr);
      canvas.height = Math.max(1, h * dpr);
      var ctx = canvas.getContext("2d");
      ctx.scale(dpr, dpr);
      ctx.fillStyle = "#f5f5f5";
      ctx.fillRect(0, 0, w, h);
      var ox = PAD - b.minX;
      var oy = PAD - b.minY;
      layoutRoutes().forEach(function (r) {
        var st = STYLE[r.lk.type] || STYLE.forward;
        var cv = r.curve;
        ctx.beginPath();
        ctx.strokeStyle = st.stroke;
        ctx.lineWidth = st.width;
        if (st.dash) {
          ctx.setLineDash(
            st.dash.split(/\s+/).map(function (v) {
              return Number(v);
            })
          );
        } else {
          ctx.setLineDash([]);
        }
        ctx.moveTo(cv.p1.x + ox, cv.p1.y + oy);
        ctx.bezierCurveTo(
          cv.c1.x + ox,
          cv.c1.y + oy,
          cv.c2.x + ox,
          cv.c2.y + oy,
          cv.p2.x + ox,
          cv.p2.y + oy
        );
        ctx.stroke();
        var text = linkLabel(r.lk);
        if (!text) return;
        var pose = labelPose(cv);
        ctx.save();
        ctx.setLineDash([]);
        ctx.translate(pose.x + ox, pose.y + oy);
        ctx.rotate((pose.ang * Math.PI) / 180);
        ctx.font = "12px Roboto, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.lineWidth = 4;
        ctx.strokeStyle = "#f5f5f5";
        ctx.strokeText(text, 0, 0);
        ctx.fillStyle = st.stroke;
        ctx.fillText(text, 0, 0);
        ctx.restore();
      });
      ctx.setLineDash([]);
      pages.forEach(function (p) {
        var box = getNodeBox(p);
        var x = box.x + ox;
        var y = box.y + oy;
        ctx.fillStyle = "#fff";
        ctx.strokeStyle = "rgba(0,0,0,0.12)";
        ctx.lineWidth = 1;
        roundRect(ctx, x, y, box.w, box.h, 4);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = "rgba(0,0,0,0.6)";
        ctx.font = "12px Roboto, sans-serif";
        ctx.textAlign = "left";
        ctx.textBaseline = "alphabetic";
        ctx.fillText(p.id, x + 12, y + 18);
        ctx.fillStyle = "rgba(0,0,0,0.87)";
        ctx.font = "500 16px Roboto, sans-serif";
        ctx.fillText(p.name, x + 12, y + 38);
        var thumbY = y + 56;
        var thumbHgt = Math.max(40, box.h - 56);
        ctx.fillStyle = "#eceff1";
        ctx.fillRect(x, thumbY, box.w, thumbHgt);
        var innerW = box.w - 16;
        var innerH = (innerW * phoneH) / phoneW;
        if (innerH > thumbHgt - 16) {
          innerH = thumbHgt - 16;
          innerW = (innerH * phoneW) / phoneH;
        }
        var ix = x + (box.w - innerW) / 2;
        var iy = thumbY + (thumbHgt - innerH) / 2;
        ctx.fillStyle = "#fff";
        ctx.strokeStyle = "#cfd8dc";
        roundRect(ctx, ix, iy, innerW, innerH, 8);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = "rgba(0,0,0,0.54)";
        ctx.font = "12px Roboto, sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(p.id, ix + innerW / 2, iy + innerH / 2);
        ctx.textAlign = "left";
      });
      var name = terminal + "-map-" + todayStamp() + ".png";
      function done() {
        toast("已导出 " + name);
      }
      if (canvas.toBlob) {
        canvas.toBlob(function (blob) {
          if (!blob) return;
          var a = document.createElement("a");
          a.href = URL.createObjectURL(blob);
          a.download = name;
          a.click();
          setTimeout(function () {
            URL.revokeObjectURL(a.href);
          }, 2000);
          done();
        });
      } else {
        var a = document.createElement("a");
        a.href = canvas.toDataURL("image/png");
        a.download = name;
        a.click();
        done();
      }
    }

    function updateFullscreenButton() {
      var btn = document.getElementById("btnFull");
      if (!btn) return;
      var on = !!(document.fullscreenElement || document.webkitFullscreenElement);
      btn.textContent = on ? "退出全屏" : "全屏";
    }

    function toggleFullscreen() {
      var el = shell || document.documentElement;
      var on = document.fullscreenElement || document.webkitFullscreenElement;
      if (on) {
        if (document.exitFullscreen) document.exitFullscreen();
        else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
        return;
      }
      var req = el.requestFullscreen || el.webkitRequestFullscreen;
      if (!req) {
        toast("当前浏览器不支持全屏");
        return;
      }
      req.call(el).catch(function () {
        toast("当前浏览器不支持全屏");
      });
    }

    restore();
    ensureMarkers();
    createNodes();
    drawConnections();
    renderLegend();
    applyTransform();

    viewport.addEventListener("mousedown", function (ev) {
      if (ev.target !== viewport && ev.target !== world && ev.target !== svg) return;
      var sx = ev.clientX;
      var sy = ev.clientY;
      var ox = panX;
      var oy = panY;
      viewport.style.cursor = "grabbing";
      function move(e) {
        panX = ox + (e.clientX - sx);
        panY = oy + (e.clientY - sy);
        applyTransform();
      }
      function up() {
        viewport.style.cursor = "";
        document.removeEventListener("mousemove", move);
        document.removeEventListener("mouseup", up);
        persist();
      }
      document.addEventListener("mousemove", move);
      document.addEventListener("mouseup", up);
    });

    viewport.addEventListener(
      "wheel",
      function (ev) {
        ev.preventDefault();
        zoomAt(ev.clientX, ev.clientY, scale * (ev.deltaY > 0 ? 0.9 : 1.1));
      },
      { passive: false }
    );

    var btnFit = document.getElementById("btnFit");
    if (btnFit) btnFit.addEventListener("click", fitAll);
    var btnReset = document.getElementById("btnReset");
    if (btnReset) btnReset.addEventListener("click", resetLayout);
    var btnExport = document.getElementById("btnExport");
    if (btnExport) btnExport.addEventListener("click", exportCanvasImage);
    var btnFull = document.getElementById("btnFull");
    if (btnFull) btnFull.addEventListener("click", toggleFullscreen);
    document.addEventListener("fullscreenchange", updateFullscreenButton);
    document.addEventListener("webkitfullscreenchange", updateFullscreenButton);
    document.addEventListener("keydown", function (ev) {
      var tag = (ev.target && ev.target.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (ev.key === "f" || ev.key === "F") {
        ev.preventDefault();
        toggleFullscreen();
      }
    });
    updateFullscreenButton();

    global.ProtoMap = ProtoMap;
    ProtoMap.exportCanvasImage = exportCanvasImage;
    ProtoMap.fitAll = fitAll;
    ProtoMap.resetLayout = resetLayout;
    ProtoMap.toggleFullscreen = toggleFullscreen;
  };

  global.ProtoMap = ProtoMap;
})(window);
