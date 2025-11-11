/// Add two integers
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// Multiply two integers
pub fn multiply(a: i32, b: i32) -> i32 {
    a * b
}

/// Divide two integers
/// Returns an error if division by zero
pub fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

/// Raise base to the power of exponent
pub fn exponent(base: i32, exp: i32) -> i32 {
    base.pow(exp as u32)
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

    #[test]
    fn test_multiply() {
        assert_eq!(multiply(2, 3), 6);
        assert_eq!(multiply(-2, 3), -6);
        assert_eq!(multiply(0, 5), 0);
    }

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

    #[test]
    fn test_exponent() {
        assert_eq!(exponent(2, 3), 8);
        assert_eq!(exponent(5, 2), 25);
        assert_eq!(exponent(10, 0), 1);
        assert_eq!(exponent(3, 4), 81);
    }
}
