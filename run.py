#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import os
import operator
import random
import nearest_neighbor as nn
import defs
import util
from histogram import *

def main():
    #PARAMETER SETUP:
    neighbors = 5
    frameset = defs.EVERY_5TH_FRAME
    category = sys.argv[1]
    inputfiles = sys.argv[2:]
    data_dict = util.parse_files(inputfiles, frames=frameset[0])

    all_data = [ data_dict[c][i][v][f] \
            for c in data_dict.keys() \
            for i in data_dict[c].keys() \
            for v in data_dict[c][i].keys() \
            for f in data_dict[c][i][v].keys() ]

    dirstring = "%s_nn" % neighbors
    if not os.path.exists(dirstring):
        os.makedirs(dirstring)
       
    #RESULT VARIABLES:
    added_results = float(0.0)
    number_instances = 0
    total_tested = 0
    total_correct = 0

    for instance in data_dict[category]:
        i = instance
        c = category
        testdata = [ data_dict[c][i][v][f] \
                for v in data_dict[c][i].keys() \
                for f in data_dict[c][i][v].keys() ]

        traindata = list(set(all_data) - set(testdata))
        number_instances += 1
        result, tests, corrects = nn.nearest_neighbor(traindata, testdata, neighbors)
        added_results += result
        total_tested += tests
        total_correct += corrects
        f = open("%s/category_%s.csv" % (dirstring, category), "a")
        f.write('%s %s,%s\n' % (category, instance, result))
        f.close()

    average_mean = added_results / number_instances
    average_aggregated = float(total_correct) / total_tested * 100
    f = open("%s/category_%s.csv" % (dirstring, category), "a")
    f.write('%s average_mean,%s\n' % (category, average_mean))
    f.write('%s average,%s\n' % (category, average_aggregated))
    f.close()

main()
