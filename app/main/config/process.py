import re
with open('quotes_raw.txt', 'r') as f:
    lines = f.readlines() 


output = {
            "easy":{},
            "medium":{},
            "hard":{}
        }
for line in lines:
    line  = line.strip()
    if len(line) > 100:
        output['easy'][len(output['easy']) +1] = re.sub(r'([^\s\w]|_)+', '', line)
    elif len(line) > 70:
        output['medium'][len(output['medium']) +1] = re.sub(r'([^\s\w]|_)+', '', line)
    else:
        output['hard'][len(output['hard']) +1] = re.sub(r'([^\s\w]|_)+', '', line)


import json
print json.dumps(output, indent=4)

