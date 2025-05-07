# hacman_api_access_key

## api.local/v1/access/tool/fob_id/{fob_id}
Each tool will have an api key sent as a header
returns:
* status_code:
* announce_name:
* (member) id:

## api.local/v1/access/door/fob_id/{fob_id}
Each door will have an api key sent as a header
* status code:
* announce_name:
* (member) id:

## api.local/v1/status
This allows us to check if the api is working.
* status_code: 200