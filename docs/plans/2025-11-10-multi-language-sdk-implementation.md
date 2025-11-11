# Multi-Language Rust SDK Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build rlib, a Rust library with C FFI bindings for C, C++, Go, Python, and JavaScript/Node.js, packaged with Nix.

**Architecture:** Cargo workspace with separated `core` (pure Rust) and `ffi` (C bindings) crates. Use cbindgen to generate C headers. Each language gets idiomatic wrapper around C FFI. Nix flake builds and packages all SDKs.

**Tech Stack:** Rust, cbindgen, ctypes (Python), cgo (Go), ffi-napi (Node.js), Nix

---

## Task 1: Set Up Cargo Workspace

**Files:**
- Create: `Cargo.toml` (workspace root)
- Create: `.gitignore`

**Step 1: Create workspace Cargo.toml**

Create `/Users/robertwendt/rlib/Cargo.toml`:

```toml
[workspace]
resolver = "2"

members = [
    "core",
    "ffi",
]

[workspace.package]
version = "0.1.0"
edition = "2021"
authors = ["rlib contributors"]
license = "MIT OR Apache-2.0"
```

**Step 2: Create .gitignore**

Create `/Users/robertwendt/rlib/.gitignore`:

```
# Rust
target/
Cargo.lock
**/*.rs.bk
*.pdb

# Nix
result
result-*

# Generated
include/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/
.pytest_cache/

# Node
node_modules/
npm-debug.log
yarn-error.log

# Go
go.sum

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store
```

**Step 3: Verify workspace structure**

Run: `cargo --version`
Expected: Output showing cargo version (confirms Rust toolchain available)

**Step 4: Commit**

```bash
git add Cargo.toml .gitignore
git commit -m "chore: initialize Cargo workspace"
```

---

## Task 2: Create Core Crate

**Files:**
- Create: `core/Cargo.toml`
- Create: `core/src/lib.rs`

**Step 1: Create core directory**

Run: `mkdir -p core/src`

**Step 2: Write core Cargo.toml**

Create `/Users/robertwendt/rlib/core/Cargo.toml`:

```toml
[package]
name = "rlib-core"
version.workspace = true
edition.workspace = true
authors.workspace = true
license.workspace = true

[lib]
crate-type = ["rlib"]

[dependencies]
```

**Step 3: Write failing test for add function**

Create `/Users/robertwendt/rlib/core/src/lib.rs`:

```rust
/// Add two integers
pub fn add(a: i32, b: i32) -> i32 {
    todo!("implement add")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
        assert_eq!(add(0, 0), 0);
    }
}
```

**Step 4: Run test to verify it fails**

Run: `cargo test -p rlib-core`
Expected: FAIL with "not yet implemented: implement add"

**Step 5: Implement add function**

Edit `/Users/robertwendt/rlib/core/src/lib.rs`, replace the `add` function:

```rust
/// Add two integers
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

**Step 6: Run test to verify it passes**

Run: `cargo test -p rlib-core`
Expected: PASS - "test tests::test_add ... ok"

**Step 7: Write failing test for multiply function**

Add to `/Users/robertwendt/rlib/core/src/lib.rs` after the `add` function:

```rust
/// Multiply two integers
pub fn multiply(a: i32, b: i32) -> i32 {
    todo!("implement multiply")
}
```

Add test to the `tests` module:

```rust
#[test]
fn test_multiply() {
    assert_eq!(multiply(2, 3), 6);
    assert_eq!(multiply(-2, 3), -6);
    assert_eq!(multiply(0, 5), 0);
}
```

**Step 8: Run test to verify it fails**

Run: `cargo test -p rlib-core`
Expected: FAIL with "not yet implemented: implement multiply"

**Step 9: Implement multiply function**

Edit `/Users/robertwendt/rlib/core/src/lib.rs`, replace the `multiply` function:

```rust
/// Multiply two integers
pub fn multiply(a: i32, b: i32) -> i32 {
    a * b
}
```

**Step 10: Run test to verify it passes**

Run: `cargo test -p rlib-core`
Expected: PASS - both test_add and test_multiply pass

**Step 11: Write failing test for divide function**

Add to `/Users/robertwendt/rlib/core/src/lib.rs` after the `multiply` function:

```rust
/// Divide two integers
/// Returns an error if division by zero
pub fn divide(a: i32, b: i32) -> Result<i32, String> {
    todo!("implement divide")
}
```

Add tests to the `tests` module:

```rust
#[test]
fn test_divide() {
    assert_eq!(divide(6, 2).unwrap(), 3);
    assert_eq!(divide(10, 5).unwrap(), 2);
    assert_eq!(divide(-10, 2).unwrap(), -5);
}

