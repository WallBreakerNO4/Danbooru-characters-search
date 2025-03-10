from danbooru_client import create_danbooru_client
from tqdm import tqdm
import os
import csv

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
            headers = ['name', 'male_frequency_avg', 'female_frequency_avg', 'post_count', 'created_at', 'updated_at']
            male_writer.writerow(headers)
            female_writer.writerow(headers)
            unknown_writer.writerow(headers)
            
            filtered_characters = [tag for tag in all_character_tags if game_name.lower() in tag.get('name', '').lower()]
            print("\n正在分析角色性别...")
            
            for tag in tqdm(filtered_characters, desc="分析角色性别"):
                name = tag.get('name', '')
                post_count = tag.get('post_count', 0)
                created_at = tag.get('created_at', '')
                updated_at = tag.get('updated_at', '')
                
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
                        gender_tags = [tag for tag in tag_related.get('related_tags', []) 
                                    if keyword in tag.get('tag', {}).get('name', '').lower()]
                        for tag in gender_tags:
                            female_releted_tags_count += 1
                            female_releted_tags_frequency_sum += tag.get('frequency', 0)
                            female_matched_tags.append(tag)
                    
                    # 从所有标签中移除female标签，再处理male标签
                    remaining_tags = [tag for tag in tag_related.get('related_tags', []) if tag not in female_matched_tags]
                    for keyword in male_gender_keywords:
                        gender_tags = [tag for tag in remaining_tags 
                                    if keyword in tag.get('tag', {}).get('name', '').lower()]
                        for tag in gender_tags:
                            male_releted_tags_count += 1
                            male_releted_tags_frequency_sum += tag.get('frequency', 0)
                    
                    # 计算平均频率
                    male_releted_tags_frequency_avg = male_releted_tags_frequency_sum / male_releted_tags_count if male_releted_tags_count > 0 else 0
                    female_releted_tags_frequency_avg = female_releted_tags_frequency_sum / female_releted_tags_count if female_releted_tags_count > 0 else 0
                    
                    # 准备CSV行数据
                    row_data = [name, male_releted_tags_frequency_avg, female_releted_tags_frequency_avg, post_count, created_at, updated_at]
                    
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
                    unknown_writer.writerow([name, 0, 0, post_count, created_at, updated_at])
                    unknown_count += 1
        
        print(f"\n角色tag保存完成:")
        print(f"男性角色: {male_count} 个，保存在 {male_filename}")
        print(f"女性角色: {female_count} 个，保存在 {female_filename}")
        print(f"未知性别: {unknown_count} 个，保存在 {unknown_filename}")
        print(f"搜索了 {page-1} 页数据")

    except Exception as e:
        print(f"保存角色tag时出错: {e}")

def get_possible_game_names(search_term):
    """获取可能的游戏名列表"""
    try:
        games = client.tag_list(
            name_matches=f"*{search_term}*",
            category=3,  # 3表示游戏分类
            order="count",
            limit=10,
            hide_empty=True
        )
        return [tag['name'] for tag in games]
    except Exception as e:
        print(f"获取游戏列表时出错: {e}")
        return []

def interactive_cli():
    print("欢迎使用Pybooru角色搜索工具")
    
    search_term = input("\n请输入游戏名称或部分名称（默认为'arknights'）: ").strip()
    
    if not search_term:
        search_term = "arknights"
        
    # 获取可能的游戏名列表
    possible_games = get_possible_game_names(search_term)
    
    if not possible_games:
        print(f"未找到与'{search_term}'相关的游戏")
        return
        
    # 显示可选游戏列表
    print("\n找到以下游戏：")
    for i, game in enumerate(possible_games, 1):
        print(f"{i}. {game}")
        
    # 让用户选择游戏
    try:
        choice = input("\n请输入序号选择游戏（留空退出）: ").strip()
        if not choice:
            print("退出程序")
            return
            
        choice = int(choice)
        if not (1 <= choice <= len(possible_games)):
            print("无效的序号")
            return
            
        game_name = possible_games[choice - 1]
        
        pages = input("请输入最大搜索页数（输入q退出，默认3）: ").strip()
        if pages.lower() == 'q':
            print("退出程序")
            return
        pages = int(pages) if pages else 3
        
        show_empty = input("是否显示无投稿的标签？(y/n, 输入q退出，默认n): ").strip().lower()
        if show_empty == 'q':
            print("退出程序")
            return
        hide_empty = show_empty != 'y'
        
        print(f"\n开始搜索游戏: {game_name}")
        save_game_characters_to_file(game_name, max_pages=pages, hide_empty=hide_empty)
        
    except ValueError:
        print("错误：请输入有效的数字")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    interactive_cli()
