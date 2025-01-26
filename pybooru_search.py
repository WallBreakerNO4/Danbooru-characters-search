from danbooru_client import create_danbooru_client
import sys
from tqdm import tqdm

# 创建Danbooru客户端
client = create_danbooru_client()

def search_by_tags(tags, limit=10):
    """
    搜索指定tag的图片
    :param tags: 要搜索的tag字符串，多个tag用空格分隔
    :param limit: 返回结果数量限制
    """
    try:
        posts = client.post_list(tags=tags, limit=limit)
        
        print(f"\n搜索tag: {tags}")
        print("-" * 50)
        
        for post in posts:
            print(f"图片ID: {post.get('id', 'N/A')}")
            print(f"图片链接: {post.get('file_url', 'N/A')}")
            print(f"标签: {post.get('tag_string', '')[:100]}...")
            print(f"评分: {post.get('score', 'N/A')}")
            print("-" * 50)
    except Exception as e:
        print(f"搜索图片时出错: {e}")

def search_game_characters(game_name, max_pages=3,hide_empty=True):
    """
    搜索指定游戏的所有角色tag
    :param game_name: 游戏名称
    :param max_pages: 最大搜索页数，默认为3页
    """
    try:
        page = 1
        limit = 1000  # 每页最大记录数
        all_character_tags = []
        
        while page <= max_pages:
            # 使用order参数直接获取按post_count排序的结果
            character_tags = client.tag_list(
                name_matches=f"*{game_name}*", 
                category=4, 
                order="count",
                page=page,
                limit=limit,
                hide_empty=hide_empty
            )
            
            # 如果没有更多数据则退出循环
            if not character_tags:
                break
                
            all_character_tags.extend(character_tags)
            page += 1
        
        if all_character_tags:
            print("\n角色列表:")
            print("-" * 50)
            found_characters = 0
            
            for tag in all_character_tags:
                name = tag.get('name', 'N/A')
                post_count = tag.get('post_count', 0)
                
                # 只显示确实相关的角色
                if game_name.lower() in name.lower():
                    print(f"角色名称: {name}")
                    print(f"发布数量: {post_count}")
                    if tag.get('related_tags'):
                        related = tag.get('related_tags').split()[:5]  # 只显示前5个相关tag
                        print(f"相关tags: {', '.join(related)}")
                    print("-" * 50)
                    found_characters += 1
            
            print(f"\n总共找到 {found_characters} 个相关角色")
            print(f"搜索了 {page-1} 页数据")
        else:
            print(f"未找到任何与 '{game_name}' 相关的角色tag")

    except Exception as e:
        print(f"搜索角色时出错: {e}")

def search_tags(name_matches):
    """
    搜索tag名称
    :param name_matches: 要搜索的tag名称（部分匹配即可）
    """
    try:
        tags = client.tag_list(name_matches=f"*{name_matches}*", order="count")
        
        if not tags:
            print(f"\n未找到匹配的tag: {name_matches}")
            return
            
        print(f"\n搜索tag名称: {name_matches}")
        print("-" * 50)
        
        for tag in tags:
            print(f"Tag名称: {tag.get('name', 'N/A')}")
            print(f"Tag类型: {get_category_name(tag.get('category', -1))}")
            print(f"发布数量: {tag.get('post_count', 0)}")
            related = tag.get('related_tags', '')
            if related:
                print(f"相关tags: {related[:100]}...")
            print("-" * 50)
    except Exception as e:
        print(f"搜索tag时出错: {e}")

def get_category_name(category_id):
    """
    获取tag类型的名称
    """
    categories = {
        0: "General",
        1: "Artist",
        3: "Copyright",
        4: "Character",
        5: "Meta"
    }
    return categories.get(category_id, "Unknown")

def save_game_characters_to_file(game_name, max_pages=3, hide_empty=True):
    """
    搜索指定游戏的所有角色tag并按性别分类保存到文件
    :param game_name: 游戏名称
    :param max_pages: 最大搜索页数，默认为3页
    :param hide_empty: 是否隐藏没有投稿的tag
    """
    try:
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

        # 创建男性和女性角色的文件名
        male_filename = f"{game_name}_male_characters.txt"
        female_filename = f"{game_name}_female_characters.txt"
        unknown_filename = f"{game_name}_unknown_gender_characters.txt"
        
        male_count = 0
        female_count = 0
        unknown_count = 0
        
        # 定义性别关键词
        male_gender_keywords = ['male', 'boy']
        female_gender_keywords = ['female', 'girl']
        
        # 打开三个文件用于写入
        with open(male_filename, 'w', encoding='utf-8') as male_file, \
             open(female_filename, 'w', encoding='utf-8') as female_file, \
             open(unknown_filename, 'w', encoding='utf-8') as unknown_file:
            
            filtered_characters = [tag for tag in all_character_tags if game_name.lower() in tag.get('name', '').lower()]
            print("\n正在分析角色性别...")
            
            for tag in tqdm(filtered_characters, desc="分析角色性别"):
                name = tag.get('name', '')
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
                    
                    # 根据频率判断性别
                    if male_releted_tags_frequency_avg > female_releted_tags_frequency_avg:
                        male_file.write(f"{name}\n")
                        male_count += 1
                    elif female_releted_tags_frequency_avg > male_releted_tags_frequency_avg:
                        female_file.write(f"{name}\n")
                        female_count += 1
                    else:
                        unknown_file.write(f"{name}\n")
                        unknown_count += 1
                        
                except Exception as e:
                    print(f"\n获取角色 {name} 的相关tag时出错: {e}")
                    unknown_file.write(f"{name}\n")
                    unknown_count += 1
        
        print(f"\n角色tag保存完成:")
        print(f"男性角色: {male_count} 个，保存在 {male_filename}")
        print(f"女性角色: {female_count} 个，保存在 {female_filename}")
        print(f"未知性别: {unknown_count} 个，保存在 {unknown_filename}")
        print(f"搜索了 {page-1} 页数据")

    except Exception as e:
        print(f"保存角色tag时出错: {e}")

if __name__ == "__main__":
    # 搜索明日方舟的角色
    # search_game_characters("arknights")
    # 保存明日方舟角色到文件，按性别分类
    save_game_characters_to_file("arknights")
