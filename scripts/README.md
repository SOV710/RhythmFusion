该文档介绍如何使用 `scripts/` 目录下的脚本将数据上传MySQL客户端（或许可以上传到别的SQL客户端，不过没试过）。需要进行如下流程： CSV→JSON 转换和数据上传，或者直接使用我的数据库备份。

## 目录结构

```text
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
└── README.md           # 本文档
```

## 前置条件

- **Python**: 3.9 及以上版本

- **Django REST Framework**: 已部署并可通过 `UploadView` 接口接收 JSON

- **网络连通**: `upload_all.sh` 能通过 HTTP 访问后端 API

- **MySQL 客户端**: 和ORM配套的，成功部署该项目的应该都有

## 如何使用

你有两种方法可以往数据库里注入数据，一种是直接用我的数据库备份，我备份了一个名为`music_recommendation`的数据库，也是默认创建的数据库，你可以这样恢复它：
```bash
# （1）在恢复前，先在 MySQL 中创建一个目标数据库（此处名字为music_recommendation）：
mysql -u root -p -e "CREATE DATABASE music_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# （2）用备份文件导入到刚建的数据库：
mysql -u root -p music_recommendation < mysql_backup.sql
```

另外，你也可以自定义导入歌曲，你先在[TuneMyMusic](https://www.tunemymusic.com/home)（或者任一可行的音乐平台）上导出你想导入歌单的CSV，将CSV文件导入`input/`文件夹，然后在使用脚本中的`convert.py`进行解析转为json，`convert.py`解析单个文件的使用方法如下：

```bash
python convert.py
```

这会将`input/`文件夹下的`.csv`文件全部解析转为`output/`文件夹下的`.json`格式文件，我在文件夹内放了我的解析范例，可供参考，你需要在实际使用的时候删除它们。

然后可通过运行`upload.sh`脚本，将歌曲导入数据库

```bash
# （1）赋予脚本可执行权限
chmod +x upload.sh

# （2）执行上传脚本
./upload.sh
```

（❗注：如果你的DRF Server不在127.0.0.1:8000下，请自行修改`upload.sh`中的`API_URL`变量为你开放的服务器域名）

## 脚本说明

- **csv2json.py**: 定义 `csv_to_json` 函数，删除多余字段，保留 `Track name` 和 `Artist name`，并插入 `School`

- **convert.py**: 扫描 `assets/` 中所有 CSV，推断 `school` 并生成 JSON 到 `output/`

- **upload.sh**: 遍历 `output/*.json`，使用 `curl` 调用 DRF 批量上传接口

- **mysql_backup.sql**: 包含 `music_song` 表的导出结构和数据，用于备份或初始化


## 注意事项

- CSV 文件名需遵循 `{school}_{...}.csv` 格式，以正确推断 `School`
