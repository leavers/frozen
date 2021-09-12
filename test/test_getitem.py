from frozen import FrozenObject


def test_query_dict():
    person = {
        'name': 'Mike',
        'age': 17,
        'scores': {
            'math': [{
                'name': 'exam1',
                'score': 87,
                'sub_score': {
                    'part 1': 25,
                    'part 2': 22,
                    'part 3': 40
                }
            }, {
                'name': 'exam2',
                'score': 92,
                'sub_score': {
                    'part 1': 30,
                    'part 2': 23,
                    'part 3': 39
                }
            }]
        }
    }

    frozen = FrozenObject(person)
    assert frozen['scores.math.1.sub_score.part 3'].unpack() == 39


def test_query_list():
    people = [{
        'name': 'Anna',
        'age': 16,
        'scores': {
            'writing': 'A',
            'math': 'B+',
            'spanish': 'B'
        }
    }, {
        'name': 'Mike',
        'age': 17,
        'scores': {
            'writing': 'B+',
            'math': 'A',
            'physical': 'C+'
        }
    }, {
        'name': 'Kerry',
        'age': 17,
        'scores': {
            'chemistry': 'B+',
            'math': 'B+',
            'art': 'B+'
        }
    }]

    frozen = FrozenObject(people)
    assert frozen['1.scores.math'].unpack() == 'A'
