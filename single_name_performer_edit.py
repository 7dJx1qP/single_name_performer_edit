import sys
import json
from stash_interface import StashInterface

import log

def read_json_input():
    json_input = sys.stdin.read()
    return json.loads(json_input)
    
json_input = read_json_input()
suffix = json_input['args']['suffix']
client = StashInterface(json_input["server_connection"])

single_name_performer_regex = "^[^\\s]*$"

try:
    log.LogInfo("suffix: {}".format(suffix))

    while True:
        variables = {
            "filter":
                {
                    "q": "",
                    "page": 1,
                    "per_page": 100,
                    "sort": "name",
                    "direction": "ASC"
                },
            "performer_filter": {
                "name": {
                    "value": single_name_performer_regex,
                    "modifier":"MATCHES_REGEX"
                }
            }
        }
        performers = client.findPerformers(variables)
        if not performers:
            break
        for performer in performers:
            name = performer.get("name")
            performer_id = performer.get("id")
            try:
                result = client.updatePerformer({
                    "id": performer_id,
                    "name": name + suffix
                })
                log.LogInfo(f"Updated {name} -> {name + suffix}")
            except Exception as e:
                log.LogError(f'Failed {name} -> {name + suffix} {e}')

except Exception as e:
    log.LogError(str(e))

log.LogInfo('done')
output = {}
output["output"] = "ok"
out = json.dumps(output)
print(out + "\n")