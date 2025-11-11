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

/// Add two integers
#[no_mangle]
pub extern "C" fn rlib_add(a: c_int, b: c_int) -> c_int {
    rlib_core::add(a, b)
}

/// Multiply two integers
#[no_mangle]
pub extern "C" fn rlib_multiply(a: c_int, b: c_int) -> c_int {
    rlib_core::multiply(a, b)
}

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

/// Get human-readable error message
#[no_mangle]
pub extern "C" fn rlib_error_message(error: RlibError) -> *const c_char {
    match error {
        RlibError::Ok => b"Success\0".as_ptr() as *const c_char,
        RlibError::DivisionByZero => b"Division by zero\0".as_ptr() as *const c_char,
        RlibError::InvalidArgument => b"Invalid argument\0".as_ptr() as *const c_char,
    }
}
