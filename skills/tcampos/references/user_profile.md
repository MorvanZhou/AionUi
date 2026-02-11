# TCampos API - 用户档案 (User Profile)

## 目录

- [List Users (拉取用户列表)](#list-users-拉取用户列表)
- [Get User Detail (获取用户档案详情)](#get-user-detail-获取用户档案详情)
- [List User Events (拉取用户事件)](#list-user-events-拉取用户事件)
- [User Object 字段说明](#user-object-字段说明)
- [Event Object 字段说明](#event-object-字段说明)

---

## List Users (拉取用户列表)

根据多种条件筛选并分页获取用户列表，返回用户的基础信息。

**Endpoint**: `POST https://tcampos.qq.com/api/profile/listUser`

### Request

```json
{
  "Filter": {
    "NameOrUid": "",
    "Name": "",
    "Uid": "",
    "UidList": [],
    "ArenaUid": "",
    "Phone": "",
    "BirthdayFrom": 0,
    "BirthdayTo": 0,
    "GenderList": [],
    "InCampList": [],
    "Email": "",
    "Organization": ""
  },
  "PageSize": 20,
  "PageNum": 1,
  "Sort": ["-UpdateAt"]
}
```

| 字段                | 类型     | 必填 | 描述                           |
| ------------------- | -------- | ---- | ------------------------------ |
| Filter              | object   |      | 筛选条件                       |
| Filter.NameOrUid    | string   |      | 模糊匹配 Name **或** Uid       |
| Filter.Name         | string   |      | 模糊匹配姓名                   |
| Filter.Uid          | string   |      | 精确匹配用户 ID                |
| Filter.UidList      | string[] |      | 多个 uid 精确匹配              |
| Filter.ArenaUid     | string   |      | 精确匹配创想家 UID             |
| Filter.Phone        | string   |      | 精确匹配手机号                 |
| Filter.Email        | string   |      | 精确匹配邮箱                   |
| Filter.Organization | string   |      | 模糊匹配学校/组织              |
| Filter.GenderList   | int[]    |      | 性别过滤 (1=男, 2=女)          |
| Filter.InCampList   | int[]    |      | 参与过的营地 ID 列表           |
| Filter.BirthdayFrom | int      |      | 生日开始时间戳                 |
| Filter.BirthdayTo   | int      |      | 生日结束时间戳                 |
| PageSize            | int      |      | 每页数量，默认 10，最大 50     |
| PageNum             | int      |      | 页码，从 1 开始                |
| Sort                | string[] |      | 排序字段，默认 `["-UpdateAt"]` |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "xxx",
    "Result": {
      "Total": 8015,
      "Entries": [
        {
          "Uid": "63485076",
          "Name": "张三",
          "Gender": 1,
          "Phone": "+8613800138000",
          "Birthday": "20100630",
          "Email": "test@example.com",
          "Organization": "深圳中学"
        }
      ]
    },
    "Timestamp": 1770352614
  }
}
```

---

## Get User Detail (获取用户档案详情)

根据用户 ID 获取完整档案信息，包括账号信息、基础信息和营地记录。

**Endpoint**: `GET https://tcampos.qq.com/api/profile/user/:uid`

### Request

| 参数 | 类型   | 必填 | 描述                    |
| ---- | ------ | ---- | ----------------------- |
| uid  | string | ✓    | 用户 ID（URL 路径参数） |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "xxx",
    "Result": {
      "AccountInfo": {
        "Uid": "94475740",
        "CreateAt": 1745376859,
        "Phone": "+8613800138000",
        "ArenaUid": "563458201446514688",
        "Channel": "tcamp",
        "AddType": "Web-H5",
        "Source": "tcamp"
      },
      "BasicInfo": {
        "Name": "张三",
        "NickName": "小张",
        "Avatar": "https://xxx/avatar.jpg",
        "Gender": 1,
        "Phone": "+8613800138000",
        "Email": "test@example.com",
        "Province": "广东省",
        "City": "深圳市",
        "Birthday": "20100630",
        "Organization": "深圳中学",
        "Category": "初中生",
        "BindWx": true,
        "WxName": "微信昵称",
        "BindQQ": false,
        "QQName": "",
        "ContactPhone": "+8613900139000",
        "ContactEmail": "contact@example.com",
        "Resume": "{\"filename\":\"简历.pdf\", \"url\":\"https://xxx\"}"
      },
      "CampRecords": null
    },
    "Timestamp": 1770352614
  }
}
```

---

## List User Events (拉取用户事件)

根据用户 ID 拉取该用户的事件记录，可按事件类型筛选。事件类型包括营地（camp）、比赛（match）、自定义（custom）等。

**Endpoint**: `POST https://tcampos.qq.com/api/profile/listUserEvent`

### Request

```json
{
  "Uid": "23892136",
  "Filter": {
    "TypeList": ["camp"]
  },
  "PageSize": 20,
  "PageNum": 1,
  "Sort": ["-CreateAt"]
}
```

| 字段            | 类型     | 必填 | 描述                                                        |
| --------------- | -------- | ---- | ----------------------------------------------------------- |
| Uid             | string   | ✓    | 用户 ID                                                     |
| Filter          | object   |      | 筛选条件                                                    |
| Filter.TypeList | string[] |      | 事件类型过滤：`camp`(营地), `match`(比赛), `custom`(自定义) |
| PageSize        | int      |      | 每页数量，默认 10，最大 50                                  |
| PageNum         | int      |      | 页码，从 1 开始                                             |
| Sort            | string[] |      | 排序字段，默认 `["-CreateAt"]`                              |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "xxx",
    "Result": {
      "Total": 6,
      "Entries": [
        {
          "Type": "camp",
          "Title": "腾讯未来产品经理创造营",
          "Desc": "",
          "CreateAt": 1746754379,
          "Data": {
            "CampID": 11115,
            "CampSlug": "J1J9Eqal"
          }
        },
        {
          "Type": "match",
          "Title": "AI 创想家大赛",
          "Desc": "2025春季赛",
          "CreateAt": 1744959930,
          "Data": {
            "MatchID": 1001
          }
        }
      ]
    },
    "Timestamp": 1770352614
  }
}
```

---

## Event Object 字段说明

### Event 基础字段

| 字段     | 类型   | 描述                         | 示例                            |
| -------- | ------ | ---------------------------- | ------------------------------- |
| Type     | string | 事件类型                     | `"camp"`, `"match"`, `"custom"` |
| Title    | string | 事件标题                     | `"腾讯未来产品经理创造营"`      |
| Desc     | string | 事件描述                     | `"2025春季赛"`                  |
| CreateAt | int    | 事件时间戳                   | `1746754379`                    |
| Data     | object | 事件数据（不同类型字段不同） | 见下方                          |

### Event Type (事件类型)

| 类型     | 描述                     |
| -------- | ------------------------ |
| `camp`   | 营地事件（参与营地班级） |
| `match`  | 比赛事件                 |
| `custom` | 自定义事件               |

### Event Data 字段（按类型）

#### camp 类型

| 字段     | 类型   | 描述          | 示例         |
| -------- | ------ | ------------- | ------------ |
| CampID   | int    | 营地班级 ID   | `11115`      |
| CampSlug | string | 营地班级 Slug | `"J1J9Eqal"` |

#### match 类型

| 字段    | 类型 | 描述    | 示例   |
| ------- | ---- | ------- | ------ |
| MatchID | int  | 比赛 ID | `1001` |

---

## User Object 字段说明

### 用户列表 (List) 返回字段

| 字段         | 类型   | 描述                     | 示例                 |
| ------------ | ------ | ------------------------ | -------------------- |
| Uid          | string | 用户唯一 ID              | `"63485076"`         |
| Name         | string | 姓名                     | `"张三"`             |
| Gender       | int    | 性别：0=未知, 1=男, 2=女 | `1`                  |
| Phone        | string | 手机号（带区号）         | `"+8613800138000"`   |
| Birthday     | string | 生日，格式 YYYYMMDD      | `"20100630"`         |
| Email        | string | 邮箱                     | `"test@example.com"` |
| Organization | string | 学校/组织                | `"深圳中学"`         |

### AccountInfo (账号信息)

| 字段     | 类型   | 描述       | 示例                   |
| -------- | ------ | ---------- | ---------------------- |
| Uid      | string | 用户 ID    | `"94475740"`           |
| CreateAt | int    | 注册时间戳 | `1745376859`           |
| Phone    | string | 注册手机号 | `"+8613800138000"`     |
| ArenaUid | string | 创想家 UID | `"563458201446514688"` |
| Channel  | string | 注册渠道   | `"tcamp"`              |
| AddType  | string | 注册方式   | `"Web-H5"`             |
| Source   | string | 来源       | `"tcamp"`              |

### BasicInfo (基础信息)

| 字段         | 类型   | 描述                     | 示例                            |
| ------------ | ------ | ------------------------ | ------------------------------- |
| Name         | string | 姓名                     | `"张三"`                        |
| NickName     | string | 昵称                     | `"小张"`                        |
| Avatar       | string | 头像 URL                 | `"https://xxx/avatar.jpg"`      |
| Gender       | int    | 性别：0=未知, 1=男, 2=女 | `1`                             |
| Phone        | string | 手机号（带区号）         | `"+8613800138000"`              |
| Email        | string | 邮箱                     | `"test@example.com"`            |
| Province     | string | 省份                     | `"广东省"`                      |
| City         | string | 城市                     | `"深圳市"`                      |
| Birthday     | string | 生日，格式 YYYYMMDD      | `"20100630"`                    |
| Organization | string | 学校/组织                | `"深圳中学"`                    |
| Category     | string | 身份类型                 | `"初中生"`                      |
| BindWx       | bool   | 是否绑定微信             | `true`                          |
| WxName       | string | 微信昵称                 | `"微信昵称"`                    |
| BindQQ       | bool   | 是否绑定 QQ              | `false`                         |
| QQName       | string | QQ 昵称                  | `""`                            |
| ContactPhone | string | 联系手机                 | `"+8613900139000"`              |
| ContactEmail | string | 联系邮箱                 | `"contact@example.com"`         |
| Resume       | string | 简历信息（JSON 字符串）  | `"{\"filename\":\"简历.pdf\"}"` |

### Category (身份类型) 可选值

| 值           | 描述         |
| ------------ | ------------ |
| 小学生       | 小学生       |
| 初中生       | 初中生       |
| 高中生       | 高中生       |
| 大学生及以上 | 大学生及以上 |
| 教师         | 教师         |
| 其他         | 其他         |

---

## 使用示例

### cURL

```bash
# 搜索用户
curl -X POST 'https://tcampos.qq.com/api/profile/listUser' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: tipe_token=YOUR_TOKEN' \
  -d '{
    "Filter": {"NameOrUid": "张三"},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": ["-UpdateAt"]
  }'

