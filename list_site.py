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


site_url = "https://vutbr.sharepoint.com/sites/IZU/"


ctx = ClientContext(site_url).with_credentials(
    UserCredential(sys.argv[1], sys.argv[2]))
web = ctx.web
ctx.load(web)
ctx.execute_query()

listFolder('Sdilene dokumenty/Přednášky - úterý od 13 hodin/Recordings/')
