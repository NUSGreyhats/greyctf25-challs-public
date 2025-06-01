package exchange

import (
	"errors"
	"fmt"
	"math"
	"time"

	"github.com/google/uuid"
	"golang.org/x/text/language"
	"golang.org/x/text/message"
)

var NUM_TICKS = 30

func (ex *Exchange) Challenge(botId uuid.UUID, playerId uuid.UUID) {
	var err error
	var msg string
	defer func() {
		if err != nil {
			ex.accounts[playerId].Message = fmt.Sprintf("Error: %s", err.Error())
			return
		}
		ex.accounts[playerId].Message = msg
	}()

	<-ex.initialized

	myAcc := ex.accounts[botId]

	prices := make([]uint32, 0, NUM_TICKS*2)
	offset := 0
	gen := ex.generator(ex.flag, time.Now().Add(time.Second*-5))

	for v := range gen {
		prices = append(prices, v)
		if len(prices) == NUM_TICKS*2 {
			break
		}
	}

	for offset = range NUM_TICKS * 2 {
		if prices[offset] == ex.Price {
			break
		}
	}

	var prev, next uint32

	prev = math.MaxUint32

	for i := range NUM_TICKS {
		cur := prices[i+offset]
		if ex.Price != cur {
			fmt.Println(offset)
			fmt.Println(ex.PriceHistory, prices)
			fmt.Println(time.Now(), ex.NextUpdate)
			fmt.Println("Clock desync")
			err = errors.New("clock desync")
			return
		}
		if i < NUM_TICKS-1 {
			next = prices[i+1+offset]
		} else {
			next = 0
		}
		if prev < cur && next < cur {
			msg, err = ex.Sell(myAcc, myAcc.Flag)
			if err != nil {
				return
			}
			fmt.Printf("%s: %s\n", botId, msg)
		} else if prev > cur && next > cur {
			amtToBuy := (myAcc.Cash - TXN_FEE) / uint64(cur)
			msg, err = ex.Buy(myAcc, amtToBuy)
			if err != nil {
				return
			}
			fmt.Printf("%s: %s\n", botId, msg)
		}
		prev = cur
		<-time.After(time.Until(ex.NextUpdate) + time.Millisecond*50)
	}
	p := message.NewPrinter(language.English)
	myCash := myAcc.Cash
	playerCash := ex.accounts[playerId].Cash
	flag := "Better luck next time"
	// Are you really better if you don't have 5x the cash?
	for range 5 {
		if playerCash < myCash {
			break
		}
		playerCash -= myCash
	}
	if playerCash > myCash {
		flag = ex.flag
	}
	msg = p.Sprintf("Bot's cash: $%.2f\nYour cash: $%.2f\nFlag: %s", float64(myCash)/100.0, float64(playerCash)/100.0, flag)
	fmt.Printf("%s:\n%s\n\n", botId, msg)
}
