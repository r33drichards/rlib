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

_lib.rlib_exponent.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.rlib_exponent.restype = ctypes.c_int

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

def exponent(base: int, exp: int) -> int:
    """Raise base to the power of exponent."""
    return _lib.rlib_exponent(base, exp)

def divide(a: int, b: int) -> int:
    """Divide two integers. Raises ValueError on division by zero."""
    result = ctypes.c_int()
    error = _lib.rlib_divide(a, b, ctypes.byref(result))
    if error != RlibError.OK:
        msg = _lib.rlib_error_message(error).decode('utf-8')
        raise ValueError(msg)
    return result.value
