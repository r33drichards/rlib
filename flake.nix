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
            rust-cbindgen
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
          buildInputs = [
            rustToolchain
            pkgs.rust-cbindgen
            pkgs.cargo-watch

            # Language tools
            pkgs.python3
            pkgs.python3Packages.pytest
            pkgs.go
            pkgs.nodejs

            # Build tools
            pkgs.gcc
            pkgs.gnumake
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
