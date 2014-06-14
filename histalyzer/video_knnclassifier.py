#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import operator
import time
import datetime
import logging
#import threading
from multiprocessing import Process, Lock, Queue
from histogram import *
from collections import Counter, OrderedDict
from random import randint

class VideoKNNClassifier:

    def __init__(self, weights, k=5, classes=None):
        self.k = k
        self.confusion_matrix = OrderedDict([ (actual,
            OrderedDict([ (predicted,0) for predicted in classes] ))
            for actual in classes ])
        self.classes = classes
        self.cweight = weights['color'][0]
        self.dweight = weights['depth'][0]
        self.conflock = Lock()
	self.number = randint(1,5000)

        lsum = lambda s, (m, w): s + w
        if self.cweight:
            self.color_weights = weights['color'][1]
            self.sum_color_weights = reduce(lsum, self.color_weights, 0)
        if self.dweight:
            self.depth_weights = weights['depth'][1]
            self.sum_depth_weights = reduce(lsum, self.depth_weights, 0)
        self.sum_weights = self.cweight + self.dweight

        self.dist_func = diff_sum

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
        if not testing_data:
            return
        actual_cat = testing_data[0][0].category
        current_instance = testing_data[0][0].instance
        logging.info("Starting {} {}".format(actual_cat, current_instance))

        strt = time.time()
        for trseq in testing_data:
            assigneds = []
            for test in trseq:                                                        
                sortkey = lambda tr: self.get_distance(test, tr)
                slist = sorted( training_data, key=sortkey )
                assigneds.append(self.get_class_label(slist))
            c = Counter(assigneds)
            commons = c.most_common()
            predicted = commons[0][0]
            self.add_to_cm(actual_cat, predicted)

        end = time.time()
        delt = datetime.timedelta(seconds=int(end - strt))
        logging.info("Instance took {}".format(delt))

        #thrds = []
        #plength = len(testing_data)/4 + 1
        #q = Queue()
        #strt = time.time()
        #for lit in chunks(testing_data, plength):
        #    t = Process(target=mproc, args=(training_data, lit, self,q,))
        #    t.start()
        #    thrds.append(t)
        #for t in thrds:
        #    t.join()
        #q.put('DONE')
        #while True:
        #    item = q.get()
        #    if item == 'DONE':
        #        break
        #    self.confusion_matrix[item[0]][item[1]] += 1
        #
        #end = time.time()
        #delt = datetime.timedelta(seconds=int(end - strt))
        #logging.info("Instance took {}".format(delt))

    def add_to_cm(self, actual, assigned):
        self.conflock.acquire()
        self.confusion_matrix[actual][assigned] += 1
        self.conflock.release()

    def calc_remaining_time(self, start, total, current):
        percentage = float(current) / total
        ptime = time.clock() - start
        rtime = ptime / percentage * (1-percentage)
        remaining = datetime.timedelta(seconds=int(rtime) )
        return remaining

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

    def get_TP(self, cat):
        return self.confusion_matrix[cat][cat]

    def get_FP(self, cat):
        fp = 0
        for act, pred in self.confusion_matrix.iteritems():
            fp += pred[cat]
        fp -= self.get_TP(cat)
        return fp

    def get_FN(self, cat):
        fn = reduce(lambda s, x: s+x,
                [v for k, v in self.confusion_matrix[cat].iteritems() if k != cat])
        return fn

    def get_TN(self, cat):
        return self.get_total_classified() - \
           self.get_TP(cat) - self.get_FP(cat) - self.get_FN(cat)

    def get_precision(self, cat):
        tp = float(self.get_TP(cat))
        fp = float(self.get_FP(cat))
        try:
            return tp / (tp + fp)
        except ZeroDivisionError:
            return 0

    def get_recall(self, cat):
        tp = float(self.get_TP(cat))
        fn = float(self.get_FN(cat))
        try: 
            return tp / (tp + fn)
        except ZeroDivisionError:
            return 0

    def get_fone(self, cat):
        pr = self.get_precision(cat)
        rc = self.get_recall(cat)
        try:
            return (2*pr*rc)/(pr+rc)
        except ZeroDivisionError:
            return 0

    def get_overall_scores(self):
        pr = reduce(lambda s, x: s+x,
                [ self.get_precision(clazz) for clazz in self.classes]
                )/ float(len(self.classes))
        rc = reduce(lambda s, x: s+x,
                [ self.get_recall(clazz) for clazz in self.classes]
                )/ float(len(self.classes))
        fone = (2*pr*rc)/(pr+rc)
        return pr, rc, fone

    
    def get_total_classified(self):
        return reduce(lambda s, x: s+x,
                [self.confusion_matrix[act][pred]
                    for act in self.confusion_matrix.iterkeys()
                    for pred in self.confusion_matrix[act].iterkeys()
                    ])

def mproc(trdata, testdata, classif, queue):
    for test in testdata:
        sortkey = lambda tr: classif.get_distance(test, tr)
        slist = sorted( trdata, key=sortkey )
        assigned_cat = classif.get_class_label(slist)
        actual_cat = test.category
        queue.put((actual_cat, assigned_cat))
    queue.close()

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
