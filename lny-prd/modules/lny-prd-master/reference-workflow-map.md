# LNY PRD Workflow 路由图

这张图描述默认工作流。步骤编号用于定位模块，实际执行按用户目标、项目状态和变更影响计算最小路径。

## PM 视图

PM 只需要记住五个阶段。括号内是内部模块，不代表每次都逐个执行。

```mermaid
flowchart LR
    DECISION[1 理解与决策\n识别意图 → 可选探索 → 目标与范围决策]
    SPEC[2 规格与原型\nUI/API/Feature/Page + Prototype]
    VERIFY[3 自动验证\nQ-S/Q-P + 一致性 + 决策兑现]
    DELIVERY[4 交付准备\n按需批准范围 + 按需估点]
    LEARN[5 发布学习\n反馈、指标、实验、新版本]

    DECISION --> SPEC --> VERIFY
    VERIFY -->|局部修改完成| LEARN
    VERIFY -->|需要批准或估点| DELIVERY --> LEARN
    LEARN -->|新证据或变更| DECISION
```

### 五阶段与内部步骤

| PM 阶段 | 内部步骤 | 说明 |
|---|---|---|
| 理解与决策 | ①、Discovery | 归一化输入，形成问题、目标、范围和成功标准；决策可暂定或已确认 |
| 规格与原型 | ② UI、③ API、④ Feature、⑤ Page、⑥ Prototype | 按最小依赖产出方案与页面，不要求每次模块全做 |
| 自动验证 | ⑦ Q-S/Q-P、事实一致性、决策兑现检查 | 自动发现偏离并回到责任步骤，只有不可逆冲突才请求决策 |
| 交付准备 | ⑧ Review、⑨ SP | 需要正式批准时确认范围，需要工程投入时估点 |
| 发布学习 | Learning、⑩ Iter | 发布反馈回到理解与决策，必要时创建新版本 |

五阶段不是新的写入层。正式产物仍由内部步骤按原有归属维护。⑧ Review 和⑨ SP 都是交付准备中的按需动作。

```mermaid
flowchart TD
    START([收到输入]) --> NORMALIZE[归一化输入与项目状态]
    NORMALIZE --> CLASSIFY{识别目标与影响}

    CLASSIFY --> EXPLORE{需要探索讨论?}
    EXPLORE -->|是| DISCOVERY[可选探索\n问题、证据、假设、方案比较]
    DISCOVERY --> TARGET
    EXPLORE -->|否| TARGET

    TARGET --> EMPTY{空目录?}
    EMPTY -->|是| INIT[① 立项\nmain_spec + 三件套骨架]
    INIT --> TARGET
    EMPTY -->|否| TARGET{当前目标}

    TARGET --> DISCOVERY_LOOP[发现或学习回流]
    DISCOVERY_LOOP -->|确认产品事实| SOURCE[回流到事实正本]
    SOURCE --> IMPACT

    TARGET --> LEARNING[学习\n发布反馈、指标、复盘]
    LEARNING --> IMPACT[按影响范围回流]

    TARGET --> FEEDBACK[原型反馈或局部修改]
    FEEDBACK --> ROUTE{A / B / C / D}
    ROUTE -->|A 视觉微调| FAST[只改目标原型页\n渲染 + 视觉自评 + 局部 Q-P]
    FAST --> DONE([当前目标完成])
    ROUTE -->|B 交互表现| UI[② UI / COMP]
    ROUTE -->|C 页面结构| UI
    ROUTE -->|D 产品事实| OWNER[③ API / ④ Feature / main_spec 正本]
    UI --> PAGE[⑤ Page\n仅受影响页面]
    OWNER --> DOWNSTREAM[同步受影响 UI、Page、API、Feature]
    DOWNSTREAM --> QS[内部门禁 Q-S\n受影响规格]
    PAGE --> QS
    QS --> PROTO[⑥ Prototype\n受影响页面]
    PROTO --> QP[内部门禁 Q-P\n作者自评 + 原型门禁]
    QP --> DONE

    TARGET --> SPEC{目标是规格或页面?}
    SPEC -->|缺 UI/API/Feature| THREE[② UI → ③ API → ④ Feature\n按依赖可并行]
    THREE --> PAGE2[⑤ Page]
    PAGE2 --> QS2[内部门禁 Q-S]
    QS2 --> PROTO2[⑥ Prototype]
    PROTO2 --> QP2[内部门禁 Q-P]
    QP2 --> REVIEW_READY{准备正式评审?}

    TARGET --> DEMO[目标是可演示原型]
    DEMO --> THREE2[补齐必要规格]
    THREE2 --> PAGE2

    TARGET --> CHECK[明确检查]
    CHECK --> QTYPE{检查类型}
    QTYPE -->|规格| QS3[内部门禁 Q-S]
    QTYPE -->|原型| QP3[内部门禁 Q-P]
    QTYPE -->|完整| QS3 --> PROTO3[必要时补⑥] --> QP3
    QS3 --> DONE
    QP3 --> DONE

    REVIEW_READY -->|用户需要正式决策| REVIEW[按需 ⑧ 产品评审\n范围、证据、批准快照]
    REVIEW -->|返修| IMPACT
    REVIEW -->|通过| ESTIMATE{需要估点?}
    ESTIMATE -->|需要工程投入估算| SP[按需 ⑨ SP\n只估已确认范围]
    ESTIMATE -->|否| DONE2([等待后续动作])
    SP --> DONE2

    TARGET --> ITER[⑩ 新版本/迭代]
    ITER -->|核验上版终态与台账| IMPACT
    IMPACT --> ROUTE2{影响范围}
    ROUTE2 -->|仅视觉| FAST
    ROUTE2 -->|规格或结构| UI
    ROUTE2 -->|产品事实| OWNER
```

## 看图规则

- **A 类**只改当前原型和视觉记录，不创建新版本，不重跑完整规格链。
- **B 类**从 UI 或 COMP 开始，只有交互契约变化时才进入 Q-S。
- **C 类**至少经过 UI、Page、Q-S、Prototype、Q-P。
- **D 类**先改事实正本，再同步下游文件，不能只改 HTML。
- **发现和学习**不是直线前置步骤。它们在获得新证据后按影响范围回流。
- **Q-S 和 Q-P**是质量门禁，判断规格和原型是否完整、可追溯、可演示。
- **⑧评审**与质量门禁位于同一 PM 阶段，但负责产品价值、范围、风险和批准决策。
- **⑨估点**只在评审确认交付范围且需要工程投入估算时进入。
- **⑩迭代**只在用户明确开启新版本时进入。

## 最小路径速查

| PM 输入 | 默认路径 |
|---|---|
| “标题左边距缩小” | A → 当前原型页 → 视觉自评 → 局部 Q-P |
| “这个按钮点击后要展开筛选” | B → UI/COMP → 必要时 Page → Q-S → Prototype → Q-P |
| “增加一个筛选入口” | C → UI → Page → Q-S → Prototype → Q-P |
| “库存字段改成可选” | D → API/Feature 正本 → 下游同步 → Q-S → Prototype → Q-P |
| “用户反馈注册后留存下降” | Learning → 证据与假设 → 按影响范围回流 |
| “继续” | 从最早未完成且与当前目标相关的责任步骤恢复 |
| “完整做完并评审” | 必要规格 → Page → Q-S → Prototype → Q-P → 自动走查 → ⑧ |

