'''
Created on 28.04.2017

@author: Mr. Jones
'''
import unittest
from slimit.parser import Parser
from slimit.visitors.scopevisitor import UnusedObjectsVisitor


def decorator(cls):
    def make_test_function(input, expected):

        def test_func(self):
            self.assertUnusedObjects(input, expected)

        return test_func

    for index, (input, expected) in enumerate(cls.TEST_CASES):
        func = make_test_function(input, expected)
        setattr(cls, 'test_case_%d' % index, func)

    return cls


@decorator
class UnusedObjectsTestCase(unittest.TestCase):

    def assertUnusedObjects(self, source, expected):
        parser = Parser()
        tree = parser.parse(source)
        uvisit = UnusedObjectsVisitor()
        uvisit.do(tree)
        self.maxDiff = None
        self.assertSequenceEqual(tree.to_ecma(), expected)

    TEST_CASES = [
        ('var a = 0;', ''),
        ('var a = 0;if(a){var b =0;}','var a = 0;\nif (a) {\n\n}')
        ]

