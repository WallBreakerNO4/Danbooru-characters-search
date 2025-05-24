import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs import create_danbooru_client


def test_tag_fuzzy_search():
    client = create_danbooru_client()

    # 测试模糊搜索标签
    tag_to_search = "*amiya*"
    search_results = client.tag_list(tag_to_search, category=4, order="count",hide_empty=True)
    print(f"模糊搜索标签 '{tag_to_search}' 的结果:")
    for tag in search_results:
        print(f"Tag: {tag['name']} - Post Count: {tag['post_count']}")


if __name__ == "__main__":
    test_tag_fuzzy_search()
