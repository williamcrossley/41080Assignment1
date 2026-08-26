import subprocess
import sys
import unittest

from proto_parser import is_valid_proto

VALID = [
    "0",
    "007",
    "42",
    "x",
    "abc",
    "a-b-1",
    "z9-9z",
    "+",
    "×", #U+00d7
    "∸",
    "⊤", #U+22a4
    "⊥",
    "←",
    "↑",
    "→",
    "↓",
    "∷",
    "Θ",
    "λx.x",
    "λ x . x",
    "λ x.x",
    "λx. x",
    "λfoo.123",
    "λx.λy.x",
    "(a b)",
    "(a  b)",
    "( a b )",
    "(a (b c))",
    "((a b) c)",
    "(λx.x y)",
    "  x  ",
    " (a b) ",
]

INVALID = [
    "",
    " ",
    "1abc",
    "-abc",
    "1-2",
    "λ.x",
    "λx x",
    "λx.",
    "(a)",
    "(ab)",
    "(a b",
    "a b)",
    "a b",
    "α", #U+03b1
    "\tx",
    "x\n",
    "λX.x",
    "λx.λy.",
]


class IsValidProtoTests(unittest.TestCase):
    def test_valid_inputs_accepted(self):
        for text in VALID:
            with self.subTest(text=text):
                self.assertTrue(is_valid_proto(text))

    def test_invalid_inputs_rejected(self):
        for text in INVALID:
            with self.subTest(text=text):
                self.assertFalse(is_valid_proto(text))


class CliExitCodeTests(unittest.TestCase):
    def run_cli(self, text):
        return subprocess.run(
            [sys.executable, "proto_parser.py", text],
            capture_output=True,
        )

    def test_valid_input_exits_zero(self):
        self.assertEqual(self.run_cli("λx.x").returncode, 0)

    def test_invalid_input_exits_nonzero(self):
        self.assertNotEqual(self.run_cli("λx x").returncode, 0)

    def test_missing_argument_exits_nonzero(self):
        result = subprocess.run(
            [sys.executable, "proto_parser.py"],
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
