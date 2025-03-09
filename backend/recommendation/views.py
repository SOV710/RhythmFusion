# recommendation/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recommendation.algorithms import hybrid_recommendation
import pandas as pd


class RecommendationAPIView(APIView):
    """
    推荐 API 视图：
    该视图负责计算并返回混合推荐结果。
    前端调用该接口时，后端将基于当前用户的行为数据和歌曲特征，
    计算出每首歌的推荐得分，并以 JSON 格式返回。
    """

    def get(self, request, format=None):
        # 示例：假设当前用户 ID 为 request.user.id（需认证）或通过查询参数传递
        user_id = request.user.id if request.user.is_authenticated else None
        if user_id is None:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 模拟：构造歌曲特征数据，实际项目中应从数据库或外部文件加载
        # 此处使用 Pandas DataFrame，行索引为歌曲 ID
        song_features = pd.DataFrame(
            {"feature1": [0.8, 0.4, 0.9, 0.2], "feature2": [0.1, 0.7, 0.2, 0.5]},
            index=[1, 2, 3, 4],
        )

        # 模拟：构造用户评分矩阵
        # 行索引为用户 ID，列索引为歌曲 ID，值为评分
        ratings_matrix = pd.DataFrame(
            {1: [5, 0, 3, 0], 2: [0, 4, 0, 0], 3: [2, 0, 0, 0], 4: [0, 5, 0, 4]},
            index=[101, 102, 103, 104],
        )

        # 调用混合推荐算法，权重 alpha 可根据需要调整，此处设为 0.5
        rec_scores = hybrid_recommendation(
            user_id, song_features, ratings_matrix, alpha=0.5
        )
        # 转换为字典格式，键为歌曲 ID，值为推荐得分
        rec_dict = rec_scores.to_dict()

        return Response(
            {"user_id": user_id, "recommendations": rec_dict}, status=status.HTTP_200_OK
        )
