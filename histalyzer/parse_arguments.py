import logging
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
    logging.info("Testing Categories: {}".format(categories))
    logging.info("SET_PARTIAL: {}".format(SET_PARTIAL))
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
        'run88': ('_run88',RUN88),
	'run161': ('_run161',RUN161),
	'run162': ('_run162',RUN162),
	'run163': ('_run163',RUN163),
	'run164': ('_run164',RUN164),
	'run165': ('_run165',RUN165),
	'run166': ('_run166',RUN166),
	'run167': ('_run167',RUN167),
	'run168': ('_run168',RUN168),
	'run169': ('_run169',RUN169),
	'run1610': ('_run1610',RUN1610),
	'run1611': ('_run1611',RUN1611),
	'run1612': ('_run1612',RUN1612),
	'run1613': ('_run1613',RUN1613),
	'run1614': ('_run1614',RUN1614),
	'run1615': ('_run1615',RUN1615),
	'run1616': ('_run1616',RUN1616)
        }
