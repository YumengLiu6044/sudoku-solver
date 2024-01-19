import unittest
from block import Block, BadBlockError


class BlockTest(unittest.TestCase):
    def test_block_equal(self):
        block1 = Block((1, 1), 3)
        block2 = Block((1, 1), 3)
        self.assertEqual(block1, block2)

    def test_block_not_equal_dif_location(self):
        block1 = Block((1, 3), 3)
        block2 = Block((1, 1), 4)
        self.assertNotEqual(block1, block2)

    def test_super_block_index(self):
        block1 = Block((4, 5), 4)
        self.assertEqual(block1.get_super_block_index(), (1, 1))

    def test_get_item_first_index(self):
        block1 = Block((3, 5), 6)
        self.assertEqual(block1[0], 3)

    def test_get_item_second_index(self):
        block1 = Block((3, 5), 6)
        self.assertEqual(block1[1], 5)

    def test_bad_given_location(self):
        with self.assertRaises(BadBlockError):
            Block((9, 9), 4)

    def test_bad_given_value(self):
        with self.assertRaises(BadBlockError):
            Block((9, 9), 10)


if __name__ == '__main__':
    unittest.main()
