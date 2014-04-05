import math

class Histogram:
    def __init__(self, htype, data):
        self.htype = htype
        if htype == 'abs':
            self.data = [int(d) for d in data.split(',') ]
        elif htype == 'prob':
            self.data = [float(d) for d in data.split(',') ]
        else:
            raise ValueError('Illegal htype!')
        self.bins = len(self.data)

def diff_sum_pair((hist1, hist2)):
    return diff_sum(hist1, hist2)

def diff_sum(hist1, hist2):
    if (not (hist1.bins == hist2.bins) ):
        raise ValueError('Histograms are of different bin-sizes!')
    if (not (hist1.htype == hist2.htype) ):
        raise ValueError('Histograms are of different bin-sizes!')
    bins = hist1.bins
    distance = 0.0
    for b in range(bins):
        distance += math.fabs(hist1.data[b] - hist2.data[b])
    return distance

