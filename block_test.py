import unittest
from block import Block


class BlockTest(unittest.TestCase):
    def test_block_equal(self):
        block1 = Block((1, 1), 3)
        block2 = Block((1, 1), 3)
        self.assertEqual(block1, block2)

    def test_block_not_equal_same_location(self):
        block1 = Block((1, 1), 3)
        block2 = Block((1, 1), 4)
        self.assertNotEqual(block1, block2)

    def test_block_not_equal_dif_location(self):
        block1 = Block((1, 3), 3)
        block2 = Block((1, 1), 4)
        self.assertNotEqual(block1, block2)

    def test_super_block_index(self):
        block1 = Block((4, 4), 4)
        self.assertEqual(block1.get_super_block_index(), (1, 1))


if __name__ == '__main__':
    unittest.main()
