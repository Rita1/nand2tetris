import unittest
from .. import assembler as amb

class TestMyClass(unittest.TestCase):

    def test_main(self):

        result = amb.Assembler.main()
        print("9", result)
        self.assertFalse(result.span()[1] == 0)


if __name__ == '__main__':
    unittest.main()
