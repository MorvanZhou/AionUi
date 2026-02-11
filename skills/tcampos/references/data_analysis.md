# TCampos Excel 数据分析指南

本文档描述 TCampos 平台导出的 Excel 数据格式规范，以及常见的数据分析场景和处理方法。

## Excel 文件结构规范

TCampos 导出的所有 Excel 文件遵循统一的结构规范：

```
┌─────────────────────────────────────────────────────────────────┐
│ 第1行: 说明信息单元格 (A1)                                         │
│        包含填写注意事项、操作说明、字段含义等                         │
├─────────────────────────────────────────────────────────────────┤
│ 第2行: 表头字段名 (Column Headers)                                 │
│        - 必填字段带 "*" 前缀                                       │
│        - 字段名可能包含中英文、空格、特殊符号                         │
├─────────────────────────────────────────────────────────────────┤
│ 第3行起: 数据行 (Data Rows)                                        │
│        - 部分单元格可能包含 hyperlink                               │
│        - 空值表示未填写                                            │
└─────────────────────────────────────────────────────────────────┘
```

### 第1行说明信息

第一行的 A1 单元格通常包含以下内容：

```
填写前请阅读以下注意事项：
1. 以下填写项中标识有"*"号的为必填项。
2. 所有单元格格式均需使用"文本"类型。（可以点击左上角全选单元格统一设置单元格格式，保存后再进行上传）
3. 如果要操作用户的通过/拒绝状态，请在操作列填写对应序号。例如需要通过该用户，则填 2；如要拒绝该用户，则填 3。
4. 如果不对该用户做任何操作处理，请删除用户的这行记录，仅保留需要更变操作的用户条目并上传系统。
```

### 第2行表头字段

**重要**: 读取数据前必须先解析第2行获取实际的字段名，因为：

- 字段名可能带有 `*` 前缀（表示必填）
- 字段名可能包含空格（如 `*用户 ID` 或 `用户ID`）
- 字段名可能包含中英文混合（如 `学校 School`）
- 字段名可能包含特殊字符（如 `Parent's Phone Number`）

---

## 各类 Excel 文件格式

### 1. 报名表 (`*_报名表.xlsx`)

#### 通用字段

| 字段名                                             | 类型     | 说明                                       |
| -------------------------------------------------- | -------- | ------------------------------------------ |
| `*操作(2-通过, 3-拒绝)`                            | int      | 操作码：2=通过, 3=拒绝，留空=不操作        |
| `*用户 ID`                                         | string   | 用户唯一标识（**关键字段，用于跨表关联**） |
| `当前状态(1-待审核, 2-已通过, 3-已拒绝，4-已移除)` | int      | 用户当前审核状态                           |
| `用户姓名`                                         | string   | TCampos 平台用户名                         |
| `报名时间`                                         | datetime | 格式：`YYYY-MM-DD HH:MM:SS`                |
| `报名通道`                                         | string   | 报名渠道来源                               |
| `更新时间`                                         | datetime | 最后更新时间                               |

#### 自定义报名表单字段

报名表中还包含营地自定义的报名表单字段，常见类型：

| 字段类型 | 示例                             | 说明                             |
| -------- | -------------------------------- | -------------------------------- |
| 文本     | `学生姓名 Name`                  | 普通文本输入                     |
| 选择     | `性别`, `就读年级 Grade`         | 单选/多选                        |
| 日期     | `出生日期`                       | 日期类型                         |
| 附件     | `奖项证明 Proof of awards_附件1` | **包含 hyperlink**，指向下载链接 |
| 长文本   | `生活中的爱好和特长...`          | 多行文本                         |

#### 附件字段的 Hyperlink 格式

附件类字段的单元格包含：

- **显示值**: 文件名（如 `IMG_0381.jpeg`）
- **Hyperlink**: 下载 URL（如 `https://tcamp.qq.com/api/download?s=...`）

