
import version
import json

bfVersion = version.get_version()
print(bfVersion) 
 
def loadConfig(filename='fontsettings.json'):
    with open(filename) as f:
        return json.load(f)