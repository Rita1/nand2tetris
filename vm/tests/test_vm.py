import unittest
import os
from os import path
from .. import vm


class TestMain(unittest.TestCase):

    def test_main_create_file(self):
        
        inst = vm.Main()
        inst.main('Test.vm')
        f = os.getcwd() + "/tests/files/Test.asm"
        self.assertTrue(path.exists(f))


if __name__ == '__main__':
    unittest.main()
