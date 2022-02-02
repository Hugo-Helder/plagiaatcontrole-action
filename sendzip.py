import requests
import os
import json
import tarfile

from requests_toolbelt.multipart.encoder import MultipartEncoder



url = os.environ.get('ACTIONS_BACKEND_URL')

contribs = requests.get('https://api.github.com/repos/' + str(os.environ.get('GITHUB_REPOSITORY')) + '/contributors')
repoinfo = requests.get('https://api.github.com/repos/' + str(os.environ.get('GITHUB_REPOSITORY')))

jwtoidc = requests.get(
    os.environ.get('ACTIONS_ID_TOKEN_REQUEST_URL') + '&audience=o6s',
    headers={
        "User-Agent": "actions/oidc-client",
        "Authorization": "Bearer " + os.environ.get('ACTIONS_ID_TOKEN_REQUEST_TOKEN'),
        'Accept': 'application/json'
    }
)

repoinfojson = repoinfo.json()
contribjson = contribs.json()
jwtoidcjson = json.loads(jwtoidc.content)

data = {
    'repositoryUrl': 'kip.git',
    'repositoryId': int(repoinfojson['id']),
    'assignmentId': os.environ.get('PG_ASSIGNMENT_ID'),  # github action input
    'repositoryName': os.environ.get('GITHUB_REPOSITORY'),
    'students': [],
    'jwtoidc': []
}

for student in contribjson:
    print(student['login'])
    print(student['id'])

    data['students'].append({
        'studentId': student['id'],
        'studentUsername': student['login']
    })

data['jwtoidc'].append(jwtoidcjson)
json_data = json.dumps(data)


def reset(tarinfo):
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = "root"
    tarinfo.mode = tarinfo.mode = int('0777', base=8)
    return tarinfo


tar = tarfile.open(os.environ['GITHUB_WORKSPACE'] + "/studentdata.tar", "w:tar")
tar.add(os.environ['GITHUB_WORKSPACE'], filter=reset, recursive=True, arcname="")
tar.close()

print(json_data)


multipart_encoder = MultipartEncoder(
    fields={
        'information': (None, json_data, 'application/json'),
        'file': ('studentdata.tar', open('{}{}'.format(os.environ.get('GITHUB_WORKSPACE'), '/studentdata.tar'), 'rb'),
                 'application/x-tar'),
    }
)

requests.post(
    url,
    data=multipart_encoder,
    # The MultipartEncoder provides the content-type header with the boundary:
    headers={'Content-Type': multipart_encoder.content_type}
)

print(multipart_encoder.to_string())
