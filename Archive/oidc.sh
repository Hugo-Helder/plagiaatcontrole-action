#!/bin/bash
OIDC_TOKEN=$(curl -L "${ACTIONS_ID_TOKEN_REQUEST_URL}&audience=o6s" -H "User-Agent: actions/oidc-client" -H "Authorization: Bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN")
JWT=$(echo "$OIDC_TOKEN" | jq -j '.value')
touch "$GITHUB_WORKSPACE/oidc.token"
echo "$JWT" > "$GITHUB_WORKSPACE/oidc.token"
cat "$GITHUB_WORKSPACE/oidc.token"
