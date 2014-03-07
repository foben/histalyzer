#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import operator
import random
import nearest_neighbor as nn
from histogram import *

def main():
    histograms = parse_sorted(sys.argv[1])
    totalinstances = 0
    training = []
    testing = []

    #Choose testing instance, add all frames
    for category, instancelist in histograms.iteritems():
        if category != 'keyboard':continue
        testing = random.choice( [ instancelist[l] for l in instancelist ] )
        break
    #Add all other data to training:
    for category, instancelist in histograms.iteritems():
        for li in instancelist:
            training.extend(instancelist[li])
    training = list(set(training) - set(testing))
    trainlength = len(training)
    testlength = len(testing)
    totallength = trainlength + testlength
    print '%s testing\n%s training\n%s total' % (testlength, trainlength, totallength)
    nn.nearest_neighbor(training, testing[0:10])

main()
