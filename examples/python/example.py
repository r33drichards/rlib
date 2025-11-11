#!/usr/bin/env python3
"""rlib Python Example"""

import sys
from pathlib import Path

# Add bindings to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "bindings" / "python"))

import rlib

def main():
    print("rlib Python Example")
    print("===================")
    print()

    # Test add
    sum_result = rlib.add(10, 5)
    print(f"10 + 5 = {sum_result}")

    # Test multiply
    product = rlib.multiply(10, 5)
    print(f"10 * 5 = {product}")

    # Test divide (success)
    quotient = rlib.divide(10, 5)
    print(f"10 / 5 = {quotient}")

    # Test divide by zero
    try:
        rlib.divide(10, 0)
    except ValueError as e:
        print(f"10 / 0 error: {e}")

if __name__ == "__main__":
    main()
