package exchange

import (
	"strings"
	"testing"
)

func TestClockDesync(t *testing.T) {
	t.Parallel()
	ex := Exchange{}
	defer ex.Close()
	ex.Init("amogus", fakePriceGenerator([]uint32{1000_00, 2000_00, 3000_00}))

	playerId := ex.NewAccount()
	botId := ex.NewAccount()
	playerAcc, _ := ex.GetAccount(playerId)
	<-ex.initialized
	ex.generator = fakePriceGenerator([]uint32{1000_00})
	ex.Challenge(botId, playerId)

	expected := "Error: clock desync"
	if playerAcc.Message != expected {
		t.Errorf("Expected %v, got %v", expected, playerAcc.Message)
	}
}

func TestPlayerLose(t *testing.T) {
	t.Parallel()
	ex := Exchange{}
	defer ex.Close()
	ex.Init("amogus", fakePriceGenerator([]uint32{1000_00, 2000_00, 3000_00}))

	playerId := ex.NewAccount()
	botId := ex.NewAccount()
	playerAcc, _ := ex.GetAccount(playerId)
	ex.Challenge(botId, playerId)

	if !strings.Contains(playerAcc.Message, "Better luck next time") {
		t.Errorf("Expected message to contain failure message, got %v", playerAcc.Message)
	}
}

func TestPlayerWin(t *testing.T) {
	t.Parallel()
	ex := Exchange{}
	defer ex.Close()
	ex.Init("amogus", fakePriceGenerator([]uint32{1000_00, 2000_00, 3000_00}))

	playerId := ex.NewAccount()
	botId := ex.NewAccount()
	playerAcc, _ := ex.GetAccount(playerId)
	playerAcc.Cash = 100_000_000_000_000_00
	ex.Challenge(botId, playerId)

	if !strings.Contains(playerAcc.Message, ex.flag) {
		t.Errorf("Expected message to contain flag message, got %v", playerAcc.Message)
	}
}

func TestBotSellOverflow(t *testing.T) {
	t.Parallel()
	ex := Exchange{}
	defer ex.Close()
	ex.Init("amogus", fakePriceGenerator([]uint32{1000_00, 1_00}))

	playerId := ex.NewAccount()
	botId := ex.NewAccount()
	playerAcc, _ := ex.GetAccount(playerId)
	playerAcc.Cash = 100_000_000_000_000_00
	ex.Challenge(botId, playerId)

	if playerAcc.Message != "Error: integer overflow" {
		t.Errorf("Expected message to integer overflow message, got %v", playerAcc.Message)
	}
}

func TestBotBuyUnderflow(t *testing.T) {
	t.Parallel()
	ex := Exchange{}
	defer ex.Close()
	ex.Init("amogus", fakePriceGenerator([]uint32{1, 2}))

	playerId := ex.NewAccount()
	botId := ex.NewAccount()
	playerAcc, _ := ex.GetAccount(playerId)
	botAcc, _ := ex.GetAccount(botId)
	botAcc.Cash = 100
	ex.Challenge(botId, playerId)

	if playerAcc.Message != "Error: integer overflow" {
		t.Errorf("Expected message to integer overflow message, got %v", playerAcc.Message)
	}
}
