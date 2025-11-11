"""Tests for rlib Python bindings."""
import pytest
import rlib

def test_add():
    """Test addition function."""
    assert rlib.add(2, 3) == 5
    assert rlib.add(-1, 1) == 0
    assert rlib.add(0, 0) == 0

def test_multiply():
    """Test multiplication function."""
    assert rlib.multiply(2, 3) == 6
    assert rlib.multiply(-2, 3) == -6
    assert rlib.multiply(0, 5) == 0

def test_exponent():
    """Test exponent function."""
    assert rlib.exponent(2, 3) == 8
    assert rlib.exponent(5, 2) == 25
    assert rlib.exponent(10, 0) == 1
    assert rlib.exponent(3, 4) == 81

def test_divide():
    """Test division function."""
    assert rlib.divide(6, 2) == 3
    assert rlib.divide(10, 5) == 2
    assert rlib.divide(-10, 2) == -5

def test_divide_by_zero():
    """Test division by zero raises error."""
    with pytest.raises(ValueError, match="Division by zero"):
        rlib.divide(10, 0)
