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
    frameset = defs.EVERY_5TH
    category = sys.argv[1]
    inputfiles = sys.argv[2:]
    all_individuals = util.parse_files(inputfiles, frames=frameset[0])

    all_data = [ all_individuals[c][i][v][f] \
            for c in all_individuals.keys() \
            for i in all_individuals[c].keys() \
            for v in all_individuals[c][i].keys() \
            for f in all_individuals[c][i][v].keys() ]


    topdir = frameset[1]
    metricdir = "ccol"
    nndir = "%snn" % neighbors

    dirstring = '/'.join([topdir, metricdir, nndir]) 
    avgfile = dirstring + '/averages.csv'
    dirstring += '/raw'
    if not os.path.exists(dirstring):
        os.makedirs(dirstring)

    f = open(avgfile, 'w+')
    f.write('category,%s_%s_%s\n' % (nndir, metricdir, topdir))
    f.close()
       
    #RESULT VARIABLES:
    added_results = float(0.0)
    number_instances = 0
    total_tested = 0
    total_correct = 0

    for instance in all_individuals[category]:
        i = instance
        c = category
        testdata = [ all_individuals[c][i][v][f] \
                for v in all_individuals[c][i].keys() \
                for f in all_individuals[c][i][v].keys() ]

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
