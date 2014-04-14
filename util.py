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
    #Split from the right, allowing for underscore in category
    name_fields = name.split('_')
    category    = name_fields[0]
    instance    = name_fields[1]
    view        = name_fields[2]
    frame       = name_fields[3]
    hist = Histogram(htype, data_string)
    return metric, category, int(instance), int(view), int(frame), hist

def parse_filelist(file_list, categories="all", instances="all",
        views="all", frames="all", weights=None, dictionary=None ):
    if not dictionary:
        individuals = {}
    else:
        individuals = dictionary

    for filename in file_list:
        individuals = parse_file(filename, categories="all", instances="all",
            views="all", frames="all", weights=weights, dictionary=individuals)
    return individuals




def parse_file(filename, categories="all", instances="all",
        views="all", frames="all", weights=None, dictionary=None ):
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
            newinst = Individual(category, instance, view, frame, weights)
            individuals[category][instance][view][frame] = newinst
        individuals[category][instance][view][frame].add_histogram(metric, hist)

    return individuals
