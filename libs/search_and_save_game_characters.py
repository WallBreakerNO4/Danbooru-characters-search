import os
from tqdm import tqdm
import csv
from libs.character_search import client, calculate_gender_frequencies


def save_characters_to_files(analyzed_characters, game_name, output_dir):
    """
    将分析好的角色数据保存到CSV文件
    :param analyzed_characters: 已分析的角色数据列表
    :param game_name: 游戏名称
    :param output_dir: 输出目录
    """
    # 创建文件名
    male_filename = os.path.join(output_dir, f"{game_name}_male_characters.csv")
    female_filename = os.path.join(output_dir, f"{game_name}_female_characters.csv")
    unknown_filename = os.path.join(output_dir, f"{game_name}_unknown_gender_characters.csv")
    
    # 按性别分组数据
    male_characters = [c for c in analyzed_characters if c["gender"] == "male"]
    female_characters = [c for c in analyzed_characters if c["gender"] == "female"]
    unknown_characters = [c for c in analyzed_characters if c["gender"] == "unknown"]
    
    # CSV头部
    headers = [
        "name",
        "male_frequency_avg",
        "female_frequency_avg",
        "post_count",
        "created_at",
        "updated_at",
    ]
    
    # 写入男性角色文件
    with open(male_filename, "w", encoding="utf-8", newline="") as male_file:
        male_writer = csv.writer(male_file)
        male_writer.writerow(headers)
        for character in male_characters:
            row_data = [
                character["name"],
                character["male_frequency_avg"],
                character["female_frequency_avg"],
                character["post_count"],
                character["created_at"],
                character["updated_at"],
            ]
            male_writer.writerow(row_data)
    
    # 写入女性角色文件
    with open(female_filename, "w", encoding="utf-8", newline="") as female_file:
        female_writer = csv.writer(female_file)
        female_writer.writerow(headers)
        for character in female_characters:
            row_data = [
                character["name"],
                character["male_frequency_avg"],
                character["female_frequency_avg"],
                character["post_count"],
                character["created_at"],
                character["updated_at"],
            ]
            female_writer.writerow(row_data)
    
    # 写入未知性别角色文件
    with open(unknown_filename, "w", encoding="utf-8", newline="") as unknown_file:
        unknown_writer = csv.writer(unknown_file)
        unknown_writer.writerow(headers)
        for character in unknown_characters:
            row_data = [
                character["name"],
                character["male_frequency_avg"],
                character["female_frequency_avg"],
                character["post_count"],
                character["created_at"],
                character["updated_at"],
            ]
            unknown_writer.writerow(row_data)


def search_and_save_game_characters(game_name, max_pages=3, hide_empty=True):
    """
    搜索指定游戏的所有角色tag并按性别分类保存到文件
    :param game_name: 游戏名称
    :param max_pages: 最大搜索页数，默认为3页
    :param hide_empty: 是否隐藏没有投稿的tag
    """
    try:
        # 创建outputs文件夹（如果不存在）
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        page = 1
        limit = 1000  # 每页最大记录数
        all_character_tags = []

        print(f"正在获取{game_name}的角色数据...")
        with tqdm(total=max_pages, desc="获取角色列表") as pbar:
            while page <= max_pages:
                character_tags = client.tag_list(
                    name_matches=f"*{game_name}*",
                    category=4,
                    order="count",
                    page=page,
                    limit=limit,
                    hide_empty=hide_empty,
                )

                # # 打印第一个tag的内容以检查结构
                # if character_tags and page == 1:
                #     print("\nDebug - First tag content:")
                #     print(character_tags[0])

                if not character_tags:
                    break

                all_character_tags.extend(character_tags)
                page += 1
                pbar.update(1)

        # 第一阶段：分析角色性别并保存在内存中
        filtered_characters = [
            tag
            for tag in all_character_tags
            if game_name.lower() in tag.get("name", "").lower()
        ]
        
        print("\n正在分析角色性别...")
        analyzed_characters = []
        
        for tag in tqdm(filtered_characters, desc="分析角色性别"):
            name = tag.get("name", "")
            post_count = tag.get("post_count", 0)
            created_at = tag.get("created_at", "")
            updated_at = tag.get("updated_at", "")

            try:
                # 使用新的函数计算性别频率
                (
                    male_releted_tags_frequency_avg,
                    female_releted_tags_frequency_avg,
                ) = calculate_gender_frequencies(name)

                # 判断性别
                if male_releted_tags_frequency_avg > female_releted_tags_frequency_avg:
                    gender = "male"
                elif female_releted_tags_frequency_avg > male_releted_tags_frequency_avg:
                    gender = "female"
                else:
                    gender = "unknown"

                # 保存角色数据到内存
                character_data = {
                    "name": name,
                    "male_frequency_avg": male_releted_tags_frequency_avg,
                    "female_frequency_avg": female_releted_tags_frequency_avg,
                    "post_count": post_count,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "gender": gender
                }
                analyzed_characters.append(character_data)

            except Exception as e:
                print(f"\n获取角色 {name} 的相关tag时出错: {e}")
                # 错误情况也保存到内存
                character_data = {
                    "name": name,
                    "male_frequency_avg": 0,
                    "female_frequency_avg": 0,
                    "post_count": post_count,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "gender": "unknown"
                }
                analyzed_characters.append(character_data)

        # 第二阶段：将内存中的数据写入文件
        print("\n正在保存角色数据到文件...")
        save_characters_to_files(analyzed_characters, game_name, output_dir)
        
        # 统计结果
        male_count = len([c for c in analyzed_characters if c["gender"] == "male"])
        female_count = len([c for c in analyzed_characters if c["gender"] == "female"])
        unknown_count = len([c for c in analyzed_characters if c["gender"] == "unknown"])
        
        male_filename = os.path.join(output_dir, f"{game_name}_male_characters.csv")
        female_filename = os.path.join(output_dir, f"{game_name}_female_characters.csv")
        unknown_filename = os.path.join(output_dir, f"{game_name}_unknown_gender_characters.csv")
        
        print(f"\n角色tag保存完成:")
        print(f"男性角色: {male_count} 个，保存在 {male_filename}")
        print(f"女性角色: {female_count} 个，保存在 {female_filename}")
        print(f"未知性别: {unknown_count} 个，保存在 {unknown_filename}")
        print(f"搜索了 {page-1} 页数据")

    except Exception as e:
        print(f"保存角色tag时出错: {e}")
