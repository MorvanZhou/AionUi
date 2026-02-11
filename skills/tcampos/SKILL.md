---
name: tcampos
description: This skill provides API access to tcampos.qq.com platform for querying camp data, camp topics, user information, and performing data analysis. This skill should be used when the user needs to query TCampos platform data, list camps, list camp topics/themes, analyze camp statistics, or interact with any tcampos.qq.com API endpoints.
---

# TCampos

## Overview

This skill enables interaction with the TCampos (tcampos.qq.com) platform through its API endpoints. It provides capabilities to:

- **查询营地班级列表** - Query and filter camps by name, time range
- **查询主题营/营地主题** - Query camp topics/themes
- **报名筛选流程** - Get selection process and export data (signup/exam/interview)
- **Excel 数据分析** - Analyze exported Excel data (signup/exam/interview records)
- **数据分析** - Analyze camp and topic data

## Capabilities

### 1. 营地班级管理 (Camp Management)

| 能力                 | 描述                                   | 可获取数据                                                   |
| -------------------- | -------------------------------------- | ------------------------------------------------------------ |
| 查询营地班级列表     | 按名称、时间范围筛选营地班级           | 营地班级ID、名称、创建者、报名人数、主题、主题营、加入方式等 |
| 营地班级详情         | 获取单个营地班级的详细信息             | 完整营地班级信息、活动时间、报名时间等                       |
| 报名筛选流程         | 获取营地的筛选环节和数据               | 筛选环节列表、各环节状态、通过人数、总报名数                 |
| 导出报名数据         | 导出报名记录Excel                      | 报名用户信息、报名时间、审核状态等                           |
| 导出笔试数据         | 导出考试记录Excel                      | 考试成绩、答题情况等                                         |
| 导出面试数据         | 导出面试记录Excel                      | 面试评分、面试状态等                                         |
| 导出营地用户         | 导出营地学员信息Excel                  | 用户ID、姓名、任务完成度、评价等                             |
| 查询任务列表         | 获取营地班级中的所有任务               | 任务ID、名称、类型、是否必修(应学)、完成进度                 |
| 查询用户任务完成情况 | 分页查询指定任务的所有用户完成情况数据 | 用户ID、用户名、完成状态、开始/完成时间、完成进度            |
| 导出任务记录         | 导出用户任务完成记录Excel              | 用户ID、完成状态、提交时间、作业内容等                       |

### 2. 主题营管理 (Camp Topic Management)

| 能力           | 描述                     | 可获取数据                                            |
| -------------- | ------------------------ | ----------------------------------------------------- |
| 查询主题营列表 | 按名称、更新时间筛选主题 | 主题ID、名称、描述、关联营地班级数量、创建/更新时间等 |

### 3. 数据分析 (Data Analysis)

| 分析类型   | 描述                         |
| ---------- | ---------------------------- |
| 热度分析   | 按报名人数排序，发现热门营地 |
| 时间分析   | 按活动时间分析营地班级分布   |
| 创建者分析 | 按创建者统计营地班级数量     |
| 主题分析   | 统计各主题下的营地班级分布   |

### 4. Excel 数据分析 (Excel Data Analysis)

TCampos 导出的 Excel 文件（报名表、考试记录表、面试记录表）遵循统一格式，支持灵活的数据分析。

| 能力           | 描述                                          |
| -------------- | --------------------------------------------- |
| 数据读取       | 解析 Excel 文件结构（说明行、表头行、数据行） |
| 字段筛选       | 按任意字段条件过滤数据                        |
| 跨表合并       | 按用户 ID 关联合并多个表的数据                |
| Hyperlink 保留 | 处理附件字段时保留下载链接                    |
| 统计分析       | 各状态人数统计、得分分布等                    |

> 📖 **Excel 格式规范与代码示例**：详见 [references/data_analysis.md](references/data_analysis.md)

### 5. 通知发送 (Notification)

TCampos 提供通知发送模版，用于批量给用户发送邮件或短信通知。通常需要配合数据筛选分析使用。

| 能力     | 描述                           |
| -------- | ------------------------------ |
| 模版填写 | 将筛选出的用户 ID 填入通知模版 |

**通知发送工作流程**:

