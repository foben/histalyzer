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
        #print '%s      --> %s' % (sorted_categories, assigned_cat)
        ######################################

        ##OLD approach
        #categories = {}
        #for n in range(neighbors):
        #    neighbor = slist[n]
        #    cat = neighbor.category
        #    if cat in categories:
        #        categories[cat] += 1
        #    else:
        #        categories[cat] = 1
        #sorted_categories = sorted(categories.iteritems(), key=operator.itemgetter(1), reverse=True)
        #print sorted_categories
        #assigned_cat = sorted_categories[0][0]
        #######################################

        actual_cat = test.category
        marker = ""
        if (assigned_cat == actual_cat):
            correct_count += 1
        else:
            failure_count += 1
        #print_line(assigned_cat, actual_cat)
        if running_count % 25 == 0:
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

