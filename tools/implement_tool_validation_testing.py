
import unittest

def tool(input):
    if isinstance(input, int):
        return input * 2
    else:
        raise ValueError("Input should be an integer")

class TestTool(unittest.TestCase):
    def test_tool(self):
        self.assertEqual(tool(2), 4)
        self.assertEqual(tool(5), 10)
        self.assertEqual(tool(0), 0)
        with self.assertRaises(ValueError):
            tool('string')
        with self.assertRaises(ValueError):
            tool(None)
        with self.assertRaises(ValueError):
            tool(3.14)

if __name__ == '__main__':
    unittest.main()
