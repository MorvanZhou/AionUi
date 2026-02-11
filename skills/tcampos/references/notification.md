# TCampos 通知发送指南

本文档描述如何使用 TCampos 平台的通知发送模版批量给用户发送邮件或短信通知。

## 通知发送模版概述

通知模版文件位于：`assets/templates/通知发送模版.xlsx`

### 模版结构

```
┌─────────────────────────────────────────────────────────────────┐
│ 第1行: 说明信息单元格 (A1)                                         │
│        包含模版使用说明、字段含义、操作注意事项等                     │
├─────────────────────────────────────────────────────────────────┤
│ 第2行: 表头字段名 (Column Headers)                                 │
│        - *操作(1-发送)                                            │
│        - *用户 ID                                                 │
│        - 其他字段...                                              │
├─────────────────────────────────────────────────────────────────┤
│ 第3行起: 数据行 (Data Rows)                                        │
│        - 填入需要发送通知的用户信息                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 关键字段说明

| 字段名          | 类型   | 必填 | 说明                                     |
| --------------- | ------ | ---- | ---------------------------------------- |
| `*操作(1-发送)` | int    | ✅   | 填写 `1` 表示向该用户发送通知            |
| `*用户 ID`      | string | ✅   | 目标用户的唯一标识（从其他数据表中获取） |

---

## 文件输出目录

| 操作类型     | 默认目录       | 说明                      |
| ------------ | -------------- | ------------------------- |
| **下载数据** | `./downloads/` | 从 API 导出的原始数据文件 |
| **生成数据** | `./outputs/`   | 处理后生成的通知模版文件  |

> **注意**：如果用户指定了具体路径，则使用用户指定的路径。

---

## 通知发送工作流程

### 整体流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                     通知发送工作流程                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: 明确筛选需求                                             │
│          确定需要发送通知的目标人群条件                              │
│          例如：必修(应学)任务未完成、报名未通过、特定营地成员等             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: 获取数据源                                               │
│          根据需求导出相关数据表：                                   │
│          - 营地用户表 (export_camp_user.py)                       │
│          - 报名表 (select_process.py --export signup)             │
│          - 考试记录表 (select_process.py --export exam)           │
│          - 任务记录表 (export_task_records.py)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: 筛选目标用户                                             │
│          根据业务条件过滤数据，提取符合条件的用户 ID 列表             │
│          使用 Python/pandas 进行数据处理                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: 填写通知模版                                             │
│          将筛选出的用户 ID 填入通知模版：                           │
│          - "*用户 ID" 列：填入用户 ID                              │
│          - "*操作(1-发送)" 列：填入 1                              │
│          数据从第3行开始填写                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: 上传并发送                                               │
│          将填写好的模版上传到 TCampos 平台执行发送                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 典型使用场景

### 场景1: 给必修(应学)任务未完成的用户发通知

**需求**: 某营地中，需要提醒那些必修(应学)任务完成度 < 100% 的学员

**步骤**:

1. **导出营地用户表**

```bash
python3 scripts/export_camp_user.py --camp-id <营地ID> --output ./downloads/
```

2. **筛选必修(应学)任务未完成的用户**

```python
import openpyxl
from openpyxl import Workbook

# 读取营地用户表
wb = openpyxl.load_workbook('./downloads/xxx_营地用户表.xlsx')
ws = wb.active

# 获取表头 (第2行)
headers = [ws.cell(2, col).value for col in range(1, ws.max_column + 1)]

# 找到关键列索引
user_id_col = None
required_task_col = None
for idx, h in enumerate(headers, 1):
    if h and '用户' in h and 'ID' in h.upper():
        user_id_col = idx
    if h and '应学任务完成度' in h:
        required_task_col = idx

# 筛选必修(应学)任务未完成的用户 (应学任务完成度 < 1)
target_users = []
for row in range(3, ws.max_row + 1):
    user_id = ws.cell(row, user_id_col).value
    completion = ws.cell(row, required_task_col).value

    if completion is not None and float(completion) < 1:
        target_users.append(user_id)

print(f"找到 {len(target_users)} 个需要通知的用户")
```

3. **生成通知模版**

```python
# 复制原始模版并填入数据
import shutil
import os

# 确保输出目录存在
os.makedirs('./outputs', exist_ok=True)

shutil.copy('assets/templates/通知发送模版.xlsx', './outputs/通知发送_必修未完成.xlsx')

wb_notify = openpyxl.load_workbook('./outputs/通知发送_必修未完成.xlsx')
ws_notify = wb_notify.active

