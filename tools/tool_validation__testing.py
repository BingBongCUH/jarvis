
import unittest

def tool_validation(tool):
    if isinstance(tool, str):
        return True
    else:
        return False

def tool_testing(tool):
    if tool_validation(tool):
        return f"Tool {tool} is valid."
    else:
        return "Invalid tool."

class TestTool(unittest.TestCase):

    def test_tool_validation(self):
        self.assertEqual(tool_validation("Hammer"), True)
        self.assertEqual(tool_validation(123), False)

    def test_tool_testing(self):
        self.assertEqual(tool_testing("Hammer"), "Tool Hammer is valid.")
        self.assertEqual(tool_testing(123), "Invalid tool.")

if __name__ == '__main__':
    unittest.main()
