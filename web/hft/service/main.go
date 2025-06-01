package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"ctf.nusgreyhats.org/hft/hft/exchange"
	"github.com/google/uuid"
)

var ex exchange.Exchange

func query(w http.ResponseWriter, req *http.Request) {
	json.NewEncoder(w).Encode(ex)
}

func newChallenge(w http.ResponseWriter, req *http.Request) {
	id := ex.NewAccount()
	botId := ex.NewAccount()
	go ex.Challenge(botId, id)
	fmt.Fprintln(w, id)
}

func newAccount(w http.ResponseWriter, req *http.Request) {
	id := ex.NewAccount()
	fmt.Fprintln(w, id)
}

func getAccountID(req *http.Request) (id uuid.UUID, err error) {
	id_str := req.PathValue("id")

	id, err = uuid.Parse(id_str)
	return
}

func trade(w http.ResponseWriter, req *http.Request) {
	id, err := getAccountID(req)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	acc, err := ex.GetAccount(id)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	var tradeRequest exchange.Trade

	err = json.NewDecoder(req.Body).Decode(&tradeRequest)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	var msg string

	switch tradeRequest.Operation {
	case exchange.OperationBuy:
		msg, err = ex.Buy(acc, tradeRequest.Amount)
	case exchange.OperationSell:
		msg, err = ex.Sell(acc, tradeRequest.Amount)
	}

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	fmt.Printf("%s: %s\n", id, msg)

	fmt.Fprintf(w, "%s", msg)
}

func queryAccount(w http.ResponseWriter, req *http.Request) {
	id, err := getAccountID(req)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	acc, err := ex.GetAccount(id)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	json.NewEncoder(w).Encode(acc)
}

func main() {
	ex.Init(os.Getenv("FLAG"), exchange.PriceGenerator)
	http.HandleFunc("GET /query", query)
	http.HandleFunc("POST /newAccount", newAccount)
	http.HandleFunc("POST /challenge", newChallenge)
	http.HandleFunc("POST /{id}/trade", trade)
	http.HandleFunc("GET /{id}", queryAccount)
	http.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/index.html")
	})

	http.ListenAndServe(":8080", nil)
}