```python
# 读取附件 hyperlink 示例
cell = ws.cell(row, col)
filename = cell.value           # 显示的文件名
download_url = cell.hyperlink.target if cell.hyperlink else None
```

---

### 2. 考试记录表 (`*_考试记录表.xlsx`)

| 字段名                                   | 类型     | 说明                         |
| ---------------------------------------- | -------- | ---------------------------- |
| `*操作(2-通过, 3-拒绝)`                  | int      | 操作码                       |
| `*用户 ID`                               | string   | 用户唯一标识（**关键字段**） |
| `当前状态(1-待审核, 2-已通过, 3-已拒绝)` | int      | 审核状态                     |
| `用户姓名`                               | string   | 用户名                       |
| `创建时间`                               | datetime | 考试开始时间                 |
| `考试状态`                               | int      | 1=进行中, 2=已完成           |
| `总得分`                                 | float    | 考试总分                     |
| `自动判题得分`                           | float    | 客观题得分（自动评分）       |
| `主观题得分`                             | float    | 主观题得分（人工评分）       |
| `更新时间`                               | datetime | 最后更新时间                 |

---

### 3. 面试记录表 (`*_面试记录表.xlsx`)

| 字段名                                   | 类型     | 说明                         |
| ---------------------------------------- | -------- | ---------------------------- |
| `*操作(2-通过, 3-拒绝)`                  | int      | 操作码                       |
| `*用户 ID`                               | string   | 用户唯一标识（**关键字段**） |
| `当前状态(1-待审核, 2-已通过, 3-已拒绝)` | int      | 审核状态                     |
| `用户姓名`                               | string   | 用户名                       |
| `面试状态`                               | int      | 面试进度状态                 |
| `面试评分`                               | float    | 面试得分                     |
| `面试备注`                               | string   | 面试官备注                   |
| `更新时间`                               | datetime | 最后更新时间                 |

---

### 4. 营地用户表 (`*_营地用户表.xlsx`)

| 字段名                       | 类型   | 说明                                    |
| ---------------------------- | ------ | --------------------------------------- |
| `*用户 ID`                   | string | 用户唯一标识（**关键字段**）            |
| `姓名`                       | string | 用户姓名                                |
| `*评价`                      | string | 用户评价文本                            |
| `性别(0-未配置，1-男，2-女)` | int    | 性别：0=未配置, 1=男, 2=女              |
| `手机号`                     | string | 用户手机号                              |
| `邮箱`                       | string | 用户邮箱                                |
| `出生日期`                   | string | 出生日期                                |
| `总任务完成度`               | float  | 所有任务的完成进度（0~1，0=0%, 1=100%） |
| `应学任务完成度`             | float  | 必修(应学)任务的完成进度                |
| `选学任务完成度`             | float  | 选修(选学)任务的完成进度                |
| `未开始任务数`               | int    | 用户尚未访问过的任务数量                |

---

### 5. 用户任务数据表 (`*_用户任务数据表.xlsx`)

| 字段名                                   | 类型     | 说明                                           |
| ---------------------------------------- | -------- | ---------------------------------------------- |
| `*操作(2-通过, 3-拒绝)`                  | int      | 操作码（用于批量审批）                         |
| `*用户 ID`                               | string   | 用户唯一标识（**关键字段**）                   |
| `当前状态(0-未开始, 1-进行中, 2-已完成)` | int      | 任务完成状态                                   |
| `开始时间`                               | datetime | 用户开始任务的时间                             |
| `完成时间`                               | datetime | 用户完成任务的时间                             |
| `完成率`                                 | float    | 任务完成进度（0=0%, 1=100%）                   |
| `姓名`                                   | string   | 用户姓名                                       |
| `<表单字段>`                             | varies   | 作业任务中的自定义表单字段（如"学员身份证号"） |
| `<任务名>_附件1` ~ `_附件N`              | string   | 用户上传的附件文件名（可能带 hyperlink）       |

> **注意**：用户任务数据表的字段会根据任务类型和配置动态变化。作业类任务会包含表单字段和附件字段。

