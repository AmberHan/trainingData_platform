# from fastapi import Request
#
#
# """
#     上下文id可以调用
#
# """
# def get_user_id_from_ctx(request: Request):
#     return getattr(request.state, 'user_id', None)  # 返回用户 ID 或 None