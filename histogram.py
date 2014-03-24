import math

class Histogram:
    def __init__(self, htype, data, sample_size=None):
        self.htype = htype
        self.sample_size = sample_size
        if htype == 'abs':
            self.data = [int(d) for d in data.split(',') ]
        elif htype == 'prob':
            self.data = [float(d) for d in data.split(',') ]
        else:
            raise ValueError('Illegal htype!')
        self.bins = len(self.data)

    #def __repr__(self):
    #    return self.name

    #def __key(self):
    #    return (self.htype, self.category, self.category, self.instance, self.view, self.frame)

    #def __hash__(self):
    #    return hash(self.__key())

    #def compare(self, other):
    #    if self.category < other.category:
    #        return -1
    #    elif self.category > other.category:
    #        return 1

    #    if self.instance < other.instance:
    #        return -1
    #    elif self.instance > other.instance:
    #        return 1

    #    if self.view < other.view:
    #        return -1
    #    elif self.view > other.view:
    #        return 1

    #    if self.frame < other.frame:
    #        return -1
    #    elif self.frame > other.frame:
    #        return 1

    #    return 0

    #def __lt__(self, other):
    #    return self.compare(other) < 0

    #def __le__(self, other):
    #    return self.compare(other) <= 0

    #def __eq__(self, other):
    #    return self.compare(other) == 0

    #def __ne__(self, other):
    #    return self.compare(other) != 0
    #      
    #def __gt__(self, other):
    #    return self.compare(other) > 0
    #            
    #def __ge__(self, other):
    #    return self.compare(other) >= 0

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

