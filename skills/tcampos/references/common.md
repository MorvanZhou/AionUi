# TCampos API - 通用信息

## Base URL

```
https://tcampos.qq.com/api
https://tcamp.qq.com/api (for login)
```

---

## Authentication

所有 API 请求需要 `tipe_token` cookie 进行认证。

### Cookie 格式

```
Cookie: tipe_token=<JWT_TOKEN>
```

### 认证失败响应

```json
{
  "Code": 1,
  "Response": {
    "Error": {
      "Code": "InvalidJWTClaims",
      "Message": "用户登录态信息无效，请重新登录",
      "Detail": "no token in cookie or header"
    },
    "RequestId": "<request_id>",
    "Timestamp": <unix_timestamp>
  }
}
```

---

## Common Response Codes

| Code | 描述                        |
| ---- | --------------------------- |
| 0    | 成功                        |
| 1    | 错误（详见 Response.Error） |

---

## Error Codes

| Error Code       | 描述             |
| ---------------- | ---------------- |
| InvalidJWTClaims | Token 无效或过期 |
| InvalidParameter | 请求参数无效     |
| Unauthorized     | 未授权访问       |

---

## 通用响应格式

### 成功响应

```json
{
  "Code": 0,
  "Response": {
    "RequestId": "<request_id>",
    "Result": { ... },
    "Timestamp": <unix_timestamp>
  }
}
```

### 错误响应

```json
{
  "Code": 1,
  "Response": {
    "Error": {
      "Code": "<error_code>",
      "Message": "<error_message>",
      "Detail": "<error_detail>"
    },
    "RequestId": "<request_id>",
    "Timestamp": <unix_timestamp>
  }
}
```

---

## 分页参数

大部分列表接口支持分页：

| 字段     | 类型  | 必填 | 描述                |
| -------- | ----- | ---- | ------------------- |
| PageSize | int   | ✅   | 每页数量（默认 20） |
| PageNum  | int   | ✅   | 页码（从 1 开始）   |
| Sort     | array | ❌   | 排序选项            |

### 分页响应

```json
{
  "Result": {
    "Entries": [...],
    "Total": 100
  }
}
```
