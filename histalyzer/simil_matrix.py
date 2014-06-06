import sys
import math
#import numpy as np

m = 0
sig = 12

def main():
    co = 0.0
    msub = None
    

    if len(sys.argv) > 2:
        msub = int(sys.argv[2])
    if len(sys.argv) > 3:
        co = float(sys.argv[3])

    simtrix = get_simil_matrix(int(sys.argv[1]), msub, co)
   # for row in simtrix:
   #     print row
    nm = np.matrix(simtrix)
    #print nm.T * nm
    print
    print nm
    print nm.T


def get_simil_matrix(size, maxsub=None, cutoff=0.0):
    matrix = [ [0] * size for i in range(size) ]
    if not maxsub:
        maxsub = size
    for i, row in enumerate(matrix):
        rights = [ i + x for x in range(maxsub) if i + x < len(row) ]
        lefts  = [ i - x for x in range(maxsub) if i - x >= 0]
        for v, r in enumerate(rights):
            newval = norm_dense(m, sig, v)/norm_dense(m, sig, 0)
            if newval >= cutoff:
                row[r] = newval 
        for v, r in enumerate(lefts):
            newval = norm_dense(m, sig, v)/norm_dense(m, sig, 0)
            if newval >= cutoff:
                row[r] = newval 
    return matrix



def get_norm(n):
    maxd = norm_dense(m, sig, 0)
    vals = []
    for i in xrange(n):
        vals.append(norm_dense(m, sig, i)/maxd)

    print vals

def norm_dense(m, sig, x):
    sig = float(sig)
    m = float(m)
    p1 = 1 / (math.sqrt(2*math.pi*sig))
    p2 = ((x - m)**2)/(2*sig* -1)
    return p1*math.exp(p2)

if __name__ == "__main__":
    main()