# 获取用户详情
curl -X GET 'https://tcampos.qq.com/api/profile/user/63485076' \
  -H 'Cookie: tipe_token=YOUR_TOKEN'
```

### Python

```python
from tcampos_api import get_api_client

api = get_api_client()

# 搜索用户
users = api.post("/profile/listUser", {
    "Filter": {"NameOrUid": "张三"},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": ["-UpdateAt"]
})

for user in users['Response']['Result']['Entries']:
    print(f"用户 {user['Uid']}: {user['Name']}")

# 获取用户详情
detail = api.get("/profile/user/63485076")
print(detail['Response']['Result'])
```

### 命令行脚本

```bash
# 搜索用户（按姓名或 UID）
python3 scripts/list_user.py list --search "张三"

# 按手机号查询
python3 scripts/list_user.py list --phone "13800138000"

# 按学校查询
python3 scripts/list_user.py list --org "深圳中学"

# 按营地 ID 查询参与过的用户
python3 scripts/list_user.py list --camp-id 11103

# 获取用户详情
python3 scripts/list_user.py get 63485076

# 查询用户事件（所有类型）
python3 scripts/list_user_event.py --uid 23892136

# 只查询营地事件
python3 scripts/list_user_event.py --uid 23892136 --type camp

# 查询营地和比赛事件
python3 scripts/list_user_event.py --uid 23892136 --type camp match

