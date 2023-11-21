from misskey import Misskey
from urllib.parse import urlparse
from sys import exit
from requests.exceptions import InvalidURL, ConnectionError


def check(prompt):
    while True:
        try:
            return {"y": True, "n": False}[input(prompt).lower()]
        except KeyError:
            print("yかnで入力してください")


# ノートのURLを取得
while True:
    # URLが正しくパースできるか確認
    try:
        note = input("ノートのURLを入力してください: ")
        mk = Misskey(urlparse(note).netloc)
    except (InvalidURL, ConnectionError):
        print("URLが正しくありません")
        continue

    # ノートのURLかどうか確認
    # URLのPathが空でないか確認
    note = urlparse(note).path.split("/")
    if len(note) == 3:
        # Pathの先頭が"/notes"か確認
        if note[1] == "notes":
            if note[2] != "":
                note_ = note[2]
                break
    print("ノートのURLを入力してください")

while True:
    # 抽選の条件を指定
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
    try:
        num_pickup = int(input("何人を選びますか？: "))
        if num_pickup > 0:
            break
        print("1以上の数字を入力してください")
    except ValueError:
        print("数字を入力してください")

print("-" * 20)
print("抽選条件")
print("リアクション: " + ("必要" if is_react else "不要"))
print("リノート: " + ("必要" if is_renote else "不要"))
print("フォロー: " + ("必要" if is_follow else "不要"))
print("リプライ: " + ("必要" if is_reply else "不要"))
print("抽選人数: " + str(num_pickup) + "人")

if not check("これでよろしいですか？(Y/n): "):
    print("処理を中断しました")
    exit()
print("抽選を開始します")
