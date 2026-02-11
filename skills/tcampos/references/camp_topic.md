# TCampos API - 主题营

## List Camp Topics (查询主题营列表)

查询主题营/营地主题列表。

**Endpoint**: `POST https://tcampos.qq.com/api/camp/listCampTopic`

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

| 字段                | 类型   | 必填 | 描述                        |
| ------------------- | ------ | ---- | --------------------------- |
| Filter.Name         | string | ❌   | 主题名称过滤（模糊匹配）    |
| Filter.UpdateAtFrom | int    | ❌   | 更新时间起始（Unix 时间戳） |
| Filter.UpdateAtTo   | int    | ❌   | 更新时间截止（Unix 时间戳） |
| PageSize            | int    | ✅   | 每页数量（默认 20）         |
| PageNum             | int    | ✅   | 页码（从 1 开始）           |
| Sort                | array  | ❌   | 排序选项                    |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "...",
    "Result": {
      "Entries": [...],
      "Total": 50
    },
    "Timestamp": 1234567890
  }
}
```

---

## Camp Topic Object 字段说明

| 字段            | 类型        | 必需 | 描述                                       | 示例                              |
| --------------- | ----------- | ---- | ------------------------------------------ | --------------------------------- |
| ID              | int         | -    | 主题唯一标识                               | 56                                |
| Slug            | string      | ✅   | 英文唯一标识（唯一）                       | "ai-agent"                        |
| Name            | string      | ✅   | 主题名称                                   | "AI Agent智能体主题营"            |
| BannerURL       | string      | -    | 头图 URL                                   | "https://static.tcamp.qq.com/..." |
| CoverURL        | string      | -    | 封面图 URL                                 | "https://static.tcamp.qq.com/..." |
| Desc            | string      | -    | 详细描述                                   | ""                                |
| Intro           | string      | -    | 短介绍                                     | ""                                |
| ExtInfo         | string      | -    | 扩展信息（存储非必需的、无业务逻辑的字段） | "{\"Field1\":\"Val1\"}"           |
| Scope           | int         | -    | 可见范围：1-公开，2-仅链接                 | 1                                 |
| ShowStatus      | int         | -    | 上架状态：0-未上架/下架（默认），1-已上架  | 1                                 |
| ShowAt          | int         | -    | 上架时间（Unix 时间戳，秒）                | 1733379154                        |
| CreateAt        | int         | -    | 创建时间（Unix 时间戳，秒）                | 1733379154                        |
| UpdateAt        | int         | -    | 修改时间（Unix 时间戳，秒）                | 1770089405                        |
| CreateBy        | string      | -    | 创建者用户 ID                              | "10961349"                        |
| CreatorName     | string      | -    | 创建者名称（仅外显）                       | "cherry"                          |
| BizIDs          | []uint      | -    | 业务数字 ID 列表                           | [1, 2]                            |
| Bizs            | array\|null | -    | 业务关联对象                               | null                              |
| ConfigJson      | any         | -    | 配置 JSON                                  | null                              |
| RelatedCamps    | array       | -    | 关联的营地班级列表                         | 见下方 RelatedCamps 子对象        |
| RelatedCampsNum | int         | -    | 关联营地班级数量                           | 3                                 |

---

## RelatedCamps 子对象

| 字段      | 类型   | 描述             |
| --------- | ------ | ---------------- |
| ID        | int    | 营地班级 ID      |
| Name      | string | 营地班级名称     |
| Slug      | string | 营地班级短标识   |
| BannerURL | string | 营地班级头图 URL |

---

## 使用示例

### cURL

```bash
curl -X POST 'https://tcampos.qq.com/api/camp/listCampTopic' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: tipe_token=<YOUR_TOKEN>' \
  -d '{
    "Filter": {"Name": "AI Agent"},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": []
  }'
```

### Python

```python
from tcampos_api import get_api_client

api = get_api_client()

# 查询主题营
topics = api.post("/camp/listCampTopic", {
    "Filter": {"Name": "", "UpdateAtFrom": 0, "UpdateAtTo": 0},
    "PageSize": 20,
    "PageNum": 1,
    "Sort": []
})

for topic in topics['Response']['Result']['Entries']:
    print(f"{topic['ID']}: {topic['Name']} - 关联营地: {topic['RelatedCampsNum']}个")
    for camp in topic.get('RelatedCamps', []):
        print(f"  - {camp['Name']}")
```
