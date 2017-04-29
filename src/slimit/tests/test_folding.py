'''
Created on 28.04.2017

@author: Mr. Jones
'''
import unittest
from slimit.parser import Parser
from slimit.visitors import foldingvisitor


def decorator(cls):
    def make_test_function(input, expected):

        def test_func(self):
            self.assertFoldingObjects(input, expected)

        return test_func

    for index, (input, expected) in enumerate(cls.TEST_CASES):
        func = make_test_function(input, expected)
        setattr(cls, 'test_case_%d' % index, func)

    return cls


@decorator
class FoldingTestCase(unittest.TestCase):

    def assertFoldingObjects(self, source, expected):
        parser = Parser()
        tree = parser.parse(source)
        uvisit = foldingvisitor.FoldingVisitor()
        uvisit.do(tree)
        print(tree.to_ecma())
        self.maxDiff = None
        self.assertSequenceEqual(tree.to_ecma(), expected)

    TEST_CASES = [
        ('var a = 3-2;','var a = 1;'),
        ('var a = 3-2+5-1+7;','var a = 12;')
        ]

