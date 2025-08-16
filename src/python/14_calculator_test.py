#!/usr/bin/env python
# 也可以通过 `assert` 语句产生 AssertionError 逐条测试
# 考虑到效率，建议使用 `unittest`
import unittest
from mymodule import my_calculator

class TestMyCalculator(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(my_calculator(1), 0)

    def test_negtive(self):
        self.assertEqual(my_calculator(-1), -21)