#[test]
fn test_divide_by_zero() {
    let result = divide(10, 0);
    assert!(result.is_err());
    assert_eq!(result.unwrap_err(), "Division by zero");
}
```

**Step 12: Run test to verify it fails**

Run: `cargo test -p rlib-core`
Expected: FAIL with "not yet implemented: implement divide"

**Step 13: Implement divide function**

Edit `/Users/robertwendt/rlib/core/src/lib.rs`, replace the `divide` function:

```rust
/// Divide two integers
/// Returns an error if division by zero
pub fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}
```

**Step 14: Run test to verify it passes**

Run: `cargo test -p rlib-core`
Expected: PASS - all tests pass

**Step 15: Commit**

```bash
git add core/
git commit -m "feat(core): add basic math functions with tests"
```

---

## Task 3: Create FFI Crate with cbindgen

**Files:**
- Create: `ffi/Cargo.toml`
- Create: `ffi/cbindgen.toml`
- Create: `ffi/src/lib.rs`

**Step 1: Create ffi directory**

Run: `mkdir -p ffi/src`

**Step 2: Write ffi Cargo.toml**

Create `/Users/robertwendt/rlib/ffi/Cargo.toml`:

```toml
[package]
name = "rlib-ffi"
version.workspace = true
edition.workspace = true
authors.workspace = true
license.workspace = true

[lib]
crate-type = ["cdylib"]
name = "rlib"

[dependencies]
rlib-core = { path = "../core" }

[build-dependencies]
cbindgen = "0.26"
```

**Step 3: Write cbindgen configuration**

Create `/Users/robertwendt/rlib/ffi/cbindgen.toml`:

```toml
language = "C"
cpp_compat = true
include_guard = "RLIB_H"
autogen_warning = "/* Warning: Auto-generated by cbindgen. Do not edit. */"
header = "/* rlib - Multi-language Rust library */"
style = "both"

[export]
include = ["RlibError"]

[export.rename]
"RlibError" = "rlib_error_t"
```

**Step 4: Write FFI error enum**

Create `/Users/robertwendt/rlib/ffi/src/lib.rs`:

```rust
use std::os::raw::{c_char, c_int};

/// Error codes for C API
#[repr(C)]
#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum RlibError {
    /// Success
    Ok = 0,
    /// Division by zero error
    DivisionByZero = 1,
    /// Invalid argument (null pointer)
    InvalidArgument = 2,
}
```

**Step 5: Write FFI wrapper for add**

Add to `/Users/robertwendt/rlib/ffi/src/lib.rs`:

```rust
/// Add two integers
#[no_mangle]
pub extern "C" fn rlib_add(a: c_int, b: c_int) -> c_int {
    rlib_core::add(a, b)
}
```

**Step 6: Write FFI wrapper for multiply**

Add to `/Users/robertwendt/rlib/ffi/src/lib.rs`:

```rust
/// Multiply two integers
#[no_mangle]
pub extern "C" fn rlib_multiply(a: c_int, b: c_int) -> c_int {
    rlib_core::multiply(a, b)
}
```

**Step 7: Write FFI wrapper for divide**

Add to `/Users/robertwendt/rlib/ffi/src/lib.rs`:

```rust
/// Divide two integers
/// Returns the result via out parameter, returns error code
#[no_mangle]
pub extern "C" fn rlib_divide(a: c_int, b: c_int, result: *mut c_int) -> RlibError {
    if result.is_null() {
        return RlibError::InvalidArgument;
    }

    match rlib_core::divide(a, b) {
        Ok(val) => {
            unsafe { *result = val; }
            RlibError::Ok
        }
        Err(_) => RlibError::DivisionByZero,
    }
}
```

**Step 8: Write error message function**

Add to `/Users/robertwendt/rlib/ffi/src/lib.rs`:

```rust
/// Get human-readable error message
#[no_mangle]
pub extern "C" fn rlib_error_message(error: RlibError) -> *const c_char {
    match error {
        RlibError::Ok => "Success\0".as_ptr() as *const c_char,
        RlibError::DivisionByZero => "Division by zero\0".as_ptr() as *const c_char,
        RlibError::InvalidArgument => "Invalid argument\0".as_ptr() as *const c_char,
    }
}
```

**Step 9: Build FFI library**

Run: `cargo build -p rlib-ffi --release`
Expected: SUCCESS - builds librlib.so (or .dylib on macOS)

**Step 10: Generate C header with cbindgen**

Run: `mkdir -p include && cbindgen ffi/ -o include/rlib.h`
Expected: Creates include/rlib.h with C function declarations

**Step 11: Verify generated header**

Run: `cat include/rlib.h`
Expected: Contains declarations for rlib_add, rlib_multiply, rlib_divide, rlib_error_message

**Step 12: Commit**

```bash
git add ffi/
git commit -m "feat(ffi): add C FFI layer with cbindgen"
```

---

## Task 4: Create Python Bindings

**Files:**
- Create: `bindings/python/setup.py`
- Create: `bindings/python/pyproject.toml`
- Create: `bindings/python/rlib/__init__.py`
- Create: `bindings/python/rlib/_ffi.py`
- Create: `bindings/python/tests/test_rlib.py`

**Step 1: Create Python package structure**

Run: `mkdir -p bindings/python/rlib bindings/python/tests`

**Step 2: Write setup.py**

Create `/Users/robertwendt/rlib/bindings/python/setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name="rlib",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.7",
    author="rlib contributors",
    description="Multi-language Rust library - Python bindings",
    long_description=open("../../README.md").read() if __file__ else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
