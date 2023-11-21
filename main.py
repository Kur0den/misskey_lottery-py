from misskey import Misskey
from urllib import parse
from sys import exit
from requests import exceptions as req_exceptions


def check(prompt):
    while True:
        try:
            return {"y": True, "n": False}[input(prompt).lower()]
        except KeyError:
            print("yかnで入力してください")


# ノートのURLを取得
while True:
    # URLとして認識できるか確認
    try:
        note_url = input("ノートのURLを入力してください: ")
        mk = Misskey(parse.urlparse(note_url).netloc)
        # ノートのURLかどうかを確認
        if parse.urlparse(note_url).path.split("/")[1] != "notes":
            print("ノートのURLを入力してください")
            continue
        break
    except req_exceptions.InvalidURL:
        print("URLとして認識できませんでした\n正しいノートのURLを入力してください")

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
    try:
        pickup = int(input("何人を選びますか？: "))
        if pickup > 0:
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
print("抽選人数: " + str(pickup) + "人")

if not check("これでよろしいですか？(Y/n): "):
    print("処理を中断しました")
    exit()
print("抽選を開始します")

# 抽選の実行
# ノートの情報を取得
print(parse.urlparse(note_url).path.split("/")[2])
# note = mk.notes_show()
