import sys

DIGITS = set("0123456789")
LETTERS = set("abcdefghijklmnopqrstuvwxyz")
GLYPHS = set("+×∸⊤⊥←↑→↓∷Θ")


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def peek(self):
        return self.text[self.pos] if self.pos < self.length else None

    def advance(self):
        ch = self.peek()
        if ch is None:
            raise ParseError(f"unexpected end of input at position {self.pos}")
        self.pos += 1
        return ch

    def expect(self, ch):
        if self.peek() != ch:
            raise ParseError(f"expected {ch!r} at position {self.pos}, found {self.peek()!r}")
        return self.advance()

    def skip_spaces(self):
        while self.peek() == " ":
            self.advance()

    def parse_input(self):
        self.skip_spaces()
        self.parse_expression()
        self.skip_spaces()
        if self.pos != self.length:
            raise ParseError(f"unexpected trailing input at position {self.pos}")

    def parse_expression(self):
        ch = self.peek()
        if ch in DIGITS:
            self.parse_numeral()
        elif ch in LETTERS:
            self.parse_variable()
        elif ch in GLYPHS:
            self.advance()
        elif ch == "λ":
            self.parse_abstraction()
        elif ch == "(":
            self.parse_application()
        else:
            raise ParseError(f"unexpected character {ch!r} at position {self.pos}")

    def parse_numeral(self):
        if self.peek() not in DIGITS:
            raise ParseError(f"expected digit at position {self.pos}")
        while self.peek() in DIGITS:
            self.advance()

    def parse_variable(self):
        if self.peek() not in LETTERS:
            raise ParseError(f"expected letter at position {self.pos}")
        self.advance()
        while self.peek() in LETTERS or self.peek() in DIGITS or self.peek() == "-":
            self.advance()

    def parse_abstraction(self):
        self.expect("λ")
        self.skip_spaces()
        self.parse_variable()
        self.skip_spaces()
        self.expect(".")
        self.skip_spaces()
        self.parse_expression()

    def parse_application(self):
        self.expect("(")
        self.skip_spaces()
        self.parse_expression()
        self.expect(" ")
        self.skip_spaces()
        self.parse_expression()
        self.skip_spaces()
        self.expect(")")


def is_valid_proto(text):
    try:
        Parser(text).parse_input()
        return True
    except ParseError:
        return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python proto_parser.py <input-string>", file=sys.stderr)
        sys.exit(2)
    sys.exit(0 if is_valid_proto(sys.argv[1]) else 1)


if __name__ == "__main__":
    main()
