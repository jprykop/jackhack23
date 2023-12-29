import random
import unittest
from django.test import TestCase
from jackhack import models

class FibonacciMixinTestCase(TestCase):
  def test_value(self):
    self.assertEqual(models.FibonacciMixin(1).value, 1)
    self.assertEqual(models.FibonacciMixin(2).value, 3)
    self.assertEqual(models.FibonacciMixin(3).value, 6)
    self.assertEqual(models.FibonacciMixin(4).value, 10)

  def test_from_value_floor(self):
    self.assertEqual(models.FibonacciMixin.from_value_floor(1).number,1)
    self.assertEqual(models.FibonacciMixin.from_value_floor(2).number,1)
    self.assertEqual(models.FibonacciMixin.from_value_floor(3).number,2)
    self.assertEqual(models.FibonacciMixin.from_value_floor(4).number,2)
    self.assertEqual(models.FibonacciMixin.from_value_floor(5).number,2)
    self.assertEqual(models.FibonacciMixin.from_value_floor(6).number,3)
    self.assertEqual(models.FibonacciMixin.from_value_floor(7).number,3)
    self.assertEqual(models.FibonacciMixin.from_value_floor(8).number,3)
    self.assertEqual(models.FibonacciMixin.from_value_floor(9).number,3)
    self.assertEqual(models.FibonacciMixin.from_value_floor(10).number,4)

  def test_from_value_ceiling(self):
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(1).number,1)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(2).number,2)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(3).number,2)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(4).number,3)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(5).number,3)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(6).number,3)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(7).number,4)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(8).number,4)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(9).number,4)
    self.assertEqual(models.FibonacciMixin.from_value_ceiling(10).number,4)

  def test_random(self):
    random.seed(3656) # randint(1,10) ten times yields [1, 2, 9, 5, 3, 7, 8, 4, 10, 6]
    self.assertEqual(models.FibonacciMixin.random(4).number,1)
    self.assertEqual(models.FibonacciMixin.random(4).number,2)
    self.assertEqual(models.FibonacciMixin.random(4).number,4)
    self.assertEqual(models.FibonacciMixin.random(4).number,3)
    self.assertEqual(models.FibonacciMixin.random(4).number,2)
    self.assertEqual(models.FibonacciMixin.random(4).number,4)
    self.assertEqual(models.FibonacciMixin.random(4).number,4)
    self.assertEqual(models.FibonacciMixin.random(4).number,3)
    self.assertEqual(models.FibonacciMixin.random(4).number,4)
    self.assertEqual(models.FibonacciMixin.random(4).number,3)

  def test_reverse_random(self):
    random.seed(3656) # randint(1,10) ten times yields [1, 2, 9, 5, 3, 7, 8, 4, 10, 6]
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,4)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,3)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,1)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,2)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,3)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,1)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,1)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,2)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,1)
    self.assertEqual(models.FibonacciMixin.reverse_random(4).number,2)
