# api/utils.py


def format_response(status: str, data=None, message=""):
    """
    格式化统一响应数据格式
    :param status: "success" 或 "error"
    :param data: 返回的数据内容，错误时为 None
    :param message: 提示信息或错误信息
    :return: 格式化后的字典
    """
    return {"status": status, "data": data, "message": message}