```

**Step 3: Write pyproject.toml**

Create `/Users/robertwendt/rlib/bindings/python/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "rlib"
version = "0.1.0"
requires-python = ">=3.7"
```

**Step 4: Write Python FFI wrapper**

Create `/Users/robertwendt/rlib/bindings/python/rlib/_ffi.py`:

```python
"""Low-level FFI bindings to librlib."""
import ctypes
import os
from pathlib import Path
import platform

# Determine shared library extension
if platform.system() == "Darwin":
    lib_ext = "dylib"
elif platform.system() == "Windows":
    lib_ext = "dll"
else:
    lib_ext = "so"

# Try to find library in multiple locations
lib_locations = [
    Path(__file__).parent / f"librlib.{lib_ext}",
    Path(__file__).parent.parent.parent.parent / "target" / "release" / f"librlib.{lib_ext}",
]

_lib = None
for lib_path in lib_locations:
    if lib_path.exists():
        _lib = ctypes.CDLL(str(lib_path))
        break

if _lib is None:
    raise RuntimeError(f"Could not find librlib.{lib_ext} in any expected location")

# Error codes
class RlibError:
    """Error codes from rlib C API."""
    OK = 0
    DIVISION_BY_ZERO = 1
    INVALID_ARGUMENT = 2

# Define function signatures
_lib.rlib_add.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.rlib_add.restype = ctypes.c_int

_lib.rlib_multiply.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.rlib_multiply.restype = ctypes.c_int

_lib.rlib_divide.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
_lib.rlib_divide.restype = ctypes.c_int

_lib.rlib_error_message.argtypes = [ctypes.c_int]
_lib.rlib_error_message.restype = ctypes.c_char_p

def add(a: int, b: int) -> int:
    """Add two integers."""
    return _lib.rlib_add(a, b)

def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return _lib.rlib_multiply(a, b)

def divide(a: int, b: int) -> int:
    """Divide two integers. Raises ValueError on division by zero."""
    result = ctypes.c_int()
    error = _lib.rlib_divide(a, b, ctypes.byref(result))
    if error != RlibError.OK:
        msg = _lib.rlib_error_message(error).decode('utf-8')
        raise ValueError(msg)
    return result.value
```

**Step 5: Write Python package __init__.py**

Create `/Users/robertwendt/rlib/bindings/python/rlib/__init__.py`:

```python
"""rlib - Multi-language Rust library."""

from rlib._ffi import add, multiply, divide

__version__ = "0.1.0"
__all__ = ["add", "multiply", "divide"]
```

**Step 6: Write failing Python tests**

Create `/Users/robertwendt/rlib/bindings/python/tests/test_rlib.py`:

```python
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

def test_divide():
    """Test division function."""
    assert rlib.divide(6, 2) == 3
    assert rlib.divide(10, 5) == 2
    assert rlib.divide(-10, 2) == -5

def test_divide_by_zero():
    """Test division by zero raises error."""
    with pytest.raises(ValueError, match="Division by zero"):
        rlib.divide(10, 0)
```

**Step 7: Run Python tests**

Run: `cd bindings/python && python -m pytest tests/ -v`
Expected: PASS - all 4 tests pass

**Step 8: Commit**

```bash
git add bindings/python/
git commit -m "feat(python): add Python bindings with ctypes"
```

---

## Task 5: Create Go Bindings

**Files:**
- Create: `bindings/go/go.mod`
- Create: `bindings/go/rlib.go`
- Create: `bindings/go/rlib_test.go`

**Step 1: Create Go directory**

Run: `mkdir -p bindings/go`

**Step 2: Initialize Go module**

Run: `cd bindings/go && go mod init github.com/yourusername/rlib-go`
Expected: Creates go.mod file

**Step 3: Write Go bindings**

Create `/Users/robertwendt/rlib/bindings/go/rlib.go`:

```go
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
```

**Step 4: Write Go tests**

Create `/Users/robertwendt/rlib/bindings/go/rlib_test.go`:

```go
package rlib

import "testing"

func TestAdd(t *testing.T) {
	tests := []struct {
		a, b, want int
	}{
		{2, 3, 5},
		{-1, 1, 0},
		{0, 0, 0},
	}

	for _, tt := range tests {
		got := Add(tt.a, tt.b)
		if got != tt.want {
			t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
		}
	}
}

