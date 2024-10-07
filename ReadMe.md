## 环境
- python: 版本需大于等于3.9
- 涉及库: sqlModel、fastApi、pydantic、python-multipart、sqlalchemy、cryptography、uvicorn

## 目录
- config 配置文件
- common 全局定义
- db 数据库位置
- log 日志位置，可在config修改路径
- router 路由设置
- schemas 请求、响应数据的类型定义及类型转换
- services 业务处理
- sqlmodels 定义表和字段以及对应增删改查
- test 测试用例
- upload_files 数据上传位置，可在config修改路径
- utils 通用的方法
- main.py 主函数
