#

# import requests
# word = 'furniture'
# obj = requests.get("http://api.conceptnet.io/c/en/furniture?rel=/r/"+word+"&limit=1000").json()
# for i in range(len(obj['edges'])):
#     if (obj['edges'][i]['start']['language'] == 'en' or obj['edges'][i]['start']['language'] == 'zh') and \
#                     obj['edges'][i]['weight'] > 1.4:
#         print obj['edges'][i]['start']['label']
#
from pydoc import help
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib



files = os.listdir('apple')

files = [os.path.join('apple', file_i)
         for file_i in os.listdir('apple')
         if '.jpg' in file_i]

# print plt.imread(files[0])

img = plt.imread(files[0])

plt.imshow(img)
matplotlib.interactive(False)
