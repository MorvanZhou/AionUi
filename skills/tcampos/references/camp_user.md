# TCampos API - 营地用户导出

## Export Camp Users (导出营地用户)

导出营地班级的学员/用户信息到 Excel 文件。

**Endpoint**: `POST https://tcampos.qq.com/api/camp/exportCampUser`

### Request

```json
{
  "CampID": 11103,
  "Mode": 1
}
```

| 字段   | 类型 | 必填 | 描述             |
| ------ | ---- | ---- | ---------------- |
| CampID | int  | Y    | 营地班级 ID      |
| Mode   | int  | N    | 导出模式，默认 1 |

### Response (Success)

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "64a8c96ec74e48ba9f4fdc0a68751d4a",
    "Result": {
      "Entries": null,
      "SheetURL": "https://tencent-tech-camp-1306124692.cos.ap-guangzhou.myqcloud.com/tlearn/export/prod/11103_AI小程序开发|2026腾讯MINI鹅冬季线下科创营_营地用户表.xlsx",
      "Total": 26
    },
    "Timestamp": 1770352388
  }
}
```

| 字段                     | 类型   | 描述                      |
| ------------------------ | ------ | ------------------------- |
| Code                     | int    | 响应码，0 表示成功        |
| Response.Result.SheetURL | string | 导出的 Excel 文件下载 URL |
| Response.Result.Total    | int    | 营地用户总数              |

---

## 营地用户表 Excel 格式

导出的文件名格式：`{CampID}_{营地名称}_营地用户表.xlsx`

### 第一行说明信息

```
填写前请阅读以下注意事项：
1. 以下填写项中标识有"*"号的为必填项。
2. 所有单元格格式均需使用"文本"类型。（可以点击左上角全选单元格统一设置单元格格式，保存后再进行上传）
3. 如需上传用户评价数据，请仅保留需要新增或修改评价的用户条目，并删除不需要修改、新增评价的用户条目。然后上传更新系统中的用户评价。只有当评价不为空时，才会更新系统中的评价文本。
4. 应学、选学、总任务完成度：是以小数记录，0 意味着 0%，1 意味着 100%。
5. 未开始任务数：用户尚未点开访问过的任务。
```

### 第二行字段说明

| 字段名                       | 类型   | 必填 | 描述                                       |
| ---------------------------- | ------ | ---- | ------------------------------------------ |
| `*用户 ID`                   | string | Y    | 用户唯一标识（**关键字段，用于跨表关联**） |
| `姓名`                       | string | N    | 用户姓名                                   |
| `*评价`                      | string | Y\*  | 用户评价文本（上传时必填才会更新）         |
| `性别(0-未配置，1-男，2-女)` | int    | N    | 性别：0=未配置, 1=男, 2=女                 |
| `手机号`                     | string | N    | 用户手机号                                 |
| `邮箱`                       | string | N    | 用户邮箱                                   |
| `出生日期`                   | string | N    | 出生日期                                   |
| `总任务完成度`               | float  | N    | 所有任务的完成进度（0~1，0=0%, 1=100%）    |
| `应学任务完成度`             | float  | N    | 必修(应学)任务的完成进度（0~1）            |
| `选学任务完成度`             | float  | N    | 选修(选学)任务的完成进度（0~1）            |
| `未开始任务数`               | int    | N    | 用户尚未访问过的任务数量                   |

---

## 使用示例

### cURL

```bash
curl -X POST 'https://tcampos.qq.com/api/camp/exportCampUser' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: tipe_token=<YOUR_TOKEN>' \
  -d '{
    "CampID": 11103,
    "Mode": 1
  }'
```

### Python

```python
from tcampos_api import get_api_client

api = get_api_client()

# 导出营地用户
result = api.post("/camp/exportCampUser", {
    "CampID": 11103,
    "Mode": 1
})

if result.get('Code') == 0:
    sheet_url = result['Response']['Result']['SheetURL']
    total = result['Response']['Result']['Total']
    print(f"营地用户数: {total}")
    print(f"下载链接: {sheet_url}")
```

### 命令行脚本

```bash
# 导出营地用户
python3 scripts/export_camp_user.py --camp-id 11103

# 指定下载目录
python3 scripts/export_camp_user.py --camp-id 11103 --output ./downloads/

# 只获取URL不下载
python3 scripts/export_camp_user.py --camp-id 11103 --no-download
```

---

## 常见使用场景

### 场景1: 统计学习进度

```python
import openpyxl

wb = openpyxl.load_workbook('11103_xxx_营地用户表.xlsx')
ws = wb.active

# 读取数据 (跳过说明行和表头行)
completed_count = 0
for row in range(3, ws.max_row + 1):
    total_progress = ws.cell(row, 8).value  # 总任务完成度
    if total_progress and float(total_progress) >= 1.0:
        completed_count += 1

print(f"完成所有任务的用户数: {completed_count}")
```

### 场景2: 与报名表关联

营地用户表可以通过 `用户 ID` 字段与报名表关联，获取用户的完整信息：

```python
# 读取营地用户表
camp_users = {}
for row in range(3, ws_user.max_row + 1):
    user_id = str(ws_user.cell(row, 1).value)
    camp_users[user_id] = {
        'progress': ws_user.cell(row, 8).value,
        'evaluation': ws_user.cell(row, 3).value
    }

# 与报名表合并
for user_id, signup_data in signup_users.items():
    if user_id in camp_users:
        signup_data['学习进度'] = camp_users[user_id]['progress']
        signup_data['评价'] = camp_users[user_id]['evaluation']
```