func TestMultiply(t *testing.T) {
	tests := []struct {
		a, b, want int
	}{
		{2, 3, 6},
		{-2, 3, -6},
		{0, 5, 0},
	}

	for _, tt := range tests {
		got := Multiply(tt.a, tt.b)
		if got != tt.want {
			t.Errorf("Multiply(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
		}
	}
}

func TestDivide(t *testing.T) {
	tests := []struct {
		a, b, want int
	}{
		{6, 2, 3},
		{10, 5, 2},
		{-10, 2, -5},
	}

	for _, tt := range tests {
		got, err := Divide(tt.a, tt.b)
		if err != nil {
			t.Errorf("Divide(%d, %d) unexpected error: %v", tt.a, tt.b, err)
		}
		if got != tt.want {
			t.Errorf("Divide(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
		}
	}
}

func TestDivideByZero(t *testing.T) {
	_, err := Divide(10, 0)
	if err == nil {
		t.Error("Divide(10, 0) expected error, got nil")
	}
	if err.Error() != "Division by zero" {
		t.Errorf("Divide(10, 0) error = %q; want %q", err.Error(), "Division by zero")
	}
}
```

**Step 5: Run Go tests**

Run: `cd bindings/go && CGO_ENABLED=1 go test -v`
Expected: PASS - all tests pass

**Step 6: Return to root directory**

Run: `cd ../..`

**Step 7: Commit**

```bash
git add bindings/go/
git commit -m "feat(go): add Go bindings with cgo"
```

---

## Task 6: Create Node.js Bindings

**Files:**
- Create: `bindings/node/package.json`
- Create: `bindings/node/index.js`
- Create: `bindings/node/index.d.ts`
- Create: `bindings/node/test/test.js`

**Step 1: Create Node directory**

Run: `mkdir -p bindings/node/test`

**Step 2: Write package.json**

Create `/Users/robertwendt/rlib/bindings/node/package.json`:

```json
{
  "name": "@rlib/rlib",
  "version": "0.1.0",
  "description": "Multi-language Rust library - Node.js bindings",
  "main": "index.js",
  "types": "index.d.ts",
  "scripts": {
    "test": "node test/test.js"
  },
  "keywords": ["rust", "ffi", "bindings"],
  "author": "rlib contributors",
  "license": "MIT OR Apache-2.0",
  "dependencies": {
    "ffi-napi": "^4.0.3",
    "ref-napi": "^3.0.3"
  }
}
```

**Step 3: Write Node.js bindings**

Create `/Users/robertwendt/rlib/bindings/node/index.js`:

```javascript
const ffi = require('ffi-napi');
const ref = require('ref-napi');
const path = require('path');
const os = require('os');

// Determine library extension
let libExt;
if (os.platform() === 'darwin') {
  libExt = 'dylib';
} else if (os.platform() === 'win32') {
  libExt = 'dll';
} else {
  libExt = 'so';
}

// Try multiple library locations
const libLocations = [
  path.join(__dirname, `librlib.${libExt}`),
  path.join(__dirname, '..', '..', 'target', 'release', `librlib.${libExt}`),
];

let libPath = null;
for (const loc of libLocations) {
  try {
    require('fs').accessSync(loc);
    libPath = loc;
    break;
  } catch (e) {
    // Continue to next location
  }
}

if (!libPath) {
  throw new Error(`Could not find librlib.${libExt} in any expected location`);
}

// Load shared library
const lib = ffi.Library(libPath, {
  'rlib_add': ['int', ['int', 'int']],
  'rlib_multiply': ['int', ['int', 'int']],
  'rlib_divide': ['int', ['int', 'int', ref.refType('int')]],
  'rlib_error_message': ['string', ['int']]
});

const RlibError = {
  OK: 0,
  DIVISION_BY_ZERO: 1,
  INVALID_ARGUMENT: 2
};

function add(a, b) {
  return lib.rlib_add(a, b);
}

function multiply(a, b) {
  return lib.rlib_multiply(a, b);
}

function divide(a, b) {
  const result = ref.alloc('int');
  const error = lib.rlib_divide(a, b, result);

  if (error !== RlibError.OK) {
    const msg = lib.rlib_error_message(error);
    throw new Error(msg);
  }

  return result.deref();
}

module.exports = { add, multiply, divide };
```

**Step 4: Write TypeScript definitions**

Create `/Users/robertwendt/rlib/bindings/node/index.d.ts`:

```typescript
/**
 * Add two integers
 */
export function add(a: number, b: number): number;

/**
 * Multiply two integers
 */
export function multiply(a: number, b: number): number;

/**
 * Divide two integers
 * @throws {Error} If division by zero
 */
export function divide(a: number, b: number): number;
```

**Step 5: Write Node.js tests**

Create `/Users/robertwendt/rlib/bindings/node/test/test.js`:

```javascript
const assert = require('assert');
const rlib = require('..');

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
  } catch (err) {
    console.error(`✗ ${name}`);
    console.error(err);
    process.exit(1);
  }
}

test('add', () => {
  assert.strictEqual(rlib.add(2, 3), 5);
  assert.strictEqual(rlib.add(-1, 1), 0);
  assert.strictEqual(rlib.add(0, 0), 0);
});

