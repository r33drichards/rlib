package main

import (
	"fmt"
	"log"

	rlib "github.com/yourusername/rlib-go"
)

func main() {
	fmt.Println("rlib Go Example")
	fmt.Println("===============")
	fmt.Println()

	// Test add
	sum := rlib.Add(10, 5)
	fmt.Printf("10 + 5 = %d\n", sum)

	// Test multiply
	product := rlib.Multiply(10, 5)
	fmt.Printf("10 * 5 = %d\n", product)

	// Test exponent
	power := rlib.Exponent(2, 8)
	fmt.Printf("2 ^ 8 = %d\n", power)

	// Test divide (success)
	quotient, err := rlib.Divide(10, 5)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}
	fmt.Printf("10 / 5 = %d\n", quotient)

	// Test divide by zero
	_, err = rlib.Divide(10, 0)
	if err != nil {
		fmt.Printf("10 / 0 error: %v\n", err)
	}
}
