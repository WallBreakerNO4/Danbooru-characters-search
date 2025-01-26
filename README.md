# Danbooru游戏角色标签分析工具

这是一个基于Pybooru的Python工具，用于从Danbooru获取和分析特定游戏的角色标签数据。该工具可以自动获取角色信息并按性别进行分类，生成相应的数据文件。

## 功能特性

- 支持按游戏名称搜索相关角色标签
- 自动将角色按性别（男性/女性/未知）分类
- 支持导出数据为CSV格式
- 支持自定义搜索页数
- 可选择是否隐藏无投稿的标签
- 包含进度条显示搜索进度

## 环境要求

- Python 3.6+
- tqdm
- Pybooru

## 安装说明

1. 克隆本仓库：
```bash
git clone [repository-url]
cd pybooru.pip
```

2. 安装依赖：
```bash
pip install -r requirement.txt
```

3. 克隆 `pybooru` 库：
```bash
git clone https://github.com/danbooru/pybooru.git
```
> pypi 上的版本太老了，需要手动克隆

4. 配置Danbooru客户端：
   - 复制 `danbooru_client.py.example` 为 `danbooru_client.py`
   - 在 `danbooru_client.py` 中填入你的Danbooru API凭证

## 使用方法

1. 搜索游戏角色并保存数据：
```python
from pybooru_search import save_game_characters_to_file

# 搜索明日方舟的角色数据，设置最大搜索3页
save_game_characters_to_file("arknights", max_pages=3, hide_empty=True)
```

2. 输出文件将保存在 `outputs` 目录下，包括：
   - `[game_name]_male_characters.csv`：男性角色数据
   - `[game_name]_female_characters.csv`：女性角色数据
   - `[game_name]_unknown_gender_characters.csv`：未知性别角色数据

## 注意事项

- 需要有效的Danbooru账号才能使用API
- Danbooru 本身的数据库并没有直接标出角色性别，本工具是基于角色标签的统计，可能存在误差

## 许可证

MIT License 