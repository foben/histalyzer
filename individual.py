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
        #dist_d3 = histogram.diff_sum(self.histograms['depth_d3-1k'], other_instance.histograms['depth_d3-1k'])
        #dist_d2 = histogram.diff_sum(self.histograms['depth_d2-1k'], other_instance.histograms['depth_d2-1k'])
        #dist_a3 = histogram.diff_sum(self.histograms['depth_a3-1k'], other_instance.histograms['depth_a3-1k'])
        #dist_blue = histogram.diff_sum(self.histograms['rgb_blue64'], other_instance.histograms['rgb_blue64'])
        #dist_green = histogram.diff_sum(self.histograms['rgb_green64'], other_instance.histograms['rgb_green64'])
        #dist_red = histogram.diff_sum(self.histograms['rgb_red64'], other_instance.histograms['rgb_red64'])
        #depthdist = dist_d3*0.2 + dist_d2 * 0.6 + dist_a3*0.2
        #rgbdist = (dist_blue + dist_green + dist_red) / float(3)
        #return 0.5 * depthdist + 0.5 * rgbdist
        dist_a3 = histogram.diff_sum(self.histograms['depth_a3-1k'], other_instance.histograms['depth_a3-1k'])
        return dist_a3

    def __repr__(self):
        return '[|' + self.name + '|]'

