import random
import numpy as np


def f(lamda, x):
    return lamda*x*(1-x)


def run(lamda, x, length):
    for _ in range(length):
        x = f(lamda, x)
    return x


def map(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


def rnd(lamda, seed):
    num = (run(seed, lamda, 100 + int((seed*100) % 32))*10000*seed) % 1
    seed = map(num, 0, 1, 3.5, 4)
    return seed, num


def generateAES():
    # seed =float(input("Enter initial Seed belongs to (3.5,4)"))
    # lamda=float(input("Enter initial lamda belongs to (0,1)"))
    seed = random.uniform(3.5, 4)
    lamda = random.uniform(0, 1)
    num = None
    y = []
    while len(y) < 256:
        seed, num = rnd(lamda, seed)
        if int(num*1000) % 256 not in y:
            y.append(int(num*1000) % 256)
            # print(int(num*1000)%256)
    y = np.array(y)
    y = np.reshape(y, (16, 16))
    return y
