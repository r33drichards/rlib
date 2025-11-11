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

func TestExponent(t *testing.T) {
	tests := []struct {
		base, exp, want int
	}{
		{2, 3, 8},
		{5, 2, 25},
		{10, 0, 1},
		{3, 4, 81},
	}

	for _, tt := range tests {
		got := Exponent(tt.base, tt.exp)
		if got != tt.want {
			t.Errorf("Exponent(%d, %d) = %d; want %d", tt.base, tt.exp, got, tt.want)
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
