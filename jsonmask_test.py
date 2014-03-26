import unittest
import jsonmask

fixture = {
    "kind": "plus#activity",
    "etag": "\"DOKFJGXi7L9ogpHc3dzouWOBEEg/ZiaatWNPRL3cQ-I-WbeQPR_yVa0\"",
    "title": "Congratulations! You have successfully fetched an explicit public activity. The attached video is your...",
    "published": "2011-09-08T21:17:41.232Z",
    "updated": "2011-10-04T17:25:26.000Z",
    "id": "z12gtjhq3qn2xxl2o224exwiqruvtda0i",
    "url": "https://plus.google.com/102817283354809142195/posts/F97fqZwJESL",
    "actor": {
        "id": "102817283354809142195",
        "displayName": "Jenny Murphy",
        "url": "https://plus.google.com/102817283354809142195",
        "image": {
            "url": "https://lh4.googleusercontent.com/-yth5HLY4Qi4/AAAAAAAAAAI/AAAAAAAAPVs/fAq4PVOVBdc/photo.jpg?sz=50"
        }
    },
    "verb": "post",
    "object": {
        "objectType": "note",
        "content": "Congratulations! You have successfully fetched an explicit public activity. The attached video is your reward. :)",
        "url": "https://plus.google.com/102817283354809142195/posts/F97fqZwJESL",
        "replies": {
            "totalItems": 16,
            "selfLink": "https://www.googleapis.com/plus/v1/activities/z12gtjhq3qn2xxl2o224exwiqruvtda0i/comments"
        },
        "plusoners": {
            "totalItems": 44,
            "selfLink": "https://www.googleapis.com/plus/v1/activities/z12gtjhq3qn2xxl2o224exwiqruvtda0i/people/plusoners"
        },
        "resharers": {
            "totalItems": 1,
            "selfLink": "https://www.googleapis.com/plus/v1/activities/z12gtjhq3qn2xxl2o224exwiqruvtda0i/people/resharers"
        },
        "attachments": [{
            "objectType": "video",
            "displayName": "Rick Astley - Never Gonna Give You Up",
            "content": "Music video by Rick Astley performing Never Gonna Give You Up. YouTube view counts pre-VEVO: 2,573,462 (C) 1987 PWL",
            "url": "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "image": {
                "url": "https://lh3.googleusercontent.com/proxy/ex1bQ9_TpVClePgZxFmCPVxYeJUHW5dixt53FLmup-q44pd1mwO6rPIPti6tDWbjitBclMm5Ou595xPEMKq2b8Qu3mQ_TzX0kOqksE8o1w=w506-h284-n",
                "type": "image/jpeg",
                "height": 284,
                "width": 506
            },
            "embed": {
                "url": "http://www.youtube.com/v/dQw4w9WgXcQ&hl=en&fs=1&autoplay=1",
                "type": "application/x-shockwave-flash"
            }
        }]
    },
    "provider": {
        "title": "Google+"
    },
    "access": {
        "kind": "plus#acl",
        "description": "Public",
        "items": [{
            "type": "public"
        }]
    }
}


