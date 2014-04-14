#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import os
import operator
import random
import nearest_neighbor as nn
import defs
import util
import argparse
from histogram import *

def parse_data(frameset, weight_dict, metrics):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = script_dir + '/data'
    individuals = {}
    for data_file in os.listdir(data_dir):
        if not data_file in metrics:
            print "Skipping %s" % data_file
            continue
        data_file = data_dir + '/' + data_file
        individuals = util.parse_file(data_file, frames=frameset[0],
                weights=weight_dict, dictionary=individuals)
    return individuals

def main():
    #ARGUMENT PARSING:
    known_metrics = ['da3', 'cr64', 'cg64', 'dd3', 'cb64', 'ccol', 'dd2']
    used_metrics = []
    parser = argparse.ArgumentParser(prog='Histalyzer')
    for m in known_metrics:
        parser.add_argument('--%s' % m, type=int)
    parser.add_argument('--nn', type=int, default=5)
    parser.add_argument('--wcolor', type=int, default=1)
    parser.add_argument('--wdepth', type=int, default=1)
    parser.add_argument('categories', nargs='+')
    parsed =  parser.parse_args()
    if len(parsed.categories) == 1:
        if parsed.categories[0] == 'all':
            categories = defs.ALL_CATEGORIES
        elif parsed.categories[0] == 'run1':
            categories = defs.RUN1
        elif parsed.categories[0] == 'run2':
            categories = defs.RUN2
        elif parsed.categories[0] == 'run3':
            categories = defs.RUN3
        elif parsed.categories[0] == 'run4':
            categories = defs.RUN4
        else:
            categories = parsed.categories
    else:
        categories = parsed.categories
    weight_color = parsed.wcolor
    weights_color = []
    weight_depth = parsed.wdepth
    weights_depth = []
    neighbors = parsed.nn

    for k, v in vars(parsed).iteritems():
        if not v or not k in known_metrics:
            continue
        if k[0] == 'c':
            weights_color.append((k, v))
            used_metrics.append(k)
        elif k[0] == 'd':
            weights_depth.append((k, v))
            used_metrics.append(k)
        else:
            raise ValueError('unknown metric type: "%s"' % k[0])

    if not weights_color:
        weight_color = 0
    if not weights_depth:
        weight_depth = 0
    weight_dict = {}
    weight_dict['color'] = ( weight_color , weights_color )
    weight_dict['depth'] = ( weight_depth , weights_depth )

    #PARAMETER SETUP:
    ######!!!!!!!!!!!!!!!!!!
    frameset = defs.EVERY_5TH
    category = categories[0]
    all_individuals = parse_data(frameset, weight_dict, used_metrics)

    all_data = [ all_individuals[c][i][v][f] \
            for c in all_individuals.keys() \
            for i in all_individuals[c].keys() \
            for v in all_individuals[c][i].keys() \
            for f in all_individuals[c][i][v].keys() ]

    topdir = frameset[1]
    metricdir = reduce(lambda x, y: x+'_'+y, used_metrics)
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

    for category in categories:
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
