from danbooru_client import create_danbooru_client

client = create_danbooru_client()

# 设置分页参数
page = 1
limit = 1000  # 每页最大200条记录
all_tags = []
max_pages = 3

# while page <= max_pages:
#     # 获取当前页的tags
#     tags = client.tag_list(order='count', page=page, limit=limit, name_matches='*arknights*')
    
#     # 如果没有更多数据则退出循环
#     if not tags:
#         break
        
#     all_tags.extend(tags)
#     page += 1

# # 统计返回的tags总数
# total_tags = len(all_tags)
# print(f"\n总共获取到 {total_tags} 个tags\n")

# for tag in all_tags:
#     print("Tag: {0} ----- {1}".format(tag['name'], tag['post_count']))

# tag_2_search = 'doctor_(arknights)'
# tag_2_search = 'skadi_the_corrupting_heart_(arknights)'
# tag_2_search = 'silverash_(arknights)'
tag_2_search = 'originium_slug_(arknights)'

tag_related = client.tag_related(tag_2_search)
tag_related_len = len(tag_related.get('related_tags'))

print(f'搜索标签: {tag_2_search}')
print(f"tag_related_len: {tag_related_len}")

# for tag in tag_related.get('related_tags'):
#     tag_info = tag.get('tag')
#     print("Tag: {0} ----- {1}".format(tag_info['name'], tag_info['post_count']))

# 过滤性别相关标签
# gender_keywords = ['male', 'female', 'boy', 'girl']
male_gender_keywords = ['male', 'boy']
female_gender_keywords = ['female', 'girl']
male_releted_post_count = 0
female_releted_post_count = 0
male_releted_tags_count = 0
female_releted_tags_count = 0
male_releted_tags_frequency_sum = 0
female_releted_tags_frequency_sum = 0

# 先处理female标签
female_matched_tags = []
for keyword in female_gender_keywords:
    gender_tags = [tag for tag in tag_related.get('related_tags') 
                    if keyword in tag.get('tag')['name'].lower()]
    if gender_tags:
        print(f"\n包含 '{keyword}' 的标签:")
        for tag in gender_tags:
            print(f"标签: {tag.get('tag').get('name')} - 频率: {tag['frequency']}")
            female_releted_tags_count += 1
            female_releted_tags_frequency_sum += tag['frequency']
            female_matched_tags.append(tag)

# 从所有标签中移除female标签，再处理male标签
remaining_tags = [tag for tag in tag_related.get('related_tags') if tag not in female_matched_tags]
for keyword in male_gender_keywords:
    gender_tags = [tag for tag in remaining_tags 
                    if keyword in tag.get('tag')['name'].lower()]
    if gender_tags:
        print(f"\n包含 '{keyword}' 的标签:")
        for tag in gender_tags:
            print(f"标签: {tag.get('tag').get('name')} - 频率: {tag['frequency']}")
            male_releted_tags_count += 1
            male_releted_tags_frequency_sum += tag['frequency']

male_releted_tags_frequency_avg = male_releted_tags_frequency_sum / male_releted_tags_count if male_releted_tags_count > 0 else 0
female_releted_tags_frequency_avg = female_releted_tags_frequency_sum / female_releted_tags_count if female_releted_tags_count > 0 else 0

print(f"\n男性相关标签的相关频率: {male_releted_tags_frequency_avg}")
print(f"女性相关标签的相关频率: {female_releted_tags_frequency_avg}")

if male_releted_tags_frequency_avg > female_releted_tags_frequency_avg:
    print(f"推测 {tag_2_search} 是男性角色")
else:
    print(f"推测 {tag_2_search} 是女性角色")

