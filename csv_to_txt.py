import os
import csv
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
    
    if not csv_files:
        print("错误：在outputs文件夹中没有找到CSV文件")
        return
    
    print(f"\n找到以下CSV文件：")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    
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
                    
                    print(f"\n已将 {csv_file} 转换为 {txt_file}")
                    print(f"总计 {total_count} 个角色，筛选后保留 {filtered_count} 个角色")
        except Exception as e:
            print(f"处理 {csv_file} 时出错: {str(e)}")

def interactive_cli():
    print("欢迎使用CSV转TXT工具")
    print("本工具将把outputs文件夹中的CSV文件转换为TXT文件，并根据post数量筛选角色")
    
    try:
        min_count = input("\n请输入最小post数量（输入q退出，默认为30）: ").strip()
        
        if min_count.lower() == 'q':
            print("退出程序")
            return
        
        min_count = int(min_count) if min_count else 30
        
        if min_count < 0:
            print("错误：最小post数量不能小于0")
            return
            
        print(f"\n开始转换，最小post数量设置为: {min_count}")
        convert_csv_to_txt(min_count)
        print("\n程序执行完毕")
            
    except ValueError:
        print("错误：请输入有效的数字")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    interactive_cli() 