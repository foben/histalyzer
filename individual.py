from histogram import *
import histogram

class Individual:
    def __init__(self, category, instance, view, frame):
        self.category = category
        self.instance = instance
        self.view = view
        self.frame = frame
        self.name = '%s_%s_%s_%s' % (self.category, self.instance, self.view, self.frame)
        self.histograms = {}

    def add_histogram(self, metric, histogram):
        self.histograms[metric] = histogram;

    def get_distance(self, other_instance):
        dist_d3 = histogram.diff_sum(self.histograms['d3'], other_instance.histograms['d3'])
        dist_d2 = histogram.diff_sum(self.histograms['d2'], other_instance.histograms['d2'])
        dist_a3 = histogram.diff_sum(self.histograms['a3'], other_instance.histograms['a3'])
        return dist_d3*0.2 + dist_d2 * 0.6 + dist_a3*0.2

    def __repr__(self):
        return '[|' + self.name + '|]'

