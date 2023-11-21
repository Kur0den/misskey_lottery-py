from misskey import Misskey
from urllib import parse
from sys import exit


def check(prompt):
    while True:
        try:
            return {"y": True, "n": False}[input(prompt).lower()]
        except KeyError:
            print("yかnで入力してください")


# ノートのURLを取得
note_url = input("ノートのURLを入力してください: ")
mk = Misskey(parse.urlparse(note_url).netloc)

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
        pickup = int(input("何人を選びますか？: "))
        if pickup > 0:
            break
        print("1以上の数字を入力してください")
    except ValueError:
        print("数字を入力してください")

print("-" * 20)
print("抽選条件")
print("リアクション: " + ("必要" if is_react else "なし"))
print("リノート: " + ("必要" if is_renote else "なし"))
print("フォロー: " + ("必要" if is_follow else "なし"))
print("リプライ: " + ("必要" if is_reply else "なし"))
print("抽選人数: " + str(pickup))

if not check("これでよろしいですか？(Y/n): "):
    print("処理を中断しました")
    exit()
print("抽選を開始します")
