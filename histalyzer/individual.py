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

    def __repr__(self):
        return '|' + self.name + '|'

    def __eq__(self, obj):
        if not isinstance(obj, Individual):
            return False
        if self.category != obj.category:
            return False
        if self.instance != obj.instance:
            return False
        if self.view != obj.view:
            return False
        if self.frame != obj.frame:
            return False
        return True

    def __ne__(self, obj):
        return not self == obj

    def __lt__(self, other):
        raise NotImplementedError("Ordering not implemented for Individuals!")
    def __gt__(self, other):
        raise NotImplementedError("Ordering not implemented for Individuals!")
    def __le__(self, other):
        raise NotImplementedError("Ordering not implemented for Individuals!")
    def __ge__(self, other):
        raise NotImplementedError("Ordering not implemented for Individuals!")
