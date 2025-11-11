# Multi-Language Rust SDK Design

**Date:** 2025-11-10
**Status:** Approved
**Author:** Design Session

## Overview

Design for `rlib`: a Rust library that compiles business logic to a shared library with C FFI, enabling distribution as SDKs for multiple programming languages (C, C++, Go, Python, JavaScript/Node.js).

## Goals

1. Write core business logic once in Rust
2. Distribute to 5+ languages via C FFI (cbindgen)
3. Use Nix for reproducible builds and SDK packaging
4. Provide idiomatic APIs for each target language
5. Maintain clean separation between core logic and FFI layer

## Non-Goals

- WASM bindings (eliminated due to runtime API limitations like HTTP requests)
- Native extensions (PyO3, Neon) - using pure FFI for maximum compatibility
- Dynamic language feature support (using C ABI keeps it simple)

## Architecture

### Approach: Separated Core and FFI Crates (Workspace)

```
rlib/
├── flake.nix                    # Nix build orchestration
├── Cargo.toml                   # Workspace root
├── core/                        # Pure Rust business logic
│   ├── Cargo.toml
│   └── src/lib.rs
├── ffi/                         # C FFI layer
│   ├── Cargo.toml
│   ├── cbindgen.toml
│   └── src/lib.rs
├── include/                     # Generated headers (built, not committed)
│   └── rlib.h
├── bindings/                    # Language-specific wrappers
│   ├── python/
│   │   ├── rlib/
│   │   │   ├── __init__.py
│   │   │   └── _ffi.py
│   │   ├── setup.py
│   │   └── tests/
│   ├── node/
│   │   ├── package.json
│   │   ├── index.js
│   │   └── test/
│   ├── go/
│   │   ├── go.mod
│   │   ├── rlib.go
│   │   └── rlib_test.go
│   └── cpp/
│       ├── rlib.hpp
│       └── tests/
└── examples/                    # Usage examples per language
    ├── c/
    ├── cpp/
    ├── go/
    ├── python/
    └── node/
```

### Key Architectural Decisions

**Decision 1: Workspace Separation**
- **Choice:** Separate `core` and `ffi` crates in Cargo workspace
- **Rationale:** Clean separation allows core to be pure Rust with zero FFI dependencies, faster iteration, independent testing
- **Alternative considered:** Single crate with feature flags (rejected: becomes messy as project scales)

**Decision 2: Pure C FFI via cbindgen**
- **Choice:** Use cbindgen to generate C headers from Rust code
- **Rationale:** Maximum language compatibility, single compilation target, no WASM limitations
- **Alternative considered:** WASM (rejected: runtime API limitations like HTTP requests, filesystem access)
- **Alternative considered:** Language-specific native extensions like PyO3/Neon (rejected: less portable, more complex build)

**Decision 3: Language Bindings as Wrappers**
- **Choice:** Each language gets idiomatic wrapper around C FFI (ctypes, cgo, ffi-napi, C++ RAII)
- **Rationale:** Hide pointer manipulation, provide native error handling, follow language conventions
- **Trade-off:** More code to maintain, but better developer experience

## Component Design

### Core Layer (`core/`)

**Purpose:** Pure Rust business logic with no FFI concerns

**Characteristics:**
- Crate type: `rlib` (Rust library only)
- Zero FFI dependencies
- Can use any Rust idioms (Result, Option, generics, traits)
- Fast compile times during development
- Independently testable with `cargo test`
- Publishable to crates.io

**Example:**
```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

pub fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}
```

### FFI Layer (`ffi/`)

**Purpose:** Thin C-compatible wrapper around core

**Characteristics:**
- Crate type: `cdylib` (shared library)
- Depends on `core` crate
- Uses `#[no_mangle]` and `extern "C"`
- Uses `cbindgen` to generate headers
- Error handling via error codes (enum)
- Memory safety: no heap allocation across FFI boundary

