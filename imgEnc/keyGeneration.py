import random
import pickle
import numpy as np

subkeys = []


def generateKey():
    for i in range(0, 8):
        key = []
        for j in range(0, 256):
            key.append(random.randint(0, 255))
        subkeys.append(key)
    arr = np.array(subkeys)
    np.savetxt("keys.txt", arr, fmt="%s")
    return subkeys
