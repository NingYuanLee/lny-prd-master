# 原型图标

生成/更新原型时 Read。**禁止**调用 Cursor 的 `user-search-iconfont-mcp`；搜图用技能包脚本（与 MCP 打同一 iconfont 接口，随技能分发、无需再配 MCP）。

## 两层

1. **套件闭集**（离线）：`kit/md-icons.js` 常用 Material 图标。`data-icon="home"` / `data-icon="搜索"`。
2. **按需检索**：规格要的图标不在闭集时，跑 `scripts/search-icons.py`（先查套件，没有再 POST `iconfont.cn/api/icon/search.json`，不登录）。命中后写入该端 `assets/icons-extra.js`，页面同样 `data-icon`。

脚本失败（无网/接口变）→ 用闭集近义项，**不中止⑥**。

## 引用顺序

```html
<script src="./assets/md-icons.js"></script>
<script src="./assets/icons-extra.js"></script>
<script src="./assets/proto-page.js"></script>
```

`index.html` 在 `proto-shell.js` 前同样先引 `md-icons.js` + `icons-extra.js`。`copy-kit.py` 会补空的 `icons-extra.js`，已有内容不覆盖。

```html
<span class="md-icon" data-icon="home" aria-hidden="true"></span>
<span class="md-icon" data-icon="kefu" aria-hidden="true"></span>
```

删除操作用 `md-icon--danger`。禁止手绘 path、emoji、外链图标字体。

## 检索

```text
python <skillDir>/scripts/search-icons.py --list-kit
python <skillDir>/scripts/search-icons.py 客服 --type fill --size 8
python <skillDir>/scripts/search-icons.py 客服 --pick 0 --name kefu --out <prdRoot>/prototypes/{终端}/assets
```

`--pick 0` 装第一条；或 `--id {iconfont数字id}`。`--name` 须 ASCII（`kefu`）。`--local-only` 只查套件。

装入后 HTML 用 `data-icon="kefu"`（或中文名若已作 alias）。镜像 `versions/` 时带上 `icons-extra.js` 与 `assets/icons/`。

## 套件闭集（优先用这些，不必上网）

| id | 中文别名 | 典型位置 |
|----|----------|----------|
| home | 首页、主页 | TabBar |
| goods | 商品、购物袋 | TabBar |
| cart | 购物车 | TabBar |
| person | 用户、我的、个人 | TabBar |
| category | 分类 | TabBar |
| settings | 设置 | 设置页 |
| search | 搜索 | 顶栏 / 搜索栏 |
| schedule | 时间 / 时钟 | 列表元信息 |
| favorite | 点赞 / 喜欢 | 列表元信息 |
| view | 查看 / 浏览 | 列表元信息 / 详情 |
| filter | 筛选 | 工具栏 |
| add | 添加、新增 | 功能栏 / 操作列 |
| edit | 编辑 | 操作列（图标钮） |
| delete | 删除 | 操作列（图标钮，可加 `md-icon--danger`） |
| view | 查看、详情、浏览 | 操作列（图标钮） / 列表元信息 |
| enable | 启用、开启 | 操作列（图标钮） |
| disable | 停用、禁用 | 操作列（图标钮） |
| copy | 复制 | 操作列 |
| refresh | 刷新 | 工具栏 |
| more | 更多 | 操作列溢出 / 顶栏 |
| check | 成功 | 状态 |
| error | 失败、错误 | 状态 |
| warning | 警告 | 状态 |
| info | 信息 | 状态 |
| empty | 空、空态 | 空态 |
| star | 收藏 | 内容 |
| image | 图片 | 占位 |
| mail | 邮件 | 联系 |
| share | 分享 | 工具栏 |
| menu | 菜单 | 壳层页单 |
| tune | — | 壳层状态演示 |
| close | 关闭 | 规格说明 |
| chevron-left / chevron-right | — | 分页 |
| arrow-up | 返回顶部、向上 | 详情页悬浮导航 |
| unfold | 全部展开 | 树总控 |
| fold | 全部收起 | 树总控 |

同一终端本批风格统一：检索默认 `--type fill`。禁止 fill/line 混用。