**Error Handling Pattern:**
```rust
#[repr(C)]
pub enum RlibError {
    Ok = 0,
    DivisionByZero = 1,
    InvalidArgument = 2,
}

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

**FFI Safety Principles:**
1. Use `std::os::raw::c_*` types for portability
2. Error codes instead of exceptions
3. Out-parameters for return values when errors are possible
4. All strings are `*const c_char` with null terminators
5. Validate all pointers before dereferencing
6. No complex types across FFI boundary (no Vec, String, HashMap)

### Language Bindings

Each language binding provides:
1. FFI wrapper that loads the shared library
2. Type mappings (C types to native types)
3. Idiomatic error handling (exceptions/Results/errors)
4. Memory management (hide pointer manipulation)
5. Language-native package structure

**Python** (`bindings/python/`):
- Uses `ctypes` to load `librlib.so`
- Wraps C error codes as Python exceptions
- Packaged with `setup.py` for PyPI distribution
- Bundles shared library in wheel

**Go** (`bindings/go/`):
- Uses `cgo` to call C functions
- Returns `error` type for Go error handling
- Distributed as Go module
- Users need `CGO_ENABLED=1` and library path set

**Node.js** (`bindings/node/`):
- Uses `ffi-napi` to load shared library
- Throws JavaScript `Error` for failures
- Published to npm registry
- Platform-specific binaries via `optionalDependencies`

**C++** (`bindings/cpp/`):
- Header-only wrapper with RAII
- Throws exceptions for error codes
- Provides namespace `rlib::`
- Distributed as header file

### Examples

Each language has a runnable example in `examples/`:
- Demonstrates API usage
- Tests that SDK packages work correctly
- Serves as documentation
- Validated in CI

## Build System

### Nix Flake

**Packages:**
- `rlib-core`: Pure Rust library (for testing)
- `rlib-ffi`: Shared library + C header
- `rlib-python`: Python wheel with bundled library
- `rlib-go`: Go module
- `rlib-node`: npm package

**Build Flow:**
1. `cargo build -p rlib-core` → Rust library
2. `cargo build -p rlib-ffi --release` → `librlib.so`/`.dylib`/`.dll`
3. `cbindgen ffi/ -o include/rlib.h` → C header
4. Package per-language SDKs with bundled shared library

**Developer Experience:**
```bash
nix develop              # Enter dev shell
cargo test -p rlib-core  # Test core logic
cargo build -p rlib-ffi  # Build FFI layer
cbindgen ffi/ -o include/rlib.h  # Generate header
nix build .#python       # Build Python SDK
nix run .#test-all       # Run all tests
```

**Reproducibility:**
- Same inputs → same outputs across machines
- Pinned dependencies via `flake.lock`
- No "works on my machine" issues

## Testing Strategy

### Multi-Level Testing

1. **Rust Unit Tests** (`core/src/lib.rs`)
   - Test pure business logic
   - Fast, no FFI overhead
   - Run: `cargo test -p rlib-core`

2. **FFI Integration Tests** (`ffi/tests/`)
   - Test C API directly
   - Validate cbindgen output
   - Ensure memory safety
   - Run: `cargo test -p rlib-ffi`

3. **Language-Specific Tests**
   - Python: `pytest` in `bindings/python/tests/`
   - Go: `go test` in `bindings/go/`
   - Node: `npm test` in `bindings/node/test/`
   - C++: Catch2/GoogleTest in `bindings/cpp/tests/`

4. **Example Tests**
   - Each example must compile and run
   - CI validates all examples
   - Prevents SDK packaging regressions

### Continuous Integration

GitHub Actions workflow:
```yaml
- Run all Rust tests (core + ffi)
- Build all Nix packages
- Run language-specific tests
- Run examples
- Check formatting and clippy
```

## Distribution

### Per-Language Distribution

**Python (PyPI):**
- Build platform-specific wheels (manylinux, macosx, win_amd64)
- Bundle `librlib.so` in wheel
- Install: `pip install rlib`

**Go (pkg.go.dev):**
- Publish as Go module
- Users set `CGO_ENABLED=1`
- Library in system path or statically linked

**Node.js (npm):**
- Publish to npm registry
- Platform-specific binaries via `optionalDependencies`
- Install: `npm install rlib`

**C/C++:**
- Manual distribution of header + library
- Link with `-lrlib`

**Nix Users:**
- Build from source: `nix build github:you/rlib#python`
- Use as flake input
- Fully reproducible

## Trade-offs

### Advantages
- Maximum language compatibility (any language with C FFI)
- Clean separation of concerns (core vs FFI)
- Single compilation target (shared library)
- No WASM runtime limitations
- Testable at every layer
- Reproducible builds via Nix

### Disadvantages
- More code to maintain (bindings per language)
- FFI restrictions (no complex types across boundary)
- Less ergonomic than native extensions
- Manual memory management visible to some callers
- Error handling via error codes (less type-safe)

## Success Criteria

1. Core Rust logic callable from C, C++, Go, Python, JavaScript/Node
2. Nix builds reproducible shared libraries
3. Nix packages distributable SDKs per language
4. Examples demonstrate usage in each target language
5. Comprehensive tests at every layer
6. Documentation covers setup and usage

## Future Considerations

### Potential Additions
- Java/JNI bindings
- C# bindings
- Ruby bindings via FFI gem
- Static linking option (`.a` library)
- Cross-compilation for embedded targets

### Maintenance
- Versioning strategy for breaking changes
- Release automation
- Documentation site
- Performance benchmarks per language

## References

- cbindgen: https://github.com/mozilla/cbindgen
- Rust FFI Guide: https://doc.rust-lang.org/nomicon/ffi.html
- Nix Flakes: https://nixos.wiki/wiki/Flakes
