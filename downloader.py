import sys

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
site_url = "https://vutbr.sharepoint.com/sites/ICS-2021/"


ctx = ClientContext(site_url).with_credentials(
    UserCredential(sys.argv[1], sys.argv[2]))
web = ctx.web
ctx.load(web)
ctx.execute_query()
print("Web title: {0}".format(web.properties['Title']))
