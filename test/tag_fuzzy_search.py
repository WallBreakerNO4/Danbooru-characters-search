import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs import create_danbooru_client
from libs.character_search import calculate_average_tag_frequency, calculate_gender_frequencies


def test_tag_fuzzy_search():
    client = create_danbooru_client()

    # 测试模糊搜索标签
    tag_to_search = "*summer flowers*"
    search_results = client.tag_list(
        tag_to_search, category=4, order="count", hide_empty=True
    )
    print(f"模糊搜索标签 '{tag_to_search}' 的结果:")
    for tag in search_results:
        print(f"Tag: {tag['name']} - Post Count: {tag['post_count']}")


def swimming_frequency():
    tag_to_search = "surtr_(colorful_wonderland)_(arknights)"
    swim_frequency = calculate_average_tag_frequency(tag_to_search, ["swim"])
    print(f"Tag: {tag_to_search} - Swim Frequency: {swim_frequency}")
    print(
        f"Tag: surtr_(arknights) - Swim Frequency: {calculate_average_tag_frequency('surtr_(arknights)', ['swim'])}"
    )


if __name__ == "__main__":
    test_tag_fuzzy_search()
