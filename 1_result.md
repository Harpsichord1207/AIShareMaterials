# 架构文档示例输出

> 这是 AI 分析后端代码库后生成的示例输出。

---

# 电商 API 架构文档

## 1. 概述

| 属性 | 值 |
|------|-----|
| 项目类型 | REST API（单体应用） |
| 业务领域 | 电商平台 |
| 主要语言 | TypeScript |
| 框架 | NestJS |
| 数据库 | PostgreSQL + Redis |

## 2. 技术栈

### 核心依赖
- **运行时**：Node.js 18+
- **框架**：NestJS 10.x
- **ORM**：TypeORM 0.3.x
- **数据库**：PostgreSQL 15, Redis 7
- **验证**：class-validator, class-transformer
- **认证**：JWT + Passport

### 开发工具
- **测试**：Jest, Supertest
- **代码检查**：ESLint, Prettier
- **构建**：TypeScript 编译器, Webpack

## 3. 目录结构

```
src/
├── modules/           # 功能模块
│   ├── auth/          # 认证与授权
│   ├── users/         # 用户管理
│   ├── products/      # 商品目录
│   ├── orders/        # 订单处理
│   ├── payments/      # 支付集成
│   └── inventory/     # 库存管理
├── common/            # 共享工具
│   ├── decorators/    # 自定义装饰器
│   ├── filters/       # 异常过滤器
│   ├── guards/        # 认证守卫
│   ├── interceptors/  # 响应拦截器
│   └── pipes/         # 验证管道
├── config/            # 配置文件
├── database/          # 迁移与种子数据
└── main.ts            # 应用入口
```

### 模块依赖关系

```mermaid
graph LR
    subgraph "核心层 Core Layer"
        Auth[Auth 认证模块]
        Users[Users 用户模块]
        Common[Common 公共模块]
    end

    subgraph "业务层 Business Layer"
        Products[Products 商品模块]
        Orders[Orders 订单模块]
        Payments[Payments 支付模块]
        Inventory[Inventory 库存模块]
    end

    subgraph "基础设施层 Infrastructure"
        Database[(Database 数据库)]
        Redis[Redis 缓存]
        S3[S3 存储]
    end

    subgraph "外部服务 External Services"
        Stripe[Stripe 支付]
        SendGrid[SendGrid 邮件]
    end

    Auth --> Users
    Auth --> Common
    Users --> Common
    Users --> Auth
    Products --> Common
    Products --> Inventory
    Products --> Auth
    Orders --> Common
    Orders --> Auth
    Orders --> Users
    Orders --> Products
    Orders --> Inventory
    Orders --> Payments
    Payments --> Common
    Payments --> Auth
    Payments --> Stripe
    Inventory --> Common
    Common --> Database
    Common --> Redis
    Payments --> S3
    Products --> S3
    Payments --> SendGrid
    Orders --> SendGrid

    style Auth fill:#e74c3c,color:#fff
    style Users fill:#3498db,color:#fff
    style Products fill:#2ecc71,color:#fff
    style Orders fill:#f39c12,color:#fff
    style Common fill:#9b59b6,color:#fff
```

## 4. 核心模块

### 认证模块
- 基于 JWT 的身份认证
- 基于角色的访问控制（RBAC）
- 使用 bcrypt 进行密码哈希
- Refresh Token 轮换机制

### 商品模块
- 商品 CRUD 操作
- 分类管理
- 搜索与筛选
- 图片上传至 S3

### 订单模块
- 订单创建与追踪
- 状态流转管理
- 与库存系统集成
- 邮件通知

## 5. 数据架构

### 实体关系图

```mermaid
erDiagram
    User ||--o{ Order : "下单"
    User ||--o{ Review : "评价"
    User ||--o{ Address : "拥有"
    
    Product ||--o{ OrderItem : "包含于"
    Product }o--|| Category : "属于"
    Product ||--o{ Review : "被评价"
    
    Order ||--|{ OrderItem : "包含"
    OrderItem }o--|| Product : "关联商品"
    
    User {
        int id PK
        string email UK
        string password_hash
        enum role
        enum status
        datetime created_at
    }
    
    Product {
        int id PK
        string name
        decimal price
        int stock
        int category_id FK
    }
    
    Order {
        int id PK
        string order_no UK
        int user_id FK
        enum status
        decimal total_amount
    }
    
    OrderItem {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
```

### 核心实体

| 实体 | 描述 | 关键字段 |
|------|------|----------|
| User | 客户账户 | id, email, role, status |
| Product | 商品信息 | id, name, price, stock |
| Order | 采购订单 | id, status, total, userId |
| OrderItem | 订单项 | id, orderId, productId, quantity |

### 数据迁移
- 位于 `src/database/migrations/`
- 执行命令：`npm run migration:run`
- 命名规范：`YYYYMMDDHHMMSS_description.ts`

