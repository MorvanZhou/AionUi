# TCampos API - 报名筛选流程 (Selection Process)

## 概述

本模块提供营地报名筛选流程相关的 API，包括：

- 获取筛选流程信息
- 导出报名记录
- 导出笔试/考试记录
- 导出面试记录

---

## Get Selection Process (获取筛选流程)

获取营地的报名筛选流程信息，包括各环节状态和统计数据。

**Endpoint**: `GET https://tcampos.qq.com/api/camp/:camp_id/selectProcess`

### Request

| 参数    | 类型   | 必填 | 描述                  | 示例  |
| ------- | ------ | ---- | --------------------- | ----- |
| camp_id | uint32 | Y    | 营地ID（URL路径参数） | 10233 |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "...",
    "Result": {
      "CampJoinMode": 1,
      "Items": [
        {
          "Detail": null,
          "EndAt": 1731254399,
          "Name": "报名",
          "StartAt": 1729612800,
          "State": 2,
          "Type": 1,
          "UserNumPassed": 100,
          "UserNumTotal": 500
        },
        {
          "Detail": null,
          "EndAt": 1732000000,
          "Name": "笔试",
          "StartAt": 1731300000,
          "State": 1,
          "Type": 2,
          "UserNumPassed": 50,
          "UserNumTotal": 100
        }
      ],
      "Summary": {
        "SignupNumTotal": 500,
        "UserNumPassed": 50
      }
    }
  }
}
```

### Result Object 字段说明

| 字段         | 类型   | 描述                                             |
| ------------ | ------ | ------------------------------------------------ |
| CampJoinMode | uint32 | 营地参与方式：1=直接加入, 2=需要审核, 3=筛选流程 |
| Items        | array  | 筛选环节列表                                     |
| Summary      | object | 数据汇总                                         |

### Item Object 字段说明

| 字段          | 类型   | 描述                                          | 示例                   |
| ------------- | ------ | --------------------------------------------- | ---------------------- |
| Name          | string | 环节名称                                      | "报名"、"笔试"、"面试" |
| Type          | uint32 | 环节类型：1=报名, 2=笔试/考试, 3=面试, 4=录取 | 1                      |
| State         | uint32 | 环节状态：0=未开始, 1=进行中, 2=已结束        | 2                      |
| StartAt       | int64  | 开始时间（Unix时间戳）                        | 1729612800             |
| EndAt         | int64  | 结束时间（Unix时间戳）                        | 1731254399             |
| UserNumPassed | int    | 该环节通过人数                                | 100                    |
| UserNumTotal  | int    | 该环节总人数                                  | 500                    |
| Detail        | object | 环节详情（可为null）                          | null                   |

### Summary Object 字段说明

| 字段           | 类型 | 描述                         |
| -------------- | ---- | ---------------------------- |
| SignupNumTotal | int  | 总报名人数                   |
| UserNumPassed  | int  | 最终通过人数（完成所有环节） |

---

## Export Signup Records (导出报名记录)

导出营地的报名记录到 Excel 文件。

**Endpoint**: `POST https://tcampos.qq.com/api/camp/exportSignupRecords`

### Request

```json
{
  "Mode": 1,
  "CampID": 11264,
  "OpStatusList": [],
  "ChannelList": [],
  "BatchList": []
}
```

| 字段         | 类型   | 必填 | 描述             |
| ------------ | ------ | ---- | ---------------- |
| CampID       | uint32 | Y    | 营地ID           |
| Mode         | int    | N    | 导出模式，默认 1 |
| OpStatusList | array  | N    | 按操作状态筛选   |
| ChannelList  | array  | N    | 按渠道筛选       |
| BatchList    | array  | N    | 按批次筛选       |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "95c6430945ae434bbed95338a85cf93e",
    "Result": {
      "Entries": null,
      "SheetURL": "https://tencent-tech-camp-1306124692.cos.ap-guangzhou.myqcloud.com/tlearn/export/prod/11264_营地名称_报名表.xlsx"
    }
  }
}
```

### Result Object 字段说明

| 字段     | 类型   | 描述                      |
| -------- | ------ | ------------------------- |
| SheetURL | string | Excel 文件下载链接        |
| Entries  | array  | 数据条目（导出时为 null） |

---

## Export Exam Records (导出考试记录)

导出营地的笔试/考试记录到 Excel 文件。

**Endpoint**: `POST https://tcampos.qq.com/api/exam/exportUserExamRecords`

### Request

```json
{
  "CampID": 11104,
  "OpStatus": [],
  "ToSheet": true
}
```

| 字段     | 类型   | 必填 | 描述                       |
| -------- | ------ | ---- | -------------------------- |
| CampID   | uint32 | Y    | 营地ID                     |
| OpStatus | array  | N    | 按操作状态筛选             |
| ToSheet  | bool   | N    | 是否导出为Excel，默认 true |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "7b5cb71cf6304dc0a37ccdd7143e60e8",
    "Result": {
      "Entries": null,
      "SheetURL": "https://tencent-tech-camp-1306124692.cos.ap-guangzhou.myqcloud.com/tlearn/export/prod/11104_营地名称_考试记录表.xlsx"
    }
  }
}
```

---

## Export Interview Records (导出面试记录)

导出营地的面试记录到 Excel 文件。

**Endpoint**: `POST https://tcampos.qq.com/api/interview/exportUserInterviewRecords`

### Request

```json
{
  "Mode": 1,
  "CampID": 11104,
  "OpStatus": []
}
```

| 字段     | 类型   | 必填 | 描述             |
| -------- | ------ | ---- | ---------------- |
| CampID   | uint32 | Y    | 营地ID           |
| Mode     | int    | N    | 导出模式，默认 1 |
| OpStatus | array  | N    | 按操作状态筛选   |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "...",
    "Result": {
      "Entries": null,
      "SheetURL": "https://tencent-tech-camp-1306124692.cos.ap-guangzhou.myqcloud.com/tlearn/export/prod/11104_营地名称_面试记录表.xlsx"
    }
  }
}
```

---

## 使用示例

### Python

```python
from tcampos_api import get_api_client

api = get_api_client()

# 获取筛选流程
process = api.get("/camp/11264/selectProcess")
print(f"总报名: {process['Response']['Result']['Summary']['SignupNumTotal']}")

# 导出报名记录
signup_export = api.post("/camp/exportSignupRecords", {
    "Mode": 1,
    "CampID": 11264,
    "OpStatusList": [],
    "ChannelList": [],
    "BatchList": []
})
print(f"报名表: {signup_export['Response']['Result']['SheetURL']}")

# 导出考试记录
exam_export = api.post("/exam/exportUserExamRecords", {
    "CampID": 11264,
    "OpStatus": [],
    "ToSheet": True
})

# 导出面试记录
interview_export = api.post("/interview/exportUserInterviewRecords", {
    "Mode": 1,
    "CampID": 11264,
    "OpStatus": []
})
```

### 命令行

```bash
# 查看筛选流程
python3 scripts/select_process.py --camp-id 11264

# 导出所有数据到当前目录
python3 scripts/select_process.py --camp-id 11264 --export all

# 导出报名记录到指定目录
python3 scripts/select_process.py --camp-id 11264 --export signup --output ./data/
```

---

## 文件下载说明

导出 API 返回的 `SheetURL` 是一个 COS 文件链接，可以直接下载。使用 `select_process.py` 脚本时会自动下载到本地。

**下载位置**：

- 默认下载到当前工作目录
- 使用 `--output` 参数指定下载目录
- 使用 `--no-download` 参数只获取 URL 不下载
