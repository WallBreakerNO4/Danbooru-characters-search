import sys
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.danbooru_client import create_danbooru_client
from libs.character_search import (
    calculate_average_tag_frequency,
    calculate_gender_frequencies,
)


def test_calculate_average_tag_frequency():
    client = create_danbooru_client()

    # 读取测试用txt文件（arknights_female_characters.txt）
    tags = []
    with open("test/arknights_female_characters.txt", "r", encoding="utf-8") as file:
        for line in file:
            tag = line.strip()
            if tag:
                tags.append(tag)
    # print(tags)
    frequencies = []
    for tag in tqdm(tags, desc="计算标签频率"):
        frequencies.append(
            calculate_average_tag_frequency(tag=tag, tag_list=["girl", "female"])
        )
    return frequencies


if __name__ == "__main__":
    # frequencies = test_calculate_average_tag_frequency()
    # # 保存结果到文件
    # with open("test/frequencies.csv", "w", encoding="utf-8") as f:
    #     for freq in frequencies:
    #         f.write(f"{freq}\n")

    # 读取文件
    frequencies = []
    with open("test/frequencies.csv", "r", encoding="utf-8") as f:
        for line in f:
            frequencies.append(float(line.strip()))
    # 绘制频率分布图（散点图）
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(frequencies)), frequencies, alpha=0.5)
    plt.title("Tag Frequency Distribution")
    plt.xlabel("Tag Index")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig("test/frequencies_distribution.png")
    plt.show()
    
