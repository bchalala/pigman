import torch

import pyro
import pyro.distributions as dist

def tower():
    blocks = pyro.sample('numblocks', dist.Normal(0, 2))
    if (blocks < 0):
        blocks = -1*blocks
    blocks += 3

    blockLocations = []
    for i in range(0, blocks):
        x = pyro.sample('x_{}'.format(i), dist.Uniform(0,10))
        x = pyro.sample('y_{}'.format(i), dist.Uniform(0, blocks))

    return blockLocations


print(tower())
