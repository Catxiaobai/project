import re
import json

data = []
with open('1.json') as f:
    for line in f:
        data.append(json.loads(line))
