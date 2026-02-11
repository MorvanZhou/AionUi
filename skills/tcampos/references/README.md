# TCampos API References

本目录包含 TCampos 平台 API 的详细文档。

## 文件结构

| 文件                                   | 内容                                         |
| -------------------------------------- | -------------------------------------------- |
| [common.md](common.md)                 | 通用信息：Base URL、认证方式、响应码、错误码 |
| [login.md](login.md)                   | 登录认证 API                                 |
| [camp.md](camp.md)                     | 营地班级相关 API                             |
| [camp_topic.md](camp_topic.md)         | 主题营相关 API                               |
| [select_process.md](select_process.md) | 报名筛选流程与数据导出 API                   |
| [camp_user.md](camp_user.md)           | 营地用户导出 API                             |
| [task.md](task.md)                     | 任务管理与数据导出 API                       |
| [user_profile.md](user_profile.md)     | 用户档案查询 API                             |
| [data_analysis.md](data_analysis.md)   | Excel 数据格式规范与分析指南                 |
| [notification.md](notification.md)     | 通知发送模版填写指南                         |

## Base URL

```
https://tcampos.qq.com/api
https://tcamp.qq.com/api (for login)
```

## 认证方式

所有 API 请求需要 `tipe_token` cookie 进行认证。

```
Cookie: tipe_token=<JWT_TOKEN>
```

详见 [common.md](common.md#authentication)
