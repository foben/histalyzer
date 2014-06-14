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
from parse_arguments import parse_categories
from histogram import *
from knnclassifier import KNNClassifier
from video_knnclassifier import VideoKNNClassifier

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
    parser.add_argument('--scores', action='store_true')
    parser.add_argument('categories', nargs='+')
    parser.add_argument('--every', type=int, default=25)
    parsed =  parser.parse_args()
    SET_NOFILES = parsed.no_files
    SET_QUIET = parsed.quiet
    SET_DEBUG = parsed.debug
    SET_EVERY = parsed.every
    SET_SCORES = parsed.scores
    if SET_QUIET:
        logging.basicConfig(level=logging.WARN)
    elif SET_DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    categories, SET_PARTIAL = parse_categories(parsed.categories)
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
    frameset = defs.get_frameset(SET_EVERY)
    all_individuals = parse_data(used_metrics)

    if not SET_NOFILES:
        dir_top, dir_raw = create_directory_structure(frameset, used_metrics, neighbors,
                partial=SET_PARTIAL, weights_color=weights_color, weights_depth=weights_depth)

    #OVERALL VARIABLES:
    classifier = KNNClassifier(weight_dict, neighbors, defs.ALL_CATEGORIES)
    classifier = VideoKNNClassifier(weight_dict, neighbors, defs.ALL_CATEGORIES)
    for category in categories:

        for instance in all_individuals[category]:
            #traindata, testdata = util.get_datasets(category, instance, all_individuals, frameset[0])
            traindata, testdata = util.get_video_datasets(category, instance, all_individuals, frameset[0])
            #result, instance_tested, instance_correct = nn.nearest_neighbor(traindata, testdata, neighbors)
            classifier.perform_classification(traindata, testdata)

    if not SET_NOFILES:
        classifier.print_confusion_matrix(dir_top + '/confusion.csv')

    if SET_SCORES:
        scrs = classifier.get_overall_scores()
        print "{},{},{}".format(scrs[0], scrs[1], scrs[2])

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

def create_directory_structure(frameset, used_metrics, neighbors, partial=None,
        weights_color=None, weights_depth=None):
    topdir = frameset[1] + '_video'
    la_weightsdir = lambda st, (m, w): st + '%s-%s_' % (m, w)
    metricdir = ''
    metricdir = reduce(la_weightsdir, weights_depth, metricdir)
    metricdir = reduce(la_weightsdir, weights_color, metricdir)
    metricdir = metricdir[0:-1]
    nndir = "%snn" % neighbors

    topdir = '_'.join([topdir, nndir]) 
    if partial:
        topdir += partial
    topdir = '/'.join([topdir, metricdir])
    raw_dir = topdir + '/raw'
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
    return topdir, raw_dir

main()
