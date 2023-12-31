import random
import unittest
from jackhack.fibonacci_weight import FibonacciWeight

class FibonacciWithMax(FibonacciWeight):
  MAX = 4

class FibonacciWeightTestCase(unittest.TestCase):
  def test_fibonacci_init(self):
    self.assertEqual(FibonacciWeight(1).number, 1)
    with self.assertRaises(IndexError):
      FibonacciWeight(0)
    with self.assertRaises(IndexError):
      FibonacciWeight(-1)
    self.assertEqual(FibonacciWithMax(4).number, 4)
    with self.assertRaises(IndexError):
      FibonacciWithMax(5)

  def test_weight(self):
    self.assertEqual(FibonacciWeight(1).weight, 1)
    self.assertEqual(FibonacciWeight(2).weight, 3)
    self.assertEqual(FibonacciWeight(3).weight, 6)
    self.assertEqual(FibonacciWeight(4).weight, 10)

  def test_from_weight_floor(self):
    self.assertEqual(FibonacciWeight.from_weight_floor(1).number, 1)
    self.assertEqual(FibonacciWeight.from_weight_floor(2).number, 1)
    self.assertEqual(FibonacciWeight.from_weight_floor(3).number, 2)
    self.assertEqual(FibonacciWeight.from_weight_floor(4).number, 2)
    self.assertEqual(FibonacciWeight.from_weight_floor(5).number, 2)
    self.assertEqual(FibonacciWeight.from_weight_floor(6).number, 3)
    self.assertEqual(FibonacciWeight.from_weight_floor(7).number, 3)
    self.assertEqual(FibonacciWeight.from_weight_floor(8).number, 3)
    self.assertEqual(FibonacciWeight.from_weight_floor(9).number, 3)
    self.assertEqual(FibonacciWeight.from_weight_floor(10).number, 4)
    self.assertEqual(FibonacciWithMax.from_weight_floor(14).number, 4)
    with self.assertRaises(IndexError):
      FibonacciWeight.from_weight_floor(0)
    with self.assertRaises(IndexError):
      FibonacciWeight.from_weight_floor(-1)
    with self.assertRaises(IndexError):
      FibonacciWithMax.from_weight_floor(15)

  def test_from_weight_ceiling(self):
    self.assertEqual(FibonacciWeight.from_weight_ceiling(1).number, 1)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(2).number, 2)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(3).number, 2)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(4).number, 3)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(5).number, 3)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(6).number, 3)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(7).number, 4)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(8).number, 4)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(9).number, 4)
    self.assertEqual(FibonacciWeight.from_weight_ceiling(10).number, 4)
    self.assertEqual(FibonacciWithMax.from_weight_ceiling(10).number, 4)
    with self.assertRaises(IndexError):
      FibonacciWeight.from_weight_ceiling(0)
    with self.assertRaises(IndexError):
      FibonacciWeight.from_weight_ceiling(-1)
    with self.assertRaises(IndexError):
      FibonacciWithMax.from_weight_ceiling(11)

  def test_random(self):
    random.seed(3656) # randint(1,10) eleven times returns 1, 2, 9, 5, 3, 7, 8, 4, 10, 6, 3
    self.assertEqual(FibonacciWeight.random(4).number, 1)
    self.assertEqual(FibonacciWeight.random(4).number, 2)
    self.assertEqual(FibonacciWeight.random(4).number, 4)
    self.assertEqual(FibonacciWeight.random(4).number, 3)
    self.assertEqual(FibonacciWeight.random(4).number, 2)
    self.assertEqual(FibonacciWeight.random(4).number, 4)
    self.assertEqual(FibonacciWeight.random(4).number, 4)
    # intentionally checking with max here to be sure ceiling vs floor yield different numbers
    self.assertEqual(FibonacciWithMax.random().number, 3)
    self.assertEqual(FibonacciWeight.random(4).number, 4)
    self.assertEqual(FibonacciWeight.random(4).number, 3)
    self.assertEqual(FibonacciWeight.random(4).number, 2)
    with self.assertRaises(IndexError):
      FibonacciWeight.random(0)
    with self.assertRaises(IndexError):
      FibonacciWeight.random(-1)
    with self.assertRaises(IndexError):
      # twelfth call randint(1,15) returns 4, which would lead to random number 3,
      # so this is (intentionally) testing that max is checked before calling randint
      FibonacciWithMax.random(5)

  def test_reverse_random(self):
    random.seed(3656) # randint(1,10) ten times yields [1, 2, 9, 5, 3, 7, 8, 4, 10, 6]
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 4)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 3)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 1)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 2)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 3)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 1)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 1)
    # intentionally checking with max here to be sure ceiling vs floor yield different numbers
    self.assertEqual(FibonacciWithMax.reverse_random().number, 2)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 1)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 2)
    self.assertEqual(FibonacciWeight.reverse_random(4).number, 3)
    with self.assertRaises(IndexError):
      FibonacciWeight.reverse_random(0)
    with self.assertRaises(IndexError):
      FibonacciWeight.reverse_random(-1)
    with self.assertRaises(IndexError):
      # twelfth call randint(1,15) returns 4, which would lead to random number 3,
      # so this is (intentionally) testing that max is checked before calling randint
      FibonacciWithMax.random(5)

  def test_equality(self):
    one = FibonacciWeight(3)
    two = FibonacciWeight(3)
    self.assertIsNot(one, two)
    self.assertEqual(one, two)

if __name__ == '__main__':
    unittest.main()