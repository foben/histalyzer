#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import operator
import time
import datetime
import logging
from histogram import *
from collections import Counter, OrderedDict

class KNNClassifier:

    def __init__(self, weights, k=5, classes=None):
        self.k = k
        self.confusion_matrix = OrderedDict([ (actual,
            OrderedDict([ (predicted,0) for predicted in classes] ))
            for actual in classes ])
        self.cweight = weights['color'][0]
        self.dweight = weights['depth'][0]

        lsum = lambda s, (m, w): s + w
        if self.cweight:
            self.color_weights = weights['color'][1]
            self.sum_color_weights = reduce(lsum, self.color_weights, 0)
        if self.dweight:
            self.depth_weights = weights['depth'][1]
            self.sum_depth_weights = reduce(lsum, self.depth_weights, 0)
        self.sum_weights = self.cweight + self.dweight

        #self.dist_func = diff_sum
        self.dist_func = diff_chi

        assert (self.cweight > 0 or self.dweight > 0)

        if self.cweight > 0 and self.dweight > 0:
            def compute(train, test):
                coldiff = reduce(lambda s, (m,w): s +
                        self.dist_func(train.histograms[m], test.histograms[m])*w,
                        self.color_weights, 0
                        ) * self.cweight

                depdiff = reduce(lambda s, (m,w): s +
                        self.dist_func(train.histograms[m], test.histograms[m])*w,
                        self.depth_weights, 0
                        ) * self.dweight
                return (coldiff + depdiff) / self.sum_weights
        elif self.cweight > 0 and self.dweight == 0:
            def compute(train, test):
                coldiff = reduce(lambda s, (m,w): s +
                        self.dist_func(train.histograms[m], test.histograms[m])*w,
                        self.color_weights, 0
                        )
                return coldiff
        elif self.cweight == 0 and self.dweight > 0:
            def compute(train, test):
                depdiff = reduce(lambda s, (m,w): s +
                        self.dist_func(train.histograms[m], test.histograms[m])*w,
                        self.depth_weights, 0
                        ) * self.dweight
                return depdiff
        else:
            raise ValueError("Something went wrong")
        self.distance_function = compute

    def get_distance(self, traini, testi):
        return self.distance_function(traini, testi)

    def get_class_label(self, slist):
        sublist =[ tr.category for tr in slist[0:self.k] ]
        c = Counter(sublist)
        maxlist = c.most_common()
        maxcat = maxlist[0][0]
        maxct = maxlist[0][1]
        for ct in maxlist[1:]:
            if ct[1] < maxct:
                break
            if sublist.index(ct[0]) < sublist.index(maxcat):
                maxcat = ct[0]
                maxct = ct[1]
        return maxcat

    def perform_classification(self, training_data, testing_data):
        total_count = len(testing_data) 
        running_count = 0
        failure_count = 0
        correct_count = 0

        start_time = time.clock()
        for test in testing_data:
            running_count += 1
            sortkey = lambda tr: self.get_distance(test, tr)
            slist = sorted( training_data, key=sortkey )
            assigned_cat = self.get_class_label(slist)
            actual_cat = test.category
            self.confusion_matrix[actual_cat][assigned_cat] += 1
            marker = ""
            if (assigned_cat == actual_cat):
                correct_count += 1
            else:
                failure_count += 1
            if running_count % 50 == 0:
                remaining = self.calc_remaining_time(start_time, total_count, running_count)
                logging.info("ETA %s %s: %s", test.category, test.instance, remaining)

        correct_percentage = float(correct_count)/ total_count * 100
        return correct_percentage, total_count, correct_count

    def calc_remaining_time(self, start, total, current):
        percentage = float(current) / total
        ptime = time.clock() - start
        rtime = ptime / percentage * (1-percentage)
        remaining = datetime.timedelta(seconds=int(rtime) )
        return remaining

    def print_line(self, assigned_cat, actual_cat):
        msg = "Assigned %s, was %s" % (assigned_cat, actual_cat)
        msg = msg.ljust(40, ' ')
        msg = "%s  %s" % (msg, "✓ " if assigned_cat == actual_cat else " ✗")
        print msg

    def print_confusion_matrix(self, filename):
        f = open(filename, 'w')
        firstrow = ''
        for heads in self.confusion_matrix.iterkeys():
            firstrow += ','
            firstrow += heads
        f.write(firstrow)
        f.write('\n')
        for actual, pdict in self.confusion_matrix.iteritems():
            currow = actual
            for predicted, value in pdict.iteritems():
                currow += ','
                currow += str(value)
            f.write(currow)
            f.write('\n')
        f.close()

