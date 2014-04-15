#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import operator
import time
import datetime
import logging
from histogram import *

def nearest_neighbor(training_data, testing_data, neighbors=3):
    total_count = len(testing_data) 
    running_count = 0
    failure_count = 0
    correct_count = 0

    testing_categories = set()
    testing_instances = set()

    for hist in testing_data:
        testing_categories.add(hist.category)
        testing_instances.add(hist.instance)
    assert (len(testing_categories) == 1), "Different Categories in testing data!"
    assert (len(testing_instances) == 1), "Different Instances in testing data!"
    logging.info("=== %s %s ===", list(testing_categories)[0], list(testing_instances)[0])


    start_time = time.clock()
    for test in testing_data:
        running_count += 1
        slist = sorted( training_data, key=lambda tr: test.get_distance(tr) )

        ##NEW approach
        sorted_categories = []
        for n in range(neighbors):
            exists = False
            cat = slist[n].category
            for i in range(len(sorted_categories)):
                if sorted_categories[i][0] == cat:
                    exists = True
                    sorted_categories[i][1] += 1
            if not exists:
                sorted_categories.append([cat, 1])

        maxn = 0
        maxcat = ''
        for i in range(len(sorted_categories)):
            if sorted_categories[i][1] > maxn:
                maxn = sorted_categories[i][1]
                maxcat = sorted_categories[i][0]
        assigned_cat = maxcat 
        actual_cat = test.category
        marker = ""
        if (assigned_cat == actual_cat):
            correct_count += 1
            #print "%s, %s, %s, %s, yes" % (test.category, test.instance, test.view, test.frame )
        else:
            failure_count += 1
            #print "%s, %s, %s, %s, no" % (test.category, test.instance, test.view, test.frame )
        #print_line(assigned_cat, actual_cat)
        if running_count % 25 == 0:
            remaining = calc_remaining_time(start_time, total_count, running_count)
            logging.info("ETA %s %s: %s", test.category, test.instance, remaining)

    correct_percentage = float(correct_count)/ total_count * 100
    return correct_percentage, total_count, correct_count

def calc_remaining_time(start, total, current):
    percentage = float(current) / total
    ptime = time.clock() - start
    rtime = ptime / percentage * (1-percentage)
    remaining = datetime.timedelta(seconds=int(rtime) )
    return remaining

def print_line(assigned_cat, actual_cat):
    msg = "Assigned %s, was %s" % (assigned_cat, actual_cat)
    msg = msg.ljust(40, ' ')
    msg = "%s  %s" % (msg, "✓ " if assigned_cat == actual_cat else " ✗")
    print msg
