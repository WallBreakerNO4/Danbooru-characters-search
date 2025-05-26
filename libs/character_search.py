from libs.danbooru_client import create_danbooru_client
from tqdm import tqdm
import os
import csv

# 创建Danbooru客户端
client = create_danbooru_client()


def calculate_average_tag_frequency(tag, tag_list):
    """
    计算指定tag与关键词列表的平均相关频率
    :param tag: 要分析的tag名称 (string)
    :param tag_list: 关键词列表 (list of string)
    :return: 平均相关频率 (float)
    """
    try:
        # 获取tag的相关标签
        tag_related = client.tag_related(tag)

        # 初始化计数器
        matched_tags_count = 0
        matched_tags_frequency_sum = 0

        # 遍历关键词列表
        for keyword in tag_list:
            # 查找包含关键词的相关标签
            gender_tags = [
                related_tag
                for related_tag in tag_related.get("related_tags", [])
                if keyword in related_tag.get("tag", {}).get("name", "").lower()
            ]
            # 累加频率
            for related_tag in gender_tags:
                matched_tags_count += 1
                matched_tags_frequency_sum += related_tag.get("frequency", 0)

        # 计算平均频率
        average_frequency = (
            matched_tags_frequency_sum / matched_tags_count
            if matched_tags_count > 0
            else 0
        )

        return average_frequency

    except Exception as e:
        print(f"计算tag {tag} 的平均频率时出错: {e}")
        return 0


def calculate_gender_frequencies(tag):
    """
    计算指定tag的男性和女性相关频率，避免重复计算
    :param tag: 要分析的tag名称 (string)
    :return: (male_frequency, female_frequency) tuple
    """
    try:
        # 获取tag的相关标签
        tag_related = client.tag_related(tag)

        # 定义性别关键词
        male_gender_keywords = ["boy"]
        female_gender_keywords = ["girl"]

        # 初始化计数器
        male_releted_tags_count = 0
        female_releted_tags_count = 0
        male_releted_tags_frequency_sum = 0
        female_releted_tags_frequency_sum = 0

        # 先处理female标签
        female_matched_tags = []
        for keyword in female_gender_keywords:
            gender_tags = [
                tag
                for tag in tag_related.get("related_tags", [])
                if keyword in tag.get("tag", {}).get("name", "").lower()
            ]
            for tag_item in gender_tags:
                female_releted_tags_count += 1
                female_releted_tags_frequency_sum += tag_item.get("frequency", 0)
                female_matched_tags.append(tag_item)

        # 从所有标签中移除female标签，再处理male标签
        remaining_tags = [
            tag_item
            for tag_item in tag_related.get("related_tags", [])
            if tag_item not in female_matched_tags
        ]
        for keyword in male_gender_keywords:
            gender_tags = [
                tag_item
                for tag_item in remaining_tags
                if keyword in tag_item.get("tag", {}).get("name", "").lower()
            ]
            for tag_item in gender_tags:
                male_releted_tags_count += 1
                male_releted_tags_frequency_sum += tag_item.get("frequency", 0)

        # 计算平均频率
        male_frequency = (
            male_releted_tags_frequency_sum / male_releted_tags_count
            if male_releted_tags_count > 0
            else 0
        )
        female_frequency = (
            female_releted_tags_frequency_sum / female_releted_tags_count
            if female_releted_tags_count > 0
            else 0
        )

        return male_frequency, female_frequency

    except Exception as e:
        print(f"计算tag {tag} 的性别频率时出错: {e}")
        return 0, 0


def get_possible_game_names(search_term):
    """获取可能的游戏名列表"""
    try:
        games = client.tag_list(
            name_matches=f"*{search_term}*",
            category=3,  # 3表示游戏分类
            order="count",
            limit=10,
            hide_empty=True,
        )
        return [tag["name"] for tag in games]
    except Exception as e:
        print(f"获取游戏列表时出错: {e}")
        return []
