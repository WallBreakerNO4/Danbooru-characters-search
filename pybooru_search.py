from libs.character_search import get_possible_game_names
from libs.search_and_save_game_characters import search_and_save_game_characters


def interactive_cli():
    print("欢迎使用Pybooru角色搜索工具")

    search_term = input("\n请输入游戏名称或部分名称（默认为'arknights'）: ").strip()

    if not search_term:
        search_term = "arknights"

    # 获取可能的游戏名列表
    possible_games = get_possible_game_names(search_term)

    if not possible_games:
        print(f"未找到与'{search_term}'相关的游戏")
        return

    # 显示可选游戏列表
    print("\n找到以下游戏：")
    for i, game in enumerate(possible_games, 1):
        print(f"{i}. {game}")

    # 让用户选择游戏
    try:
        choice = input("\n请输入序号选择游戏（留空退出）: ").strip()
        if not choice:
            print("退出程序")
            return

        choice = int(choice)
        if not (1 <= choice <= len(possible_games)):
            print("无效的序号")
            return

        game_name = possible_games[choice - 1]

        pages = input("请输入最大搜索页数（输入q退出，默认3）: ").strip()
        if pages.lower() == "q":
            print("退出程序")
            return
        pages = int(pages) if pages else 3

        show_empty = (
            input("是否显示无投稿的标签？(y/n, 输入q退出，默认n): ").strip().lower()
        )
        if show_empty == "q":
            print("退出程序")
            return
        hide_empty = show_empty != "y"

        print(f"\n开始搜索游戏: {game_name}")
        search_and_save_game_characters(
            game_name, max_pages=pages, hide_empty=hide_empty
        )

    except ValueError:
        print("错误：请输入有效的数字")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    interactive_cli()