test('multiply', () => {
  assert.strictEqual(rlib.multiply(2, 3), 6);
  assert.strictEqual(rlib.multiply(-2, 3), -6);
  assert.strictEqual(rlib.multiply(0, 5), 0);
});

test('divide', () => {
  assert.strictEqual(rlib.divide(6, 2), 3);
  assert.strictEqual(rlib.divide(10, 5), 2);
  assert.strictEqual(rlib.divide(-10, 2), -5);
});

test('divide by zero', () => {
  try {
    rlib.divide(10, 0);
    throw new Error('Expected error for division by zero');
  } catch (err) {
    assert.strictEqual(err.message, 'Division by zero');
  }
});

console.log('\nAll tests passed!');
```

**Step 6: Install Node dependencies**

Run: `cd bindings/node && npm install`
Expected: Installs ffi-napi and ref-napi

**Step 7: Run Node tests**

Run: `npm test`
Expected: PASS - "All tests passed!"

**Step 8: Return to root directory**

Run: `cd ../..`

**Step 9: Commit**

```bash
git add bindings/node/
git commit -m "feat(node): add Node.js bindings with ffi-napi"
```

---

## Task 7: Create C++ Wrapper

**Files:**
- Create: `bindings/cpp/rlib.hpp`
- Create: `bindings/cpp/tests/test_rlib.cpp`

**Step 1: Create C++ directory**

Run: `mkdir -p bindings/cpp/tests`

**Step 2: Write C++ header wrapper**

Create `/Users/robertwendt/rlib/bindings/cpp/rlib.hpp`:

```cpp
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
```

**Step 3: Write C++ tests**

Create `/Users/robertwendt/rlib/bindings/cpp/tests/test_rlib.cpp`:

```cpp
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
```

**Step 4: Create Makefile for C++ tests**

Create `/Users/robertwendt/rlib/bindings/cpp/tests/Makefile`:

```makefile
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I../../../include
LDFLAGS = -L../../../target/release -lrlib

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -Wl,-rpath,@loader_path/../../../target/release
else
    LDFLAGS += -Wl,-rpath,$$ORIGIN/../../../target/release
endif

test_rlib: test_rlib.cpp
	$(CXX) $(CXXFLAGS) -o test_rlib test_rlib.cpp $(LDFLAGS)

test: test_rlib
	./test_rlib

clean:
	rm -f test_rlib

.PHONY: test clean
```

**Step 5: Build and run C++ tests**

Run: `cd bindings/cpp/tests && make test`
Expected: PASS - "All tests passed!"

**Step 6: Clean and return to root**

Run: `make clean && cd ../../..`

**Step 7: Commit**

```bash
git add bindings/cpp/
git commit -m "feat(cpp): add C++ header wrapper with RAII"
```

---

## Task 8: Create Examples

**Files:**
- Create: `examples/c/example.c`
- Create: `examples/c/Makefile`
- Create: `examples/cpp/example.cpp`
- Create: `examples/cpp/Makefile`
- Create: `examples/go/example.go`
- Create: `examples/python/example.py`
- Create: `examples/node/example.js`

**Step 1: Create example directories**

Run: `mkdir -p examples/{c,cpp,go,python,node}`

**Step 2: Write C example**

Create `/Users/robertwendt/rlib/examples/c/example.c`:

```c
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
```

**Step 3: Write C Makefile**

Create `/Users/robertwendt/rlib/examples/c/Makefile`:

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -I../../include
LDFLAGS = -L../../target/release -lrlib

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -Wl,-rpath,@loader_path/../../target/release
else
    LDFLAGS += -Wl,-rpath,$$ORIGIN/../../target/release
endif

example: example.c
	$(CC) $(CFLAGS) -o example example.c $(LDFLAGS)

run: example
	./example

clean:
	rm -f example

.PHONY: run clean
```

**Step 4: Write C++ example**

Create `/Users/robertwendt/rlib/examples/cpp/example.cpp`:

```cpp
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
```

**Step 5: Write C++ Makefile**

Create `/Users/robertwendt/rlib/examples/cpp/Makefile`:

```makefile
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I../../include
LDFLAGS = -L../../target/release -lrlib

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -Wl,-rpath,@loader_path/../../target/release
else
    LDFLAGS += -Wl,-rpath,$$ORIGIN/../../target/release
endif

example: example.cpp
	$(CXX) $(CXXFLAGS) -o example example.cpp $(LDFLAGS)

run: example
	./example

clean:
	rm -f example

.PHONY: run clean
```

**Step 6: Write Go example**

Create `/Users/robertwendt/rlib/examples/go/example.go`:

```go
package main

import (
	"fmt"
	"log"

	rlib "../../bindings/go"
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
```

**Step 7: Write Python example**

Create `/Users/robertwendt/rlib/examples/python/example.py`:

```python
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
```

**Step 8: Make Python example executable**

Run: `chmod +x examples/python/example.py`

**Step 9: Write Node.js example**

