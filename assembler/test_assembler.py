import unittest

class TestMyClass(unittest.TestCase):

    def test_parse9(self):

        result = Parser.parse("9")
        print("9", result)
        self.assertFalse(result.span()[1] == 0)


if __name__ == '__main__':
    unittest.main()