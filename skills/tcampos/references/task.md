# TCampos API - 任务管理 (Task)

## 目录

- [List Camp Tasks (查询营地任务列表)](#list-camp-tasks-查询营地任务列表)
- [List User Task Records (查询用户任务完成情况)](#list-user-task-records-查询用户任务完成情况)
- [Export Task Records (导出任务记录)](#export-task-records-导出任务记录)
- [Task Object 字段说明](#task-object-字段说明)
- [用户任务数据表 Excel 字段说明](#用户任务数据表-excel-字段说明)

---

## List Camp Tasks (查询营地任务列表)

查询指定营地班级中的所有任务及其进度。

**Endpoint**: `POST https://tcampos.qq.com/api/task/listCampTask`

### Request

```json
{
  "CampID": 11103,
  "Filter": {
    "Name": "",
    "TypeList": []
  },
  "PageSize": 20,
  "PageNum": 1,
  "Sort": []
}
```

| 字段            | 类型     | 必填 | 描述                                             |
| --------------- | -------- | ---- | ------------------------------------------------ |
| CampID          | int      | ✓    | 营地班级 ID                                      |
| Filter          | object   | ✓    | 过滤条件                                         |
| Filter.Name     | string   |      | 任务名称模糊搜索                                 |
| Filter.TypeList | string[] |      | 任务类型过滤，可选类型见 [Task Type](#task-type) |
| PageSize        | int      |      | 每页数量，默认 20                                |
| PageNum         | int      |      | 页码，从 1 开始                                  |
| Sort            | array    |      | 排序条件                                         |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "4fd379324bf645faa9dccd26a24f6cd1",
    "Result": {
      "Entries": [
        {
          "ID": 3406,
          "Name": "【重要】入营协议签署与身份证号收集",
          "Progress": {
            "Doing": 0,
            "Done": 25,
            "NotStart": 1,
            "StartDoneRatio": 1,
            "Total": 26,
            "TotalDoneRatio": 0.9615384615384616
          },
          "Required": true,
          "Type": "homework"
        }
      ],
      "Total": 9
    },
    "Timestamp": 1770352614
  }
}
```

---

## List User Task Records (查询用户任务完成情况)

分页查询指定任务的所有用户完成情况数据。

**Endpoint**: `POST https://tcampos.qq.com/api/task/listUserTaskRecord`

### Request

```json
{
  "TaskID": 1162,
  "Filter": {
    "Keyword": "",
    "UserName": "",
    "OpStatus": [2],
    "Exercise": {
      "PassStatusList": []
    },
    "Creation": {}
  },
  "PageSize": 20,
  "PageNum": 1,
  "Sort": []
}
```

| 字段            | 类型   | 必填 | 描述                                                              |
| --------------- | ------ | ---- | ----------------------------------------------------------------- |
| TaskID          | int    | ✓    | 任务 ID                                                           |
| Filter          | object | ✓    | 过滤条件                                                          |
| Filter.Keyword  | string |      | 关键词搜索（用户名、ID等）                                        |
| Filter.UserName | string |      | 用户名精确搜索                                                    |
| Filter.OpStatus | int[]  |      | 按完成状态过滤，见下方状态值说明。0: 未开始, 1: 进行中, 2: 已完成 |
| Filter.Exercise | object |      | 作业类任务的过滤条件（PassStatusList: 审批状态）                  |
| Filter.Creation | object |      | 作品提交任务的过滤条件                                            |
| PageSize        | int    |      | 每页数量，默认 20                                                 |
| PageNum         | int    |      | 页码，从 1 开始                                                   |
| Sort            | array  |      | 排序条件                                                          |

### OpStatus 完成状态值

| 值  | 描述          |
| --- | ------------- |
| 0   | 未开始        |
| 1   | 进行中/待审核 |
| 2   | 已完成/已通过 |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "abc123def456",
    "Result": {
      "Entries": [
        {
          "Uid": "30111610",
          "UserName": "shangrui",
          "OpStatus": 2,
          "StartAt": 1750042149,
          "FinishAt": 1758766682,
          "Progress": 100
        }
      ],
      "Progress": {
        "Total": 17912,
        "Done": 885,
        "Doing": 0,
        "NotStart": 17027,
        "TotalDoneRatio": 0.0494,
        "StartDoneRatio": 0
      },
      "Total": 885
    },
    "Timestamp": 1705200000
  }
}
```

## UserTaskRecord Object 字段说明

| 字段     | 类型   | 描述                        | 示例                            |
| -------- | ------ | --------------------------- | ------------------------------- |
| Uid      | string | 用户 ID                     | `"30111610"`                    |
| UserName | string | 用户名                      | `"shangrui"`                    |
| OpStatus | int    | 任务完成状态                | 0：未开始，1：进行中，2：已完成 |
| StartAt  | int    | 开始时间戳                  | `1750042149`                    |
| FinishAt | int    | 完成时间戳                  | `1758766682`                    |
| Progress | int    | 任务完成进度百分比（0-100） | `100` 表示 100%                 |

---

## Task Object 字段说明

| 字段     | 类型   | 描述                 | 示例                                   |
| -------- | ------ | -------------------- | -------------------------------------- |
| ID       | int    | 任务唯一 ID          | `3406`                                 |
| Name     | string | 任务名称             | `"【重要】入营协议签署与身份证号收集"` |
| Type     | string | 任务类型             | 可选类型见 [Task Type](#task-type)     |
| Required | bool   | 是否为必修(应学)任务 | `true`                                 |
| Progress | object | 任务进度统计         | 见下方                                 |

### Progress Object 字段说明

| 字段           | 类型  | 描述                                                                                                 | 示例     |
| -------------- | ----- | ---------------------------------------------------------------------------------------------------- | -------- |
| Total          | int   | 应完成该任务的总人数                                                                                 | `26`     |
| Done           | int   | 已完成人数                                                                                           | `25`     |
| Doing          | int   | 进行中人数                                                                                           | `0`      |
| NotStart       | int   | 未开始人数                                                                                           | `1`      |
| TotalDoneRatio | float | 总体完成率：所有人中（包括开始学习和未开始学习的），有多少人完成了这个任务。计算公式：`Done / Total` | `0.9615` |
| StartDoneRatio | float | 已开始用户完成率：在已开始学习的人中，有多少人完成了这个任务。计算公式：`Done / (Done + Doing)`      | `1.0`    |

#### 完成率计算说明

- **TotalDoneRatio（总体完成率）**：衡量所有应学用户的整体完成情况
  - 分子：已完成人数（Done）
  - 分母：总营地学员人数（Total = Done + Doing + NotStart）
  - 示例：25 / 26 = 0.9615（约 96.15%）

- **StartDoneRatio（已开始用户完成率）**：衡量已投入学习的用户最终完成的比例
  - 分子：已完成人数（Done）
  - 分母：已开始学习的人数（Done + Doing）
  - 示例：25 / (25 + 0) = 1.0（100%）
  - 注意：如果所有开始的人都完成了，该值为 1.0；如果没人开始，该值可能为 0 或 NaN

### **Task Types (任务类型)**

| 类型       | 描述                               |
| ---------- | ---------------------------------- |
| `homework` | 作业任务（用户提交的作业数据表单） |
| `creation` | 作品上传任务                       |
| `article`  | 图文任务                           |
| `material` | 资料、文档任务                     |
| `video`    | 视频任务                           |
| `audio`    | 音频任务                           |
| `link`     | 链接任务                           |

> **⚠️ 重要说明：在按任务类型筛选的时候**
>
> **正确的视频任务筛选逻辑**：
>
> ```python
> def is_video_task(task):
>     return task.get('Type') == 'video'  # 按作品类型筛选
> ```

---

## Export Task Records (导出任务记录)

导出指定任务的用户完成记录到 Excel。

**Endpoint**: `POST https://tcampos.qq.com/api/task/exportUserTaskRecords`

### Request

```json
{
  "TaskID": 3406,
  "OpStatus": [],
  "Mode": 1
}
```

| 字段     | 类型  | 必填 | 描述                    |
| -------- | ----- | ---- | ----------------------- |
| TaskID   | int   | ✓    | 任务 ID                 |
| OpStatus | int[] |      | 按状态过滤，如 `[1, 2]` |
| Mode     | int   |      | 导出模式，默认 1        |

### OpStatus 状态值

| 值  | 描述          |
| --- | ------------- |
| 0   | 未开始        |
| 1   | 进行中/待审核 |
| 2   | 已完成/已通过 |
| 3   | 已拒绝/未通过 |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "64a8c96ec74e48ba9f4fdc0a68751d4a",
    "Result": {
      "Entries": null,
      "SheetURL": "https://tencent-tech-camp-1306124692.cos.ap-guangzhou.myqcloud.com/tlearn/export/prod/11103_AI小程序开发|2026腾讯MINI鹅冬季线下科创营_3406_用户任务数据表.xlsx",
      "Total": 26
    },
    "Timestamp": 1770352388
  }
}
```

---

## 用户任务数据表 Excel 字段说明

导出文件名格式：`{CampID}_{CampName}_{TaskID}_用户任务数据表.xlsx`

### 文件结构

| 行号    | 内容                     |
| ------- | ------------------------ |
| 第1行   | 说明信息（操作注意事项） |
| 第2行   | 字段名/表头              |
| 第3行起 | 数据行                   |

### 第一行说明信息示例

```
请阅读以下注意事项：
1. 如果该任务为作业，用户重复提交作业时，完成时间也会更新为最新的提交时间；
2. 任务完成率是以小数记录，0 意味着 0%，1 意味着 100%。
```

### 通用字段

| 字段名                                   | 类型     | 描述                         |
| ---------------------------------------- | -------- | ---------------------------- |
| `*操作(2-通过, 3-拒绝)`                  | int      | 操作码（用于批量审批）       |
| `*用户 ID`                               | string   | 用户唯一标识（**关键字段**） |
| `当前状态(0-未开始, 1-进行中, 2-已完成)` | int      | 任务完成状态                 |
| `开始时间`                               | datetime | 用户开始任务的时间           |
| `完成时间`                               | datetime | 用户完成任务的时间           |
| `完成率`                                 | float    | 任务完成进度 (0~1)           |
| `姓名`                                   | string   | 用户姓名                     |

### 动态字段

根据任务类型不同，可能包含以下动态字段：

| 字段类型 | 示例                                  | 描述                                     |
| -------- | ------------------------------------- | ---------------------------------------- |
| 表单字段 | `学员身份证号`                        | 作业任务中的自定义表单字段               |
| 附件字段 | `入营协议签署与上传_附件1` ~ `_附件6` | 用户上传的附件文件名（可能带 hyperlink） |

---

## 使用示例

### cURL

```bash
# 查询营地任务列表
curl -X POST 'https://tcampos.qq.com/api/task/listCampTask' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: tipe_token=YOUR_TOKEN' \
  -d '{
    "CampID": 11103,
    "Filter": {"Name": "", "TypeList": []},
    "PageSize": 100,
    "PageNum": 1,
    "Sort": []
  }'

