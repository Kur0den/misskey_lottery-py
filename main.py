from misskey import Misskey
from misskey.exceptions import MisskeyAPIException
from urllib.parse import urlparse
from sys import exit
from requests.exceptions import InvalidURL, ConnectionError


def check(prompt: str, reverse: bool = False) -> bool:
    """
    Function to display a prompt asking the user yes or no and return the result.

    Args:
        prompt (str): The prompt to display.
        reverse (bool, optional): If True, the function will return True if the user answered no, False if the user answered yes. Defaults to False.

    Returns:
        bool: True if the user answered yes, False if the user answered no.
    """
    while True:
        try:
            return (
                {"y": True, "n": False}[input(prompt).lower()]
                if not reverse
                else {"y": False, "n": True}[input(prompt).lower()]
            )
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
                note = note[2]
                # ノートが存在するか確認
                try:
                    # ノート投稿者を取得
                    note_user = mk.notes_show(note)["user"]["id"]
                    break
                except MisskeyAPIException:
                    print("ノートが存在しません")
    print("正しいノートのURLを入力してください")

# 抽選の条件を指定
while True:
    # リアクション
    is_react = check("リアクションを抽選の条件に加えますか？(Y/n): ")
    # リノート
    is_renote = check("リノートを抽選の条件に加えますか？(Y/n): ")
    # リプライ
    is_reply = check("リプライを抽選の条件に加えますか？(Y/n): ")

    # すべてがFalseの場合は入力をやり直す
    if not (is_react or is_renote or is_reply):
        print("=" * 20)
        print(" - リアクション\n - リノート\n - リプライ\nのいずれか1つは条件に指定してください")
        print("=" * 20)
        continue
    break

# フォロー
print("!: フォローを抽選条件に使用するためには、'つながりの公開範囲'の公開が必要です")
print("!: 'つながりの公開範囲'は、'設定'の'プライバシー'から変更できます")
is_follow = check("フォローを抽選の条件に加えますか？(Y/n): ")

is_include_self = check("抽選にノート投稿者を含めますか？(Y/n): ", True)


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
print("リプライ: " + ("必要" if is_reply else "不要"))
print("フォロー: " + ("必要" if is_follow else "不要"))
print("抽選人数: " + str(num_pickup) + "人")

# 抽選を開始するか確認
if not check("これでよろしいですか？(Y/n): "):
    print("処理を中断しました")
    exit()
print("抽選を開始します")


lottery_list = set()

# リアクションが抽選条件時
if is_react:
    react_users = set()
    # リアクションを取得
    reacts = mk.notes_reactions(note)
    for i in reacts:
        if is_include_self and i["user"]["id"] == note_user:
            continue
        react_users.add((i["user"]["username"], i["user"]["host"]))
    # 取得したリストを結合
    if lottery_list == set():
        lottery_list = react_users
    else:
        lottery_list &= react_users

# リノートが抽選条件時
if is_renote:
    renote_users = set()
    # リノートを取得
    renotes = mk.notes_renotes(note)
    for i in renotes:
        if is_include_self and i["user"]["id"] == note_user:
            continue
        renote_users.add((i["user"]["username"], i["user"]["host"]))
    # 取得したリストを結合
    if lottery_list == set():
        lottery_list = renote_users
    else:
        lottery_list &= renote_users

# リプライが抽選条件時
if is_reply:
    reply_users = set()
    # リプライを取得
    replys = mk.notes_replies(note)
    for i in replys:
        if is_include_self and i["user"]["id"] == note_user:
            continue
        reply_users.add((i["user"]["username"], i["user"]["host"]))
    # 取得したリストを結合
    if lottery_list == set():
        lottery_list = reply_users
    else:
        lottery_list &= reply_users

# フォローが抽選条件時
if is_follow:
    follow_users = set()
    # フォローを取得
    followers = mk.users_show(note_user)["followersCount"]
    run_count = followers // 100 + 1
    last_id = ""
    for i in range(run_count):
        follows = mk.users_followers(
            note_user,
            limit=100,
            since_id=last_id if last_id != "" else None,
        )
        for j in follows:
            follow_users.add((j["follower"]["username"], j["follower"]["host"]))
        last_id = follows[-1]["id"]

    for i in follows:
        follow_users.add((i["follower"]["username"], i["follower"]["host"]))
    # 取得したリストを結合
    lottery_list &= follow_users


print(lottery_list)
print(len(lottery_list))
