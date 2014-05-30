from defs import *

def parse_categories(categorylist):
    SET_PARTIAL = None
    ##Single category, run or all specified:
    if len(categorylist) == 1:
        cat = categorylist[0]
        if cat== 'all':
            categories = ALL_CATEGORIES
        elif cat in runmap:
            SET_PARTIAL, categories = runmap[cat]
        else:
            categories = categorylist
            SET_PARTIAL = '_' + categorylist[0]
    ##List of categories specified:
    else:
        categories = categorylist
        SET_PARTIAL = '_' + '_'.join(categories)
    print "Cats: {} \n SET_PARTIAL: {}".format(categories, SET_PARTIAL)
    return categories, SET_PARTIAL

runmap = {
        'run1': ('_run1', RUN1),
        'run2': ('_run2', RUN2),
        'run3': ('_run3', RUN3),
        'run4': ('_run4', RUN4),
        'run12': ('_run12', RUN12),
        'run34': ('_run34', RUN34),
        'run81': ('_run81',RUN81),
        'run82': ('_run82',RUN82),
        'run83': ('_run83',RUN83),
        'run84': ('_run84',RUN84),
        'run85': ('_run85',RUN85),
        'run86': ('_run86',RUN86),
        'run87': ('_run87',RUN87),
        'run88': ('_run88',RUN88)
        }
