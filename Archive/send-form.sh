#!/bin/bash
ls $GITHUB_WORKSPACE
curl --location --request POST 'http://20.50.138.112:8092/project/file/' \
--form 'file=@"'"$GITHUB_WORKSPACE"'"/studentdata.zip' \
--form 'information="{
    \"repositoryUrl\": \"kip.git\",
    \"repositoryId\": 1,
    \"courseId\": \"b2a29e54-4a83-48ec-8c72-8bf12e07a967\",
    \"repositoryName\": \"bananannanannanannanananannana\",
    \"students\": [
        {
            \"studentId\": 1,
            \"studentUsername\": \"Tim\"
        },
        {
            \"studentId\": 2,
            \"studentUsername\": \"Tom\"
        }
    ]
}";type=application/json'