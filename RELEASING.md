# Release Process

This document describes how to create a new release of rlib across all language bindings.

## Prerequisites

Before creating a release, ensure:

1. All tests pass: `nix run .#test-all`
2. CHANGELOG.md is updated with the new version
3. Version numbers are updated in:
   - `core/Cargo.toml`
   - `ffi/Cargo.toml`
   - `bindings/python/setup.py`
   - `bindings/node/package.json`
4. You have the necessary API tokens configured as GitHub secrets:
   - `PYPI_API_TOKEN` - For publishing to PyPI
   - `NPM_TOKEN` - For publishing to npm

## Creating a Release

### 1. Update Version Numbers

Update the version in all package files:

```bash
# Update Cargo.toml files
vim core/Cargo.toml   # Update version
vim ffi/Cargo.toml    # Update version

# Python (version is read from env in CI, but update default)
vim bindings/python/setup.py

# Node.js
vim bindings/node/package.json
```

### 2. Update Changelog

Add release notes to CHANGELOG.md:

```markdown
## [0.2.0] - 2025-11-11

### Added
- New function: subtract()
- Support for Windows ARM64

### Changed
- Improved error messages

### Fixed
- Memory leak in divide function
```

### 3. Commit and Tag

```bash
# Commit version changes
git add -A
git commit -m "chore: bump version to 0.2.0"

# Create and push tag
git tag v0.2.0
git push origin master
git push origin v0.2.0
```

### 4. GitHub Actions Workflow

Pushing the tag triggers the release workflow (`.github/workflows/release.yml`) which:

1. **Builds FFI libraries** for multiple platforms:
   - Linux (x86_64)
   - macOS (x86_64, ARM64)
   - Windows (x86_64)

2. **Generates C header** using cbindgen

3. **Publishes Python package** to PyPI:
   - Builds wheel with bundled FFI libraries
   - Publishes automatically if `PYPI_API_TOKEN` is configured

4. **Publishes Node.js package** to npm:
   - Packages with bundled FFI libraries
   - Publishes automatically if `NPM_TOKEN` is configured

5. **Tags Go module**:
   - Creates `bindings/go/v0.2.0` tag for Go module versioning

6. **Creates GitHub Release**:
   - Attaches pre-built FFI libraries
   - Includes release notes
   - Links to published packages

## Manual Release (Without GitHub Actions)

If you need to release manually:

### Build FFI Libraries

```bash
# Linux
cargo build --release --target x86_64-unknown-linux-gnu -p rlib-ffi

# macOS x86_64
cargo build --release --target x86_64-apple-darwin -p rlib-ffi

# macOS ARM64
cargo build --release --target aarch64-apple-darwin -p rlib-ffi

# Windows
cargo build --release --target x86_64-pc-windows-msvc -p rlib-ffi
```

### Generate Header

```bash
cbindgen ffi/ -o include/rlib.h
```

### Publish Python Package

```bash
cd bindings/python

# Create lib directory and copy FFI libraries
mkdir -p rlib/lib
cp ../../target/release/librlib.so rlib/lib/  # Linux
cp ../../target/release/librlib.dylib rlib/lib/  # macOS
cp ../../target/release/rlib.dll rlib/lib/  # Windows

# Build and publish
python -m build
twine upload dist/*
```

### Publish Node.js Package

```bash
cd bindings/node

# Create lib directory and copy FFI libraries
mkdir -p lib
cp ../../target/release/librlib.so lib/  # Linux
cp ../../target/release/librlib.dylib lib/  # macOS
cp ../../target/release/rlib.dll lib/  # Windows

# Publish
npm publish
```

### Tag Go Module

```bash
git tag bindings/go/v0.2.0
git push origin bindings/go/v0.2.0
```

## Verifying the Release

After release, verify each package:

### Python
```bash
pip install rlib==0.2.0
python -c "import rlib; print(rlib.add(2, 3))"
```

### Node.js
```bash
npm install @rlib/rlib@0.2.0
node -e "const rlib = require('@rlib/rlib'); console.log(rlib.add(2, 3))"
```

### Go
```bash
go get github.com/r33drichards/rlib-go@bindings/go/v0.2.0
# Test in a Go program
```

### C/C++
Download artifacts from GitHub Release and test compilation.

## Rollback

If you need to rollback a release:

1. **PyPI**: Cannot delete, but can yank: `twine yank rlib 0.2.0`
2. **npm**: Can unpublish within 72 hours: `npm unpublish @rlib/rlib@0.2.0`
3. **Go**: Delete the Git tag: `git push origin :bindings/go/v0.2.0`
4. **GitHub Release**: Delete from GitHub UI

## Troubleshooting

### Python Package Won't Build
- Ensure FFI libraries exist in `bindings/python/rlib/lib/`
- Check that `MANIFEST.in` includes lib files
- Verify `setup.py` has `package_data` configured

### Node.js Package Missing Libraries
- Check `package.json` `files` field includes `lib/*`
- Ensure libraries exist in `bindings/node/lib/`

### Go Module Not Found
- Verify tag format: `bindings/go/v0.2.0`
- Check that tag is pushed: `git ls-remote --tags origin`
- Wait a few minutes for Go module proxy to update

### GitHub Actions Fails
- Check secrets are configured: `PYPI_API_TOKEN`, `NPM_TOKEN`
- Review workflow logs in GitHub Actions tab
- Ensure all tests pass before tagging
