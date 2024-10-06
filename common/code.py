# util/code.py
from fastapi import status


class Code:
    def __init__(self, status_code: int, success: bool, message: str):
        self.status = status_code
        self.success = success
        self.message = message

    def to_dict(self):
        return {
            "status": self.status,
            "success": self.success,
            "msg": self.message
        }


# 预定义的错误码
LicenseExpired = Code(status.HTTP_403_FORBIDDEN, False, "license expired")
Success = Code(status.HTTP_200_OK, True, "请求处理成功")
Error = Code(status.HTTP_400_BAD_REQUEST, False, "请求处理失败")
SaveSuccess = Code(status.HTTP_200_OK, True, "新增成功")
UploadSuccess = Code(status.HTTP_200_OK, True, "上传成功")
SaveFail = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "新增失败")
UpdateSuccess = Code(status.HTTP_200_OK, True, "更新成功")
UpdateFail = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "更新失败")
DeleteSuccess = Code(status.HTTP_200_OK, True, "删除成功")
DeleteFail = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "删除失败")
RequestParamError = Code(status.HTTP_400_BAD_REQUEST, False, "请求参数有误")
ServiceInsideError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "服务器内部错误")
DdSelectNotFindError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "数据库未查找到记录")
HasChildNodeError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "数据节点存在子节点 无法删除")
TaskStoped = Code(status.HTTP_200_OK, True, "此任务为停用状态，请在任务管理中开启！")
ClusterNodesEmpty = Code(status.HTTP_200_OK, True, "集群节点为空")
ClusterIsSearching = Code(status.HTTP_400_BAD_REQUEST, False, "集群正在搜索中，请稍后...")
ComError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "")
AlreadyUsed = Code(status.HTTP_400_BAD_REQUEST, False, "此用户名已被占用")
RegisterSuccess = Code(status.HTTP_200_OK, True, "注册成功")
RegisterErr = Code(status.HTTP_400_BAD_REQUEST, False, "注册失败，请联系管理员！")
AddSuccess = Code(status.HTTP_200_OK, True, "添加成功")
DelSuccess = Code(status.HTTP_200_OK, True, "删除成功")
AccountPassUnmatch = Code(status.HTTP_200_OK, False, "该账号原密码不匹配")
SignupPassUnmatch = Code(status.HTTP_400_BAD_REQUEST, False, "注册两次输入密码不匹配")
AccountNameExist = Code(status.HTTP_400_BAD_REQUEST, False, "账号昵称已被使用")
UploadSuffixError = Code(status.HTTP_400_BAD_REQUEST, False, "该上传文件格式目前暂不支持")
UploadSizeLimit = Code(status.HTTP_400_BAD_REQUEST, False, "目前上传仅支持小于5M的文件内容")
InvalidRequest = Code(status.HTTP_400_BAD_REQUEST, False, "请求无效")
LoginSuccess = Code(status.HTTP_200_OK, True, "登录成功")
LoginInfoError = Code(status.HTTP_401_UNAUTHORIZED, False, "用户名或密码错误")
LogoutSuccess = Code(status.HTTP_200_OK, True, "退出成功")
LogoutFail = Code(status.HTTP_400_BAD_REQUEST, False, "退出失败")
TokenNotFound = Code(status.HTTP_401_UNAUTHORIZED, False, "请求未携带Token, 无权访问")
TokenInvalid = Code(status.HTTP_401_UNAUTHORIZED, False, "无效的Token信息")
NotFeatureFindError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "特征值获取失败")
TooManyFeatureFindError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "人脸过多")
UploadFileError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "上传文件服务器失败")
NotLogin = Code(status.HTTP_401_UNAUTHORIZED, False, "登录失效，请重新登录")
DbPersonUploadSuccess = Code(status.HTTP_200_OK, True, "人员上传成功")
DbPersonUploadFail = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "人员上传失败")
DbPersonUpdateSuccess = Code(status.HTTP_200_OK, True, "人员更新成功")
CompareResultGone = Code(status.HTTP_200_OK, True, "上次比对已失效，请从新比对")
AddTaskErr = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "此国标摄像机已在其它服务器配置任务！")
CreateFirstNodeErr = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "创建节点失败！")
QueryClusterInfoErr = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "查询失败，请确认您的ip是正确的！")
AddClusterInfoErr = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "加入节点失败！")
UpgradeSuccess = Code(status.HTTP_200_OK, True, "升级成功")
UpgradeFail = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "升级失败")
RequestSuccess = Code(status.HTTP_200_OK, True, "success")
RecordNotFound = Code(status.HTTP_200_OK, False, "暂无记录")
RequestSystemError = Code(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "服务器开小差了，请稍后再试...")
BadRequest = Code(status.HTTP_400_BAD_REQUEST, False, "请求失败")
DeleteNoIDRequest = Code(status.HTTP_400_BAD_REQUEST, False, "请选择项目")
