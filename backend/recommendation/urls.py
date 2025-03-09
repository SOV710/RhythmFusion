# recommendation/urls.py
from django.urls import path
from .views import RecommendationAPIView

urlpatterns = [
    # 推荐接口：
    # 当客户端请求 URL 为 /recommendations/ 时，将调用 RecommendationAPIView，
    # 返回当前用户的混合推荐结果
    path("", RecommendationAPIView.as_view(), name="recommendation"),
]
