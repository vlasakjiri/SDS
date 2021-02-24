import sys

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
site_url = "https://vutbr.sharepoint.com/sites/ICS-2021/"


ctx = ClientContext(site_url).with_credentials(
    UserCredential(sys.argv[1], sys.argv[2]))
web = ctx.web
ctx.load(web)
ctx.execute_query()


root = ctx.web.get_folder_by_server_relative_url(
    'Sdilene dokumenty/General/Recordings')
ctx.load(root)
ctx.execute_query()


folders = root.folders
ctx.load(folders)
ctx.execute_query()

print("Folders:")
for folder in folders:
    print(folder.properties["ServerRelativeUrl"])


print("Files:")
files = root.files
ctx.load(files)
ctx.execute_query()
for file in files:
    print(file.properties["ServerRelativeUrl"])
