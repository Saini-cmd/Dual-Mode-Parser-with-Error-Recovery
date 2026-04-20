from parser import Parser
from tokenizer import Tokenizer, TokenizerError


def run_parser(expr, mode):
    """Run parser safely and return result or error."""
    try:
        Tokenizer(expr).get_tokens()
        parser = Parser(expr, mode)
        return parser.parse()
    except Exception as e:
        return f"Error: {e}"


def print_section(title, expr, result):
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)
    print(f"Expression : {expr}")
    print(f"Result     : {result}")
    print("=" * 60)


def main():
    print("Simple Expression Evaluator (Dual Mode Comparison)")
    print("Type expressions like: 2 + 3 * 4")
    print("Type 'exit' to quit\n")

    while True:
        expr = input("\n>>> ").strip()

        if expr.lower() == "exit":
            break

        if not expr:
            continue

        # ─────────────────────────────────────────────
        # Run PANIC MODE
        # ─────────────────────────────────────────────
        panic_result = run_parser(expr, "panic")
        print_section("PANIC MODE RESULT", expr, panic_result)

        # ─────────────────────────────────────────────
        # Run MINIMAL INSERT MODE
        # ─────────────────────────────────────────────
        minimal_result = run_parser(expr, "minimal")
        print_section("MINIMAL INSERT RESULT", expr, minimal_result)


if __name__ == "__main__":
    main()