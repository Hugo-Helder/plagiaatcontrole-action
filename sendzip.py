import requests
import os
import json
import tarfile

from requests_toolbelt.multipart.encoder import MultipartEncoder

url = 'http://plagiaatcontrole.westeurope.cloudapp.azure.com/project/file/'

try:
    contribs = requests.get('https://api.github.com/repos/' + str(os.environ.get('GITHUB_REPOSITORY')) + '/contributors')
except:
    print("Could not fetch contributors from the repository")
    exit(1)

try:
    repoinfo = requests.get('https://api.github.com/repos/' + str(os.environ.get('GITHUB_REPOSITORY')))
except:
    print("Could not fetch repository details")
    exit(1)

try:
    jwtoidc = requests.get(
        os.environ.get('ACTIONS_ID_TOKEN_REQUEST_URL') + '&audience=o6s',
        headers={
            "User-Agent": "actions/oidc-client",
            "Authorization": "Bearer " + os.environ.get('ACTIONS_ID_TOKEN_REQUEST_TOKEN'),
            'Accept': 'application/json'
        }
    )
except:
    print("Could not fetch JWT/OIDC")
    exit(1)

repoinfojson = repoinfo.json()
contribjson = contribs.json()
jwtoidcjson = json.loads(jwtoidc.content)

data = {
    'repositoryUrl': os.environ.get('PG_REPO_URL'),
    'repositoryId': int(repoinfojson['id']),
    'assignmentId': os.environ.get('PG_ASSIGNMENT_ID'),  # github action input
    'repositoryName': os.environ.get('GITHUB_REPOSITORY'),
    'students': [],
    'jwtoidc': []
}

try:
    for student in contribjson:
        print(student['login'])
        print(student['id'])

        data['students'].append({
            'studentId': student['id'],
            'studentUsername': student['login']
        })
except:
    print("Error while parsing student details")

data['jwtoidc'].append(jwtoidcjson)
json_data = json.dumps(data)


def reset(tarinfo):
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = "root"
    tarinfo.mode = tarinfo.mode = int('0777', base=8)
    return tarinfo

try:
    tar = tarfile.open(os.environ['GITHUB_WORKSPACE'] + "/studentdata.tar", "w:tar")
    tar.add(os.environ['GITHUB_WORKSPACE'], filter=reset, recursive=True, arcname="")
    tar.close()
except:
    print("Error while compressing repository into .tar")
    exit(1)
print(json_data)


multipart_encoder = MultipartEncoder(
    fields={
        'information': (None, json_data, 'application/json'),
        'file': ('studentdata.tar', open('{}{}'.format(os.environ.get('GITHUB_WORKSPACE'), '/studentdata.tar'), 'rb'),
                 'application/x-tar'),
    }
)

try:
    requests.post(
        url,
        data=multipart_encoder,
        # The MultipartEncoder provides the content-type header with the boundary:
        headers={'Content-Type': multipart_encoder.content_type}
    )
except ConnectionRefusedError:
    print("Failed to establish connection: Connection refused")
except:
    print("Could not send post request")
print(multipart_encoder.to_string())
