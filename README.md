# Tiny Symbolic Execution Engine

## Introduction

This repository contains a basic implementation of a symbolic execution engine using Python and Z3. It's designed as an educational tool to demonstrate the core concepts of symbolic execution in software analysis.

## Description

The symbolic execution engine provided in this project uses Python to symbolically execute a given program, using Z3 as a theorem prover to solve constraints and explore different execution paths.

## Installation

To use this symbolic execution engine, you need to have Python installed along with the Z3 theorem prover. You can install Z3 using pip:

```bash
pip install z3-solver
```

## Usage

```python
def test_function(x, y):
    z = 2 * x
    if z == y:
        if y == x + 10:
            assert False


if __name__ == "__main__":
    engine = TinySymbolicExecutionEngine()
    # Create symbolic variables for the function arguments using Z3
    x = BitVec("x", 32)
    y = BitVec("y", 32)
    engine.execute_path(test_function, x, y)
```

```bash
Assertion failed under: [y = 20, x = 10]
```
