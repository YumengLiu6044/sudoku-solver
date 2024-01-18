import unittest
from block import Block


class BlockTest(unittest.TestCase):
    def test_block_equal(self):
        block1 = Block((1, 1), 3)
        block2 = Block((1, 1), 3)
        self.assertEqual(block1, block2)  # add assertion here


if __name__ == '__main__':
    unittest.main()
