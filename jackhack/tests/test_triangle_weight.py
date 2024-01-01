import random
import unittest
from jackhack.triangle_weight import TriangleWeight

class TriangleWithMax(TriangleWeight):
  MAX = 4

class TriangleWeightTestCase(unittest.TestCase):
  def test_triangle_init(self):
    self.assertEqual(TriangleWeight(1).number, 1)
    with self.assertRaises(IndexError):
      TriangleWeight(0)
    with self.assertRaises(IndexError):
      TriangleWeight(-1)
    self.assertEqual(TriangleWithMax(4).number, 4)
    with self.assertRaises(IndexError):
      TriangleWithMax(5)

  def test_weight(self):
    self.assertEqual(TriangleWeight(1).weight, 1)
    self.assertEqual(TriangleWeight(2).weight, 3)
    self.assertEqual(TriangleWeight(3).weight, 6)
    self.assertEqual(TriangleWeight(4).weight, 10)

  def test_from_weight_floor(self):
    self.assertEqual(TriangleWeight.from_weight_floor(1).number, 1)
    self.assertEqual(TriangleWeight.from_weight_floor(2).number, 1)
    self.assertEqual(TriangleWeight.from_weight_floor(3).number, 2)
    self.assertEqual(TriangleWeight.from_weight_floor(4).number, 2)
    self.assertEqual(TriangleWeight.from_weight_floor(5).number, 2)
    self.assertEqual(TriangleWeight.from_weight_floor(6).number, 3)
    self.assertEqual(TriangleWeight.from_weight_floor(7).number, 3)
    self.assertEqual(TriangleWeight.from_weight_floor(8).number, 3)
    self.assertEqual(TriangleWeight.from_weight_floor(9).number, 3)
    self.assertEqual(TriangleWeight.from_weight_floor(10).number, 4)
    self.assertEqual(TriangleWithMax.from_weight_floor(14).number, 4)
    with self.assertRaises(IndexError):
      TriangleWeight.from_weight_floor(0)
    with self.assertRaises(IndexError):
      TriangleWeight.from_weight_floor(-1)
    with self.assertRaises(IndexError):
      TriangleWithMax.from_weight_floor(15)

  def test_from_weight_ceiling(self):
    self.assertEqual(TriangleWeight.from_weight_ceiling(1).number, 1)
    self.assertEqual(TriangleWeight.from_weight_ceiling(2).number, 2)
    self.assertEqual(TriangleWeight.from_weight_ceiling(3).number, 2)
    self.assertEqual(TriangleWeight.from_weight_ceiling(4).number, 3)
    self.assertEqual(TriangleWeight.from_weight_ceiling(5).number, 3)
    self.assertEqual(TriangleWeight.from_weight_ceiling(6).number, 3)
    self.assertEqual(TriangleWeight.from_weight_ceiling(7).number, 4)
    self.assertEqual(TriangleWeight.from_weight_ceiling(8).number, 4)
    self.assertEqual(TriangleWeight.from_weight_ceiling(9).number, 4)
    self.assertEqual(TriangleWeight.from_weight_ceiling(10).number, 4)
    self.assertEqual(TriangleWithMax.from_weight_ceiling(10).number, 4)
    with self.assertRaises(IndexError):
      TriangleWeight.from_weight_ceiling(0)
    with self.assertRaises(IndexError):
      TriangleWeight.from_weight_ceiling(-1)
    with self.assertRaises(IndexError):
      TriangleWithMax.from_weight_ceiling(11)

  def test_random(self):
    random.seed(3656) # randint(1,10) eleven times returns 1, 2, 9, 5, 3, 7, 8, 4, 10, 6, 3
    self.assertEqual(TriangleWeight.random(4).number, 1)
    self.assertEqual(TriangleWeight.random(4).number, 2)
    self.assertEqual(TriangleWeight.random(4).number, 4)
    self.assertEqual(TriangleWeight.random(4).number, 3)
    self.assertEqual(TriangleWeight.random(4).number, 2)
    self.assertEqual(TriangleWeight.random(4).number, 4)
    self.assertEqual(TriangleWeight.random(4).number, 4)
    # intentionally checking with max here to be sure ceiling vs floor yield different numbers
    self.assertEqual(TriangleWithMax.random().number, 3)
    self.assertEqual(TriangleWeight.random(4).number, 4)
    self.assertEqual(TriangleWeight.random(4).number, 3)
    self.assertEqual(TriangleWeight.random(4).number, 2)
    with self.assertRaises(IndexError):
      TriangleWeight.random(0)
    with self.assertRaises(IndexError):
      TriangleWeight.random(-1)
    with self.assertRaises(IndexError):
      # twelfth call randint(1,15) returns 4, which would lead to random number 3,
      # so this is (intentionally) testing that max is checked before calling randint
      TriangleWithMax.random(5)

  def test_reverse_random(self):
    random.seed(3656) # randint(1,10) ten times yields [1, 2, 9, 5, 3, 7, 8, 4, 10, 6]
    self.assertEqual(TriangleWeight.reverse_random(4).number, 4)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 3)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 1)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 2)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 3)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 1)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 1)
    # intentionally checking with max here to be sure ceiling vs floor yield different numbers
    self.assertEqual(TriangleWithMax.reverse_random().number, 2)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 1)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 2)
    self.assertEqual(TriangleWeight.reverse_random(4).number, 3)
    with self.assertRaises(IndexError):
      TriangleWeight.reverse_random(0)
    with self.assertRaises(IndexError):
      TriangleWeight.reverse_random(-1)
    with self.assertRaises(IndexError):
      # twelfth call randint(1,15) returns 4, which would lead to random number 3,
      # so this is (intentionally) testing that max is checked before calling randint
      TriangleWithMax.random(5)

  def test_equality(self):
    one = TriangleWeight(3)
    two = TriangleWeight(3)
    self.assertIsNot(one, two)
    self.assertEqual(one, two)
    self.assertEqual(one, 3)

  def test_int(self):
    one = TriangleWeight(3)
    self.assertIsNot(one, 3)
    self.assertIs(int(one),3)

  def test_hash(self):
    self.assertEqual(set([1,2]), set([TriangleWeight(1), TriangleWeight(2)]))

if __name__ == '__main__':
    unittest.main()
