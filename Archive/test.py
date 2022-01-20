import requests
import os
import json
import tarfile

from shutil import make_archive

jwtoidc = requests.get(
    os.environ.get('ACTIONS_ID_TOKEN_REQUEST_URL') + '&audience=o6s',
    headers={
        "User-Agent": "actions/oidc-client",
        "Authorization": "Bearer " + os.environ.get('ACTIONS_ID_TOKEN_REQUEST_TOKEN'),
        'Accept': 'application/json'
    }
)



jwtoidcjson = json.loads(jwtoidc.content)

print(jwtoidcjson)
