#include <stdio.h>
#include "../../include/rlib.h"

int main() {
    printf("rlib C Example\n");
    printf("==============\n\n");

    // Test add
    int sum = rlib_add(10, 5);
    printf("10 + 5 = %d\n", sum);

    // Test multiply
    int product = rlib_multiply(10, 5);
    printf("10 * 5 = %d\n", product);

    // Test divide (success)
    int quotient;
    rlib_error_t err = rlib_divide(10, 5, &quotient);
    if (err == Ok) {
        printf("10 / 5 = %d\n", quotient);
    } else {
        printf("Error: %s\n", rlib_error_message(err));
    }

    // Test divide by zero
    err = rlib_divide(10, 0, &quotient);
    if (err != Ok) {
        printf("10 / 0 error: %s\n", rlib_error_message(err));
    }

    return 0;
}
