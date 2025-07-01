package safemath

import "testing"

func TestSafeMultiplyNormal(t *testing.T) {
	res, err := safeMultiply(1073741824, 1073741824)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
		return
	}
	if res != 1152921504606846976 {
		t.Errorf("Wanted 1152921504606846976, got %v", res)
	}
}

func TestSafeMultiplyOverflow(t *testing.T) {
	_, err := safeMultiply(8589934592, 8589934592)
	if err == nil {
		t.Errorf("Expected overflow error, got nil")
		return
	}
	if err.Error() != "integer overflow" {
		t.Errorf("Expected integer overflow, got %v", err.Error())
	}
}

func TestSafeMultiplyWithFeesNormal(t *testing.T) {
	res, err := SafeMultiplyWithFees(100, 100, 100, true)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
		return
	}
	if res != 9900 {
		t.Errorf("Wanted 9900, got %v", res)
	}
}

func TestSafeMultiplyWithFeesNormalAdd(t *testing.T) {
	res, err := SafeMultiplyWithFees(100, 100, 100, false)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
		return
	}
	if res != 10100 {
		t.Errorf("Wanted 10100, got %v", res)
	}
}

func TestSafeMultiplyWithFeesUnderflow(t *testing.T) {
	_, err := SafeMultiplyWithFees(1, 10, 100, true)
	if err == nil {
		t.Errorf("Expected underflow error, got nil")
		return
	}
	if err.Error() != "integer underflow" {
		t.Errorf("Expected integer underflow, got %v", err.Error())
	}
}
func TestSafeMultiplyWithFeesOverflow(t *testing.T) {
	_, err := SafeMultiplyWithFees(4294967295, 4294967295, 8589934599, false)
	if err == nil {
		t.Errorf("Expected overflow error, got nil")
		return
	}
	if err.Error() != "integer overflow" {
		t.Errorf("Expected integer overflow, got %v", err.Error())
	}
}

func TestSafeMultiplyWithFeesOverflow2(t *testing.T) {
	_, err := SafeMultiplyWithFees(8589934592, 8589934592, 100, true)
	if err == nil {
		t.Errorf("Expected overflow error, got nil")
		return
	}
	if err.Error() != "integer overflow" {
		t.Errorf("Expected integer overflow, got %v", err.Error())
	}
}