filter_tests = [{
    "m": 'a', "o": None, "e": None
}, {
    "m": 'a', "o": {"b": 1}, "e": None
}, {
    "m": 'a', "o": [{"b": 1}], "e": None
}, {
    "m": None, "o": {"a": 1}, "e": {"a": 1}
}, {
    "m": '', "o": {"a": 1}, "e": {"a": 1}
}, {
    "m": 'a', "o": {"a": 1, "b": 1}, "e": {"a": 1}
}, {
    "m": 'notEmptyStr', "o": {"notEmptyStr": ''}, "e": {"notEmptyStr": ''}
}, {
    "m": 'notEmptyNum', "o": {"notEmptyNum": 0}, "e": {"notEmptyNum": 0}
}, {
    "m": 'a,b', "o": {"a": 1, "b": 1, "c": 1}, "e": {"a": 1, "b": 1}
}, {
    "m": 'obj/s', "o": {"obj": {"s": 1, "t": 2}, "b": 1}, "e": {"obj": {"s": 1}}
}, {
    "m": 'arr/s', "o": {"arr": [{"s": 1, "t": 2}, {"s": 2, "t": 3}], "b": 1}, "e": {"arr": [{"s": 1}, {"s": 2}]}
}, {
    "m": 'a/s/g,b', "o": {"a": {"s": {"g": 1, "z": 1}}, "t": 2, "b": 1}, "e": {"a": {"s": {"g": 1}}, "b": 1}
}, {
    "m": 'a/*/g', "o": {"a": {"s": {"g": 3}, "t": {"g": 4}, "u": {"z": 1}}, "b": 1}, "e": {"a": {"s": {"g": 3}, "t": {"g": 4}}}
}, {
    "m": 'a/*', "o": {"a": {"s": {"g": 3}, "t": {"g": 4}, "u": {"z": 1}}, "b": 3}, "e": {"a": {"s": {"g": 3}, "t": {"g": 4}, "u": {"z": 1}}}
}, {
    "m": 'a(g)', "o": {"a": [{"g": 1, "d": 2}, {"g": 2, "d": 3}]}, "e": {"a": [{"g": 1}, {"g": 2}]}
}, {
    "m": 'a,c', "o": {"a": [], "c": {}}, "e": {"a": [], "c": {}}
}, {
    "m": 'b(d/*/z)', "o": {"b": [{"d": {"g": {"z": 22}, "b": 34}}]}, "e": {"b": [{"d": {"g": {"z": 22}}}]
                                                                           }
}, {
    "m": 'url,obj(url,a/url)', "o": {"url": 1, "id": '1', "obj": {"url": 'h', "a": [{"url": 1, "z": 2}], "c": 3}}, "e": {"url": 1, "obj": {"url": 'h', "a": [{"url": 1}]}}
}, {
    "m": 'kind', "o": fixture, "e": {"kind": 'plus#activity'}
}, {
    "m": 'object(objectType)', "o": fixture, "e": {"object": {"objectType": 'note'}}
}, {
    "m": 'url,object(content,attachments/url)', "o": fixture, "e": {
        "url": 'https://plus.google.com/102817283354809142195/posts/F97fqZwJESL', "object": {
            "content": 'Congratulations! You have successfully fetched an explicit public activity. The attached video is your reward. :)', "attachments": [{"url": 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'}]
        }
    }
}, {
    "m": 'i', "o": [{"i": 1, "o": 2}, {"i": 2, "o": 2}], "e": [{"i": 1}, {"i": 2}]
}]

compiler_tests = {
    'a': {"a": {"type": 'object'}}, 'a,b,c': {
        "a": {"type": 'object'}, "b": {"type": 'object'}, "c": {"type": 'object'}
    }, 'a/*/c': {
        "a": {"type": 'object', "properties": {
              '*': {"type": 'object', "properties": {
                    "c": {"type": 'object'}
                    }}
              }}
    }, 'a,b(d/*/g,b),c': {
        "a": {"type": 'object'}, "b": {"type": 'array', "properties": {
            "d": {"type": 'object', "properties": {
                  '*': {"type": 'object', "properties": {
                  "g": {"type": 'object'}
                  }}
                  }}, "b": {"type": 'object'}
        }}, "c": {"type": 'object'}
    }
}


# Filter tests
filter_test_compiled_mask = {
    "a": {"type": 'object'},
    "b": {
    "type": 'array',
    "properties": {
        "d": {
        "type": 'object',
        "properties": {
            '*': {
            "type": 'object',
            "properties": {
                "z": {"type": 'object'}
            }
            }
        }
        },
        "b": {
        "type": 'array',
        "properties": {
            "g": {"type": 'object'}
        }
        }
    }
    },
    "c": {"type": 'object'}
}

filter_test_object = {
    "a": 11,
    "n": 00,
    "b": [{
    "d": {"g": {"z": 22}, "b": 34, "c": {"a": 32}},
    "b": [{"z": 33}],
    "k": 99
    }],
    "c": 44,
    "g": 99
}

filter_test_expected = {
    "a": 11,
    "b": [{
    "d": {
    "g": {
        "z": 22
    }
    }
    }],
    "c": 44
}

class TestCase(unittest.TestCase):

    def test_filter(self):
        actual = jsonmask.apply_mask(filter_test_object, filter_test_compiled_mask)
        self.assertEqual(filter_test_expected, actual)

def make_test(test):
    e = test['e']
    o = test['o']
    m = test['m']

    def _test(self):
        self.assertEqual(e, jsonmask.Mask(m)(o))
    _test.__doc__ = 'm = %s   original = %s   expected = %s\n' % (m, o, e)
    return _test


def make_compiler_test(sel, expected_compiled):
    def _test(self):
        self.assertEqual(expected_compiled, jsonmask.compile_mask(sel))
    _test.__doc__ = 'sel = %s   expected = %s' % (sel, expected_compiled)
    return _test

for i, test in enumerate(filter_tests):
    setattr(TestCase, 'test_filter_%s' % i, make_test(test))

for i, (sel, expected) in enumerate(compiler_tests.items()):
    setattr(TestCase, 'test_compiler_%s' %
            i, make_compiler_test(sel, expected))

if __name__ == '__main__':
    unittest.main()
