import sys
import os
import yaml

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext


def parseYaml(path):
    with open(path, 'r', encoding='utf8') as stream:
        try:
            obj = yaml.safe_load(stream)
            if obj is None:
                obj = dict()
            return obj

        except yaml.YAMLError as exc:
            print(exc)


def listFolder(path, ctx):
    root = ctx.web.get_folder_by_server_relative_url(
        path)
    ctx.load(root)
    ctx.execute_query()

    folders = root.folders
    ctx.load(folders)
    ctx.execute_query()

    files = root.files
    ctx.load(files)
    ctx.execute_query()
    return files


def connectToSite(site_url):
    ctx = ClientContext(site_url).with_credentials(
        UserCredential(sys.argv[1], sys.argv[2]))
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    return ctx


def downloadFile(file_url, download_path, ctx):
    with open(download_path, "wb") as local_file:
        file = ctx.web.get_file_by_server_relative_url(
            file_url).download(local_file).execute_query()

    print("[Ok] file has been downloaded: {0}".format(download_path))


config = parseYaml("config.yaml")
for subject in config:
    name = subject["name"]
    path = subject["path"]
    folder_relative_url = subject["folder_relative_url"]
    site_url = subject["site_url"]
    ctx = connectToSite(site_url)

    if not os.path.exists(path):
        print(f"Path {path} does not exist. Creating it now...")
        os.mkdir(path)

    remote_files = listFolder(folder_relative_url, ctx)
    local_files = os.listdir(path)
    for remote_file in remote_files:
        if remote_file.properties["Name"] in local_files:
            continue
        print(
            f"Downloading {remote_file.properties['Name']} into {path}")
        file_url = remote_file.properties['ServerRelativeUrl']
        download_path = os.path.join(path, remote_file.properties['Name'])
        downloadFile(file_url, download_path, ctx)
