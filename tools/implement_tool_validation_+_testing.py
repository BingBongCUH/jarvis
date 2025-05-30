
import unittest

def validate_tool(tool):
    if not isinstance(tool, str):
        raise ValueError("Tool name must be a string.")
    if len(tool) < 3:
        raise ValueError("Tool name must be at least 3 characters long.")
    return True

class TestToolValidation(unittest.TestCase):
    def test_validate_tool(self):
        self.assertTrue(validate_tool("Hammer"))
        self.assertRaises(ValueError, validate_tool, 123)
        self.assertRaises(ValueError, validate_tool, "Ax")

if __name__ == "__main__":
    unittest.main()