# 查询用户任务完成情况（只查询已完成的）
curl -X POST 'https://tcampos.qq.com/api/task/listUserTaskRecord' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: tipe_token=YOUR_TOKEN' \
  -d '{
    "TaskID": 1162,
    "Filter": {"Keyword": "", "UserName": "", "OpStatus": [2], "Exercise": {"PassStatusList": []}, "Creation": {}},
    "PageSize": 100,
    "PageNum": 1,
    "Sort": []
  }'

# 导出任务记录
curl -X POST 'https://tcampos.qq.com/api/task/exportUserTaskRecords' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: tipe_token=YOUR_TOKEN' \
  -d '{
    "TaskID": 3406,
    "OpStatus": [],
    "Mode": 1
  }'
```

### Python

```python
from tcampos_api import get_api_client

api = get_api_client()

# 查询营地任务列表
tasks = api.post("/task/listCampTask", {
    "CampID": 11103,
    "Filter": {"Name": "", "TypeList": []},
    "PageSize": 100,
    "PageNum": 1,
    "Sort": []
})

# 遍历任务
for task in tasks['Response']['Result']['Entries']:
    print(f"任务 {task['ID']}: {task['Name']}")
    print(f"  类型: {task['Type']}, 必修: {task['Required']}")
    print(f"  完成率: {task['Progress']['TotalDoneRatio']*100:.1f}%")

