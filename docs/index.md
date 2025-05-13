# RhythmFusion 音乐推荐系统文档

<div align="center">
    <img src="https://via.placeholder.com/200x200.png?text=RhythmFusion" alt="RhythmFusion Logo" width="200"/>
</div>

## 文档概述

欢迎使用 RhythmFusion 音乐推荐系统文档！本文档旨在帮助开发者和用户了解和使用 RhythmFusion 系统。RhythmFusion 是一个基于 Django 和 Vue.js 构建的现代化音乐推荐系统，提供个性化推荐、歌单管理及音乐播放功能，为用户创造流畅、智能的音乐体验。

## 目录

1. [系统架构](architecture.md)
2. [后端文档](backend/index.md)
   - [API 接口](api_doc.md)
   - [数据模型](backend/models.md)
   - [推荐算法](backend/recommendation.md)
3. [前端文档](frontend/index.md)
   - [组件结构](frontend/components.md)
   - [状态管理](frontend/state.md)
   - [路由设计](frontend/routing.md)
4. [部署指南](deployment.md)
5. [数据导入与准备](data_preparation.md)
6. [开发指南](development.md)
7. [使用教程](user_guide.md)

## 系统特点

- **混合推荐算法**：结合协同过滤和内容特征的创新推荐方案
- **响应式前端**：基于 Vue 3 和 TypeScript 的现代化用户界面
- **RESTful API**：规范化的后端接口设计
- **高效索引**：使用 FAISS 向量检索实现快速推荐
- **可扩展架构**：模块化设计支持功能和规模扩展

## 快速开始

如果您想快速开始使用 RhythmFusion，请参考[部署指南](deployment.md)和[使用教程](user_guide.md)。对于开发者，建议先了解[系统架构](architecture.md)和[开发指南](development.md)。

## 技术栈概览

**前端**：Vue 3.5.13, TypeScript, Vite 6.2.1, Pinia, Axios, SCSS  
**后端**：Django 5.0.2, Django REST Framework, SQLite/MySQL  
**推荐系统**：SVD协同过滤, 内容特征提取, FAISS向量检索

## 贡献

我们欢迎任何形式的贡献，包括但不限于：功能建议、代码贡献、文档改进等。请查看[开发指南](development.md)了解如何参与项目开发。 