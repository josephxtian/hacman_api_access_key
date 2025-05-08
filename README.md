# hacman_api_access_key

## api.local/v1/access/tool/fob_id/{fob_id}
Each tool will have an api key sent as a header in the request. This will be checked against a csv list linking tool_id to api_key.
returns:
* status_code:
* announce_name:
* (member) id:

## api.local/v1/access/door/fob_id/{fob_id}
* status code:
* announce_name:
* (member) id:

## api.local/v1/status
This allows us to check if the api is working.
* status_code: 200