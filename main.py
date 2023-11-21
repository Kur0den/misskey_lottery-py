from misskey import Misskey
from urllib.parse import urlparse
from sys import exit
from requests.exceptions import InvalidURL, ConnectionError


def check(prompt: str) -> bool:
    """
    Function to display a prompt asking the user yes or no and return the result.

    Args:
        prompt (str): The prompt to display.

    Returns:
        bool: True if the user answered yes, False if the user answered no.
    """
    while True:
        try:
            return {"y": True, "n": False}[input(prompt).lower()]
        except KeyError:
            print("yかnで入力してください")


# ノートのURLを取得
while True:
    try:
        note = input("ノートのURLを入力してください: ")
        # misskey.pyのMisskeyクラスのインスタンスを生成
        mk = Misskey(urlparse(note).netloc)
    # URLが正しくパースできない場合
    # ドメインが存在しない場合は入力をやり直す
    except (InvalidURL, ConnectionError):
        print("URLが正しくありません")
        continue

    # URLが正しくパースできるか確認
    # ノートのURLかどうか確認
    # URLのPathが空でないか確認
    note = urlparse(note).path.split("/")
    if len(note) == 3:
        # Pathの先頭が"/notes"か確認
        if note[1] == "notes":
            # ノートのIDが空でないか確認
            if note[2] != "":
                # ノートのIDを変数に格納
                note_ = note[2]
                break
    print("ノートのURLを入力してください")

# 抽選の条件を指定
while True:
    # リアクション
    is_react = check("リアクションを抽選の条件に加えますか？(Y/n): ")
    # リノート
    is_renote = check("リノートを抽選の条件に加えますか？(Y/n): ")
    # フォロー
    is_follow = check("フォローを抽選の条件に加えますか？(Y/n): ")
    # リプライ
    is_reply = check("リプライを抽選の条件に加えますか？(Y/n): ")

    # すべてがFalseの場合は入力をやり直す
    if not (is_react or is_renote or is_follow or is_reply):
        print("少なくとも1つは条件を指定してください")
        continue
    break

# 抽選人数
while True:
    # 入力が整数か確認
    try:
        num_pickup = int(input("何人を選びますか？: "))
        # 1以上の整数か確認
        if num_pickup > 0:
            break
        print("1以上の整数を入力してください")
    except ValueError:
        print("整数を入力してください")

# 抽選条件を表示
print("-" * 20)
print("抽選条件")
print("リアクション: " + ("必要" if is_react else "不要"))
print("リノート: " + ("必要" if is_renote else "不要"))
print("フォロー: " + ("必要" if is_follow else "不要"))
print("リプライ: " + ("必要" if is_reply else "不要"))
print("抽選人数: " + str(num_pickup) + "人")

# 抽選を開始するか確認
if not check("これでよろしいですか？(Y/n): "):
    print("処理を中断しました")
    exit()
print("抽選を開始します")
