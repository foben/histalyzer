from histalyzer import util

def test_test_not_in_training():
    weights = {
            'color': (0,[] ),
            'depth': (1,[ ('dd2',1)  ] )
            }

    input_data = util.parse_file('/home/ope/dev/python/histalyzer/data/dd2',
            weights=weights)
    train_data, test_data = util.get_datasets('apple', 1, input_data)
    for tri in test_data:
        assert tri not in train_data