---

## 数据处理最佳实践

### 1. 读取 Excel 数据

使用 `openpyxl` 读取数据时的标准流程：

```python
import openpyxl
from openpyxl.utils import get_column_letter

def read_tcampos_excel(filepath: str) -> tuple[dict, list[str], list[dict]]:
    """
    读取 TCampos 导出的 Excel 文件

    Returns:
        (info, headers, data)
        - info: 第1行说明信息
        - headers: 第2行字段名列表
        - data: 数据行列表 (每行为 dict)
    """
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    # 第1行: 说明信息
    info = ws.cell(1, 1).value

    # 第2行: 字段名 (动态读取，不要硬编码)
    headers = []
    for col in range(1, ws.max_column + 1):
        val = ws.cell(2, col).value
        if val:
            headers.append(val)

    # 第3行起: 数据
    data = []
    for row in range(3, ws.max_row + 1):
        row_data = {}
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row, col)
            row_data[header] = {
                'value': cell.value,
                'hyperlink': cell.hyperlink.target if cell.hyperlink else None
            }
        data.append(row_data)

    return info, headers, data
```

### 2. 用户 ID 字段识别

由于用户 ID 字段名可能有多种变体，建议使用模糊匹配：

```python
def find_user_id_column(headers: list[str]) -> str:
    """
    在表头中查找用户 ID 字段
    可能的变体: '*用户 ID', '用户 ID', '*用户ID', '用户ID'
    """
    for header in headers:
        # 移除 * 和空格后比较
        normalized = header.replace('*', '').replace(' ', '').lower()
        if normalized in ['用户id', 'userid', '用户id']:
            return header
    raise ValueError("未找到用户 ID 字段")
```

### 3. 跨表数据合并

按用户 ID 合并报名表和考试表：

```python
def merge_by_user_id(signup_data: list[dict], exam_data: list[dict]) -> list[dict]:
    """
    按用户 ID 合并两个表的数据
    """
    # 构建考试数据索引
    exam_by_user = {}
    exam_user_id_col = find_user_id_column(list(exam_data[0].keys()) if exam_data else [])
    for row in exam_data:
        user_id = row[exam_user_id_col]['value']
        exam_by_user[str(user_id)] = row

    # 合并到报名数据
    signup_user_id_col = find_user_id_column(list(signup_data[0].keys()) if signup_data else [])
    merged = []
    for signup_row in signup_data:
        user_id = str(signup_row[signup_user_id_col]['value'])
        merged_row = dict(signup_row)

        if user_id in exam_by_user:
            # 添加考试数据 (添加前缀避免字段冲突)
            for key, val in exam_by_user[user_id].items():
                if key not in merged_row:
                    merged_row[f'考试_{key}'] = val

        merged.append(merged_row)

    return merged
```

### 4. 按条件筛选数据

```python
def filter_data(data: list[dict], conditions: dict) -> list[dict]:
    """
    按条件筛选数据

    Args:
        data: 数据列表
        conditions: 筛选条件 {字段名: 期望值} 或 {字段名: lambda函数}

    Example:
        # 筛选已通过的用户
        filter_data(data, {'当前状态(1-待审核, 2-已通过, 3-已拒绝)': '2'})

        # 筛选得分大于60的
        filter_data(data, {'总得分': lambda x: float(x or 0) >= 60})
    """
    result = []
    for row in data:
        match = True
        for field, condition in conditions.items():
            cell = row.get(field, {})
            value = cell.get('value') if isinstance(cell, dict) else cell

            if callable(condition):
                if not condition(value):
                    match = False
                    break
            else:
                if str(value) != str(condition):
                    match = False
                    break

        if match:
            result.append(row)

    return result
```

### 5. 保存数据 (保留 Hyperlink)

保存处理后的数据时，需要保留原有的 hyperlink：