# 输出原始 JSON
python3 scripts/list_user.py list --search "张三" --raw
python3 scripts/list_user.py get 63485076 --raw
python3 scripts/list_user_event.py --uid 23892136 --raw
```

---

## 常见使用场景

### 1. 按手机号查找用户

```python
import sys
sys.path.insert(0, '.codebuddy/skills/tcampos/scripts')
from list_user import list_users, get_user_detail

# 按手机号搜索
result = list_users(phone="13800138000")
users = result['Response']['Result']['Entries']

if users:
    uid = users[0]['Uid']
    # 获取详情
    detail = get_user_detail(uid)
    print(detail['Response']['Result'])
```

### 2. 查找某营地的所有用户

```python
# 查找参与营地 11103 的用户
result = list_users(in_camp_list=[11103], page_size=50)
users = result['Response']['Result']['Entries']

for user in users:
    print(f"{user['Name']} ({user['Uid']})")
```

### 3. 按学校统计用户

```python
# 查找某学校的用户
result = list_users(organization="深圳中学", page_size=50)
total = result['Response']['Result']['Total']
print(f"深圳中学共有 {total} 名用户")
```

### 4. 查询用户参与过的营地

```python
import sys
sys.path.insert(0, '.codebuddy/skills/tcampos/scripts')
from list_user_event import list_user_events

# 获取用户的营地事件
result = list_user_events(uid="23892136", type_list=["camp"])
events = result['Response']['Result']['Entries']

print(f"用户参与过 {len(events)} 个营地:")
for event in events:
    print(f"  - {event['Title']} (ID: {event['Data'].get('CampID')})")
```
