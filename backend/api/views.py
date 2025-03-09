# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response


class BaseAPIView(APIView):
    """
    基础 API 视图类，提供统一响应格式和错误处理：
    返回的数据格式统一为：
    {
        "status": "success" 或 "error",
        "data": <具体数据或 null>,
        "message": <提示信息>
    }
    所有其他 API 视图可继承此类以获得统一的响应结构。
    """

    def success_response(self, data, message=""):
        """
        构造成功响应
        :param data: 成功返回的数据
        :param message: 可选的提示信息
        :return: Response 对象
        """
        return Response({"status": "success", "data": data, "message": message})

    def error_response(self, errors, message=""):
        """
        构造错误响应
        :param errors: 错误信息（通常为 serializer.errors）
        :param message: 可选的错误提示
        :return: Response 对象
        """
        return Response(
            {"status": "error", "data": None, "message": message, "errors": errors}
        )
