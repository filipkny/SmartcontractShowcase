

import os
from PIL import Image
import numpy as np

picture = Image.open("deniiro.jpeg")

#Original value(цвет который будем менять)
r1, g1, b1 = 0, 0, 0

for i in range(256):
    data = np.array(picture)
    #Value that we want to replace it with(цвет выхода)
    [r2, g2, b2] = list(np.random.choice(range(256), size=3))
    print(r2,g2,b2)
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]

    mask = (red == r1) & (green == g1) & (blue == b1)

    data[:,:,:3][mask] = [r2, g2, b2]

    im = Image.fromarray(data)
    im.save('{}.png'.format(i))