1. 明确筛选需求（如：必修(应学)未完成、报名未通过等）
2. 导出相关数据表（营地用户表、报名表、考试记录表等）
3. 按条件筛选目标用户，提取用户 ID
4. 将用户 ID 填入通知模版（`*用户 ID` 列 + `*操作(1-发送)` 填 1）
5. 将数据表导出到 Excel 文件

**通知模版**: `assets/templates/通知发送模版.xlsx`

> 📖 **完整流程与代码示例**：详见 [references/notification.md](references/notification.md)

## Configuration

配置文件 `.tcampos-config` 位于**当前项目工作目录**下（而非 scripts 目录，以确保凭据安全）：

```json
{
  "account": "+86...",
  "passwd": "...",
  "tipe_token": "<JWT_TOKEN>"
}
```

> ⚠️ **安全提示**：请将 `.tcampos-config` 添加到 `.gitignore` 中，避免凭据被提交到版本控制系统。

## 文件输出目录

| 操作类型     | 默认目录       | 说明                                                       |
| ------------ | -------------- | ---------------------------------------------------------- |
| **下载数据** | `./downloads/` | 从 API 导出的 Excel 文件（营地用户表、报名表、考试记录等） |
| **生成数据** | `./outputs/`   | AI 分析处理后生成的文件（通知模版、筛选结果、统计报告等）  |

> **注意**：如果用户指定了具体路径，则使用用户指定的路径；如果目录不存在会自动创建。

## Authentication

### 首次登录（对话方式）

当配置文件不存在或缺少凭据时，**AI 会主动询问用户提供手机号和密码**，然后通过命令行登录：

```
AI: 检测到未登录，请提供 TCampos 账号信息：
    1. 手机号（如13800138000）
    2. 密码

用户: 手机号是 13800138000，密码是 xxx
```

AI 收到信息后会，将手机号补上 +86 的区号信息，执行登录命令并保存凭据。

### 命令行登录

也可以通过命令行直接登录：

```bash
python3 scripts/login.py --account "+86..." --password "..."
python3 scripts/login.py --refresh  # 使用缓存凭据刷新
```

### 自动 Token 刷新

API 客户端自动处理 Token 过期：

1. 从当前工作目录的 `.tcampos-config` 读取 `tipe_token` 发起请求
2. Token 过期时自动使用缓存的 `account`/`passwd` 重新登录
3. 更新配置文件中的新 Token
4. 重试原请求

## API Operations

### Login (登录)

认证并获取 `tipe_token`。

**脚本**: `scripts/login.py`

```bash
# 命令行登录
python3 scripts/login.py --account "+86..." --password "..."
python3 scripts/login.py --refresh  # 使用缓存凭据刷新
```

**首次使用**: AI 会通过对话询问用户的手机号和密码，然后执行登录命令。

详细接口说明见 [references/login.md](references/login.md)

---

### List Camps (查询营地班级列表)

按条件查询营地班级列表。

**脚本**: `scripts/list_camp.py`

```bash
python3 scripts/list_camp.py --name "<keyword>" --page-size 20 --page-num 1
python3 scripts/list_camp.py --slug "NRp5lExN"  # 按 Slug 精准搜索
python3 scripts/list_camp.py --slugs "NRp5lExN" "ucCjXKl0"  # 多个 Slug
python3 scripts/list_camp.py --topic-name "Mini鹅"  # 按主题营名称搜索
python3 scripts/list_camp.py --update-from 1700000000 --update-to 1710000000
python3 scripts/list_camp.py --raw  # 输出原始 JSON
```

**可获取数据**:

- 营地班级基本信息: ID, Name, Slug, CreatorName, CreateBy
- 报名数据: SignupNum（已报名数）, SignupSuccNum（报名成功数）
- 时间信息: ActionStartAt（活动开始）, ActionEndAt（活动结束）, SignupStartAt（报名开始）, SignupEndAt（报名结束）, CreateAt, UpdateAt
- 分类信息: PlanID, PlanName（方案）, Topics（主题）, TopicIDs, BizIDs（业务）, JoinMode（参与方式）, Type（营地类型）, Scope（可见范围）
- 状态信息: ShowStatus（上架状态）, ShowAt（上架时间）, ExpireMode（过期模式）, RecomWeight（推荐权重）
- 其他: BannerURL（头图）, ActionAddr（活动地址）, ActionCity（活动城市）, JoinPrompt, JoinWording, JoinQrcode, ExtInfo

