#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import operator
import time
import datetime
from histogram import *

def nearest_neighbor(training_data, testing_data, neighbors=3):
    total_count = len(testing_data) 
    running_count = 0
    failure_count = 0
    correct_count = 0

    testing_categories = set()

    for hist in testing_data:
        testing_categories.add(hist.category)
    print "%s different categories in test data." % len(testing_categories)

    start_time = time.clock()
    for test in testing_data:
        running_count += 1
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
            correct_count += 1
        else:
            failure_count += 1
        #print_line(assigned_cat, actual_cat)
        calc_remaining_time(start_time, total_count, running_count)
    correct_percentage = float(correct_count)/ total_count * 100
    return correct_percentage

def calc_remaining_time(start, total, current):
    percentage = float(current) / total
    ptime = time.clock() - start
    rtime = ptime / percentage * (1-percentage)
    remaining = datetime.timedelta(seconds=int(rtime) )
    print remaining
    return remaining



def print_line(assigned_cat, actual_cat):
    msg = "Assigned %s, was %s" % (assigned_cat, actual_cat)
    msg = msg.ljust(40, ' ')
    msg = "%s  %s" % (msg, "✓ " if assigned_cat == actual_cat else " ✗")
    print msg

