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
