import urllib.request
import yaml


# Misskey ノート作成
def sendNote(content: str, fileIDList: [str], mk, vis: str):
    if (not fileIDList):
        fileIDList = None
    return mk.notes_create(text=content, file_ids=fileIDList, visibility=vis)


# Misskeyのドライブにアップロード
def uploadDiscordFile(attachments, mk):
    fileIDList = []
    # Misskeyのドライブにファイルをアップロードする
    for attachment in attachments:
        req = urllib.request.Request(attachment.url, headers={'User-Agent': "Mozilla/5.0"})
        # Discord の 添付ファイル ダウンロード
        with urllib.request.urlopen(req) as web_file:
            # Misskeyのドライブにファイル アップロード
            file = mk.drive_files_create(web_file, name=attachment.filename)
            # "fileIDList" に アップロードしたファイルのID 追加
            fileIDList.append(file["id"])
    return fileIDList


# config.yml 読み込み
def ConfigLoad():
    with open('config.yml',encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.Loader)
