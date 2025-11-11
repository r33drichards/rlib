# Contributing to rlib

Thank you for your interest in contributing to rlib! This document explains how to add new functionality to the library and expose it across all supported languages.

## Table of Contents

- [Development Setup](#development-setup)
- [Adding a New Function](#adding-a-new-function)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Development Setup

### Prerequisites

- **Nix** (recommended) - Provides reproducible development environment
- **OR** Manual setup:
  - Rust 1.70+
  - cbindgen
  - Python 3.7+
  - Go 1.18+
  - Node.js 14+
  - GCC/Clang

### Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/rlib.git
cd rlib

# Enter development environment (Nix)
nix develop

# OR manually ensure all tools are installed
cargo --version
cbindgen --version
python3 --version
go version
node --version
```

## Adding a New Function

Follow this workflow to add a new function that's available in all supported languages. We'll use Test-Driven Development (TDD) throughout.

> **Real-world example:** See commit [`e27f782`](https://github.com/yourusername/rlib/commit/e27f782) which added the `exponent` function following this exact guide. It demonstrates the complete workflow from Core Rust to all language bindings with tests.

### Example: Adding a `subtract` function

#### Step 1: Add to Core Rust Library (with TDD)

**File:** `core/src/lib.rs`

1. **Write the failing test first:**

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // ... existing tests ...

    #[test]
    fn test_subtract() {
        assert_eq!(subtract(10, 5), 5);
        assert_eq!(subtract(0, 5), -5);
        assert_eq!(subtract(-10, -5), -5);
    }
}
```

2. **Add the function signature with `todo!()`:**

```rust
/// Subtract two integers
pub fn subtract(a: i32, b: i32) -> i32 {
    todo!("implement subtract")
}
```

3. **Run the test to verify it fails:**

```bash
cargo test -p rlib-core
# Should see: "not yet implemented: implement subtract"
```

4. **Implement the function:**

```rust
/// Subtract two integers
pub fn subtract(a: i32, b: i32) -> i32 {
    a - b
}
```

5. **Run the test to verify it passes:**

```bash
cargo test -p rlib-core
# Should see: test tests::test_subtract ... ok
```

#### Step 2: Add to FFI Layer

**File:** `ffi/src/lib.rs`

Add the C-compatible wrapper:

```rust
/// Subtract two integers
#[no_mangle]
pub extern "C" fn rlib_subtract(a: c_int, b: c_int) -> c_int {
    rlib_core::subtract(a, b)
}
```

#### Step 3: Regenerate C Header

```bash
# Generate the updated header
cbindgen ffi/ -o include/rlib.h

# Verify the new function appears in the header
grep rlib_subtract include/rlib.h
```

Expected output in `include/rlib.h`:
```c
/**
 * Subtract two integers
 */
int32_t rlib_subtract(int32_t a, int32_t b);
```

#### Step 4: Update Language Bindings

##### Python (`bindings/python/rlib/_ffi.py`)

1. **Add function signature:**

```python
# Define function signatures
_lib.rlib_subtract.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.rlib_subtract.restype = ctypes.c_int
```

2. **Add Python wrapper:**

```python
def subtract(a: int, b: int) -> int:
    """Subtract two integers."""
    return _lib.rlib_subtract(a, b)
```

3. **Export from package (`bindings/python/rlib/__init__.py`):**

```python
from rlib._ffi import add, multiply, divide, subtract

__version__ = "0.1.0"
__all__ = ["add", "multiply", "divide", "subtract"]
```

4. **Add test (`bindings/python/tests/test_rlib.py`):**

```python
def test_subtract():
    """Test subtraction function."""
    assert rlib.subtract(10, 5) == 5
    assert rlib.subtract(0, 5) == -5
    assert rlib.subtract(-10, -5) == -5
```

5. **Run Python tests:**

```bash
cd bindings/python
PYTHONPATH=. pytest tests/ -v
cd ../..
```

##### Go (`bindings/go/rlib.go`)

1. **Add Go wrapper:**

```go
// Subtract two integers
func Subtract(a, b int) int {
	return int(C.rlib_subtract(C.int(a), C.int(b)))
}
```

2. **Add test (`bindings/go/rlib_test.go`):**

```go
func TestSubtract(t *testing.T) {
	tests := []struct {
		a, b, want int
	}{
		{10, 5, 5},
		{0, 5, -5},
		{-10, -5, -5},
	}

	for _, tt := range tests {
		got := Subtract(tt.a, tt.b)
		if got != tt.want {
			t.Errorf("Subtract(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
		}
	}
}
```

3. **Run Go tests:**

```bash
cd bindings/go
CGO_ENABLED=1 go test -v
cd ../..
```

##### Node.js (`bindings/node/index.js`)

1. **Add to FFI library definition:**

```javascript
const lib = ffi.Library(libPath, {
  'rlib_add': ['int', ['int', 'int']],
  'rlib_multiply': ['int', ['int', 'int']],
  'rlib_subtract': ['int', ['int', 'int']],  // Add this
  'rlib_divide': ['int', ['int', 'int', ref.refType('int')]],
  'rlib_error_message': ['string', ['int']]
});
```

2. **Add JavaScript wrapper:**

```javascript
function subtract(a, b) {
  return lib.rlib_subtract(a, b);
}

module.exports = { add, multiply, subtract, divide };  // Export it
```

3. **Add TypeScript definition (`bindings/node/index.d.ts`):**

```typescript
/**
 * Subtract two integers
 */
export function subtract(a: number, b: number): number;
```

4. **Add test (`bindings/node/test/test.js`):**

```javascript
test('subtract', () => {
  assert.strictEqual(rlib.subtract(10, 5), 5);
  assert.strictEqual(rlib.subtract(0, 5), -5);
  assert.strictEqual(rlib.subtract(-10, -5), -5);
});
```

5. **Run Node.js tests:**

```bash
cd bindings/node
npm test
cd ../..
```

##### C++ (`bindings/cpp/rlib.hpp`)

1. **Add inline function:**

```cpp
/**
 * Subtract two integers
 */
inline int subtract(int a, int b) {
    return rlib_subtract(a, b);
}
```

2. **Add test (`bindings/cpp/tests/test_rlib.cpp`):**

```cpp
void test_subtract() {
    assert(rlib::subtract(10, 5) == 5);
    assert(rlib::subtract(0, 5) == -5);
    assert(rlib::subtract(-10, -5) == -5);
    std::cout << "✓ test_subtract" << std::endl;
}

int main() {
    test_add();
    test_multiply();
    test_subtract();  // Call the new test
    test_divide();
    test_divide_by_zero();
    std::cout << "\nAll tests passed!" << std::endl;
    return 0;
}
```

3. **Run C++ tests:**

```bash
cd bindings/cpp/tests
make test
make clean
cd ../../..
```

#### Step 5: Update Examples (Optional)

Add usage of the new function to examples:

- `examples/c/example.c`
- `examples/cpp/example.cpp`
- `examples/go/example.go`
- `examples/python/example.py`
- `examples/node/example.js`

#### Step 6: Run Full Test Suite

```bash
# Run all tests via Nix
nix run .#test-all

# OR manually run each
cargo test --all
cd bindings/python && PYTHONPATH=. pytest tests/ -v && cd ../..
cd bindings/go && CGO_ENABLED=1 go test -v && cd ../..
cd bindings/node && npm test && cd ../..
cd bindings/cpp/tests && make test && make clean && cd ../../..
```

#### Step 7: Commit Your Changes

```bash
git add core/ ffi/ include/ bindings/ examples/
git commit -m "feat: add subtract function

- Add subtract(a, b) to core library with tests
- Add rlib_subtract to FFI layer
- Update C header with cbindgen
- Add bindings for Python, Go, Node.js, C++
- Update examples to demonstrate subtract
- All tests passing (25/25)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Testing

### Test Organization

- **Rust Core Tests:** `core/src/lib.rs` (in `#[cfg(test)]` module)
- **Python Tests:** `bindings/python/tests/test_rlib.py`
- **Go Tests:** `bindings/go/rlib_test.go`
- **Node.js Tests:** `bindings/node/test/test.js`
- **C++ Tests:** `bindings/cpp/tests/test_rlib.cpp`

### Running Tests

```bash
# All tests at once
nix run .#test-all

# Individual test suites
cargo test -p rlib-core              # Rust core
cargo test -p rlib-ffi               # Rust FFI
cd bindings/python && pytest         # Python
cd bindings/go && go test            # Go
cd bindings/node && npm test         # Node.js
cd bindings/cpp/tests && make test   # C++
```

## Handling Complex Types

### Functions with Error Handling

For functions that can fail, use the same pattern as `divide`:

**Core (Rust):**
```rust
pub fn risky_operation(input: i32) -> Result<i32, String> {
    if input < 0 {
        Err("Input must be non-negative".to_string())
    } else {
        Ok(input * 2)
    }
}
```

**FFI:**
```rust
#[no_mangle]
pub extern "C" fn rlib_risky_operation(input: c_int, result: *mut c_int) -> RlibError {
    if result.is_null() {
        return RlibError::InvalidArgument;
    }

    match rlib_core::risky_operation(input) {
        Ok(val) => {
            unsafe { *result = val; }
            RlibError::Ok
        }
        Err(_) => RlibError::InvalidArgument,  // Or add a new error variant
    }
}
```

**Language bindings then convert the error code to native error handling** (exceptions in Python/C++/JavaScript, error returns in Go).

## Adding New Error Types

If you need a new error variant:

1. Add to `RlibError` enum in `ffi/src/lib.rs`
2. Update `rlib_error_message` function
3. Regenerate header with `cbindgen`
4. Update error handling in all language bindings

## Code Style

- **Rust:** Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- **Python:** Follow [PEP 8](https://pep8.org/)
- **Go:** Follow [Effective Go](https://go.dev/doc/effective_go)
- **JavaScript:** Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **C++:** Follow [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)

## Submitting Changes

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feat/subtract-function`
3. **Follow the steps above** to add your function across all layers
4. **Ensure all tests pass**: `nix run .#test-all`
5. **Commit with conventional commits**: `feat:`, `fix:`, `docs:`, etc.
6. **Push** to your fork: `git push origin feat/subtract-function`
7. **Open a Pull Request** with:
   - Clear description of what you added
   - Test results showing all tests pass
   - Any relevant documentation updates

## Getting Help

- **Issues:** Open an issue on GitHub for bugs or feature requests
- **Questions:** Use GitHub Discussions for questions about the architecture
- **Design Docs:** See `docs/plans/` for detailed architecture documentation

## License

By contributing, you agree that your contributions will be licensed under the same terms as the project (MIT OR Apache-2.0).
