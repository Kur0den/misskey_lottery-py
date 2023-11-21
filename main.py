from misskey import Misskey
from urllib import parse

# ノートのURLを取得
note_url = input("ノートのURLを入力してください: ")
mk = Misskey(parse.urlparse(note_url).netloc)
