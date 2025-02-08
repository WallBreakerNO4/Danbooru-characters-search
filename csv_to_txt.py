import os
import csv
import re
import datetime

def convert_name(name):
    # 将下划线转换为空格
    name = name.replace('_', ' ')
    # 在括号前添加转义字符
    name = re.sub(r'([()])', r'\\\1', name)
    return name

def convert_csv_to_txt(min_post_count, updated_at_threshold=None):
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
                # 检查必要的字段
                required_fields = ['name', 'post_count']
                for field in required_fields:
                    if field not in reader.fieldnames:
                        print(f"警告: {csv_file} 中没有找到必要的列 ({field})")
                        continue
                
                # 如果用户提供了updated_at过滤条件，且csv中存在该列，则使用
                has_updated_at = 'updated_at' in reader.fieldnames
                
                with open(txt_path, 'w', encoding='utf-8') as txtfile:
                    filtered_count = 0
                    total_count = 0
                    for row in reader:
                        total_count += 1
                        if row['name'] and row['post_count']:
                            post_count = int(row['post_count'])
                            if post_count < min_post_count:
                                continue
                            
                            # 如果设置了过滤时间，并且存在updated_at字段，则进行日期过滤
                            if updated_at_threshold and has_updated_at:
                                try:
                                    # 先尝试使用固定格式解析
                                    try:
                                        row_date = datetime.datetime.strptime(row['updated_at'], "%Y-%m-%d %H:%M:%S")
                                    except ValueError:
                                        # 使用 fromisoformat 解析ISO 8601 格式日期
                                        row_date = datetime.datetime.fromisoformat(row['updated_at'])
                                        # 如果解析后的日期包含时区信息，则转换为本地时间并去除时区
                                        if row_date.tzinfo is not None:
                                            row_date = row_date.astimezone().replace(tzinfo=None)
                                except Exception as e:
                                    print(f"无法解析 {csv_file} 中的日期 {row.get('updated_at')}: {e}")
                                    continue
                                # 过滤掉晚于阈值的记录，保留用户输入日期之前的角色
                                if row_date > updated_at_threshold:
                                    continue
                            
                            converted_name = convert_name(row['name'])
                            txtfile.write(f"{converted_name}\n")
                            filtered_count += 1
                    
                    print(f"\n已将 {csv_file} 转换为 {txt_file}")
                    print(f"总计 {total_count} 个角色，筛选后保留 {filtered_count} 个角色")
        except Exception as e:
            print(f"处理 {csv_file} 时出错: {str(e)}")

def interactive_cli():
    print("欢迎使用CSV转TXT工具")
    print("本工具将把outputs文件夹中的CSV文件转换为TXT文件，并根据post数量及updated_at日期筛选角色")
    
    try:
        min_count = input("\n请输入最小post数量（输入q退出，默认为30）: ").strip()
        
        if min_count.lower() == 'q':
            print("退出程序")
            return
        
        min_count = int(min_count) if min_count else 30
        
        if min_count < 0:
            print("错误：最小post数量不能小于0")
            return
        
        print("\n请输入updated_at过滤日期（只需要输入年、月、日；时分秒默认00:00:00）")
        print("若留空，则默认使用 2024年10月15日")
        year_input = input("年份 (例如 2025)：").strip()
        updated_at_threshold = None
        if not year_input:
            updated_at_threshold = datetime.datetime(2024, 10, 15)
        else:
            try:
                month_input = input("月份 (例如 2)：").strip()
                day_input = input("日 (例如 8)：").strip()
                if not month_input or not day_input:
                    print("错误：必须同时提供月份和日")
                    return
                year = int(year_input)
                month = int(month_input)
                day = int(day_input)
                updated_at_threshold = datetime.datetime(year, month, day)
            except ValueError:
                print("错误：请输入有效的数字")
                return
            
        print(f"\n开始转换，最小post数量设置为: {min_count}")
        if updated_at_threshold:
            print(f"日期过滤阈值设置为: {updated_at_threshold.strftime('%Y-%m-%d %H:%M:%S')}")
        convert_csv_to_txt(min_count, updated_at_threshold)
        print("\n程序执行完毕")
            
    except ValueError:
        print("错误：请输入有效的数字")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    interactive_cli()