Create `/Users/robertwendt/rlib/examples/node/example.js`:

```javascript
#!/usr/bin/env node
const path = require('path');
const rlib = require('../../bindings/node');

console.log('rlib Node.js Example');
console.log('====================');
console.log();

// Test add
const sum = rlib.add(10, 5);
console.log(`10 + 5 = ${sum}`);

// Test multiply
const product = rlib.multiply(10, 5);
console.log(`10 * 5 = ${product}`);

// Test divide (success)
const quotient = rlib.divide(10, 5);
console.log(`10 / 5 = ${quotient}`);

// Test divide by zero
try {
  rlib.divide(10, 0);
} catch (err) {
  console.log(`10 / 0 error: ${err.message}`);
}
```

**Step 10: Make Node.js example executable**

Run: `chmod +x examples/node/example.js`

**Step 11: Test C example**

Run: `cd examples/c && make run && make clean && cd ../..`
Expected: Prints output showing math operations

**Step 12: Test C++ example**

Run: `cd examples/cpp && make run && make clean && cd ../..`
Expected: Prints output showing math operations

**Step 13: Test Python example**

Run: `python3 examples/python/example.py`
Expected: Prints output showing math operations

**Step 14: Test Node.js example**

Run: `node examples/node/example.js`
Expected: Prints output showing math operations

**Step 15: Commit**

```bash
git add examples/
git commit -m "feat(examples): add usage examples for all languages"
```

---

## Task 9: Create Nix Flake

**Files:**
- Create: `flake.nix`
- Create: `flake.lock`
- Create: `.envrc` (optional direnv integration)

**Step 1: Write flake.nix**

Create `/Users/robertwendt/rlib/flake.nix`:

```nix
{
  description = "rlib - Multi-language Rust library";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, rust-overlay, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };

        rustToolchain = pkgs.rust-bin.stable.latest.default.override {
          extensions = [ "rust-src" "rust-analyzer" ];
        };

        # FFI shared library
        rlib-ffi = pkgs.rustPlatform.buildRustPackage {
          pname = "rlib-ffi";
          version = "0.1.0";
          src = ./.;

          cargoLock = {
            lockFile = ./Cargo.lock;
          };

          nativeBuildInputs = with pkgs; [
            cbindgen
          ];

          buildPhase = ''
            cargo build --release -p rlib-ffi
            mkdir -p include
            cbindgen ffi/ -o include/rlib.h
          '';

          installPhase = ''
            mkdir -p $out/lib $out/include
            cp target/release/librlib${pkgs.stdenv.hostPlatform.extensions.sharedLibrary} $out/lib/
            cp include/rlib.h $out/include/
          '';
        };

        # Python package
        rlib-python = pkgs.python3Packages.buildPythonPackage {
          pname = "rlib";
          version = "0.1.0";
          src = ./bindings/python;

          propagatedBuildInputs = [ rlib-ffi ];

          postInstall = ''
            mkdir -p $out/${pkgs.python3.sitePackages}/rlib
            cp ${rlib-ffi}/lib/librlib${pkgs.stdenv.hostPlatform.extensions.sharedLibrary} \
               $out/${pkgs.python3.sitePackages}/rlib/
          '';

          pythonImportsCheck = [ "rlib" ];
        };

        # Node.js package
        rlib-node = pkgs.buildNpmPackage {
          pname = "rlib";
          version = "0.1.0";
          src = ./bindings/node;

          npmDepsHash = pkgs.lib.fakeHash;

          buildInputs = [ rlib-ffi ];

          postInstall = ''
            mkdir -p $out/lib/node_modules/@rlib/rlib
            cp ${rlib-ffi}/lib/librlib${pkgs.stdenv.hostPlatform.extensions.sharedLibrary} \
               $out/lib/node_modules/@rlib/rlib/
          '';
        };

      in {
        packages = {
          default = rlib-ffi;
          ffi = rlib-ffi;
          python = rlib-python;
          node = rlib-node;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            rustToolchain
            cbindgen
            cargo-watch

            # Language tools
            python3
            python3Packages.pytest
            go
            nodejs

            # Build tools
            gcc
            gnumake
          ];

          shellHook = ''
            echo "🦀 rlib development environment"
            echo ""
            echo "Available commands:"
            echo "  cargo test -p rlib-core        # Test core Rust"
            echo "  cargo build -p rlib-ffi        # Build FFI layer"
            echo "  cbindgen ffi/ -o include/rlib.h  # Generate header"
            echo "  nix build .#python             # Build Python package"
            echo "  nix build .#node               # Build Node package"
            echo ""

            export LD_LIBRARY_PATH="$PWD/target/release:$LD_LIBRARY_PATH"
            export DYLD_LIBRARY_PATH="$PWD/target/release:$DYLD_LIBRARY_PATH"
          '';
        };

        apps = {
          test-all = {
            type = "app";
            program = toString (pkgs.writeShellScript "test-all" ''
              set -e

              echo "Testing Rust core..."
              ${rustToolchain}/bin/cargo test -p rlib-core

              echo ""
              echo "Testing Rust FFI..."
              ${rustToolchain}/bin/cargo test -p rlib-ffi

              echo ""
              echo "Building FFI library..."
              ${rustToolchain}/bin/cargo build --release -p rlib-ffi

              echo ""
              echo "Generating C header..."
              mkdir -p include
              ${pkgs.cbindgen}/bin/cbindgen ffi/ -o include/rlib.h

              echo ""
              echo "Testing Python bindings..."
              cd bindings/python
              ${pkgs.python3}/bin/python -m pytest tests/ -v
              cd ../..

              echo ""
              echo "Testing Go bindings..."
              cd bindings/go
              CGO_ENABLED=1 ${pkgs.go}/bin/go test -v
              cd ../..

              echo ""
              echo "Testing Node.js bindings..."
              cd bindings/node
              ${pkgs.nodejs}/bin/npm test
              cd ../..

              echo ""
              echo "Testing C++ bindings..."
              cd bindings/cpp/tests
              ${pkgs.gnumake}/bin/make test
              ${pkgs.gnumake}/bin/make clean
              cd ../../..

              echo ""
              echo "✓ All tests passed!"
            '');
          };
        };
      }
    );
}
```

