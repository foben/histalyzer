import histogram
import logging
from histogram import Histogram
from individual import Individual

def split_histogram_line(line):
    fields      = line.split(':')
    metric      = fields[0]
    htype       = fields[1]
    name        = fields[2]
    data_string = fields[3]
    name_fields = name.split('_')
    category    = name_fields[0]
    instance    = name_fields[1]
    view        = name_fields[2]
    frame       = name_fields[3]
    hist = Histogram(htype, data_string)
    return metric, category, int(instance), int(view), int(frame), hist

def parse_file(filename, categories="all", instances="all",
        views="all", frames="all", dictionary=None ):
    if not dictionary:
        individuals = {}
    else:
        individuals = dictionary

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

    logging.info("Parsing '%s'", filename)
    f = open(filename)
    contents = f.read().splitlines()
    for line in contents:
        metric, category, instance, view, frame, hist = split_histogram_line(line)
        if check_categories and not category in categories: continue
        if check_instances and not instance in instances: continue 
        if check_views and not view in views: continue
        if check_frames and not frame in frames: continue

        if not category in individuals:
            individuals[category] = dict()
        if not instance in individuals[category]:
            individuals[category][instance] = dict()
        if not view in individuals[category][instance]:
            individuals[category][instance][view] = dict()
        if not frame in individuals[category][instance][view]:
            newinst = Individual(category, instance, view, frame)
            individuals[category][instance][view][frame] = newinst
        individuals[category][instance][view][frame].add_histogram(metric, hist)

    return individuals


def get_datasets(for_category, for_instance, input_data, tr_frames=None):
    all_frames_for_training = True if not tr_frames else False
    #Use all instances, views and frames for testing:
    testdata = [ input_data[for_category][for_instance][v][f] \
            for v in input_data[for_category][for_instance].keys() \
            for f in input_data[for_category][for_instance][v].keys() ]

    #Use only chosen frames for training.
    #Discard any frames from the instance to test.
    traindata = [ input_data[c][i][v][f] \
        for c in input_data.keys() \
        for i in input_data[c].keys() \
            if (c != for_category or (c == for_category and i != for_instance))
        for v in input_data[c][i].keys() \
        for f in input_data[c][i][v].keys()
            if (all_frames_for_training or f in tr_frames)]
    return traindata, testdata

def get_video_datasets(for_category, for_instance, input_data, tr_frames=None):
    all_frames_for_training = True if not tr_frames else False

    ##Construct list of video-sequence frames:
    seqlist = []
    for frlist in [xrange(1,26), xrange(26,51), xrange(51,76), xrange(76,101)]:
        for view in [1, 2, 4]:
            clist = []
            for frame in frlist:
                try:
                    clist.append(input_data[for_category][for_instance][view][frame])
                except KeyError as ke:
                    pass
                    #print "{} {} failed with: {}".format(for_category, for_instance, ke.args)
            if len(clist) < 15:
                continue
            seqlist.append(sorted(clist, key=lambda ind: ind.frame))

    #Use only chosen frames for training.
    #Discard any frames from the instance to test.
    traindata = [ input_data[c][i][v][f] \
        for c in input_data.keys() \
        for i in input_data[c].keys() \
            if (c != for_category or (c == for_category and i != for_instance))
        for v in input_data[c][i].keys() \
        for f in input_data[c][i][v].keys()
            if (all_frames_for_training or f in tr_frames)]
    return traindata, seqlist
