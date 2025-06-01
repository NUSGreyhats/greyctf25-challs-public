package exchange

import (
	"iter"
	"testing"
	"time"

	"github.com/google/uuid"
)

func fakePriceGenerator(sequence []uint32) func(string, time.Time) iter.Seq[uint32] {
	return func(string, time.Time) iter.Seq[uint32] {
		return func(yield func(uint32) bool) {
			i := 0
			for {
				v := sequence[i%len(sequence)]
				if !yield(v) {
					return
				}
				i++
			}
		}
	}
}

func TestNoFlag(t *testing.T) {
	defer func() {
		expected := "FLAG cannot be empty!"
		r := recover()
		if r == nil {
			t.Errorf("Expected panic")
		} else if r != expected {
			t.Errorf("Expected %v, got %v", expected, r)
		}

	}()
	ex := Exchange{}

	ex.Init("", fakePriceGenerator([]uint32{1}))
}

func TestAccount(t *testing.T) {
	ex := Exchange{}
	defer ex.Close()

	ex.Init("amogus", fakePriceGenerator([]uint32{1}))

	_, err := ex.GetAccount(uuid.New())

	if err == nil {
		t.Errorf("Expected error, got nil")
		return
	}

	if err.Error() != "account not found" {
		t.Errorf("Expected account not found error, got %v", err.Error())
	}
}

func TestCreateAccount(t *testing.T) {
	ex := Exchange{}
	defer ex.Close()

	ex.Init("amogus", fakePriceGenerator([]uint32{1}))
	accId := ex.NewAccount()
	acc, err := ex.GetAccount(accId)
	if err != nil {
		t.Errorf("Unexpected error %v", err.Error())
		return
	}

	if acc.Cash != 10_000_000_000 {
		t.Errorf("Expected acc.Cash to be 10_000_000_000, got %v", acc.Cash)
	}

	if acc.Flag != 0 {
		t.Errorf("Expected acc.Flag to be 0, got %v", acc.Cash)
	}

}
func TestSell(t *testing.T) {
	ex := Exchange{}
	defer ex.Close()

	ex.Init("amogus", fakePriceGenerator([]uint32{100000}))
	accId := ex.NewAccount()
	acc, err := ex.GetAccount(accId)
	if err != nil {
		t.Errorf("Unexpected error %v", err.Error())
		return
	}

	// Test selling without sufficient $FLAG
	_, err = ex.Sell(acc, 1)
	if err == nil {
		t.Errorf("Expected error for insufficient funds, got nil")
		return
	}
	if err.Error() != "insufficient funds" {
		t.Errorf("Expected insufficient funds error, got %v", err.Error())
	}

	// Add $FLAG to account
	acc.Flag = 10

	// Test successful sell
	msg, err := ex.Sell(acc, 5)
	if err != nil {
		t.Errorf("Unexpected error %v", err.Error())
		return
	}
	expectedMsg := "Sold 5 $FLAG for $4,900.00 at $1,000.00"
	if msg != expectedMsg {
		t.Errorf("Expected message '%v', got '%v'", expectedMsg, msg)
	}

	// Verify account balances
	if acc.Flag != 5 {
		t.Errorf("Expected acc.Flag to be 5, got %v", acc.Flag)
	}
	if acc.Cash != 10000490000 {
		t.Errorf("Expected acc.Cash to be %v, got %v", 10000490000, acc.Cash)
	}

	// Test selling more $FLAG than available
	_, err = ex.Sell(acc, 10)
	if err == nil {
		t.Errorf("Expected error for insufficient funds, got nil")
		return
	}
	if err.Error() != "insufficient funds" {
		t.Errorf("Expected insufficient funds error, got %v", err.Error())
	}

	// Test integer overflow
	acc.Flag = 18446744073709505
	_, err = ex.Sell(acc, 18446744073709505)
	if err == nil {
		t.Errorf("Expected error for integer overflow, got nil")
		return
	}
	if err.Error() != "integer overflow" {
		t.Errorf("Expected integer overflow error, got %v", err.Error())
	}
}
func TestBuy(t *testing.T) {
	ex := Exchange{}
	defer ex.Close()

	ex.Init("amogus", fakePriceGenerator([]uint32{100000}))
	accId := ex.NewAccount()
	acc, err := ex.GetAccount(accId)
	if err != nil {
		t.Errorf("Unexpected error %v", err.Error())
		return
	}

	// Test buying without sufficient cash
	_, err = ex.Buy(acc, 20_000_000) // Attempt to buy $FLAG worth $200,000,000
	if err == nil {
		t.Errorf("Expected error for insufficient funds, got nil")
		return
	}
	if err.Error() != "insufficient funds" {
		t.Errorf("Expected insufficient funds error, got %v", err.Error())
	}

	// Test successful buy
	msg, err := ex.Buy(acc, 10) // Buy 10 $FLAG
	if err != nil {
		t.Errorf("Unexpected error %v", err.Error())
		return
	}
	expectedMsg := "Bought 10 $FLAG for $10,100.00 at $1,000.00"
	if msg != expectedMsg {
		t.Errorf("Expected message '%v', got '%v'", expectedMsg, msg)
	}

	// Verify account balances
	if acc.Flag != 10 {
		t.Errorf("Expected acc.Flag to be 10, got %v", acc.Flag)
	}
	if acc.Cash != 9998990000 {
		t.Errorf("Expected acc.Cash to be 9998990000, got %v", acc.Cash)
	}

	// Test integer overflow
	_, err = ex.Buy(acc, 1844674407370955)
	if err == nil {
		t.Errorf("Expected error for integer overflow, got nil")
		return
	}
	if err.Error() != "integer overflow" {
		t.Errorf("Expected integer overflow error, got %v", err.Error())
	}
}

func TestPriceHistory(t *testing.T) {
	t.Parallel()
	ex := Exchange{}
	defer ex.Close()
	ex.Init("amogus", fakePriceGenerator([]uint32{1}))

	time.Sleep(time.Second * 16)
	for _, v := range ex.PriceHistory {
		if v != 1 {
			t.Errorf("Expected %v, got %v", 1, v)
		}
	}
}
