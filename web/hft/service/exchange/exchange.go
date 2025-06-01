package exchange

import (
	"errors"
	"iter"
	"time"

	"ctf.nusgreyhats.org/hft/hft/safemath"
	"github.com/google/uuid"
	"golang.org/x/text/language"
	"golang.org/x/text/message"
)

var TXN_FEE uint64 = 10_000
var DELAY = time.Millisecond * 500

type Account struct {
	Cash    uint64 `json:"cash"`
	Flag    uint64 `json:"flag"`
	Message string `json:"message"`
}

type TradeOperation int

const (
	OperationBuy TradeOperation = iota
	OperationSell
	OperationHodl
)

type Trade struct {
	Operation TradeOperation `json:"op"`
	Amount    uint64         `json:"amt"`
}

type Exchange struct {
	Price        uint32    `json:"price"`
	PriceHistory []uint32  `json:"priceHistory"`
	NextUpdate   time.Time `json:"nextUpdate"`

	accounts  map[uuid.UUID]*Account                   `json:"-"`
	flag      string                                   `json:"-"`
	generator func(string, time.Time) iter.Seq[uint32] `json:"-"`

	quit        chan struct{} `json:"-"`
	initialized chan struct{} `json:"-"`
}

func (ex *Exchange) Init(flag string, generator func(string, time.Time) iter.Seq[uint32]) {
	if len(flag) == 0 {
		panic("FLAG cannot be empty!")
	}

	ex.accounts = make(map[uuid.UUID]*Account)
	ex.quit = make(chan struct{})
	ex.initialized = make(chan struct{})

	ex.NextUpdate = time.Now()
	ex.PriceHistory = make([]uint32, 0, 31)
	ex.flag = flag
	ex.generator = generator

	go func() {
		for ex.Price = range generator(flag, ex.NextUpdate) {
			if len(ex.PriceHistory) == 0 {
				close(ex.initialized)
			}
			ex.NextUpdate = ex.NextUpdate.Add(DELAY)
			ex.PriceHistory = append(ex.PriceHistory, ex.Price)
			if len(ex.PriceHistory) > 30 {
				ex.PriceHistory = ex.PriceHistory[1:]
			}
			select {
			case <-time.After(time.Until(ex.NextUpdate)):
				continue
			case <-ex.quit:
				return
			}
		}
	}()
}

func (ex *Exchange) NewAccount() uuid.UUID {
	id := uuid.New()
	ex.accounts[id] = &Account{
		Cash: 10_000_000_000,
		Flag: 0,
	}
	return id
}

func (ex *Exchange) GetAccount(id uuid.UUID) (acc *Account, err error) {
	acc, exists := ex.accounts[id]

	if !exists {
		err = errors.New("account not found")
	}
	return
}

func (ex *Exchange) Buy(acc *Account, amount uint64) (msg string, err error) {
	<-ex.initialized
	cost, err := safemath.SafeMultiplyWithFees(uint64(ex.Price), amount, TXN_FEE, false)
	if err != nil {
		return
	}
	if acc.Cash < cost {
		err = errors.New("insufficient funds")
		return
	}
	acc.Flag += amount
	acc.Cash -= cost
	p := message.NewPrinter(language.English)
	msg = p.Sprintf("Bought %v $FLAG for $%.2f at $%.2f", amount, float64(cost)/100.0, float64(ex.Price)/100.0)
	return
}

func (ex *Exchange) Sell(acc *Account, amount uint64) (msg string, err error) {
	<-ex.initialized
	if amount > acc.Flag {
		err = errors.New("insufficient funds")
		return
	}

	profit, err := safemath.SafeMultiplyWithFees(uint64(ex.Price), amount, TXN_FEE, true)
	if err != nil {
		return
	}

	acc.Cash += profit
	acc.Flag -= amount
	p := message.NewPrinter(language.English)
	msg = p.Sprintf("Sold %v $FLAG for $%.2f at $%.2f", amount, float64(profit)/100.0, float64(ex.Price)/100.0)
	return
}

func (ex *Exchange) Close() {
	close(ex.quit)
}
