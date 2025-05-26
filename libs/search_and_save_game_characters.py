import os
from tqdm import tqdm
import csv
from libs.character_search import client, calculate_gender_frequencies


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

        # 创建男性和女性角色的文件名（添加outputs路径）
        male_filename = os.path.join(output_dir, f"{game_name}_male_characters.csv")
        female_filename = os.path.join(output_dir, f"{game_name}_female_characters.csv")
        unknown_filename = os.path.join(
            output_dir, f"{game_name}_unknown_gender_characters.csv"
        )

        male_count = 0
        female_count = 0
        unknown_count = 0

        # 打开三个CSV文件用于写入
        with open(male_filename, "w", encoding="utf-8", newline="") as male_file, open(
            female_filename, "w", encoding="utf-8", newline=""
        ) as female_file, open(
            unknown_filename, "w", encoding="utf-8", newline=""
        ) as unknown_file:

            # 创建CSV写入器
            male_writer = csv.writer(male_file)
            female_writer = csv.writer(female_file)
            unknown_writer = csv.writer(unknown_file)

            # 写入CSV头部
            headers = [
                "name",
                "male_frequency_avg",
                "female_frequency_avg",
                "post_count",
                "created_at",
                "updated_at",
            ]
            male_writer.writerow(headers)
            female_writer.writerow(headers)
            unknown_writer.writerow(headers)

            filtered_characters = [
                tag
                for tag in all_character_tags
                if game_name.lower() in tag.get("name", "").lower()
            ]
            print("\n正在分析角色性别...")

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

                    # 准备CSV行数据
                    row_data = [
                        name,
                        male_releted_tags_frequency_avg,
                        female_releted_tags_frequency_avg,
                        post_count,
                        created_at,
                        updated_at,
                    ]

                    # 根据频率判断性别并写入相应的CSV文件
                    if (
                        male_releted_tags_frequency_avg
                        > female_releted_tags_frequency_avg
                    ):
                        male_writer.writerow(row_data)
                        male_count += 1
                    elif (
                        female_releted_tags_frequency_avg
                        > male_releted_tags_frequency_avg
                    ):
                        female_writer.writerow(row_data)
                        female_count += 1
                    else:
                        unknown_writer.writerow(row_data)
                        unknown_count += 1

                except Exception as e:
                    print(f"\n获取角色 {name} 的相关tag时出错: {e}")
                    unknown_writer.writerow(
                        [name, 0, 0, post_count, created_at, updated_at]
                    )
                    unknown_count += 1

        print(f"\n角色tag保存完成:")
        print(f"男性角色: {male_count} 个，保存在 {male_filename}")
        print(f"女性角色: {female_count} 个，保存在 {female_filename}")
        print(f"未知性别: {unknown_count} 个，保存在 {unknown_filename}")
        print(f"搜索了 {page-1} 页数据")

    except Exception as e:
        print(f"保存角色tag时出错: {e}")
