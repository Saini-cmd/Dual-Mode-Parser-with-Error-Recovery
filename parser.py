from tokenizer import Tokenizer


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, input_string, mode="panic"):
        self.tokens = Tokenizer(input_string).get_tokens()
        self.pos = 0

        self.mode = mode
        self.error_count = 0

        self.inserted = []
        self.skipped = []

        self.step = 1
        self.expression = input_string

        # Only tokens that safely separate expressions
        self.sync_tokens = {'PLUS', 'MINUS', 'EOF'}

    # ---------------------------
    # Helpers
    # ---------------------------
    def current_token(self):
        return self.tokens[self.pos]

    def advance(self):
        if self.current_token().type != 'EOF':
            self.pos += 1

    # ---------------------------
    # Error reporting
    # ---------------------------
    def _report(self, msg):
        tok = self.current_token()
        print(f"\n⚠ Error at {tok.pos}: {msg} (got {tok})")
        self.error_count += 1

    # ---------------------------
    # Panic mode (deletion-based)
    # ---------------------------
    def panic_mode(self):
        self._report("entering panic mode")

        while self.current_token().type not in ('NUMBER', 'EOF'):
            self.skipped.append(self.current_token())
            self.advance()

        print(f"Recovered at: {self.current_token()}")

    # ---------------------------
    # Minimal insertion (insertion-based)
    # ---------------------------
    def minimal_insert(self, expected, default=0):
        self._report(f"expected {expected}, inserting {default}")

        self.inserted.append((self.pos, default))
        return default

    # ---------------------------
    # eat() with recovery hook
    # ---------------------------
    def eat(self, token_type):
        if self.current_token().type == token_type:
            self.advance()
            return True

        # recovery
        if self.mode == "panic":
            self.panic_mode()
        else:
            self.minimal_insert(token_type)

        return False

    # ---------------------------
    # Grammar
    # ---------------------------
    # E → T ((+|-) T)*
    def parse(self):
        result = self.parse_E()

        if self.current_token().type != 'EOF':
            self._report("extra tokens after expression")

        return result

    def parse_E(self):
        value = self.parse_T()

        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token().type
            self.eat(op)
            right = self.parse_T()

            value = value + right if op == 'PLUS' else value - right

        return value

    # T → F ((*|/) F)*
    def parse_T(self):
        value = self.parse_F()

        while self.current_token().type in ('MULT', 'DIV'):
            op = self.current_token().type
            self.eat(op)
            right = self.parse_F()

            if op == 'MULT':
                value *= right
            else:
                if right == 0:
                    self._report("division by zero → using 1")
                    right = 1
                value /= right

        return value

    # # F → NUMBER
    def parse_F(self):
        while True:
            token = self.current_token()

            # ── SUCCESS CASE ─────────────────────────────
            if token.type == 'NUMBER':
                value = token.value
                self.advance()
                return value

            # ── ERROR CASE ───────────────────────────────
            self._report(f"expected NUMBER, got {token.type}")

            if self.mode == "panic":
                self.panic_mode()

                # after recovery, try again instead of returning 0
                if self.current_token().type == 'EOF':
                    return 0

            else:
                # minimal insert = assume 0 but DO NOT break stream
                self.minimal_insert("NUMBER", 0)
                return 0