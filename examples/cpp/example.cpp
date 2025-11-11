#include <iostream>
#include "../../bindings/cpp/rlib.hpp"

int main() {
    std::cout << "rlib C++ Example" << std::endl;
    std::cout << "================" << std::endl << std::endl;

    // Test add
    int sum = rlib::add(10, 5);
    std::cout << "10 + 5 = " << sum << std::endl;

    // Test multiply
    int product = rlib::multiply(10, 5);
    std::cout << "10 * 5 = " << product << std::endl;

    // Test divide (success)
    try {
        int quotient = rlib::divide(10, 5);
        std::cout << "10 / 5 = " << quotient << std::endl;
    } catch (const rlib::Error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    // Test divide by zero
    try {
        rlib::divide(10, 0);
    } catch (const rlib::Error& e) {
        std::cout << "10 / 0 error: " << e.what() << std::endl;
    }

    return 0;
}
