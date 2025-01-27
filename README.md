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
git clone https://github.com/WallBreakerNO4/Danbooru-characters-search.git
cd Danbooru-characters-search
```

2. 安装依赖：

```bash
pip install -r requirement.txt
```

3. 安装 Pybooru:
```bash
git clone https://github.com/LuqueDaniel/pybooru.git
```
> pypi 上的库太老了，需要手动安装


4. 配置 Danbooru 客户端：
    - 复制 `danbooru_client.py.example` 为 `danbooru_client.py`
    - 在 `danbooru_client.py` 中填入你的 Danbooru API 凭证

## 使用方法

### 1. 获取角色数据

运行主程序：

```bash
python pybooru_search.py
```

按照交互式提示操作：
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

### 2. 转换为 txt 格式

运行转换程序：

```bash
python csv_to_txt.py
```

按照交互式提示操作：
- 输入最小 post 数量（默认为 30）
- 程序会自动处理 outputs 目录下的所有 CSV 文件
- 生成的 txt 文件与原 CSV 文件同名，但扩展名改为 .txt
- 转换完成后程序自动退出

生成的 txt 文件格式兼容 [sd-dynamic-prompts](https://github.com/adieyal/sd-dynamic-prompts)，可直接用于提示词生成。

## 注意事项

- 需要有效的 Danbooru 账号才能使用 API
- Danbooru 本身的数据库并没有直接标出角色性别，本工具是基于相关标签的统计进行判断，可能存在误差

## TODO

- 添加更多分类方法（如过滤和 swim 相关的角色），而不是单纯的按性别分类

## 许可证

MIT License
