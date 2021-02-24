import sys
import os

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext


def listFolder(path):
    root = ctx.web.get_folder_by_server_relative_url(
        path)
    ctx.load(root)
    ctx.execute_query()

    folders = root.folders
    ctx.load(folders)
    ctx.execute_query()

    for folder in folders:
        print(folder.properties["ServerRelativeUrl"])
        listFolder(folder.properties["ServerRelativeUrl"])

    files = root.files
    ctx.load(files)
    ctx.execute_query()
    for file in files:
        print(file.properties["ServerRelativeUrl"])


site_url = "https://vutbr.sharepoint.com/sites/IPK2020L/"


ctx = ClientContext(site_url).with_credentials(
    UserCredential(sys.argv[1], sys.argv[2]))
web = ctx.web
ctx.load(web)
ctx.execute_query()

listFolder('Sdilene dokumenty/General/Recordings')

file_url = "/sites/IPK2020L/Sdilene dokumenty/General/Recordings/Meeting in _General_-20210209_090016-Meeting Recording.mp4"
download_path = "test.mp4"
with open(download_path, "wb") as local_file:
    file = ctx.web.get_file_by_server_relative_url(
        file_url).download(local_file).execute_query()

print("[Ok] file has been downloaded: {0}".format(download_path))
