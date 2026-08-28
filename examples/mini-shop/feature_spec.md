# 功能规格说明书 - Mini Shop

## 文档信息

| 属性 | 内容 |
|------|------|
| 文档版本 | v1.0.0 |
| 创建日期 | 2026-08-13 |
| 最后更新 | 2026-08-13 |
| 维护人 | 产品经理 |
| 状态 | 草稿 |

### 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.0.0 | 2026-08-13 | 初始版本 | 产品经理 |

## 1. 阅读说明与清单结构约定

单功能详述落在 `feature/FEATURE-*.md`。

## 2. 全局规则

- 编号：`FEATURE-{三位序号}`
- 状态：`draft` / `active` / `deprecated`
- 评审状态：`pending` / `reviewing` / `approved` / `blocked`
- 优先级：`P0` / `P1` / `P2`

## 3. Feature 索引表

| 功能编号 | 功能名称 | 模块编号 | 所属模块 | 优先级 | 状态 | 评审状态 | 分支数 | 关联页面 | 关联接口 | 明细路径 |
|----------|----------|----------|----------|--------|------|----------|--------|----------|----------|----------|
| FEATURE-001 | 浏览在售商品 | MODULE-001 | 商品 | P0 | active | approved | 3 | PAGE-MP-001, PAGE-MP-002, PAGE-MP-003, PAGE-AD-001, PAGE-AD-008 | API-MP-001, API-MP-002, API-AD-001, API-AD-002 | feature/FEATURE-001.md |
| FEATURE-002 | 维护后台商品 | MODULE-001 | 商品 | P0 | active | approved | 3 | PAGE-AD-001, PAGE-AD-002 | API-AD-001, API-AD-002, API-AD-003 | feature/FEATURE-002.md |
| FEATURE-003 | 登记到货提醒 | MODULE-001 | 商品 | P1 | active | approved | 1 | PAGE-MP-004 | API-MP-003 | feature/FEATURE-003.md |

| 统计项 | 数值 |
|--------|------|
| 有效 Feature 个数 | 3 |

## 4. 特殊说明（如有）

无
