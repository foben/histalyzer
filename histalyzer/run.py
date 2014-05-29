#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import os
import operator
import random
import logging
import defs
import util
import argparse
from histogram import *
from knnclassifier import KNNClassifier

def main():
    #ARGUMENT PARSING:
    known_metrics = ['cr64', 'cg64', 'cb64','ccol',\
            'dd2', 'da3', 'dd3', 'dd2_64', 'da3_64', 'dd3_64',\
            'dd2_128', 'dd3_128', 'da3_128']
    used_metrics = []
    parser = argparse.ArgumentParser(prog='Histalyzer')
    for m in known_metrics:
        parser.add_argument('--%s' % m, type=int)
    parser.add_argument('--nn', type=int, default=5)
    parser.add_argument('--wcolor', type=int, default=1)
    parser.add_argument('--wdepth', type=int, default=1)
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--no_files', action='store_true')
    parser.add_argument('--print_total', action='store_true')
    parser.add_argument('categories', nargs='+')
    parser.add_argument('--every', type=int, default=25)
    parsed =  parser.parse_args()
    SET_NOFILES = parsed.no_files
    SET_PRINTTOTAL = parsed.print_total
    SET_QUIET = parsed.quiet
    SET_DEBUG = parsed.debug
    SET_EVERY = parsed.every
    if SET_QUIET:
        logging.basicConfig(level=logging.WARN)
    elif SET_DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
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
        elif parsed.categories[0] == 'run12':
            categories = defs.RUN12
        elif parsed.categories[0] == 'run34':
            categories = defs.RUN34
        else:
            categories = parsed.categories
        categories_string = parsed.categories[0]
    else:
        categories = parsed.categories
        categories_string = '_'.join(categories)
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
    #frameset = defs.EVERY_5TH
    #frameset = defs.EVERY_25TH
    frameset = defs.get_frameset(SET_EVERY)
    all_individuals = parse_data(used_metrics)

    if not SET_NOFILES:
        dir_raw, file_avg = create_directory_structure(frameset, used_metrics, neighbors, weights_color=weights_color, weights_depth=weights_depth)

    #OVERALL VARIABLES:
    overall_tested = 0
    overall_correct = 0
    
    classifier = KNNClassifier(weight_dict, neighbors, defs.ALL_CATEGORIES)

    for category in categories:
        #CATEGORY VARIABLES:
        category_tested = 0
        category_correct = 0

        for instance in all_individuals[category]:
            traindata, testdata = util.get_datasets(category, instance, all_individuals, frameset[0])
            #result, instance_tested, instance_correct = nn.nearest_neighbor(traindata, testdata, neighbors)
            result, instance_tested, instance_correct = classifier.perform_classification(traindata, testdata)
            category_tested += instance_tested
            overall_tested += instance_tested
            category_correct += instance_correct
            overall_correct += instance_correct
            if not SET_NOFILES:
                f = open("%s/category_%s.csv" % (dir_raw, category), "a")
                f.write('%s %s,%s\n' % (category, instance, result))
                f.close()

        average_aggregated = float(category_correct) / category_tested * 100
        if not SET_NOFILES:
            f = open("%s/category_%s.csv"% (dir_raw, category), "a")
            f.write('%s average,%s\n' % (category, average_aggregated))
            f.close()
    
    classifier.print_confusion_matrix(dir_raw + '/confusion.csv')

    overall_percentage = float(overall_correct)/overall_tested * 100
    logging.info("Overall %% %f", overall_percentage)
    if not SET_NOFILES:
        f = open(file_avg, "a")
        f.write('overall_%s,%s,%s\n' % (categories_string, overall_tested, overall_correct))
        f.close()

    if SET_PRINTTOTAL:
        print "%f" %  overall_percentage

def parse_data(metrics):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = script_dir + '/data'
    individuals = {}
    for data_file in os.listdir(data_dir):
        if not data_file in metrics:
            logging.info("Skipping %s", data_file)
            continue
        data_file = data_dir + '/' + data_file
        individuals = util.parse_file(data_file, dictionary=individuals)
    return individuals

def create_directory_structure(frameset, used_metrics, neighbors, weights_color=None, weights_depth=None):
    topdir = frameset[1]
    la_weightsdir = lambda st, (m, w): st + '%s-%s_' % (w, m)
    metricdir = ''
    metricdir = reduce(la_weightsdir, weights_depth, metricdir)
    metricdir = reduce(la_weightsdir, weights_color, metricdir)
    metricdir = metricdir[0:-1]
    nndir = "%snn" % neighbors

    dirstring = '_'.join([topdir, nndir]) 
    dirstring = '/'.join([dirstring, metricdir])
    avgfile = dirstring + '/averages.csv'
    dirstring += '/raw'
    if not os.path.exists(dirstring):
        os.makedirs(dirstring)

    f = open(avgfile, 'a')
    f.write('category,%s_%s_%s\n' % (nndir, metricdir, topdir))
    f.close()
    return dirstring, avgfile

main()