# 从第3行开始填写数据
for idx, user_id in enumerate(target_users):
    row = idx + 3  # 数据从第3行开始
    ws_notify.cell(row, 1, 1)        # *操作(1-发送) 列填 1
    ws_notify.cell(row, 2, user_id)  # *用户 ID 列填用户ID

wb_notify.save('./outputs/通知发送_必修未完成.xlsx')
print(f"通知模版已生成: ./outputs/通知发送_必修未完成.xlsx")
```

---

### 场景2: 给报名未通过的用户发通知

**需求**: 给报名状态为"已拒绝"的用户发送通知

**步骤**:

1. **导出报名表**

```bash
python3 scripts/select_process.py --camp-id <营地ID> --export signup --output ./downloads/
```

2. **筛选报名被拒绝的用户**

```python
import openpyxl
from openpyxl import Workbook

# 读取报名表
wb = openpyxl.load_workbook('./downloads/xxx_报名表.xlsx')
ws = wb.active

# 获取表头
headers = [ws.cell(2, col).value for col in range(1, ws.max_column + 1)]

# 找到关键列
user_id_col = None
status_col = None
for idx, h in enumerate(headers, 1):
    if h and '用户' in h and 'ID' in h.upper():
        user_id_col = idx
    if h and '当前状态' in h:
        status_col = idx

# 筛选已拒绝的用户 (状态=3)
rejected_users = []
for row in range(3, ws.max_row + 1):
    user_id = ws.cell(row, user_id_col).value
    status = ws.cell(row, status_col).value

    if str(status) == '3':  # 3 表示已拒绝
        rejected_users.append(user_id)

print(f"找到 {len(rejected_users)} 个被拒绝的用户")
```

3. **生成通知模版**

```python
import shutil
import os

os.makedirs('./outputs', exist_ok=True)
shutil.copy('assets/templates/通知发送模版.xlsx', './outputs/通知发送_报名拒绝.xlsx')

wb_notify = openpyxl.load_workbook('./outputs/通知发送_报名拒绝.xlsx')
ws_notify = wb_notify.active

for idx, user_id in enumerate(rejected_users):
    row = idx + 3
    ws_notify.cell(row, 1, 1)        # 操作列填 1
    ws_notify.cell(row, 2, user_id)  # 用户ID列

wb_notify.save('./outputs/通知发送_报名拒绝.xlsx')
print(f"通知模版已生成: ./outputs/通知发送_报名拒绝.xlsx")
```

---

### 场景3: 给考试成绩低于及格线的用户发通知

**需求**: 给考试总得分 < 60 的用户发送补考提醒

**步骤**:

1. **导出考试记录表**

```bash
python3 scripts/select_process.py --camp-id <营地ID> --export exam --output ./downloads/
```

2. **筛选低分用户**

```python
import openpyxl

wb = openpyxl.load_workbook('./downloads/xxx_考试记录表.xlsx')
ws = wb.active

headers = [ws.cell(2, col).value for col in range(1, ws.max_column + 1)]

# 找到关键列
user_id_col = None
score_col = None
for idx, h in enumerate(headers, 1):
    if h and '用户' in h and 'ID' in h.upper():
        user_id_col = idx
    if h and '总得分' in h:
        score_col = idx

# 筛选低分用户
low_score_users = []
for row in range(3, ws.max_row + 1):
    user_id = ws.cell(row, user_id_col).value
    score = ws.cell(row, score_col).value

    if score is not None and float(score) < 60:
        low_score_users.append(user_id)

print(f"找到 {len(low_score_users)} 个低分用户")
```

3. **生成通知模版** (同上)

---

### 场景4: 给特定任务未完成的用户发通知

**需求**: 某个特定任务（如"入营问卷"）未完成的用户需要催促

**步骤**:

1. **查询任务列表，获取任务 ID**

```bash
python3 scripts/list_camp_task.py --camp-id <营地ID> --name "入营问卷"
```

2. **导出该任务的用户记录**

```bash
python3 scripts/export_task_records.py --task-id <任务ID> --output ./downloads/
```

3. **筛选未完成的用户**

```python
import openpyxl

wb = openpyxl.load_workbook('./downloads/xxx_用户任务数据表.xlsx')
ws = wb.active

headers = [ws.cell(2, col).value for col in range(1, ws.max_column + 1)]

user_id_col = None
status_col = None
for idx, h in enumerate(headers, 1):
    if h and '用户' in h and 'ID' in h.upper():
        user_id_col = idx
    if h and '当前状态' in h:
        status_col = idx

