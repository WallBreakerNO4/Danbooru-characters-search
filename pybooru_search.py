from danbooru_client import create_danbooru_client
import sys
from tqdm import tqdm
import os
import csv
import argparse

# 创建Danbooru客户端
client = create_danbooru_client()

def save_game_characters_to_file(game_name, max_pages=3, hide_empty=True):
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
                    hide_empty=hide_empty
                )
                
                if not character_tags:
                    break
                    
                all_character_tags.extend(character_tags)
                page += 1
                pbar.update(1)

        # 创建男性和女性角色的文件名（添加outputs路径）
        male_filename = os.path.join(output_dir, f"{game_name}_male_characters.csv")
        female_filename = os.path.join(output_dir, f"{game_name}_female_characters.csv")
        unknown_filename = os.path.join(output_dir, f"{game_name}_unknown_gender_characters.csv")
        
        male_count = 0
        female_count = 0
        unknown_count = 0
        
        # 定义性别关键词
        male_gender_keywords = ['male', 'boy']
        female_gender_keywords = ['female', 'girl']
        
        # 打开三个CSV文件用于写入
        with open(male_filename, 'w', encoding='utf-8', newline='') as male_file, \
             open(female_filename, 'w', encoding='utf-8', newline='') as female_file, \
             open(unknown_filename, 'w', encoding='utf-8', newline='') as unknown_file:
            
            # 创建CSV写入器
            male_writer = csv.writer(male_file)
            female_writer = csv.writer(female_file)
            unknown_writer = csv.writer(unknown_file)
            
            # 写入CSV头部
            headers = ['name', 'male_frequency_avg', 'female_frequency_avg', 'post_count']
            male_writer.writerow(headers)
            female_writer.writerow(headers)
            unknown_writer.writerow(headers)
            
            filtered_characters = [tag for tag in all_character_tags if game_name.lower() in tag.get('name', '').lower()]
            print("\n正在分析角色性别...")
            
            for tag in tqdm(filtered_characters, desc="分析角色性别"):
                name = tag.get('name', '')
                post_count = tag.get('post_count', 0)
                try:
                    # 获取角色的相关标签
                    tag_related = client.tag_related(name)
                    
                    # 初始化性别相关计数
                    male_releted_tags_count = 0
                    female_releted_tags_count = 0
                    male_releted_tags_frequency_sum = 0
                    female_releted_tags_frequency_sum = 0
                    
                    # 先处理female标签
                    female_matched_tags = []
                    for keyword in female_gender_keywords:
                        gender_tags = [tag for tag in tag_related.get('related_tags') 
                                    if keyword in tag.get('tag')['name'].lower()]
                        for tag in gender_tags:
                            female_releted_tags_count += 1
                            female_releted_tags_frequency_sum += tag['frequency']
                            female_matched_tags.append(tag)
                    
                    # 从所有标签中移除female标签，再处理male标签
                    remaining_tags = [tag for tag in tag_related.get('related_tags') if tag not in female_matched_tags]
                    for keyword in male_gender_keywords:
                        gender_tags = [tag for tag in remaining_tags 
                                    if keyword in tag.get('tag')['name'].lower()]
                        for tag in gender_tags:
                            male_releted_tags_count += 1
                            male_releted_tags_frequency_sum += tag['frequency']
                    
                    # 计算平均频率
                    male_releted_tags_frequency_avg = male_releted_tags_frequency_sum / male_releted_tags_count if male_releted_tags_count > 0 else 0
                    female_releted_tags_frequency_avg = female_releted_tags_frequency_sum / female_releted_tags_count if female_releted_tags_count > 0 else 0
                    
                    # 准备CSV行数据
                    row_data = [name, male_releted_tags_frequency_avg, female_releted_tags_frequency_avg, post_count]
                    
                    # 根据频率判断性别并写入相应的CSV文件
                    if male_releted_tags_frequency_avg > female_releted_tags_frequency_avg:
                        male_writer.writerow(row_data)
                        male_count += 1
                    elif female_releted_tags_frequency_avg > male_releted_tags_frequency_avg:
                        female_writer.writerow(row_data)
                        female_count += 1
                    else:
                        unknown_writer.writerow(row_data)
                        unknown_count += 1
                        
                except Exception as e:
                    print(f"\n获取角色 {name} 的相关tag时出错: {e}")
                    unknown_writer.writerow([name, 0, 0, post_count])
                    unknown_count += 1
        
        print(f"\n角色tag保存完成:")
        print(f"男性角色: {male_count} 个，保存在 {male_filename}")
        print(f"女性角色: {female_count} 个，保存在 {female_filename}")
        print(f"未知性别: {unknown_count} 个，保存在 {unknown_filename}")
        print(f"搜索了 {page-1} 页数据")

    except Exception as e:
        print(f"保存角色tag时出错: {e}")

def interactive_cli():
    print("欢迎使用Pybooru角色搜索工具")
    print("输入游戏名称开始搜索，输入'q'退出")
    
    while True:
        game_name = input("\n请输入游戏名称（默认arknights）: ").strip()
        
        if game_name.lower() == 'q':
            print("退出程序")
            break
            
        if not game_name:
            game_name = "arknights"
            
        try:
            pages = input("请输入最大搜索页数（默认3）: ").strip()
            pages = int(pages) if pages else 3
            
            show_empty = input("是否显示无投稿的标签？(y/n, 默认n): ").strip().lower()
            hide_empty = show_empty != 'y'
            
            print(f"\n开始搜索游戏: {game_name}")
            save_game_characters_to_file(game_name, max_pages=pages, hide_empty=hide_empty)
            
        except ValueError:
            print("错误：请输入有效的数字")
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    interactive_cli()
