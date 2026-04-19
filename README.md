# Dual-Mode Expression Parser with Error Recovery

## 📌 Overview

This project implements a **recursive descent parser** for arithmetic expressions with a focus on **error recovery techniques in compiler design**.

Unlike basic parsers that stop at the first syntax error, this system **recovers and continues parsing**, allowing meaningful output even for faulty input.

It evaluates expressions such as:

```
3 + 4 * 2
```

and compares two recovery strategies:

* **Panic Mode (deletion-based)**
* **Minimal Insertion (insertion-based)**

---

## ⚙️ Architecture

The system follows a simple compiler pipeline:

```
Input String → Tokenizer → Token Stream → Parser → Result
```

### 🔹 Components

* **Tokenizer (`tokenizer.py`)**

  * Converts input into tokens (`NUMBER`, `PLUS`, `MULT`, etc.)
  * Handles invalid characters using exceptions

* **Parser (`parser.py`)**

  * Implements recursive descent parsing
  * Evaluates expressions while handling syntax errors
  * Supports dual recovery modes

* **Main Driver (`main.py`)**

  * Takes user input
  * Runs both recovery modes
  * Displays side-by-side results

---

## 📖 Grammar

The parser is based on the following grammar:

```
E → T ((+ | -) T)*
T → F ((* | /) F)*
F → NUMBER
```

Each rule maps to a function:

* `parse_E()`
* `parse_T()`
* `parse_F()`

---

## 🚨 Error Recovery Strategies

### 1️⃣ Panic Mode

* Skips tokens until a safe synchronization point is found
* Sync tokens: `+`, `-`, `EOF`

**Example:**

```
Input: 3 + * 5
→ Skips '*' and continues parsing
```

**Pros:**

* Simple and fast
* Prevents crashes

**Cons:**

* May discard valid tokens
* Can lose context

---

### 2️⃣ Minimal Insertion

* Inserts missing tokens (default value = `0`)
* Continues parsing without removing input

**Example:**

```
Input: 3 + * 5
→ Treated as: 3 + 0 * 5
```

**Pros:**

* Preserves input structure
* Fewer cascading errors

**Cons:**

* Assumes default values
* May slightly affect correctness

---

## ✨ Features

* Dual-mode parser (switch at runtime)
* Arithmetic expression evaluation
* Detailed error reporting with position tracking
* Tracks inserted and skipped tokens
* Handles division-by-zero safely
* Modular design (Tokenizer + Parser separation)

---

## 🎯 Learning Outcomes

This project demonstrates:

* Recursive descent parsing
* Grammar-based parsing design
* Syntax error detection and recovery
* Trade-offs between recovery strategies
* Reducing cascading errors in compilers

---

## 🧪 Example Run

```
>>> 3 + * 5

PANIC MODE RESULT
Result: 8

MINIMAL INSERT RESULT
Result: 3
```

---

## 🏁 Conclusion

Error recovery is a crucial part of parser design.

* **Panic Mode** offers simplicity and safety
* **Minimal Insertion** improves continuity and reduces cascading errors

This project shows how combining both approaches leads to more robust and user-friendly parsers.

---

## 📚 Reference

Inspired by:

> *"Don't Panic! Better, Fewer, Syntax Errors for LR Parsers"*
> — Diekmann & Tratt (2020)

---

