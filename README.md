# Danbooru游戏角色标签分析工具

这是一个基于 Pybooru 的 Python 工具，用于从 Danbooru 获取和分析特定游戏的角色标签数据。该工具可以自动获取角色信息并按性别进行分类，生成相应的数据文件。

## 功能特性

- 支持按游戏名称搜索相关角色标签
- 自动将角色按性别（男性/女性/未知）分类
- 基于相关标签频率的智能性别判断
- 支持导出数据为 CSV 格式
- 支持自定义搜索页数
- 可选择是否隐藏无投稿的标签
- 包含进度条显示搜索进度
- 交互式命令行界面，方便操作

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

3. 配置 Danbooru 客户端：
    - 复制 `danbooru_client.py.example` 为 `danbooru_client.py`
    - 在 `danbooru_client.py` 中填入你的 Danbooru API 凭证

## 使用方法

1. 运行主程序：

```bash
python pybooru_search.py
```

2. 按照交互式提示操作：
    - 输入游戏名称或部分名称（默认为 'arknights'）
    - 从搜索结果中选择具体的游戏
    - 设置最大搜索页数（默认为 3）
    - 选择是否显示无投稿的标签

输出文件将保存在 `outputs` 目录下，包括：
- `[game_name]_male_characters.csv`：男性角色数据
- `[game_name]_female_characters.csv`：女性角色数据
- `[game_name]_unknown_gender_characters.csv`：未知性别角色数据

每个 CSV 文件包含以下信息：
- name：角色名称
- male_frequency_avg：男性相关标签的平均频率
- female_frequency_avg：女性相关标签的平均频率
- post_count：投稿数量

3. 转换为 [sd-dynamic-prompts](https://github.com/adieyal/sd-dynamic-prompts) 兼容格式的 txt 文件（可选）：

```bash
python csv_to_txt.py [minimal_post_count] # 小于这个数的角色会被过滤
```

## 注意事项

- 需要有效的 Danbooru 账号才能使用 API
- Danbooru 本身的数据库并没有直接标出角色性别，本工具是基于相关标签的统计进行判断，可能存在误差
- 

## 许可证

MIT License
