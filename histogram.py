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

    def __key(self):
        return (self.htype, self.category, self.category, self.instance, self.view, self.frame)

    def __hash__(self):
        return hash(self.__key())

    def compare(self, other):
        if self.category < other.category:
            return -1
        elif self.category > other.category:
            return 1

        if self.instance < other.instance:
            return -1
        elif self.instance > other.instance:
            return 1

        if self.view < other.view:
            return -1
        elif self.view > other.view:
            return 1

        if self.frame < other.frame:
            return -1
        elif self.frame > other.frame:
            return 1

        return 0

    def __lt__(self, other):
        return self.compare(other) < 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __ne__(self, other):
        return self.compare(other) != 0
          
    def __gt__(self, other):
        return self.compare(other) > 0
                
    def __ge__(self, other):
        return self.compare(other) >= 0

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
        categories = add_to_dict(categories, hist)
    #    category = hist.category
    #    instance = hist.instance
    #    if not category in categories:
    #        categories[category] = {}
    #    if not instance in categories[category]:
    #        categories[category][instance] = []
    #    categories[category][instance].append(hist)
    #    #categories[category][instance].append(0 + len(categories[category][instance]))
    return categories

def parse_selected(filename, categories="all", instances="all",
        views="all", frames="all" ):
    print "parsing selection"
    check_categories = not categories == 'all'
    check_instances = not instances == 'all'
    check_views = not views == 'all'
    check_frames = not frames == 'all'

    if check_categories:
        assert (isinstance(categories, list)),\
                'Must be "all" or list: %s!' % categories
        assert all(isinstance(n, str) for n in categories),\
                'Must be a list of strings: %s' % categories

    if check_instances:
        assert isinstance(instances, list),\
                'Must be "all" or list: %s' % instances
        assert all(isinstance(n, int) for n in instances),\
                'Must be a list of ints: %s' % instances

    if check_views:
        assert isinstance(views, list),\
                'Must be "all" or list: %s' % views
        assert all(isinstance(n, int) for n in views),\
                'Must be a list of ints: %s' % views

    if check_frames:
        assert isinstance(frames, list),\
                'Must be "all" or list: %s' % frames
        assert all(isinstance(n, int) for n in frames),\
                'Must be a list of ints: %s' % frames

    print "assertions passed!"

    histograms = parse_histograms(filename)
    category_dict = {}
    for hist in histograms:
        if check_categories and not hist.category in categories: continue
        if check_instances and not hist.instance in instances: continue 
        if check_views and not hist.view in views: continue
        if check_frames and not hist.frame in frames: continue
        category_dict = add_to_dict(category_dict, hist)
    return category_dict


def add_to_dict(categories_dict, hist):
    categories = categories_dict
    category = hist.category
    instance = hist.instance
    if not category in categories:
        categories[category] = {}
    if not instance in categories[category]:
        categories[category][instance] = []
    categories[category][instance].append(hist)
    return categories

def get_list_from_hdict(hdict):
    result = []
    for cat, ilist in hdict.iteritems():
        for i in ilist:
            for h in hdict[cat][i]:
                result.append(h)
    return result


