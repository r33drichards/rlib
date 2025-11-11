#include "../rlib.hpp"
#include <cassert>
#include <iostream>
#include <stdexcept>

void test_add() {
    assert(rlib::add(2, 3) == 5);
    assert(rlib::add(-1, 1) == 0);
    assert(rlib::add(0, 0) == 0);
    std::cout << "✓ test_add" << std::endl;
}

void test_multiply() {
    assert(rlib::multiply(2, 3) == 6);
    assert(rlib::multiply(-2, 3) == -6);
    assert(rlib::multiply(0, 5) == 0);
    std::cout << "✓ test_multiply" << std::endl;
}

void test_divide() {
    assert(rlib::divide(6, 2) == 3);
    assert(rlib::divide(10, 5) == 2);
    assert(rlib::divide(-10, 2) == -5);
    std::cout << "✓ test_divide" << std::endl;
}

void test_divide_by_zero() {
    try {
        rlib::divide(10, 0);
        std::cerr << "✗ Expected exception for division by zero" << std::endl;
        std::exit(1);
    } catch (const rlib::Error& e) {
        assert(std::string(e.what()) == "Division by zero");
        std::cout << "✓ test_divide_by_zero" << std::endl;
    }
}

int main() {
    test_add();
    test_multiply();
    test_divide();
    test_divide_by_zero();
    std::cout << "\nAll tests passed!" << std::endl;
    return 0;
}
