# 常量定义
API_URL_PREFIX = "/training"

TOKEN_FOR_SaaS = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ3NDUwMjU5MjMsInVzZXIiOiJ7XCJpZFwiOlwiZTZjY2QzNmQtNGYxNi00NmZjLTg4ZDUtMDczNjU4NjZkMjA1XCIsXCJwZXJtaXNzaW9uc1wiOltcInByb2R1Y3RNYW5nZTpwdWJsaXNoXCIsXCJjb2RlTWFuZ2U6dmlld1wiLFwiZGV2aWNlTWFuYWdlOmFkZFwiLFwiYWRtaW5NYW5hZ2VcIixcIm9yZGVyTWFuZ2VcIixcImRldmljZU1hbmFnZTp2aWV3XCIsXCJwcm9kdWN0TWFuZ2U6YWRkXCIsXCJhZG1pbk1hbmFnZTp2aWV3XCIsXCJjb2RlTWFuZ2U6YWRkXCIsXCJwcm9kdWN0TWFuZ2U6b2ZmU2FsZVwiLFwib3JkZXJNYW5nZTpjYW5jZWxcIixcInByb2R1Y3RDZW50ZXI6ZG93bmxvYWRcIixcInByb2R1Y3RDZW50ZXI6YnV5XCIsXCJwcm9kdWN0TWFuZ2U6dmlld1wiLFwiYXBpXCIsXCJob21lXCIsXCJvcmRlck1hbmdlOnBheVwiLFwiYWRtaW5NYW5hZ2U6YWRkXCIsXCJvcmRlck1hbmdlOmRvd25sb2FkXCIsXCJwcm9kdWN0Q2VudGVyXCIsXCJkZXZpY2VNYW5hZ2U6dW5iaW5kXCIsXCJvcmRlck1hbmdlOnZpZXdcIixcImFkbWluTWFuYWdlOmVkaXRcIixcImRldmljZU1hbmFnZVwiLFwidmlwTWFuYWdlOmFkZFwiLFwidmlwTWFuYWdlOnZpZXdcIixcInByb2R1Y3RDZW50ZXI6dmlld1wiLFwidmlwTWFuYWdlOmVkaXRcIixcInZpcE1hbmFnZVwiLFwicHJvZHVjdE1hbmdlOmVkaXRcIixcImNvZGVNYW5nZVwiLFwicHJvZHVjdE1hbmdlXCJdLFwidXNlcm5hbWVcIjpcImJhc2ljXCJ9In0.vwjAFkWuEyadRLvIOGK8LFE3MjpY3SQ7j6AlTXnQDG8"

CONFIG_CENTER_KEY = "/micro/registry/training-config.conf"

RECORD_NOT_FOUND = "record not found"

CURRENT_USER_ID_KEY = "Current_user_id"


# 产品类型枚举
class ProductType:
    SOFTWARE = 1
    SOFT_AND_HARDWARE = 2
    SDK = 3
    APP = 4
    SD_KEY = 5


PRODUCT_TYPE_NAME = {
    ProductType.SOFTWARE: "软件",
    ProductType.SOFT_AND_HARDWARE: "软硬一体",
    ProductType.SDK: "算法",
    ProductType.APP: "应用",
    ProductType.SD_KEY: "算法密钥",
    }


# 版本枚举
class Edition:
    ALPHA = "alpha"
    BETA = "beta"
    TRY = "trial"
    TEST = "test"
    GOLD = "official"
    CUSTOM = "custom"
