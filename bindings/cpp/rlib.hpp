#pragma once

#include "../../include/rlib.h"
#include <stdexcept>
#include <string>

namespace rlib {

/**
 * Exception thrown when rlib operations fail
 */
class Error : public std::runtime_error {
public:
    explicit Error(rlib_error_t code)
        : std::runtime_error(rlib_error_message(code))
        , code_(code) {}

    rlib_error_t code() const { return code_; }

private:
    rlib_error_t code_;
};

/**
 * Add two integers
 */
inline int add(int a, int b) {
    return rlib_add(a, b);
}

/**
 * Multiply two integers
 */
inline int multiply(int a, int b) {
    return rlib_multiply(a, b);
}

/**
 * Raise base to the power of exponent
 */
inline int exponent(int base, int exp) {
    return rlib_exponent(base, exp);
}

/**
 * Divide two integers
 * @throws Error if division by zero
 */
inline int divide(int a, int b) {
    int result;
    rlib_error_t err = rlib_divide(a, b, &result);
    if (err != Ok) {
        throw Error(err);
    }
    return result;
}

} // namespace rlib
