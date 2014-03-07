import math

class Histogram:
    def __init__(self, htype, name, data):
        its10 = False
        if "water_bottle_10" in name:
            its10 = True
        self.htype = htype
        self.name = name
        identstring = name.split('.')[0]
        offset = -1
        if name.count('_') == 3:
            offset = 0
            self.category = identstring.split('_')[0]
        elif name.count('_') == 4:
            offset = 1
            self.category = identstring.split('_')[0] + '_' + identstring.split('_')[1]
        else:
            raise Exception('Illegal string to parse: %s' % name)
        self.instance = int(identstring.split('_')[1 + offset])
        self.view = int(identstring.split('_')[2 + offset])
        self.frame = int(identstring.split('_')[3 + offset])
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

def parse_histograms(filename):
    infile = open(filename)
    histograms = []
    for line in infile:
        line = line.rstrip('\n')
        fields = line.split(':')
        histograms.append(Histogram(fields[0], fields[2], fields[3]))
    return histograms


def parse_sorted(filename):
    histograms = parse_histograms(filename)
    categories = {}
    for hist in histograms:
        category = hist.category
        instance = hist.instance
        if not category in categories:
            categories[category] = {}
        if not instance in categories[category]:
            categories[category][instance] = []
        categories[category][instance].append(hist)
        #categories[category][instance].append(0 + len(categories[category][instance]))
    return categories



