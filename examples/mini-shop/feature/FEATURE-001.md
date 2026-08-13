# FEATURE-001 浏览在售商品

## 1. 基本信息
| 属性 | 内容 |
|------|------|
| 功能编号 | FEATURE-001 |
| 功能名称 | 浏览在售商品 |
| 所属模块 | 商品 |
| 优先级 | P0 |
| 状态 | active |
| 关联 STORY | STORY-001（主）; STORY-002（次） |
| 分支数 | 2 |

## 2. 功能目标与范围
- 目标：买家浏览推荐与列表；运营在后台核对商品
- 范围内：分页查询、失败重试
- 范围外：下单、支付、登录（框架承接）

## 3. 核心规则
| 规则编号 | 规则说明 |
|----------|----------|
| BR-1 | 小程序列表仅展示在售商品 |
| BR-2 | 请求失败须提供重试入口 |

## 4. 交互与状态（概要）
- 正常流：进页请求列表并渲染卡片或表格
- 异常流：失败提示并允许重试
- 边界条件：空列表展示空态

## 5. 验收标准
| AC 编号 | 验收描述（可验证） | 关联规则 | 关联接口 |
|---------|-------------------|----------|----------|
| AC-1 | 首页初始化后展示不超过 4 条推荐商品 | BR-1 | API-MP-001 |
| AC-2 | 商品列表可翻页且仅含在售商品 | BR-1 | API-MP-001 |
| AC-3 | 后台列表可按名称筛选并分页 | — | API-AD-001 |
| AC-4 | 小程序请求失败出现重试入口 | BR-2 | API-MP-001 |

## 6. 关联对象
- 关联页面：PAGE-MP-001, PAGE-MP-002, PAGE-AD-001
- 关联接口：API-MP-001, API-AD-001
- 关联第三方接口：无
- 引用文档：ui/PAGE-MP-001.md, ui/PAGE-MP-002.md, ui/PAGE-AD-001.md, api/API-MP-001.md, api/API-AD-001.md

## 7. 时序图（按触发条件必填）

```mermaid
sequenceDiagram
    participant User as 用户
    participant UI_MP_002 as PAGE-MP-002 商品列表
    participant API_MP_001 as API-MP-001 查询在售商品
    User->>UI_MP_002: 进入 PAGE-MP-002
    UI_MP_002->>API_MP_001: 调用 API-MP-001
    API_MP_001-->>UI_MP_002: 返回列表或失败
    UI_MP_002-->>User: 渲染卡片或提示重试
```

## 8. 流程图（按触发条件必填）

```mermaid
flowchart TD
    startNode[开始] --> enterPage[PAGE-MP-002 进入列表]
    enterPage --> callApi[调用 API-MP-001]
    callApi --> ok{API-MP-001 成功?}
    ok -->|是| showList[PAGE-MP-002 渲染列表]
    ok -->|否| retry[PAGE-MP-002 提示失败并允许重试]
    showList --> finished[结束]
    retry --> finished
```

## 9. 变更备注（可选）
- 夹具首版
