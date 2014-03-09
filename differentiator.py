import sys
import histogram
import matplotlib.pyplot as plt
from histogram import *
from defs import *

def main():
    categories = ['apple']
    instances = [1]
    views = [1]
    frames = 'all'

    category_dict = parse_selected(sys.argv[1], categories, instances, views, frames)
    hlist = sorted(histogram.get_list_from_hdict(category_dict))
    difflist = []
    for i in range(len(hlist)):
        for j in range(i+1, len(hlist)):
            h1 = hlist[i]
            h2 = hlist[j]
            if h1 == h2: continue
            dist = histogram.diff_sum(h1, h2)
            difflist.append( (dist, h1, h2) )
    sorted_difflist = sorted(difflist, key=lambda inp: inp[0])
       

main()
