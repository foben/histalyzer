from histogram import *
import histogram

class Individual:
    def __init__(self, category, instance, view, frame, weights):
        self.category = category
        self.instance = instance
        self.view = view
        self.frame = frame
        self.name = '%s_%s_%s_%s' % (self.category, self.instance, self.view, self.frame)
        self.histograms = {}
        self.weight_color = weights['color'][0]
        lsum = lambda s, (m, w): s + w
        if self.weight_color:
            self.weights_color = weights['color'][1]
            self.sum_weights_color = reduce(lsum, self.weights_color, 0)
        self.weight_depth = weights['depth'][0]
        if self.weight_depth:
            self.weights_depth = weights['depth'][1]
            self.sum_weights_depth = reduce(lsum, self.weights_depth, 0)
        self.sum_weights = self.weight_depth + self.weight_color

    def add_histogram(self, metric, histogram):
        self.histograms[metric] = histogram;

    def get_distance(self, other_instance):
        lweight = lambda s, (m, w): s + w*histogram.diff_sum(self.histograms[m],
                other_instance.histograms[m])
        if self.weight_color:
            coldiff = reduce(lweight , self.weights_color, 0) * self.weight_color
            coldiff /= self.sum_weights_color
        else:
            coldiff = 0

        if self.weight_depth:
            depthdiff = reduce(lweight , self.weights_depth, 0) * self.weight_depth
            depthdiff /= self.sum_weights_depth
        else:
            depthdiff = 0

        return( (coldiff + depthdiff) / (self.weight_color + self.weight_depth))



    def __repr__(self):
        return '[|' + self.name + '|]'

