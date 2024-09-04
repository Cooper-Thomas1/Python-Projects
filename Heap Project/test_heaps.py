#! /usr/bin/env python3

import unittest

import heaps
from heaps import *

import inspect
import warnings
from random import Random

SEED = 2200
RUNS = 10
SIZE = 1000
RANGE = 1000


class TestHeaps(unittest.TestCase):
    def setUp(self):
        source = inspect.getsource(heaps)
        redflags = [
            ('import', 'It looks like you are using imports, which is not allowed!'),
            ('.sort(', 'It looks like you are using a builtin sorting method, which is not allowed!'),
            ('sorted(', 'It looks like you are using a builtin sorting method, which is not allowed!'),
        ]
        for redflag, warning in redflags:
            if redflag in source:
                warnings.warn(warning)

    def __test_sorting(self, sort, name, key=None, reverse=False):
        random = Random(SEED)
        for i in range(RUNS):
            xs = [random.randint(0, RANGE) for _ in range(SIZE)]
            expected = sorted(xs.copy(), key=key, reverse=reverse)
            received = sort(xs.copy(), key=key, reverse=reverse)
            msg = f'heapsort failed on run {i} with xs={xs}'
            self.assertEqual(received, expected, msg=msg)

    def test_heapsort(self):
        self.__test_sorting(heapsort, 'heapsort')

    def test_heapsort_key(self):
        def key(x):
            q, r = divmod(x, 10)
            return (r, q)
        self.__test_sorting(heapsort, 'heapsort(key=moddiv)', key=key)

    def test_heapsort_reverse(self):
        self.__test_sorting(heapsort, 'heapsort(reverse=True)', reverse=True)

    def test_example(self):
        heap = Heap([6, 16, 4, 12, 15, 20, 25, 10], reverse=True)
        self.assertEqual(heap.peek(), 25)
        heap.push(30)
        self.assertEqual(heap.pop(), 30)
        self.assertEqual(heap.pop(), 25)
        self.assertEqual(heap.pop(), 20)
        self.assertEqual(heap.peek(), 16)
        heap.push(21)
        heap.push(16)
        self.assertEqual(heap.pop(), 21)
        self.assertEqual(heap.pop(), 16)
        self.assertEqual(heap.pop(), 16)
        self.assertEqual(heap.pop(), 15)


if __name__ == '__main__':
    unittest.main()
