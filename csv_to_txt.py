import os
import csv
import argparse
import re

def convert_name(name):
    # 将下划线转换为空格
    name = name.replace('_', ' ')
    # 在括号前添加转义字符
    name = re.sub(r'([()])', r'\\\1', name)
    return name

def convert_csv_to_txt(min_post_count):
    # 获取outputs文件夹中的所有csv文件
    csv_files = [f for f in os.listdir('outputs') if f.endswith('.csv')]
    
    for csv_file in csv_files:
        # 读取CSV文件
        csv_path = os.path.join('outputs', csv_file)
        txt_file = csv_file.replace('.csv', '.txt')
        txt_path = os.path.join('outputs', txt_file)
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if 'name' not in reader.fieldnames or 'post_count' not in reader.fieldnames:
                    print(f"警告: {csv_file} 中没有找到必要的列 (name 或 post_count)")
                    continue
                
                # 只保存符合条件的name到txt文件
                with open(txt_path, 'w', encoding='utf-8') as txtfile:
                    filtered_count = 0
                    total_count = 0
                    for row in reader:
                        total_count += 1
                        if row['name'] and row['post_count']:  # 确保name和post_count不为空
                            post_count = int(row['post_count'])
                            if post_count >= min_post_count:
                                converted_name = convert_name(row['name'])
                                txtfile.write(f"{converted_name}\n")
                                filtered_count += 1
                    
                    print(f"已将 {csv_file} 转换为 {txt_file}")
                    print(f"总计 {total_count} 个角色，筛选后保留 {filtered_count} 个角色")
        except Exception as e:
            print(f"处理 {csv_file} 时出错: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将CSV文件转换为TXT文件，并根据post_count筛选角色')
    parser.add_argument('min_post_count', type=int, help='最小post数量，小于该数量的角色将被剔除')
    args = parser.parse_args()
    
    convert_csv_to_txt(args.min_post_count) 