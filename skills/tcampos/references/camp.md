# TCampos API - 营地班级

## List Camps (查询营地班级列表)

查询营地班级列表。

**Endpoint**: `POST https://tcampos.qq.com/api/camp/listCamp`

### Request

```json
{
  "Filter": {
    "Name": "",
    "UpdateAtFrom": 0,
    "UpdateAtTo": 0
  },
  "PageSize": 20,
  "PageNum": 1,
  "Sort": []
}
```

**按 Slug 精准搜索**（可选）：

```json
{
  "Filter": {
    "CampSlugList": ["NRp5lExN", "ucCjXKl0"]
  },
  "PageSize": 20,
  "PageNum": 1,
  "Sort": []
}
```

**按主题营筛选**（可选）：

```json
{
  "Filter": {
    "TopicName": "Mini鹅"
  },
  "PageSize": 20,
  "PageNum": 1,
  "Sort": []
}
```

| 字段                | 类型     | 必填 | 描述                                |
| ------------------- | -------- | ---- | ----------------------------------- |
| Filter.Name         | string   | ❌   | 营地名称过滤（模糊匹配）            |
| Filter.TopicName    | string   | ❌   | 主题营名称过滤（模糊匹配）          |
| Filter.CampSlugList | []string | ❌   | 营地 Slug 列表（精准匹配，类似 ID） |
| Filter.UpdateAtFrom | int      | ❌   | 更新时间起始（Unix 时间戳）         |
| Filter.UpdateAtTo   | int      | ❌   | 更新时间截止（Unix 时间戳）         |
| PageSize            | int      | ✅   | 每页数量（默认 20）                 |
| PageNum             | int      | ✅   | 页码（从 1 开始）                   |
| Sort                | array    | ❌   | 排序选项                            |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "...",
    "Result": {
      "Entries": [...],
      "Total": 100
    },
    "Timestamp": 1234567890
  }
}
```

---

## Camp Object 字段说明

| 字段             | 类型        | 必需 | 描述                                                                                             | 示例                               |
| ---------------- | ----------- | ---- | ------------------------------------------------------------------------------------------------ | ---------------------------------- |
| ID               | int         | -    | 营地唯一标识                                                                                     | 11196                              |
| Slug             | string      | -    | 营地字符串短标识（后台生成）                                                                     | "ucCjXKl0"                         |
| Name             | string      | ✅   | 营地名称                                                                                         | "活动xx报名"                       |
| Type             | uint        | -    | 营地类型：1-线上营（默认），2-线下营                                                             | 1                                  |
| Scope            | uint        | -    | 可见范围：1-公开（默认），2-仅链接                                                               | 2                                  |
| ExpireMode       | uint        | -    | 过期模式：1-长期有效（默认），2-需设置报名时间和活动时间                                         | 2                                  |
| JoinMode         | uint        | -    | 参与方式：1-报名即入营（默认），2-报名筛选后参加（所有筛选流程），3-报名筛选后参加（仅报名流程） | 1                                  |
| BannerURL        | string      | -    | 头图 URL                                                                                         | "https://static.tcamp.qq.com/..."  |
| PlanID           | uint32      | -    | 方案 ID                                                                                          | 15                                 |
| PlanName         | string      | -    | 方案名称（仅外显）                                                                               | "Mini鹅科创营地"                   |
| CreateAt         | int         | -    | 数据创建时间（Unix 时间戳，秒）                                                                  | 1768965883                         |
| CreateBy         | string      | -    | 数据创建者的用户 ID                                                                              | "10961349"                         |
| CreatorName      | string      | -    | 数据创建者的名称（仅外显）                                                                       | "cherry"                           |
| UpdateAt         | int         | -    | 修改时间（Unix 时间戳，秒）                                                                      | 1770277666                         |
| ShowStatus       | int         | -    | 上架状态：0-未上架/已下架（默认），1-已上架                                                      | 1                                  |
| ShowAt           | int         | -    | 上架时间（Unix 时间戳，秒）                                                                      | 1768965984                         |
| SignupIntro      | string      | ✅   | 报名介绍                                                                                         | ""                                 |
| SignupStartAt    | int         | -    | 报名开始时间（Unix 时间戳，秒）                                                                  | 1770134400                         |
| SignupEndAt      | int         | -    | 报名结束时间（Unix 时间戳，秒）                                                                  | 1774972799                         |
| SignupFormSchema | string      | -    | 报名表单 schema                                                                                  | ""                                 |
| SignupNum        | int         | -    | 已报名数（人数）                                                                                 | 4                                  |
| SignupSuccNum    | int         | -    | 报名成功数（人数）                                                                               | 4                                  |
| ActionStartAt    | int         | -    | 活动开始时间（Unix 时间戳，秒）                                                                  | 1770134400                         |
| ActionEndAt      | int         | -    | 活动结束时间（Unix 时间戳，秒）                                                                  | 1774972799                         |
| ActionAddr       | string      | -    | 活动地址，当 Type=2 时必填                                                                       | "{xxxx}"                           |
| ActionCity       | string      | -    | 活动城市，从 ActionAddr 提取                                                                     | "广州市"                           |
| JoinPrompt       | int         | -    | 入营提示：0-不提示，1-提示                                                                       | 0                                  |
| JoinWording      | string      | -    | 入营提示语，当 JoinPrompt>0 时必填                                                               | "welcome"                          |
| JoinQrcode       | string      | -    | 入营二维码，当 JoinPrompt>0 时必填                                                               | "https://xxxxx"                    |
| ExtInfo          | string      | -    | 扩展信息（存储非必需的、无业务逻辑的字段）                                                       | "{\"Field1\":\"Val1\"}"            |
| RecomWeight      | int         | -    | 推荐权重                                                                                         | 1                                  |
| Topics           | array       | -    | 关联主题列表                                                                                     | [{"Name": "AI Agent智能体主题营"}] |
| TopicIDs         | []uint      | -    | 主题数字 ID 列表                                                                                 | [1, 2]                             |
| Bizs             | array\|null | -    | 业务关联对象                                                                                     | null                               |
| BizIDs           | string      | -    | 关联业务信息的 ID 列表（逗号分隔）                                                               | "42,16,1"                          |
| InCollection     | any         | -    | 是否在收藏中                                                                                     | null                               |

---

## JoinMode 参与方式详解

| 值  | 说明                                                                                                       |
| --- | ---------------------------------------------------------------------------------------------------------- |
| 1   | **报名即入营**：用户报名后直接成为营地成员                                                                 |
| 2   | **报名筛选后参加（所有筛选流程）**：可在筛选流程中添加笔试、面试等环节，活动开始时间必须在报名结束时间之后 |
| 3   | **报名筛选后参加（仅报名流程）**：仅有报名的筛选流程，允许活动开始时间可以早于报名结束时间，允许重合       |

---

## Topics 子对象

| 字段 | 类型   | 描述     |
| ---- | ------ | -------- |
| Name | string | 主题名称 |

---

## 使用示例

### cURL

```bash
curl -X POST 'https://tcampos.qq.com/api/camp/listCamp' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: tipe_token=<YOUR_TOKEN>' \
  -d '{
    "Filter": {"Name": "未来"},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": []
  }'
```

### Python

```python
from tcampos_api import get_api_client

api = get_api_client()

# 按名称模糊搜索
camps = api.post("/camp/listCamp", {
    "Filter": {"Name": "未来", "UpdateAtFrom": 0, "UpdateAtTo": 0},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": []
})

# 按 Slug 精准搜索
camps = api.post("/camp/listCamp", {
    "Filter": {"CampSlugList": ["NRp5lExN"]},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": []
})

# 按主题营名称搜索
camps = api.post("/camp/listCamp", {
    "Filter": {"TopicName": "Mini鹅"},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": []
})

for camp in camps['Response']['Result']['Entries']:
    print(f"{camp['ID']}: {camp['Name']} - 报名人数: {camp['SignupNum']}")
```