**Step 2: Generate Cargo.lock**

Run: `cargo generate-lockfile`
Expected: Creates Cargo.lock file

**Step 3: Initialize Nix flake**

Run: `nix flake update`
Expected: Creates flake.lock

**Step 4: Enter Nix dev shell to verify**

Run: `nix develop`
Expected: Enters shell with all development tools

**Step 5: Exit dev shell**

Run: `exit`

**Step 6: Create .envrc for direnv (optional)**

Create `/Users/robertwendt/rlib/.envrc`:

```bash
use flake
```

**Step 7: Commit**

```bash
git add flake.nix flake.lock Cargo.lock .envrc
git commit -m "feat(nix): add Nix flake for reproducible builds"
```

---

## Task 10: Create README and Documentation

**Files:**
- Create: `README.md`
- Create: `LICENSE-MIT`
- Create: `LICENSE-APACHE`

**Step 1: Write README**

Create `/Users/robertwendt/rlib/README.md`:

```markdown
# rlib

A multi-language Rust library demonstrating how to build once and distribute to multiple languages using C FFI.

## Features

- **Core logic in Rust** - Write business logic once in safe, fast Rust
- **C FFI layer** - Thin wrapper using cbindgen for maximum compatibility
- **Multiple language bindings** - C, C++, Go, Python, JavaScript/Node.js
- **Nix-based builds** - Reproducible builds and packaging
- **Comprehensive examples** - See usage in every supported language

## Supported Languages

- **C** - Direct FFI usage
- **C++** - Header-only wrapper with RAII and exceptions
- **Go** - cgo bindings with idiomatic error handling
- **Python** - ctypes wrapper with Pythonic API
- **JavaScript/Node.js** - ffi-napi bindings

## Quick Start

### Using Nix (Recommended)

```bash
# Enter development environment
nix develop

# Build FFI library
cargo build --release -p rlib-ffi

# Generate C header
cbindgen ffi/ -o include/rlib.h

# Run all tests
nix run .#test-all
```

### Manual Build

Requirements:
- Rust (1.70+)
- cbindgen
- Python 3.7+
- Go 1.18+
- Node.js 14+
- GCC/Clang

```bash
# Build core and FFI
cargo build --release

# Generate header
cbindgen ffi/ -o include/rlib.h

# Test Rust
cargo test

# Test Python
cd bindings/python && python -m pytest

# Test Go
cd bindings/go && CGO_ENABLED=1 go test

# Test Node.js
cd bindings/node && npm install && npm test
```

## Usage Examples

### C

```c
#include "rlib.h"

int main() {
    int sum = rlib_add(10, 5);

    int quotient;
    rlib_error_t err = rlib_divide(10, 5, &quotient);
    if (err == Ok) {
        printf("Result: %d\n", quotient);
    }
}
```

### C++

```cpp
#include "rlib.hpp"