```python
from openpyxl import Workbook
from openpyxl.worksheet.hyperlink import Hyperlink

def save_with_hyperlinks(data: list[dict], output_path: str, headers: list[str] = None):
    """
    保存数据到 Excel，保留 hyperlink 格式

    Args:
        data: 数据列表，每个单元格为 {'value': ..., 'hyperlink': ...}
        output_path: 输出文件路径
        headers: 自定义表头顺序，默认使用第一行数据的 keys
    """
    wb = Workbook()
    ws = wb.active

    if not data:
        wb.save(output_path)
        return

    # 确定表头
    if headers is None:
        headers = list(data[0].keys())

    # 写入表头 (第1行，跳过说明行)
    for col, header in enumerate(headers, 1):
        ws.cell(1, col, header)

    # 写入数据
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, header in enumerate(headers, 1):
            cell_data = row_data.get(header, {})

            if isinstance(cell_data, dict):
                value = cell_data.get('value')
                hyperlink = cell_data.get('hyperlink')
            else:
                value = cell_data
                hyperlink = None

            cell = ws.cell(row_idx, col_idx, value)

            # 保留 hyperlink
            if hyperlink:
                cell.hyperlink = hyperlink
                cell.style = 'Hyperlink'  # 应用超链接样式

    wb.save(output_path)
```

---

## 常见使用场景

### 场景1: 导出已通过用户名单

```python
# 读取报名表
info, headers, data = read_tcampos_excel('xxx_报名表.xlsx')

# 筛选已通过 (状态=2)
status_col = '当前状态(1-待审核, 2-已通过, 3-已拒绝，4-已移除)'
passed = filter_data(data, {status_col: '2'})

# 提取需要的字段
result = []
for row in passed:
    result.append({
        '用户ID': row['*用户 ID']['value'],
        '姓名': row.get('学生姓名 Name', {}).get('value'),
        '学校': row.get('学校 School', {}).get('value'),
    })
```

### 场景2: 合并报名和考试数据

```python
# 读取两个表
_, _, signup_data = read_tcampos_excel('xxx_报名表.xlsx')
_, _, exam_data = read_tcampos_excel('xxx_考试记录表.xlsx')

# 按用户 ID 合并
merged = merge_by_user_id(signup_data, exam_data)

# 筛选考试得分 >= 60 的
high_score = filter_data(merged, {
    '总得分': lambda x: float(x or 0) >= 60
})
```

### 场景3: 统计各状态人数

```python
from collections import Counter

_, _, data = read_tcampos_excel('xxx_报名表.xlsx')
status_col = '当前状态(1-待审核, 2-已通过, 3-已拒绝，4-已移除)'

status_count = Counter(row[status_col]['value'] for row in data)
print(f"待审核: {status_count.get('1', 0)}")
print(f"已通过: {status_count.get('2', 0)}")
print(f"已拒绝: {status_count.get('3', 0)}")
print(f"已移除: {status_count.get('4', 0)}")
```

### 场景4: 下载用户附件

```python
import urllib.request

def download_attachments(data: list[dict], attachment_fields: list[str], output_dir: str):
    """下载所有用户的附件"""
    for row in data:
        user_id = row['*用户 ID']['value']
        for field in attachment_fields:
            cell = row.get(field, {})
            if cell.get('hyperlink'):
                filename = cell.get('value', 'unknown')
                url = cell['hyperlink']
                output_path = f"{output_dir}/{user_id}_{filename}"
                urllib.request.urlretrieve(url, output_path)
                print(f"Downloaded: {output_path}")
```

---

## 注意事项

1. **字段名动态获取**: 不要硬编码字段名，始终从第2行读取
2. **用户 ID 标准化**: 用户 ID 是字符串类型，比较时注意类型转换
3. **空值处理**: 未填写的单元格值为 `None`，需做空值判断
4. **Hyperlink 保留**: 处理附件类字段时，保留 hyperlink 信息
5. **编码问题**: 文件名可能包含中文，注意路径编码
6. **大文件处理**: 数据量大时考虑使用 `openpyxl` 的 `read_only` 模式
