import discord
import util
from misskey import Misskey

import database

config = util.ConfigLoad()
mk = Misskey(config["Misskey"]["address"], i=config["Misskey"]["token"])


def CreateMessage(attachments, content, guild_id, channel_id, message_id):
    print("CreateMessage")
    # MisskeyのドライブにアップロードしたファイルのIDリスト
    fileIDList = util.uploadDiscordFile(attachments, mk)
    # Misskey ノート 作成
    note = util.sendNote(content, fileIDList, mk, config["Misskey"]["visibility"])
    # データベースにIDリスト登録
    database.addIDList(guild_id, channel_id, message_id, note["createdNote"]["id"])


def DeleteMessage(message):
    print("DeleteMessage")
    # データベース ノートIDを取得
    noteID = database.getNoteID(message.guild_id, message.channel_id, message.message_id)
    # もし該当するノートがあるなら
    if (noteID):
        # ノートを削除
        mk.notes_delete(note_id=noteID)
        # データベースから削除
        database.deleteRecord(message.guild_id, message.channel_id, message.message_id)
        return True
    return False


class MyClient(discord.Client):
    try:

        # ログインしたら
        async def on_ready(self):
            print(f'Logged on as {self.user}!')

        # メッセージが送信されたら
        async def on_message(self, message):

            cfg_guild_id = config["Discord"]["guild_id"]
            cfg_channel_id = config["Discord"]["channel_id"]

            guild_id = message.guild.id
            channel_id = message.channel.id

            # config に書かれた サーバーID 、チャンネルID ではないか
            if cfg_guild_id != guild_id or cfg_channel_id != channel_id:
                return

            # メッセージ(ノート) 作成処理
            CreateMessage(
                message.attachments,
                message.content,
                guild_id,
                channel_id,
                message.id
            )

        # メッセージが削除されたら
        async def on_raw_message_delete(self, message):
            # メッセージ(ノート) 削除処理
            DeleteMessage(message)

        # メッセージが編集されたら
        async def on_raw_message_edit(self, message):
            # メッセージ(ノート) 削除処理
            if (DeleteMessage(message)):
                # メッセージ(ノート) 作成処理
                data = message.data
                CreateMessage(
                    data["attachments"] if "attachments" in data else [],
                    data["content"],
                    message.guild_id,
                    message.channel_id,
                    message.message_id
                )

    except Exception as err:
        print(err)


# Discord Bot 起動準備
intents = discord.Intents.all()
client = MyClient(intents=intents)


# Discord Bot 起動
client.run(config["Discord"]["token"])

database.close()
