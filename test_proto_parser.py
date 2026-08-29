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
    "(((a b) c) d)",
    "(a (b (c (d e))))",
    "((× 2) 3)",
    "λf.λx.(f (f x))",
    "λa.λb.λc.λd.(a (b (c d)))",
    "a-b1-c2-d3-e4-f5g6h7",
    "1234567890123456789",
    "(λadd.(add 1) +)",
    "   (a (b c))   ",
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
    "(× 2 3)",
    "(a (b c) d)",
    "(λx.x)",
    "(((a b) c)",
    "((a b) c))",
    "λx.λy.(x y",
    "(a (b c)",
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

    def test_invalid_utf8_argument_exits_nonzero(self):
        result = self.run_cli(chr(0xDCFF))
        self.assertEqual(result.returncode, 1)

    def test_invalid_argument_count_exits_nonzero(self):
        result = subprocess.run(
            [sys.executable, "proto_parser.py", "arg1", "arg2"],
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
