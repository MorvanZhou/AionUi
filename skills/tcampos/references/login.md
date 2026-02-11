# TCampos API - 登录认证

## Login UI (交互式登录)

提供简单的终端交互界面让用户输入手机号和密码。

**脚本**: `scripts/login_ui.py`

### 使用方式

```bash
# 打开交互式登录（如果已登录则提示）
python3 scripts/login_ui.py

# 强制重新登录
python3 scripts/login_ui.py --force

# 仅检查是否需要登录
python3 scripts/login_ui.py --check
```

### 功能特点

- 终端交互式输入，跨平台兼容（macOS/Linux/Windows）
- 密码输入时隐藏显示
- 支持多种国家/地区代码（+86、+852、+853、+886、+1）
- 自动保存凭据到配置文件
- 集成到 API 客户端，缺少凭据时自动提示

### 自动登录集成

当使用 `get_api_client()` 时，如果配置文件不存在或缺少凭据，会自动提示登录：

```python
from tcampos_api import get_api_client

# 如果需要登录，会自动提示交互式输入
api = get_api_client()

# 禁用自动提示
api = get_api_client(interactive=False)
```

---

## Login (命令行登录)

登录获取 `tipe_token`。

**Endpoint**: `POST https://tcamp.qq.com/api/account/passwdLogin`

### Request

```json
{
  "Account": "+86...",
  "Passwd": "..."
}
```

| 字段    | 类型   | 必填 | 描述                                  |
| ------- | ------ | ---- | ------------------------------------- |
| Account | string | ✅   | 手机号（含国家码，如 +8613800138000） |
| Passwd  | string | ✅   | 密码                                  |

### Response (Success)

登录成功后，`tipe_token` 通过 `Set-Cookie` 响应头返回。

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "...",
    "Result": {},
    "Timestamp": 1234567890
  }
}
```

---

## 使用示例

### cURL

```bash
curl -X POST 'https://tcamp.qq.com/api/account/passwdLogin' \
  -H 'Content-Type: application/json' \
  -c cookies.txt \
  -d '{
    "Account": "+8613800138000",
    "Passwd": "your_password"
  }'
```

### Python

```python
from tcampos_api import get_api_client

# 首次登录
import subprocess
subprocess.run([
    'python3', 'scripts/login.py',
    '--account', '+8613800138000',
    '--password', 'your_password'
])

# 之后使用 API 客户端（自动处理 Token 刷新）
api = get_api_client()
```
