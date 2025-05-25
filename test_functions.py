#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from libs.character_search import calculate_average_tag_frequency, calculate_gender_frequencies

# 测试通用的calculate_average_tag_frequency函数
print("=== 测试通用的calculate_average_tag_frequency函数 ===")
tag_to_test = "dark-skinned_female"
keywords_to_test = ["female", "girl"]

avg_frequency = calculate_average_tag_frequency(tag_to_test, keywords_to_test)
print(f"标签 '{tag_to_test}' 与关键词 {keywords_to_test} 的平均相关频率: {avg_frequency}")

# 测试专门的calculate_gender_frequencies函数
print("\n=== 测试专门的calculate_gender_frequencies函数 ===")
male_freq, female_freq = calculate_gender_frequencies(tag_to_test)
print(f"标签 '{tag_to_test}' 的男性频率: {male_freq}, 女性频率: {female_freq}")

# 测试另一个tag
print("\n=== 测试另一个标签 ===")
another_tag = "silverash_(arknights)"
male_freq2, female_freq2 = calculate_gender_frequencies(another_tag)
print(f"标签 '{another_tag}' 的男性频率: {male_freq2}, 女性频率: {female_freq2}")

if male_freq2 > female_freq2:
    print(f"推测 {another_tag} 是男性角色")
elif female_freq2 > male_freq2:
    print(f"推测 {another_tag} 是女性角色")
else:
    print(f"无法确定 {another_tag} 的性别")