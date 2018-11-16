import pyro
import pyro.distributions as dist

def sampleblocks(n, XDIM, YDIM):
    blocks = []
    satisfied = False

    while(not satisfied):
        blocks = []
        satisfied = True

        for i in range(n):
            xdim = pyro.sample('xdim', dist.Uniform(0, XDIM))
            ydim = pyro.sample('ydim', dist.Uniform(0, YDIM))
            xsize = pyro.sample('xsize', dist.Normal(50, 20))
            ysize = pyro.sample('xsize', dist.Normal(50, 20))
            # CONVERTING TO INTS FROM TENSORS, BAD!
            blocks.append((int(xdim.item()), int(ydim.item()), 
                int(xsize.item()), int(ysize.item())))

        for block in blocks:
            for block2 in blocks:
                if(block == block2):
                    continue
                else:
                    # NOT USING PYRO.CONDITION
                    satisfied = \
                        (block[0] + block[2]/2 < block2[0] - block[2]/2 or
                         block[0] - block[2]/2 > block2[0] + block[2]/2 or
                         block[1] + block[3]/2 < block2[1] - block[3]/2 or
                         block[1] - block[3]/2 > block2[1] + block[3]/2)

    return blocks