import sys
import math


class Histogram:
    def __init__(self, htype, name, data):
        self.htype = htype
        self.name = name
        self.category = name.split('_')[0]
        if htype == 'abs':
            self.data = [int(d) for d in data.split(',') ]
        elif htype == 'prob':
            self.data = [float(d) for d in data.split(',') ]
        else:
            raise ValueError('Illegal htype!')
        self.bins = len(self.data)

    def __repr__(self):
        return self.name
def diff_sum_pair((hist1, hist2)):
    return diff_sum(hist1, hist2)

def diff_sum(hist1, hist2):
    if (not (hist1.bins == hist2.bins) ):
        print "Histograms are of different bin-sizes!"
        return
    if (not (hist1.htype == hist2.htype) ):
        print "Histograms are of different htypes!"
        return
    bins = hist1.bins
    distance = 0.0
    for b in range(bins):
        distance += math.fabs(hist1.data[b] - hist2.data[b])
    return distance



def main():
    infile = open(sys.argv[1])
    histograms = []
    for line in infile:
        line = line.rstrip('\n')
        fields = line.split(':')
        histograms.append(Histogram(fields[0], fields[2], fields[3]))
    pairs = [ (h1, h2) for h1 in histograms for h2 in histograms ]
    for pair in pairs:
        #print '%s <> %s: %s' % (pair[0].name, pair[1].name, diff_sum_pair(pair) )
        print '%s <> %s: %s' % (pair[0].category, pair[1].category, diff_sum_pair(pair) )
        


main()
