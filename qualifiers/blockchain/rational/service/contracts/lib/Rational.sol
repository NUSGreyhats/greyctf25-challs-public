// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

// Upper 128 bits is the numerator, lower 128 bits is the denominator
type Rational is uint256;

using {add as +, sub as -, mul as *, div as /, eq as ==, neq as !=} for Rational global;

// ======================================== CONVERSIONS ========================================

library RationalLib {
    Rational constant ZERO = Rational.wrap(0);

    function fromUint128(uint128 x) internal pure returns (Rational) {
        return toRational(x, 1);
    }

    function toUint128(Rational x) internal pure returns (uint128) {
        (uint256 numerator, uint256 denominator) = fromRational(x);
        return numerator == 0 ? 0 : uint128(numerator / denominator);
    }
}

// ======================================== OPERATIONS ========================================

function add(Rational x, Rational y) pure returns (Rational) {
    (uint256 xNumerator, uint256 xDenominator) = fromRational(x);
    (uint256 yNumerator, uint256 yDenominator) = fromRational(y);

    if (xNumerator == 0) return y;
    if (yNumerator == 0) return x;

    // (a / b) + (c / d) = (ad + cb) / bd
    uint256 numerator = xNumerator * yDenominator + yNumerator * xDenominator;
    uint256 denominator = xDenominator * yDenominator;

    return toRational(numerator, denominator);
}

function sub(Rational x, Rational y) pure returns (Rational) {
    (uint256 xNumerator, uint256 xDenominator) = fromRational(x);
    (uint256 yNumerator, uint256 yDenominator) = fromRational(y);

    if (yNumerator != 0) require(xNumerator != 0, "Underflow");

    // (a / b) - (c / d) = (ad - cb) / bd
    // a / b >= c / d implies ad >= cb, so the subtraction will never underflow when x >= y
    uint256 numerator = xNumerator * yDenominator - yNumerator * xDenominator;
    uint256 denominator = xDenominator * yDenominator;

    return toRational(numerator, denominator);
}

function mul(Rational x, Rational y) pure returns (Rational) {
    (uint256 xNumerator, uint256 xDenominator) = fromRational(x);
    (uint256 yNumerator, uint256 yDenominator) = fromRational(y);

    if (xNumerator == 0 || yNumerator == 0) return RationalLib.ZERO;

    // (a / b) * (c / d) = ac / bd
    uint256 numerator = xNumerator * yNumerator;
    uint256 denominator = xDenominator * yDenominator;

    return toRational(numerator, denominator);
}

function div(Rational x, Rational y) pure returns (Rational) {
    (uint256 xNumerator, uint256 xDenominator) = fromRational(x);
    (uint256 yNumerator, uint256 yDenominator) = fromRational(y);

    if (xNumerator == 0) return RationalLib.ZERO;
    require(yNumerator != 0, "Division by zero");

    // (a / b) / (c / d) = ad / bc
    uint256 numerator = xNumerator * yDenominator;
    uint256 denominator = xDenominator * yNumerator;

    return toRational(numerator, denominator);
}

function eq(Rational x, Rational y) pure returns (bool) {
    (uint256 xNumerator,) = fromRational(x);
    (uint256 yNumerator,) = fromRational(y);
    if (xNumerator == 0 && yNumerator == 0) return true;

    return Rational.unwrap(x) == Rational.unwrap(y);
}

function neq(Rational x, Rational y) pure returns (bool) {
    return !eq(x, y);
}

// ======================================== HELPERS ========================================

function fromRational(Rational v) pure returns (uint256 numerator, uint256 denominator) {
    numerator = Rational.unwrap(v) >> 128;
    denominator = Rational.unwrap(v) & type(uint128).max;
}

function toRational(uint256 numerator, uint256 denominator) pure returns (Rational) {
    if (numerator == 0) return RationalLib.ZERO;

    uint256 d = gcd(numerator, denominator);
    numerator /= d;
    denominator /= d;

    require(numerator <= type(uint128).max && denominator <= type(uint128).max, "Overflow");

    return Rational.wrap(numerator << 128 | denominator);
}

function gcd(uint256 x, uint256 y) pure returns (uint256) {
    while (y != 0) {
        uint256 t = y;
        y = x % y;
        x = t;
    }
    return x;
}
