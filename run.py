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
    neighbors = 3

    added_results = float(0.0)
    number_instances = 0
    total_tested = 0
    total_correct = 0

    for instance, testdata in data_dict[category].iteritems():
        number_instances += 1
        traindata = get_training_data(testdata, data_dict)
        print 'Testing category "%s", instance %s' % (category, instance)
        result, tests, corrects = nn.nearest_neighbor(traindata, testdata, neighbors)
        added_results += result
        total_tested += tests
        total_correct += corrects
        f = open("category_%s.csv" % category, "a")
        f.write('%s %s,%s\n' % (category, instance, result))
        f.close()

    average_mean = added_results / number_instances
    average_aggregated = float(total_correct) / total_tested * 100
    f = open("category_%s.csv" % category, "a")
    #f.write('%s average_mean ,%s\n' % (category, average_mean))
    f.write('%s average ,%s\n' % (category, average_aggregated))
    f.close()

def get_training_data(test_data, data_dict):
    training = []
    for category, instancelist in data_dict.iteritems():
        for li in instancelist:
            training.extend(instancelist[li])
    training = list(set(training) - set(test_data))
    return training


main()
