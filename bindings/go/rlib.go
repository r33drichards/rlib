package rlib

/*
#cgo LDFLAGS: -L../../target/release -lrlib
#include "../../include/rlib.h"
*/
import "C"
import "errors"

// Add two integers
func Add(a, b int) int {
	return int(C.rlib_add(C.int(a), C.int(b)))
}

// Multiply two integers
func Multiply(a, b int) int {
	return int(C.rlib_multiply(C.int(a), C.int(b)))
}

// Divide two integers
func Divide(a, b int) (int, error) {
	var result C.int
	err := C.rlib_divide(C.int(a), C.int(b), &result)

	if err != C.Ok {
		msg := C.GoString(C.rlib_error_message(err))
		return 0, errors.New(msg)
	}

	return int(result), nil
}