## 6. API 参考

### 认证接口
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /auth/register | 创建新账户 |
| POST | /auth/login | 用户登录 |
| POST | /auth/refresh | 刷新访问令牌 |

### 商品接口
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /products | 商品列表（分页） |
| GET | /products/:id | 商品详情 |
| POST | /products | 创建商品（管理员） |
| PATCH | /products/:id | 更新商品（管理员） |

### 订单接口
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /orders | 用户订单列表 |
| POST | /orders | 创建新订单 |
| GET | /orders/:id | 订单详情 |

### 订单创建流程

```mermaid
sequenceDiagram
    participant C as Client 客户端
    participant Auth as Auth 认证服务
    participant Order as Order 订单服务
    participant Product as Product 商品服务
    participant Inventory as Inventory 库存服务
    participant Payment as Payment 支付服务
    participant DB as Database 数据库
    participant Stripe as Stripe 支付网关
    participant SendGrid as SendGrid 邮件服务

    Note over C,Order: 1. 用户认证
    C->>+Auth: POST /auth/login
    Auth->>+DB: 验证用户凭据
    DB-->>-Auth: 用户信息
    Auth-->>-C: JWT Token

    Note over C,Order: 2. 创建订单
    C->>+Order: POST /orders {items}
    Order->>Auth: 验证 JWT
    Auth-->>Order: 用户ID
    
    Order->>+Product: 查询商品价格
    Product-->>-Order: 商品详情
    
    Order->>+Inventory: 检查库存
    Inventory-->>-Order: 库存充足
    
    Order->>+DB: 创建订单记录
    DB-->>-Order: 订单ID
    
    Order->>Inventory: 预留库存
    Order-->>-C: 订单创建成功

    Note over C,Payment: 3. 支付处理
    C->>+Payment: POST /payments
    Payment->>+Stripe: 创建支付
    Stripe-->>-Payment: 支付成功
    Payment->>Order: 更新订单状态
    Payment-->>-C: 支付确认

    Note over Payment,SendGrid: 4. 后续处理
    Payment->>+SendGrid: 发送确认邮件
    SendGrid-->>-Payment: 已发送
```

## 7. 外部依赖

| 服务 | 用途 | 集成方式 |
|------|------|----------|
| AWS S3 | 文件存储 | SDK |
| Stripe | 支付处理 | SDK |
| SendGrid | 邮件发送 | API |
| Redis | 缓存、会话 | ioredis |

## 8. 配置说明

### 环境变量

| 变量名 | 必填 | 描述 |
|--------|------|------|
| DATABASE_URL | 是 | PostgreSQL 连接字符串 |
| REDIS_URL | 是 | Redis 连接字符串 |
| JWT_SECRET | 是 | Token 签名密钥 |
| AWS_ACCESS_KEY_ID | 是 | S3 访问密钥 |
| AWS_SECRET_ACCESS_KEY | 是 | S3 密钥 |
| STRIPE_SECRET_KEY | 是 | Stripe API 密钥 |

## 9. 部署考量

### 健康检查
- `/health` - 应用健康检查端点
- 数据库连接检查
- Redis 连接检查

### 扩展策略
- 无状态设计，支持水平扩展
- Redis 用于会话分发
- 数据库连接池

### 监控
- 结构化 JSON 日志
- 错误追踪（推荐 Sentry）
- 性能指标采集

### 部署架构图

```mermaid
graph TB
    subgraph "客户端层"
        Web[Web Browser<br/>网页浏览器]
        Mobile[Mobile App<br/>移动应用]
    end

    subgraph "接入层"
        LB[Load Balancer<br/>Nginx 负载均衡]
    end

    subgraph "应用层"
        App1[API Server 1<br/>NestJS]
        App2[API Server 2<br/>NestJS]
        App3[API Server 3<br/>NestJS]
    end

    subgraph "数据层"
        DB[(PostgreSQL<br/>主从复制)]
        Cache[Redis<br/>集群缓存]
    end

    subgraph "存储层"
        S3[AWS S3<br/>对象存储]
    end

    subgraph "外部服务"
        Stripe[Stripe<br/>支付网关]
        SendGrid[SendGrid<br/>邮件服务]
    end

    Web --> LB
    Mobile --> LB
    LB --> App1
    LB --> App2
    LB --> App3
    App1 --> DB
    App2 --> DB
    App3 --> DB
    App1 --> Cache
    App2 --> Cache
    App3 --> Cache
    App1 --> S3
    App2 --> S3
    App3 --> S3
    App1 --> Stripe
    App2 --> Stripe
    App3 --> Stripe
    App1 --> SendGrid
    App2 --> SendGrid
    App3 --> SendGrid

    style LB fill:#667eea,color:#fff
    style DB fill:#e74c3c,color:#fff
    style Cache fill:#f39c12,color:#fff
    style S3 fill:#3498db,color:#fff
```