int main() {
    int sum = rlib::add(10, 5);

    try {
        int quotient = rlib::divide(10, 5);
    } catch (const rlib::Error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}
```

### Go

```go
import rlib "github.com/yourusername/rlib-go"

sum := rlib.Add(10, 5)

quotient, err := rlib.Divide(10, 5)
if err != nil {
    log.Fatal(err)
}
```

### Python

```python
import rlib

sum_result = rlib.add(10, 5)

try:
    quotient = rlib.divide(10, 5)
except ValueError as e:
    print(f"Error: {e}")
```

### JavaScript/Node.js

```javascript
const rlib = require('@rlib/rlib');

const sum = rlib.add(10, 5);

try {
    const quotient = rlib.divide(10, 5);
} catch (err) {
    console.error('Error:', err.message);
}
```

## Project Structure

```
rlib/
├── core/              # Pure Rust business logic
├── ffi/               # C FFI wrapper
├── bindings/          # Language-specific bindings
│   ├── python/
│   ├── node/
│   ├── go/
│   └── cpp/
├── examples/          # Usage examples
└── docs/              # Documentation and design docs
```

## Architecture

See [Design Document](docs/plans/2025-11-10-multi-language-rust-sdk-design.md) for detailed architecture.

**Key principles:**
- Core and FFI are separate Cargo crates
- cbindgen generates C headers from Rust
- Each language gets idiomatic wrapper around C FFI
- Nix provides reproducible builds

## Testing

```bash
# All tests
nix run .#test-all

# Individual layers
cargo test -p rlib-core
cargo test -p rlib-ffi
python -m pytest bindings/python/tests/
go test bindings/go/
npm test --prefix bindings/node
```

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.

## Contributing

Contributions welcome! This project demonstrates a pattern for building multi-language SDKs from Rust.
```

**Step 2: Write MIT License**

Create `/Users/robertwendt/rlib/LICENSE-MIT`:

```
MIT License

Copyright (c) 2025 rlib contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Step 3: Write Apache License**

Create `/Users/robertwendt/rlib/LICENSE-APACHE`:

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   [Standard Apache 2.0 License Text - Full text available at:
    https://www.apache.org/licenses/LICENSE-2.0.txt]

   Copyright 2025 rlib contributors

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

**Step 4: Commit**

```bash
git add README.md LICENSE-MIT LICENSE-APACHE
git commit -m "docs: add README and license files"
```

---

## Task 11: Final Integration Test

**Step 1: Clean build**

Run: `cargo clean`

**Step 2: Build release FFI**

Run: `cargo build --release -p rlib-ffi`
Expected: SUCCESS

**Step 3: Generate header**

Run: `mkdir -p include && cbindgen ffi/ -o include/rlib.h`
Expected: Creates include/rlib.h

**Step 4: Run all Rust tests**

Run: `cargo test --all`
Expected: PASS - all Rust tests pass

**Step 5: Test Python bindings**

Run: `cd bindings/python && python3 -m pytest tests/ -v && cd ../..`
Expected: PASS - all 4 Python tests pass

**Step 6: Test Go bindings**

Run: `cd bindings/go && CGO_ENABLED=1 go test -v && cd ../..`
Expected: PASS - all 4 Go tests pass

**Step 7: Test Node.js bindings**

Run: `cd bindings/node && npm test && cd ../..`
Expected: PASS - all tests pass

**Step 8: Test C++ bindings**

Run: `cd bindings/cpp/tests && make test && make clean && cd ../../..`
Expected: PASS - all tests pass

**Step 9: Run C example**

Run: `cd examples/c && make run && make clean && cd ../..`
Expected: Prints correct output

**Step 10: Run C++ example**

Run: `cd examples/cpp && make run && make clean && cd ../..`
Expected: Prints correct output

**Step 11: Run Python example**

Run: `python3 examples/python/example.py`
Expected: Prints correct output

**Step 12: Run Node.js example**

Run: `node examples/node/example.js`
Expected: Prints correct output

**Step 13: Run Go example (if CGO available)**

Run: `cd examples/go && CGO_ENABLED=1 go run example.go && cd ../..`
Expected: Prints correct output

**Step 14: Test Nix build (if Nix available)**

Run: `nix flake check`
Expected: All checks pass (or skip if Nix not available)

**Step 15: Final commit**

```bash
git add -A
git commit -m "chore: final integration test verification"
```

---

## Summary

You now have:
- ✅ Cargo workspace with core and FFI crates
- ✅ Pure Rust business logic (add, multiply, divide)
- ✅ C FFI layer with cbindgen
- ✅ Python bindings (ctypes)
- ✅ Go bindings (cgo)
- ✅ Node.js bindings (ffi-napi)
- ✅ C++ wrapper (header-only RAII)
- ✅ Examples for all languages
- ✅ Nix flake for reproducible builds
- ✅ Comprehensive tests at every layer
- ✅ Documentation (README, design doc, licenses)

## Next Steps

1. **Customize business logic** - Replace demo math functions with real functionality
2. **Add CI/CD** - GitHub Actions workflow for automated testing
3. **Publish packages** - PyPI (Python), npm (Node.js), crates.io (Rust)
4. **Cross-compilation** - Build for multiple platforms
5. **Performance benchmarks** - Compare FFI overhead across languages
6. **Static linking** - Provide .a static library option
7. **More languages** - Java/JNI, Ruby, C#

## Build Commands Reference

```bash
# Development
nix develop                    # Enter dev environment
cargo test --all               # Run all Rust tests
nix run .#test-all             # Run tests for all languages

# Building
cargo build --release          # Build release
cbindgen ffi/ -o include/rlib.h  # Generate header

# Packaging
nix build .#ffi                # Build FFI library
nix build .#python             # Build Python package
nix build .#node               # Build Node package
```
