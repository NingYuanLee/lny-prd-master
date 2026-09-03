# UI设计清单 - Mini Shop

## 文档信息

| 属性 | 内容 |
|------|------|
| 文档版本 | v1.0.0 |
| 创建日期 | 2026-08-13 |
| 最后更新 | 2026-08-13 |
| 维护人 | UI设计师 |
| 状态 | 草稿 |

### 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.0.0 | 2026-08-13 | 初始版本 | UI设计师 |

## 1. 阅读说明与清单结构约定

本文件仅维护 §2～§4 索引与 §5 全局说明。页面/组件详述落在 `ui/PAGE-*.md`、`ui/COMP-*.md`。

## 2. UI 框架（按终端，与 `main_spec.md` → 第4章终端说明 一致）

| 终端名称 | 类型编码 | UI 框架名称 | 官方文档或主页 URL |
|----------|----------|-------------|-------------------|
| 微信小程序 | MP | 无 | 无 |
| 管理后台 | AD | 无 | 无 |

## 3. 页面索引清单

> 页面分组服务于人可读的信息架构，不等同于 `feature_spec.md` 的 `MODULE-*` 领域模块。

### 3.1 页面分组注册

#### 3.1.1 小程序主包/分包与 TabBar（MP）

| 包类型 | 包模块 | 路径前缀 |
|--------|--------|----------|
| 主包 | index | `pages/index` |
| 主包 | goods | `pages/goods` |
| 主包 | order | `pages/order` |
| 主包 | kit | `pages/kit` |

**底部 TabBar（主包，如有）**：首页 `pages/index/index`；商品 `pages/goods/index`

#### 3.1.2 桌面业务壳菜单分组（AD）

| 所属终端 | 菜单分组 | 分组说明 |
|----------|----------|----------|
| 管理后台 | 商品 | 商品浏览与维护任务 |
| 管理后台 | 套件 | UI 套件回归页面 |

### 3.2 页面索引表

#### 3.2.1 移动端页面（MP）

| 页面编号 | 页面名称 | 所属终端 | 包模块 | 页面路由 | 主包/分包 | 状态 | 明细路径 |
|----------|----------|----------|----------|----------|-----------|------|----------|
| PAGE-MP-001 | 首页 | 微信小程序 | index | pages/index/index | 主包 | active | ui/PAGE-MP-001.md |
| PAGE-MP-002 | 商品列表 | 微信小程序 | goods | pages/goods/index | 主包 | active | ui/PAGE-MP-002.md |
| PAGE-MP-003 | 商品详情 | 微信小程序 | goods | pages/goods/detail | 主包 | active | ui/PAGE-MP-003.md |
| PAGE-MP-004 | 表单 | 微信小程序 | kit | pages/kit/form | 主包 | active | ui/PAGE-MP-004.md |
| PAGE-MP-005 | 步骤向导 | 微信小程序 | goods | pages/goods/wizard | 主包 | fixture | ui/PAGE-MP-005.md |
| PAGE-MP-008 | 分类树 | 微信小程序 | goods | pages/goods/category-tree | 主包 | fixture | ui/PAGE-MP-008.md |
| PAGE-MP-013 | 分类导航 | 微信小程序 | goods | pages/goods/category-nav | 主包 | fixture | ui/PAGE-MP-013.md |
| PAGE-MP-014 | 订单列表 | 微信小程序 | order | pages/order/list | 主包 | fixture | ui/PAGE-MP-014.md |
| PAGE-MP-015 | 章节目录 | 微信小程序 | kit | pages/kit/chapter-list | 主包 | fixture | ui/PAGE-MP-015.md |
| PAGE-MP-009 | 物流时间轴 | 微信小程序 | order | pages/order/logistics | 主包 | fixture | ui/PAGE-MP-009.md |

#### 3.2.2 桌面业务壳页面（AD）

| 页面编号 | 页面名称 | 所属终端 | 菜单分组 | 页面路由 | 状态 | 明细路径 |
|----------|----------|----------|----------|----------|------|----------|
| PAGE-AD-001 | 商品列表 | 管理后台 | 商品 | views/goods/index | active | ui/PAGE-AD-001.md |
| PAGE-AD-002 | 商品表单 | 管理后台 | 商品 | views/goods/form | active | ui/PAGE-AD-002.md |
| PAGE-AD-007 | 时间轴 | 管理后台 | 套件 | views/kit/timeline | fixture | ui/PAGE-AD-007.md |
| PAGE-AD-008 | 商品详情 | 管理后台 | 商品 | views/goods/detail | active | ui/PAGE-AD-008.md |
| PAGE-AD-009 | 表单 | 管理后台 | 套件 | views/kit/form | fixture | ui/PAGE-AD-009.md |

## 4. 局部自定义UI组件索引清单（如有）

| 组件编号 | 组件名称 | 明细路径 |
|----------|----------|----------|
| COMP-001 | 商品卡片 | ui/COMP-001.md |

## 5. 全局视觉约定（如有）

无