# 查询用户任务完成情况（分页查询已完成的用户）
user_records = api.post("/task/listUserTaskRecord", {
    "TaskID": 1162,
    "Filter": {"Keyword": "", "UserName": "", "OpStatus": [2], "Exercise": {"PassStatusList": []}, "Creation": {}},
    "PageSize": 100,
    "PageNum": 1,
    "Sort": []
})

# 遍历用户完成情况
for record in user_records['Response']['Result']['Entries']:
    print(f"用户 {record['Uid']} ({record['UserName']}): 状态={record['OpStatus']}, 完成率={record['Progress']}")

# 导出指定任务的记录
export_result = api.post("/task/exportUserTaskRecords", {
    "TaskID": 3406,
    "OpStatus": [],
    "Mode": 1
})

sheet_url = export_result['Response']['Result']['SheetURL']
print(f"下载链接: {sheet_url}")
```

### 命令行脚本

```bash
# 查询营地任务列表
python3 scripts/list_camp_task.py --camp-id 11103

# 按任务名称筛选
python3 scripts/list_camp_task.py --camp-id 11103 --name "入营"

# 按任务类型筛选
python3 scripts/list_camp_task.py --camp-id 11103 --type homework

# 查询用户任务完成情况
python3 scripts/list_user_task_record.py --task-id 1162

