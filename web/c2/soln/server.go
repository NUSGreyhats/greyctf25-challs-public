package main

import (
	"fmt"
	"net/http"
	"os"
)

func handleExec(w http.ResponseWriter, r *http.Request) {
	f, _ := os.Create("output")
	defer f.Close()
	f.ReadFrom(r.Body)
	fmt.Fprintln(w, "Done")
}

func main() {

	http.HandleFunc("PUT /", handleExec)

	http.ListenAndServe(":8081", nil)
}
