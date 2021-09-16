Frozen Box
==========

``frozen-box`` is a container that:

* makes internal object immutable;
* supports dot notation access.

Example:

.. code-block:: python

    from frozen import freeze

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
    print(frozen['scores.math.1.sub_score.part 3'])  # 39
    print(frozen.scores.math[1].sub_score['part 3'])  # 39