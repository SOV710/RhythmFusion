# recommendation/tests.py

from django.test import TestCase
import pandas as pd
from recommendation.algorithms import (
    compute_content_similarity,
    compute_collaborative_score,
    hybrid_recommendation,
)


class RecommendationAlgorithmTest(TestCase):
    def setUp(self):
        # 构造示例歌曲特征数据，假设有3首歌，每首歌用2个特征表示
        self.song_features = pd.DataFrame(
            {"feature1": [0.8, 0.4, 0.9], "feature2": [0.1, 0.7, 0.2]}, index=[1, 2, 3]
        )  # 行索引为歌曲ID

        # 构造用户评分矩阵，假设有2个用户和3首歌，评分为 1-5
        # 行为用户ID，列为歌曲ID
        self.ratings_matrix = pd.DataFrame(
            {1: [5, 0, 3], 2: [0, 4, 0], 3: [2, 0, 0]}, index=[101, 102, 103]
        )  # 用户ID 101,102,103

    def test_content_similarity(self):
        sim_matrix = compute_content_similarity(self.song_features)
        # 测试相似度矩阵的形状
        self.assertEqual(sim_matrix.shape, (3, 3))

    def test_collaborative_score(self):
        # 测试对用户 101 的协同过滤预测评分
        scores = compute_collaborative_score(self.ratings_matrix, 101)
        self.assertEqual(len(scores), 3)

    def test_hybrid_recommendation(self):
        # 测试混合推荐的输出，权重设为 0.6
        scores = hybrid_recommendation(
            101, self.song_features, self.ratings_matrix, alpha=0.6
        )
        # 检查返回的 Series 是否排序（降序）
        self.assertTrue((scores.diff().dropna() <= 0).all())
