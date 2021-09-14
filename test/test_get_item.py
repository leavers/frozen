from frozen import freeze


def test_query_dict():
    person = {
        'name': 'Mike',
        'age': 17,
        'scores': {
            'math': [{
                'name': 'test 1',
                'score': 87,
                'sub_score': {
                    'part 1': 25,
                    'part 2': 22,
                    'part 3': 40
                }
            }, {
                'name': 'test 2',
                'score': 92,
                'sub_score': {
                    'part 1': 30,
                    'part 2': 23,
                    'part 3': 39
                }
            }]
        }
    }

    frozen = freeze(person)
    assert frozen['scores.math.1.sub_score.part 3'].unpack() == 39
    person['scores']['math'][1]['sub_score']['part 3'] = -1
    assert frozen['scores.math.1.sub_score.part 3'].unpack() == 39
    assert frozen.scores.math[1].sub_score['part 3'].unpack() == 39


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

    frozen = freeze(people)
    assert frozen['1.scores.math'] == 'A'
    people[1]['scores']['math'] = 'B'
    assert frozen['1.scores.math'] == 'A'
    assert frozen[1].scores.math == 'A'


def test_query_object():
    class TreeNode:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    t3 = TreeNode(3)
    t4 = TreeNode(4)
    t5 = TreeNode(5)
    t6 = TreeNode(6)
    t1 = TreeNode(1, left=t3, right=t4)
    t2 = TreeNode(2, left=t5, right=t6)
    root = TreeNode(0, left=t1, right=t2)

    frozen = freeze(root)
    assert frozen['val'] == 0
    assert frozen.val == 0
    assert frozen['left.left.val'] == 3
    assert frozen.left.left.val == 3
    assert frozen['left.right.val'] == 4
    assert frozen.left.right.val == 4
    assert frozen['right.left.val'] == 5
    assert frozen.right.left.val == 5
    assert frozen['right.right.val'] == 6
    assert frozen.right.right.val == 6
