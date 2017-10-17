#

import requests
word = 'furniture'
obj = requests.get("http://api.conceptnet.io/c/en/furniture?rel=/r/"+word+"&limit=1000").json()
for i in range(len(obj['edges'])):
    if (obj['edges'][i]['start']['language'] == 'en' or obj['edges'][i]['start']['language'] == 'zh') and \
                    obj['edges'][i]['weight'] > 1.4:
        print obj['edges'][i]['start']['label']
