import json
import os
from PIL import Image
import numpy as np
import requests

import ipfsApi

print(os.getcwd())
api = ipfsApi.Client('127.0.0.1', 5001)
picture = Image.open("../deniiro.jpeg")

r1, g1, b1 = 0, 0, 0

for i in range(10):
    data = np.array(picture)

    [r2, g2, b2] = list(np.random.choice(range(256), size=3))
    print(r2,g2,b2)
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]

    mask = (red == r1) & (green == g1) & (blue == b1)

    data[:,:,:3][mask] = [r2, g2, b2]

    im = Image.fromarray(data)
    im.save('../images/{}.png'.format(i))

    with open('../images/{}.png'.format(i),'rb') as f:
        files = {
            "0" : (f)
        }

        res = api.add(files=f,recursive=False)

    print("Response of adding image " + str(res))
    metadata = {
        "name" : "{}".format(i),
        "description" : "Tombo's Deniiro #{}".format(i),
        "image" : "https://ipfs.io/ipfs/{}".format(res[0]['Hash']),
        "attributes" : [ ]
    }

    print(metadata)

    with open(f"../metadata/{i}","w") as f:
        json.dump(metadata,f)