> 📖 **完整字段说明**：详见 [references/camp.md](references/camp.md#camp-object-字段说明)

详细接口说明见 [references/camp.md](references/camp.md)

---

### List Camp Topics (查询主题营列表)

按条件查询主题营/营地主题列表。

**脚本**: `scripts/list_camp_topic.py`

```bash
python3 scripts/list_camp_topic.py --name "<keyword>" --page-size 20 --page-num 1
python3 scripts/list_camp_topic.py --update-from 1700000000 --update-to 1710000000
python3 scripts/list_camp_topic.py --raw  # 输出原始 JSON
```

**可获取数据**:

- 主题基本信息: ID, Slug, Name, Desc（详细描述）, Intro（短介绍）
- 图片信息: BannerURL（头图）, CoverURL（封面图）
- 关联数据: RelatedCamps（关联营地班级列表）, RelatedCampsNum（关联营地班级数量）, BizIDs（业务ID）
- 时间信息: CreateAt（创建时间）, UpdateAt（修改时间）, ShowAt（上架时间）
- 状态信息: Scope（可见范围）, ShowStatus（上架状态）
- 创建者信息: CreateBy（创建者ID）, CreatorName（创建者名称）
- 其他: ExtInfo（扩展信息）, ConfigJson

> 📖 **完整字段说明**：详见 [references/camp_topic.md](references/camp_topic.md#camp-topic-object-字段说明)

详细接口说明见 [references/camp_topic.md](references/camp_topic.md)

---

### Selection Process (报名筛选流程)

获取营地班级的筛选流程信息，并导出各环节数据。

**脚本**: `scripts/select_process.py`

```bash
# 查看筛选流程信息
python3 scripts/select_process.py --camp-id 11264

# 导出报名记录（默认保存到 ./downloads/）
python3 scripts/select_process.py --camp-id 11264 --export signup

# 导出笔试/考试记录
python3 scripts/select_process.py --camp-id 11264 --export exam

# 导出面试记录
python3 scripts/select_process.py --camp-id 11264 --export interview

# 导出所有数据
python3 scripts/select_process.py --camp-id 11264 --export all

# 指定下载目录
python3 scripts/select_process.py --camp-id 11264 --export signup --output /custom/path/

# 只获取URL不下载
python3 scripts/select_process.py --camp-id 11264 --export signup --no-download
```

**可获取数据**:

- 筛选流程信息: CampJoinMode（参与方式）、Items（环节列表）、Summary（数据汇总）
- 环节信息: Name（环节名称）、Type（类型：1报名/2笔试/3面试/4录取）、State（状态：0未开始/1进行中/2已结束）
- 时间信息: StartAt（开始时间）、EndAt（结束时间）
- 统计数据: UserNumPassed（通过人数）、SignupNumTotal（总报名数）
- 导出Excel: 报名表、考试记录表、面试记录表

> 📖 **完整字段说明**：详见 [references/select_process.md](references/select_process.md)

详细接口说明见 [references/select_process.md](references/select_process.md)

---

### Export Camp Users (导出营地用户)

导出营地班级的学员/用户信息到 Excel。

**脚本**: `scripts/export_camp_user.py`

```bash
# 导出营地用户（默认保存到 ./downloads/）
python3 scripts/export_camp_user.py --camp-id 11103

# 指定下载目录
python3 scripts/export_camp_user.py --camp-id 11103 --output /custom/path/

# 只获取URL不下载
python3 scripts/export_camp_user.py --camp-id 11103 --no-download

# 输出原始 JSON
python3 scripts/export_camp_user.py --camp-id 11103 --raw
```

**可获取数据**:

- 用户基本信息: 用户ID、姓名、性别、手机号、邮箱、出生日期
- 学习进度: 总任务完成度、应学任务完成度、选学任务完成度、未开始任务数
- 评价信息: 用户评价文本

> 📖 **完整字段说明**：详见 [references/camp_user.md](references/camp_user.md)

详细接口说明见 [references/camp_user.md](references/camp_user.md)

---

### List Camp Tasks (查询营地任务列表)

查询指定营地班级中的所有任务（包括视频、音频、作业、作品上传、链接、图文、资料任务类型）及其完成进度。

**脚本**: `scripts/list_camp_task.py`

```bash
# 列出所有任务
python3 scripts/list_camp_task.py --camp-id 11103

# 按任务名称筛选
python3 scripts/list_camp_task.py --camp-id 11103 --name "入营"

# 按任务类型筛选
python3 scripts/list_camp_task.py --camp-id 11103 --type homework
python3 scripts/list_camp_task.py --camp-id 11103 --type article

# 输出原始 JSON
python3 scripts/list_camp_task.py --camp-id 11103 --raw
```

**可获取数据**:

- 任务基本信息: ID、Name（名称）、Type（任务类型）、Required（是否必修/应学）
- 完成进度: Total（总人数）、Done（已完成）、Doing（进行中）、NotStart（未开始）
- 完成率: TotalDoneRatio（总体完成率）、StartDoneRatio（已开始用户完成率）

> 📖 **完整字段说明**：详见 [references/task.md](references/task.md#task-object-字段说明)

详细接口说明见 [references/task.md](references/task.md)

---

### List User Task Records (查询用户任务完成情况)

分页查询指定任务的所有用户完成情况数据。

**脚本**: `scripts/list_user_task_record.py`

```bash
# 查询所有用户的任务完成情况
python3 scripts/list_user_task_record.py --task-id 1162 --page-size 20 --page-num 1

# 只查询已完成的用户
python3 scripts/list_user_task_record.py --task-id 1162 --status 2

# 只查询进行中的用户
python3 scripts/list_user_task_record.py --task-id 1162 --status 1

# 只查询未开始的用户
python3 scripts/list_user_task_record.py --task-id 1162 --status 0

# 按用户名搜索
python3 scripts/list_user_task_record.py --task-id 1162 --username "张三"

# 输出原始 JSON
python3 scripts/list_user_task_record.py --task-id 1162 --raw
```

**可获取数据**:

- 用户信息: Uid（用户ID）、UserName（用户名）
- 完成状态: OpStatus（完成状态：0未开始/1进行中/2已完成）
- 完成进度: Progress（完成进度百分比：0-100）
- 时间信息: StartAt（开始时间戳）、FinishAt（完成时间戳）

> 📖 **完整字段说明**：详见 [references/task.md](references/task.md#usertaskrecord-object-字段说明)

详细接口说明见 [references/task.md](references/task.md#list-user-task-records-查询用户任务完成情况)

---

### Export Task Records (导出任务记录)

导出指定任务的用户完成记录到 Excel。

**脚本**: `scripts/export_task_records.py`

```bash
# 导出任务记录（默认保存到 ./downloads/）
python3 scripts/export_task_records.py --task-id 3406

# 指定下载目录
python3 scripts/export_task_records.py --task-id 3406 --output /custom/path/

# 只导出已完成的记录
python3 scripts/export_task_records.py --task-id 3406 --status 2

# 只获取URL不下载
python3 scripts/export_task_records.py --task-id 3406 --no-download

# 输出原始 JSON
python3 scripts/export_task_records.py --task-id 3406 --raw
```

**可获取数据**:

- 用户信息: 用户ID、姓名
- 完成状态: 当前状态（0未开始/1进行中/2已完成）、完成率
- 时间信息: 开始时间、完成时间
- 作业内容: 表单字段、附件（带 hyperlink）

> 📖 **完整字段说明**：详见 [references/task.md](references/task.md#用户任务数据表-excel-字段说明)

详细接口说明见 [references/task.md](references/task.md)

---

### List Users (查询用户档案)

搜索用户列表或获取单个用户的详细档案信息。

**脚本**: `scripts/list_user.py`

```bash
# 搜索用户（按姓名或 UID 模糊匹配）
python3 scripts/list_user.py list --search "张三"

# 按手机号精确查询
python3 scripts/list_user.py list --phone "13800138000"

# 按邮箱查询
python3 scripts/list_user.py list --email "test@example.com"

# 按学校/组织模糊查询
python3 scripts/list_user.py list --org "深圳中学"

# 按性别筛选（1=男, 2=女）
python3 scripts/list_user.py list --gender 1 2

# 按营地 ID 查询参与过的用户
python3 scripts/list_user.py list --camp-id 11103

# 获取单个用户详情
python3 scripts/list_user.py get 63485076

# 输出原始 JSON
python3 scripts/list_user.py list --search "张三" --raw
python3 scripts/list_user.py get 63485076 --raw
```

**可获取数据**:

- 用户列表: Uid、姓名、性别、手机号、生日、邮箱、学校
- 用户详情:
  - 账号信息: UID、创想家UID、注册渠道、注册方式、注册时间
  - 基础信息: 姓名、昵称、头像、性别、手机、邮箱、省市、生日、学校、身份
  - 社交绑定: 微信/QQ 绑定状态和昵称
  - 营地记录: 参与的营地列表

> 📖 **完整字段说明**：详见 [references/user_profile.md](references/user_profile.md)

详细接口说明见 [references/user_profile.md](references/user_profile.md)

---

### List User Events (查询用户事件)

查询用户历史参与过的营地班级、比赛或其他类型的事件记录。

**脚本**: `scripts/list_user_event.py`

```bash
# 查询用户所有事件
python3 scripts/list_user_event.py --uid 23892136

# 只查询营地事件
python3 scripts/list_user_event.py --uid 23892136 --type camp

# 只查询比赛事件
python3 scripts/list_user_event.py --uid 23892136 --type match

# 查询多种类型事件
python3 scripts/list_user_event.py --uid 23892136 --type camp match

# 分页查询
python3 scripts/list_user_event.py --uid 23892136 --page-size 50 --page-num 1

# 输出原始 JSON
python3 scripts/list_user_event.py --uid 23892136 --raw
```

**可获取数据**:

- 事件基本信息: Type（类型）、Title（标题）、Desc（描述）、CreateAt（时间）
- 营地事件: CampID、CampSlug
- 比赛事件: MatchID
- 自定义事件: 其他自定义数据

**事件类型**:
| 类型 | 描述 |
|------|------|
| `camp` | 营地事件（用户参与的营地班级） |
| `match` | 比赛事件 |
| `custom` | 自定义事件 |

> 📖 **完整字段说明**：详见 [references/user_profile.md](references/user_profile.md#event-object-字段说明)

详细接口说明见 [references/user_profile.md](references/user_profile.md)

## Resources

### scripts/

| 脚本                     | 功能                              |
| ------------------------ | --------------------------------- |
| `tcampos_api.py`         | API 基础客户端，含自动 Token 刷新 |
| `login.py`               | 命令行登录和凭据管理              |
| `list_camp.py`           | 查询营地班级列表                  |
| `list_camp_topic.py`     | 查询主题营列表                    |
| `select_process.py`      | 报名筛选流程查询与数据导出        |
| `export_camp_user.py`    | 导出营地用户/学员信息             |
| `list_camp_task.py`      | 查询营地任务列表                  |
| `export_task_records.py` | 导出任务用户完成记录              |
| `list_user.py`           | 查询用户档案（搜索/详情）         |
| `list_user_event.py`     | 查询用户事件（营地/比赛/自定义）  |

> **注意**：`.tcampos-config` 配置文件保存在当前项目工作目录下，不在 scripts 目录中。

### references/

| 文件                | 内容                                         |
| ------------------- | -------------------------------------------- |
| `README.md`         | API 文档索引                                 |
| `common.md`         | 通用信息：Base URL、认证方式、响应码、错误码 |
| `login.md`          | 登录认证 API                                 |
| `camp.md`           | 营地班级相关 API                             |
| `camp_topic.md`     | 主题营相关 API                               |
| `select_process.md` | 报名筛选流程与数据导出 API                   |
| `camp_user.md`      | 营地用户导出 API                             |
| `task.md`           | 任务管理与数据导出 API                       |
| `user_profile.md`   | 用户档案查询 API                             |
| `data_analysis.md`  | Excel 数据格式规范与分析指南                 |
| `notification.md`   | 通知发送模版填写指南                         |

### assets/

| 文件/目录                     | 内容                   |
| ----------------------------- | ---------------------- |
| `templates/通知发送模版.xlsx` | 批量发送通知的模版文件 |

## Error Handling

| 错误码             | 描述       | 处理方式                |
| ------------------ | ---------- | ----------------------- |
| `InvalidJWTClaims` | Token 过期 | 自动刷新                |
| HTTP 401/403       | 认证失败   | 自动刷新                |
| 登录失败           | 凭据无效   | AI 询问用户重新提供凭据 |
