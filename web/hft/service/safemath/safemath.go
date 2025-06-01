package safemath

import (
	"errors"
)

func safeMultiply(a uint64, b uint64) (uint64, error) {
	var res uint64
	var prev uint64
	for range a {
		prev = res
		res += b
		if prev > res {
			return 0, errors.New("integer overflow")
		}
	}
	return res, nil
}

func SafeMultiplyWithFees(a uint64, b uint64, fee uint64, subtract bool) (uint64, error) {
	res, err := safeMultiply(a, b)
	if err != nil {
		return 0, err
	}
	withoutFees := res
	if subtract {
		res -= fee
		if res > withoutFees {
			return 0, errors.New("integer underflow")
		}
	} else {
		res += fee
		if res < withoutFees {
			return 0, errors.New("integer overflow")
		}
	}
	return res, nil
}
