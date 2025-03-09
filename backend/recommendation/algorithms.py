# recommendation/algorithms.py

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def compute_content_similarity(song_features: pd.DataFrame) -> pd.DataFrame:
    """
    计算基于内容的歌曲相似度矩阵。

    参数:
      song_features: DataFrame, 行为歌曲，列为特征
    返回:
      DataFrame, 余弦相似度矩阵，其中 entry (i, j) 表示歌曲 i 与歌曲 j 的相似度。
    """
    # 计算余弦相似度，返回二维 numpy 数组
    sim_matrix = cosine_similarity(song_features.values)
    # 将结果转换为 DataFrame，行列索引与 song_features 相同
    return pd.DataFrame(
        sim_matrix, index=song_features.index, columns=song_features.index
    )


def compute_collaborative_score(
    ratings_matrix: pd.DataFrame, user_id: int
) -> pd.Series:
    """
    使用基于物品的协同过滤方法，计算用户对每首歌的预测评分。

    参数:
      ratings_matrix: DataFrame, 行为用户，列为歌曲，值为评分
      user_id: int, 指定用户的 id
    返回:
      Series, 每首歌的预测评分。
    """
    # 计算歌曲之间的相似度矩阵（协同过滤部分）
    song_similarity = cosine_similarity(ratings_matrix.T)
    song_similarity = pd.DataFrame(
        song_similarity, index=ratings_matrix.columns, columns=ratings_matrix.columns
    )

    # 取出该用户的评分记录（Series）
    user_ratings = ratings_matrix.loc[user_id]
    # 只考虑用户评分过的歌曲
    rated_songs = user_ratings[user_ratings > 0].index
    if len(rated_songs) == 0:
        # 如果用户没有评分记录，返回一个全零的 Series
        return pd.Series(0, index=ratings_matrix.columns)

    # 对于每首歌，计算预测评分
    pred_scores = {}
    for song in ratings_matrix.columns:
        # 获取当前歌曲与用户评分过的歌曲的相似度
        sims = song_similarity.loc[song, rated_songs]
        ratings = user_ratings[rated_songs]
        numerator = np.dot(sims, ratings)
        denominator = np.abs(sims).sum()
        pred_scores[song] = numerator / denominator if denominator != 0 else 0
    return pd.Series(pred_scores)


def hybrid_recommendation(
    user_id: int,
    song_features: pd.DataFrame,
    ratings_matrix: pd.DataFrame,
    alpha: float = 0.5,
) -> pd.Series:
    """
    混合推荐算法：结合基于内容的推荐和协同过滤推荐。

    参数:
      user_id: int, 当前用户 id
      song_features: DataFrame, 每首歌的内容特征，行为歌曲
      ratings_matrix: DataFrame, 用户评分矩阵，行为用户，列为歌曲
      alpha: float, 内容推荐和协同过滤的权重，alpha∈[0,1]
             alpha 越高表示内容推荐占比越大。
    返回:
      Series, 每首歌的综合推荐得分，推荐得分越高，歌曲越适合该用户。

    计算方法:
      综合得分 = α * content_score + (1 - α) * collaborative_score

      - content_score: 对于每首歌，计算与用户已听歌曲的内容相似度均值。
      - collaborative_score: 使用协同过滤预测的评分。
    """
    # 基于内容推荐部分：计算歌曲内容相似度矩阵
    content_sim = compute_content_similarity(song_features)

    # 假设我们有用户的行为数据，用户已听歌曲用 ratings_matrix 中的评分来表示
    # 获取该用户已评分歌曲的索引
    user_ratings = ratings_matrix.loc[user_id]
    rated_songs = user_ratings[user_ratings > 0].index
    if len(rated_songs) == 0:
        # 如果用户没有评分记录，则内容评分设置为0
        content_scores = pd.Series(0, index=song_features.index)
    else:
        # 对于每首歌 i，计算 content_score(i) = 平均(相似度(song i 与用户已评分歌曲))
        content_scores = content_sim.loc[:, rated_songs].mean(axis=1)

    # 协同过滤部分：计算预测评分
    collab_scores = compute_collaborative_score(ratings_matrix, user_id)

    # 综合得分：线性加权组合两部分得分
    hybrid_scores = alpha * content_scores + (1 - alpha) * collab_scores
    return hybrid_scores.sort_values(ascending=False)
