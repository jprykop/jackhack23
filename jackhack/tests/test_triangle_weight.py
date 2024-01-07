import random
import unittest
from unittest.mock import Mock, patch, call
import jackhack.triangle_weight as tw

class TriangleWeightTestCase(unittest.TestCase):

  def test_trinum(self):
    self.assertIs(tw.trinum(1), 1)
    self.assertIs(tw.trinum(2), 3)
    self.assertIs(tw.trinum(3), 6)
    self.assertIs(tw.trinum(4), 10)
    with self.assertRaises(IndexError):
      tw.trinum(0)
    with self.assertRaises(IndexError):
      tw.trinum(-1)
    t_with_max = tw.TriangleWeight(4)
    self.assertEqual(t_with_max.max, 4)
    with self.assertRaises(IndexError):
      t_with_max.trinum(5)

  def test_from_trinum_floor(self):
    self.assertIs(tw.from_trinum_floor(1), 1)
    self.assertIs(tw.from_trinum_floor(2), 1)
    self.assertIs(tw.from_trinum_floor(3), 2)
    self.assertIs(tw.from_trinum_floor(4), 2)
    self.assertIs(tw.from_trinum_floor(5), 2)
    self.assertIs(tw.from_trinum_floor(6), 3)
    self.assertIs(tw.from_trinum_floor(7), 3)
    self.assertIs(tw.from_trinum_floor(8), 3)
    self.assertIs(tw.from_trinum_floor(9), 3)
    self.assertIs(tw.from_trinum_floor(10), 4)
    with self.assertRaises(IndexError):
      tw.from_trinum_floor(0)
    with self.assertRaises(IndexError):
      tw.from_trinum_floor(-1)
    t_with_max = tw.TriangleWeight(4)
    self.assertIs(t_with_max.from_trinum_floor(14), 4)
    with self.assertRaises(IndexError):
      t_with_max.from_trinum_floor(15)

  def test_from_trinum_ceiling(self):
    self.assertIs(tw.from_trinum_ceiling(1), 1)
    self.assertIs(tw.from_trinum_ceiling(2), 2)
    self.assertIs(tw.from_trinum_ceiling(3), 2)
    self.assertIs(tw.from_trinum_ceiling(4), 3)
    self.assertIs(tw.from_trinum_ceiling(5), 3)
    self.assertIs(tw.from_trinum_ceiling(6), 3)
    self.assertIs(tw.from_trinum_ceiling(7), 4)
    self.assertIs(tw.from_trinum_ceiling(8), 4)
    self.assertIs(tw.from_trinum_ceiling(9), 4)
    self.assertIs(tw.from_trinum_ceiling(10), 4)
    with self.assertRaises(IndexError):
      tw.from_trinum_ceiling(0)
    with self.assertRaises(IndexError):
      tw.from_trinum_ceiling(-1)
    t_with_max = tw.TriangleWeight(4)
    self.assertIs(t_with_max.from_trinum_ceiling(10), 4)
    with self.assertRaises(IndexError):
      t_with_max.from_trinum_ceiling(11)

  def test_trirand(self):
    # originally wrote this to use seed(3656), hence the careful ordering of asserts
    mock_randint = Mock(side_effect=[1, 2, 9, 5, 3, 7, 8, 4, 10, 6, 3])
    with patch('random.randint', mock_randint):
      self.assertIs(tw.trirand(4), 1)
      self.assertIs(tw.trirand(4), 2)
      self.assertIs(tw.trirand(4), 4)
      self.assertIs(tw.trirand(4), 3)
      self.assertIs(tw.trirand(4), 2)
      self.assertIs(tw.trirand(4), 4)
      self.assertIs(tw.trirand(4), 4)
      t_with_max = tw.TriangleWeight(4)
      self.assertIs(t_with_max.trirand(), 3)
      self.assertIs(tw.trirand(4), 4)
      self.assertIs(tw.trirand(4), 3)
      self.assertIs(tw.trirand(4), 2)
      with self.assertRaises(IndexError):
        tw.trirand(0)
      with self.assertRaises(IndexError):
        tw.trirand(-1)
      with self.assertRaises(IndexError):
        t_with_max.trirand(5)
    self.assertEqual(mock_randint.mock_calls, [call(1,10) for n in range(0,11)])


  def test_reverse_trirand(self):
    # originally wrote this to use seed(3656), hence the careful ordering of asserts
    mock_randint = Mock(side_effect=[1, 2, 9, 5, 3, 7, 8, 4, 10, 6, 3])
    with patch('random.randint', mock_randint):
      self.assertIs(tw.reverse_trirand(4), 4)
      self.assertIs(tw.reverse_trirand(4), 3)
      self.assertIs(tw.reverse_trirand(4), 1)
      self.assertIs(tw.reverse_trirand(4), 2)
      self.assertIs(tw.reverse_trirand(4), 3)
      self.assertIs(tw.reverse_trirand(4), 1)
      self.assertIs(tw.reverse_trirand(4), 1)
      t_with_max = tw.TriangleWeight(4)
      self.assertIs(t_with_max.reverse_trirand(), 2)
      self.assertIs(tw.reverse_trirand(4), 1)
      self.assertIs(tw.reverse_trirand(4), 2)
      self.assertIs(tw.reverse_trirand(4), 3)
      with self.assertRaises(IndexError):
        tw.reverse_trirand(0)
      with self.assertRaises(IndexError):
        tw.reverse_trirand(-1)
      with self.assertRaises(IndexError):
        t_with_max.trirand(5)
    self.assertEqual(mock_randint.mock_calls, [call(1,10) for n in range(0,11)])

if __name__ == '__main__':
    unittest.main()
