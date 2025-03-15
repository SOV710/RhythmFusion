# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response


class BaseAPIView(APIView):
    """
    Base API view class that provides a unified response format and error handling:
    The returned data is standardized as follows:
    {
        "status": "success" or "error",
        "data": <specific data or null>,
        "message": <prompt message>
    }
    All other API views can inherit from this class to ensure a consistent response structure.
    """

    def success_response(self, data, message=""):
        """
        Construct a success response.
        :param data: Data successfully returned
        :param message: Optional prompt message
        :return: Response object
        """
        return Response({"status": "success", "data": data, "message": message})

    def error_response(self, errors, message=""):
        """
        Construct a failed response
        :param errors: error info (usually serializer.errors
        :param message: optional error hint
        :return: Response 对象
        """
        return Response(
            {"status": "error", "data": None, "message": message, "errors": errors}
        )
