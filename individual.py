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
        self.weights = { 
                'color' : { 'cb64': 1, 'cg64': 1, 'cr64': 1},
                'depth': { 'dd3': 2, 'dd2': 6, 'da3': 2}
                }

    def add_histogram(self, metric, histogram):
        self.histograms[metric] = histogram;

    def get_distance(self, other_instance):
        #dist_d3 = histogram.diff_sum(self.histograms['dd3'], other_instance.histograms['dd3'])
        #dist_d2 = histogram.diff_sum(self.histograms['dd2'], other_instance.histograms['dd2'])
        #dist_a3 = histogram.diff_sum(self.histograms['da3'], other_instance.histograms['da3'])
        #dist_blue = histogram.diff_sum(self.histograms['cb64'], other_instance.histograms['cb64'])
        #dist_green = histogram.diff_sum(self.histograms['cg64'], other_instance.histograms['cg64'])
        #dist_red = histogram.diff_sum(self.histograms['cr64'], other_instance.histograms['cr64'])
        dist_ccol = histogram.diff_sum(self.histograms['ccol'], other_instance.histograms['ccol'])
        #depthdist = dist_d3*0.2 + dist_d2 * 0.6 + dist_a3*0.2
        #rgbdist = (dist_blue + dist_green + dist_red) / float(3)
        #return 0.5 * depthdist + 0.5 * rgbdist
        return dist_ccol

    def __repr__(self):
        return '[|' + self.name + '|]'

