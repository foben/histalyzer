#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import operator
import random
import nearest_neighbor as nn
from defs import *
from histogram import *

def main():
    #data_dict = parse_sorted(sys.argv[1])
    data_dict = parse_selected(sys.argv[1], frames=range(0,331,5))
    category = sys.argv[2]

    for instance, testdata in data_dict[category].iteritems():
        traindata = get_training_data(testdata, data_dict)
        print 'Testing category "%s", instance %s' % (category, instance)
        result = nn.nearest_neighbor(traindata, testdata)
        f = open("category_%s.csv" % category, "a")
        f.write('%s %s,%s\n' % (category, instance, result))
        f.close()

def get_training_data(test_data, data_dict):
    training = []
    for category, instancelist in data_dict.iteritems():
        for li in instancelist:
            training.extend(instancelist[li])
    training = list(set(training) - set(test_data))
    return training


main()
