import sqlite3

filepath = "message.sqlite"


# データベース 接続
# "filepath" がない場合 ファイル作成される
conn = sqlite3.connect(filepath)

# sqlite を操作するためのカーソルオブジェクト 作成
cur = conn.cursor()

# テーブルがなかったら作成
cur.execute(
    "CREATE TABLE IF NOT EXISTS id_list (discord_guild bigint , discord_channel bigint ,discord_message bigint, misskey_note text);"
)


# DiscordのギルドID、チャンネルID、メッセージID、 MisskeyのノートID を登録
def addIDList(discord_guild: int, discord_channel: int, discord_message: int, misskey_note: str):
    # レコード追加
    cur.execute(
        'INSERT INTO id_list (discord_guild, discord_channel, discord_message,misskey_note) VALUES(?,?,?,?);',
        (discord_guild, discord_channel, discord_message, misskey_note)
    )
    conn.commit()


# DiscordのギルドID、チャンネルID、メッセージID から 該当する ノートを取得
def getNoteID(discord_guild: int, discord_channel: int, discord_message: int):
    cur.execute(
        "SELECT * FROM id_list WHERE discord_guild = ? AND discord_channel = ? AND discord_message = ?",
        (discord_guild, discord_channel, discord_message)
    )
    docs = cur.fetchall()
    conn.commit()
    for doc in docs:
        return doc[3]
    return False


# DiscordのギルドID、チャンネルID、メッセージID から 該当する レコードを削除
def deleteRecord(discord_guild: int, discord_channel: int, discord_message: int):
    cur.execute(
        "DELETE FROM id_list WHERE discord_guild = ? AND discord_channel = ? AND discord_message = ?",
        (discord_guild, discord_channel, discord_message)
    )
    conn.commit()


# 閉じる
def close():
    conn.close()