# 筛选未完成的用户 (状态=0未开始 或 状态=1进行中)
incomplete_users = []
for row in range(3, ws.max_row + 1):
    user_id = ws.cell(row, user_id_col).value
    status = ws.cell(row, status_col).value

    if str(status) in ['0', '1']:  # 0=未开始, 1=进行中
        incomplete_users.append(user_id)

print(f"找到 {len(incomplete_users)} 个未完成任务的用户")
```

---

## 通用工具函数

以下是可复用的工具函数，用于简化通知模版的生成过程：

```python
import openpyxl
import shutil
import os
from typing import List

def generate_notification_template(
    user_ids: List[str],
    template_path: str = 'assets/templates/通知发送模版.xlsx',
    output_path: str = './outputs/通知发送.xlsx',
    operation_col: int = 1,
    user_id_col: int = 2,
    start_row: int = 3
) -> str:
    """
    根据用户 ID 列表生成通知发送模版

    Args:
        user_ids: 需要发送通知的用户 ID 列表
        template_path: 原始模版文件路径
        output_path: 输出文件路径（默认保存到 ./outputs/）
        operation_col: "*操作(1-发送)" 所在列号 (默认第1列)
        user_id_col: "*用户 ID" 所在列号 (默认第2列)
        start_row: 数据开始行号 (默认第3行)

    Returns:
        生成的文件路径
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    # 复制模版
    shutil.copy(template_path, output_path)

    # 打开并填写数据
    wb = openpyxl.load_workbook(output_path)
    ws = wb.active

    for idx, user_id in enumerate(user_ids):
        row = start_row + idx
        ws.cell(row, operation_col, 1)      # 操作列填 1
        ws.cell(row, user_id_col, user_id)  # 用户ID列

    wb.save(output_path)

    return output_path


def extract_user_ids_from_excel(
    filepath: str,
    filter_func = None,
    header_row: int = 2,
    data_start_row: int = 3
) -> List[str]:
    """
    从 TCampos 导出的 Excel 中提取用户 ID

    Args:
        filepath: Excel 文件路径
        filter_func: 过滤函数，接收 (row_dict, headers) 返回 bool
        header_row: 表头所在行 (默认第2行)
        data_start_row: 数据开始行 (默认第3行)

    Returns:
        符合条件的用户 ID 列表
    """
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    # 读取表头
    headers = {}
    for col in range(1, ws.max_column + 1):
        header = ws.cell(header_row, col).value
        if header:
            headers[header] = col

    # 找到用户 ID 列
    user_id_col = None
    for h, col in headers.items():
        if h and '用户' in h and 'ID' in h.upper():
            user_id_col = col
            break

    if not user_id_col:
        raise ValueError("未找到用户 ID 列")

    # 提取用户 ID
    user_ids = []
    for row in range(data_start_row, ws.max_row + 1):
        # 构建行数据字典
        row_data = {}
        for header, col in headers.items():
            row_data[header] = ws.cell(row, col).value

        user_id = ws.cell(row, user_id_col).value

        # 应用过滤条件
        if filter_func is None or filter_func(row_data, headers):
            if user_id:
                user_ids.append(str(user_id))

    return user_ids


# 使用示例
if __name__ == '__main__':
    # 示例：筛选必修(应学)任务未完成的用户并生成通知

    def incomplete_required_task(row_data, headers):
        """筛选应学任务完成度 < 1 的用户"""
        for h in headers:
            if '应学任务完成度' in h:
                completion = row_data.get(h)
                if completion is not None:
                    return float(completion) < 1
        return False

    # 提取用户
    users = extract_user_ids_from_excel(
        './downloads/xxx_营地用户表.xlsx',
        filter_func=incomplete_required_task
    )

    # 生成通知模版
    output = generate_notification_template(
        user_ids=users,
        output_path='./outputs/通知发送_必修未完成.xlsx'
    )

    print(f"已生成通知模版: {output}, 共 {len(users)} 个用户")
```

---

## 注意事项

1. **模版结构**：
   - 第1行是说明信息，不要删除
   - 第2行是表头字段名，不要修改
   - 数据从第3行开始填写

2. **字段填写**：
   - `*操作(1-发送)` 必须填写 `1` 才会发送
   - `*用户 ID` 必须是有效的用户标识

3. **用户 ID 来源**：
   - 从营地用户表、报名表、考试记录表等数据源获取
   - 确保用户 ID 是字符串格式，避免数字被截断

4. **数据验证**：
   - 填写前检查用户 ID 是否有效
   - 建议先小批量测试，确认无误后再批量发送

5. **筛选逻辑**：
   - 根据实际业务需求编写筛选条件
   - 复杂筛选可能需要跨表关联（参考 [data_analysis.md](data_analysis.md#3-跨表数据合并)）
