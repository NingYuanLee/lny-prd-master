# 原型写盘与 BUG 预防（§F–G）

### F. 中文 UTF-8 写盘纪律（必做，防乱码）

乱码是写盘方式问题。写后跑验收，失败则整文件重写。

#### F.1 根因与正确写盘

| 现象 | 根因 | 正确做法 | 禁止 |
|------|------|---------|------|
| 页面出现 `?`/半拉中文 | StrReplace 破坏 UTF-8 多字节中文 | 整文件 UTF-8 写入；仅改 ASCII 可用 StrReplace | StrReplace 含 CJK / >3 行区块 |
| `UnicodeDecodeError: invalid continuation byte` | 文件已是无效 UTF-8 | 从同端已验收页复制再改 | `read_text(errors='replace')` 后写回 |
| PowerShell `python -c` 失败 | Windows GBK 与 UTF-8 混用 | 中文写在 `.py` 源码内（`# -*- coding: utf-8 -*-`） | `python -c "…中文…"` / Shell heredoc |
| 原型镜像不一致 | 对主路径和镜像分次 StrReplace | 同时写 `prototypes/` + `versions/.../prototypes/`，或 `shutil.copy2` | 对两路径分别 StrReplace |

#### F.2 写后验收（必做）

```bash
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/MP/PAGE-MP-010.html <prdRoot>/versions/v1.0.0/prototypes/MP/PAGE-MP-010.html
```

exit 0 才可继续；exit 1 不得交付，按 F.1 整文件重写。禁止未跑验收就汇报「已更新」；禁止把 `repair-*` 当常规步骤。

### G. 原型 BUG 预防规则（必守）

交付前消除已知 BUG。

#### G.1 代码变更引用检查（必做）

删除或重命名函数/变量/类/id/DOM 前，先全文件搜索引用并修复：

| 变更类型 | 须搜索 |
|---------|--------|
| 删除函数 `foo()` | `foo(` |
| 删除变量/类/id | 单词边界；`getElementById` |
| `<script src>` | 须有对应 `</script>`；Network 200；Console 无 ReferenceError |
| 新增全局调用 | `assets/` 下确有 `var XXX` / `global.XXX`；禁止凭记忆写 `ProtoApiClient` |
| 壳层菜单超出视口 | `.proto-sidebar__nav` 有 `overflow-y: auto` |

#### G.2 状态演示按钮归位（必做）

规则见 [`reference-shell.md`](reference-shell.md) 状态演示。搜索 `demo-` / `setDemo` / `mock-` / `alert('原型`；模拟后端 → 移入状态演示；用户操作保留。状态演示用套件 `.md-toggle`。

#### G.3 自检清单（逐页过）

| 序号 | 检查项 | 通过标准 |
|------|--------|---------|
| G3.1 | JS 控制台 | 无红色报错 |
| G3.2 | 渲染完整 | 无意外 `display:none` |
| G3.3 | 演示按钮归位 | 无后端模拟用的 `demo-*` / `setDemo*` |
| G3.4 | 状态演示选项 | 与 `ui/COMP-*.md` 状态矩阵逐字一致 |
| G3.5 | 链接可操作 | `href` / `location.href` / `postMessage` 有效 |
| G3.6 | UTF-8 | `verify-prototype-utf8.py` exit 0 |
| G3.7 | 版本演示标记 | 无 `v{版}` 开头的演示 id |
| G3.8 | alert 桩位 | 无 `alert('原型：…')`；接口模拟须标 `// 接口桩位-待接入` |
| G3.9 | 无重复监听 | 同一操作无全局 click + 局部 onclick 两套 |
| G3.10 | script 闭合 | 外部脚本均有 `</script>` |
| G3.11 | 全局变量存在 | `assets/` 有定义；`rg "ProtoApiClient" prototypes/` 为 0 |
| G3.12 | 侧栏可滚动 | `.proto-sidebar__nav` `overflow-y: auto` |
| G3.13 | 套件引用 | `mui-kit.css` + `md-icons.js` + `icons-extra.js`；index 另引 shell；无 `prototypes-mui-app/`；无自造主题 |
| G3.14 | 业务图标 | `data-icon` 属闭集或 extras 已 register；无手绘 path；未调 Cursor iconfont MCP |
