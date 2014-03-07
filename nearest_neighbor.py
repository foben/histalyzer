#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import operator
from histogram import *

def nearest_neighbor(training_data, testing_data, neighbors=3):
    total_count = 0
    failure_count = 0
    correct_count = 0

    for test in testing_data:
        total_count += 1
        slist = sorted( training_data, key=lambda tr: diff_sum(test, tr) )
        categories = {}
        for n in range(neighbors):
            neighbor = slist[n]
            cat = neighbor.category
            if cat in categories:
                categories[cat] += 1
            else:
                categories[cat] = 1
        assigned_cat = sorted(categories.iteritems(), key=operator.itemgetter(1), reverse=True)[0][0]
        actual_cat = test.category
        marker = ""
        if (assigned_cat == actual_cat):
            marker = "✓ "
            correct_count += 1
        else:
            marker = " ✗"
            failure_count += 1
        msg = "Assigned %s, was %s" % (assigned_cat, actual_cat)
        msg = msg.ljust(40, ' ')
        msg = "%s  %s" % (msg, marker)
        print msg
    correct_percentage = float(correct_count)/ total_count * 100
    print "%s Total, %s correct, %s false" % (total_count, correct_count, failure_count)
    print "%.3f %% accuracy!" % correct_percentage
    return correct_percentage