# 查询已完成的用户
python3 scripts/list_user_task_record.py --task-id 1162 --status 2

# 查询进行中的用户
python3 scripts/list_user_task_record.py --task-id 1162 --status 1

# 按用户名搜索
python3 scripts/list_user_task_record.py --task-id 1162 --username "张三"

# 导出任务记录
python3 scripts/export_task_records.py --task-id 3406

# 导出到指定目录
python3 scripts/export_task_records.py --task-id 3406 --output ./downloads/

# 只导出已完成的记录
python3 scripts/export_task_records.py --task-id 3406 --status 2
```

---

## 常见使用场景

### 1. 分析营地任务完成情况

```python
import sys
sys.path.insert(0, '.codebuddy/skills/tcampos/scripts')
from list_camp_task import list_camp_task

result = list_camp_task(camp_id=11103)
tasks = result['Response']['Result']['Entries']

# 统计必修(应学)任务完成情况
required_tasks = [t for t in tasks if t['Required']]
for task in required_tasks:
    progress = task['Progress']
    print(f"{task['Name']}: {progress['Done']}/{progress['Total']} 已完成")
```

### 2. 批量导出所有作业任务记录

```python
import sys
sys.path.insert(0, '.codebuddy/skills/tcampos/scripts')
from list_camp_task import list_camp_task
from export_task_records import export_task_records

# 获取所有作业任务
result = list_camp_task(camp_id=11103, type_list=['homework'])
homework_tasks = result['Response']['Result']['Entries']

# 导出每个作业任务的记录
for task in homework_tasks:
    print(f"导出任务: {task['Name']}")
    export = export_task_records(task_id=task['ID'])
    print(f"  下载链接: {export['Response']['Result']['SheetURL']}")
```

### 3. 找出未完成任务的用户

```python
import openpyxl

# 读取任务数据表
wb = openpyxl.load_workbook('任务数据表.xlsx')
ws = wb.active

# 找出未完成的用户
headers = [ws.cell(2, col).value for col in range(1, ws.max_column + 1)]
status_col = None
for i, h in enumerate(headers):
    if '状态' in str(h):
        status_col = i + 1
        break

for row in range(3, ws.max_row + 1):
    status = ws.cell(row, status_col).value
    if status != 2:  # 非已完成状态
        user_id = ws.cell(row, 2).value
        name = ws.cell(row, 7).value
        print(f"用户 {user_id} ({name}): 状态={status}")
```
