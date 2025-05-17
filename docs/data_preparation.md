# RhythmFusion 数据准备指南

本文档详细介绍了 RhythmFusion 音乐推荐系统的数据准备和导入流程，包括数据格式要求、预处理步骤和导入方法。

## 数据要求

RhythmFusion 需要以下数据才能正常运行推荐系统：

### 歌曲元数据

每首歌曲需要包含以下基本信息：

- 歌曲名称 (title)
- 艺术家 (artist)
- 音乐流派/学派 (school)
- 专辑名称 (album) - 可选
- 时长 (duration) - 可选

### 数据格式

系统支持从 CSV 文件导入歌曲数据，CSV 文件格式要求如下：

```
"Track name","Artist name"
"Bohemian Rhapsody","Queen"
"Hotel California","Eagles"
...
```

文件命名格式应为 `{school}_{序号}.csv`，如 `rock_1.csv`，系统会根据文件名自动推断音乐流派/学派。

## 数据准备工具

RhythmFusion 提供了一系列脚本工具，用于数据转换和批量导入：

### 脚本目录结构

```
scripts/
├── input/              # 原始 CSV 数据目录
│   ├── blues_1.csv
│   └── ...
├── output/             # 中转生成的 JSON 文件目录
│   ├── blues_1.json
│   └── ...
├── csv2json.py         # CSV→JSON 转换库
├── convert.py          # CSV→JSON 转换脚本
├── upload.sh           # 批量上传脚本 (curl + DRF 接口)
├── mysql_backup.sql    # MySQL 备份/恢复脚本
└── README.md           # 脚本说明文档
```

### 导入流程

数据导入有两种方式：

#### 方式一：使用现有数据库备份（推荐）

如果您想快速开始，可以使用项目提供的数据库备份：

```bash
# 1. 创建 MySQL 数据库
mysql -u root -p -e "CREATE DATABASE music_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 导入数据库备份
mysql -u root -p music_recommendation < scripts/mysql_backup.sql
```

#### 方式二：自定义数据导入

如果您想导入自己的音乐数据，请按照以下步骤操作：

1. **准备 CSV 文件**：

   从音乐平台（如 [TuneMyMusic](https://www.tunemymusic.com/home)）导出歌单为 CSV 格式，并按照 `{school}_{序号}.csv` 命名规则将文件放入 `scripts/input/` 目录。
2. **转换为 JSON 格式**：

   ```bash
   cd scripts
   python convert.py
   ```

   这将处理 `input/` 目录中的所有 CSV 文件，生成的 JSON 文件将保存到 `output/` 目录。
3. **上传数据**：

   ```bash
   # 赋予脚本执行权限
   chmod +x upload.sh

   # 执行上传脚本
   ./upload.sh

   # Windows
   powershell .\upload.ps1
   ```

   > 注意：如果您的 Django 服务不在 127.0.0.1:8000，请修改 `upload.sh` 中的 `API_URL` 变量。
   >

## CSV 文件转换细节

`csv2json.py` 脚本执行以下转换操作：

1. 读取 CSV 文件的 "Track name" 和 "Artist name" 列
2. 根据文件名自动推断 "School" 字段
3. 生成包含 `title`、`artist` 和 `school` 字段的 JSON 对象
4. 将结果保存为 JSON 文件

示例：

```python
# 自动推断学派
def infer_school_from_filename(filename):
    # 从文件名 blues_1.csv 中提取 blues
    name_parts = os.path.basename(filename).split('_')
    if len(name_parts) > 0:
        return name_parts[0]
    return "unknown"

# CSV 转 JSON
def csv_to_json(csv_file, json_file, school=None):
    # 如果没有指定学派，则从文件名推断
    if school is None:
        school = infer_school_from_filename(csv_file)
  
    # 处理 CSV 数据
    songs = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Track name' in row and 'Artist name' in row:
                songs.append({
                    'title': row['Track name'],
                    'artist': row['Artist name'],
                    'school': school
                })
  
    # 写入 JSON 文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
```

## 批量上传

`upload.sh` 脚本使用 curl 调用 Django REST Framework 的 API 接口，将 JSON 数据上传到服务器：

```bash
#!/bin/bash

API_URL="http://127.0.0.1:8000/api/music/csv/"

# 遍历 output 目录中的所有 JSON 文件
for json_file in output/*.json; do
  echo "Uploading $json_file..."
  
  # 使用 curl 发送 POST 请求
  curl -X POST \
    -H "Content-Type: application/json" \
    -d @"$json_file" \
    "$API_URL"
  
  echo "Done."
done
```

## 建立推荐模型

数据导入后，需要初始化推荐系统的各个组件。执行以下命令：

```bash
# 进入后端目录
cd backend

# 1. 构建用户-歌曲交互矩阵
python manage.py build_interaction_matrix

# 2. 训练协同过滤模型
python manage.py train_cf_model --factors 1

# 3. 生成内容特征向量
python manage.py generate_content_vectors

# 4. 生成混合向量
python manage.py generate_hybrid_vectors

# 5. 构建 FAISS 索引
python manage.py build_faiss_index
```

这些命令将依次：

1. 从用户-歌曲交互记录构建交互矩阵
2. 使用 SVD 算法训练协同过滤模型
3. 为每首歌曲生成基于艺术家和流派的内容特征向量
4. 将协同过滤向量和内容特征向量合并为混合向量
5. 构建高效的向量搜索索引

## 数据验证

导入数据后，您可以通过以下方式验证数据是否正确导入：

```bash
# 进入 Django Shell
python manage.py shell

# 查询数据
from music.models import Song
print(f"Total songs: {Song.objects.count()}")
print(f"Schools: {list(Song.objects.values_list('school', flat=True).distinct())}")
```

## 数据维护

### 定期更新推荐模型

随着用户交互数据的积累，建议定期更新推荐模型以提升推荐效果：

```bash
# 在crontab中设置定期任务
0 3 * * * cd /path/to/RhythmFusion/backend && python manage.py build_interaction_matrix && python manage.py train_cf_model --factors 50 && python manage.py generate_hybrid_vectors && python manage.py build_faiss_index
```

上述命令安排系统每天凌晨3点更新推荐模型。

### 数据备份

建议定期备份歌曲数据和用户数据：

```bash
# 备份 MySQL 数据库
mysqldump -u root -p music_recommendation > backup_$(date +%Y%m%d).sql
```

## 疑难解答

### 常见问题

1. **CSV 解析错误**

   - 检查 CSV 文件编码是否为 UTF-8
   - 确保列名正确（"Track name" 和 "Artist name"）
   - 检查 CSV 分隔符是否为逗号
2. **上传失败**

   - 确认 Django 服务正在运行
   - 检查 API URL 是否正确
   - 验证 JSON 格式是否有效
3. **推荐模型初始化失败**

   - 确保已导入足够的歌曲数据
   - 检查是否存在用户交互数据（歌单、喜好记录）
   - 查看 Django 日志以获取详细错误信息
4. **批量导入速度慢**

   - 考虑将大量数据分批导入
   - 临时禁用数据库索引再导入后重建
   - 调整 Django 配置以优化批处理性能

## 参考资料

- [数据导入脚本使用说明](../scripts/README.md)
- [Django 批量操作文档](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#bulk-create)
- [FAISS 索引指南](https://github.com/facebookresearch/faiss/wiki/Getting-started)
- [SVD 推荐算法原理](https://en.wikipedia.org/wiki/Singular_value_decomposition)
