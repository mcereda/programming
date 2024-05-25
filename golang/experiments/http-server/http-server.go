package main

import (
	"errors"
	"log"
	"net/http"
)

func getHealth(w http.ResponseWriter, r *http.Request) {
	log.Println("Got request at '/healthz'")

	if _, err := w.Write([]byte("OK")); err != nil {
		log.Panicln("Error writing response:", err)
	}
}

func main() {
	http.Handle("/", http.FileServer(http.Dir("")))
	http.HandleFunc("/healthz", getHealth)

	log.Println("Starting the HTTP server")
	err := http.ListenAndServe(
		"0.0.0.0:8080",
		nil,
	)
	if errors.Is(err, http.ErrServerClosed) {
		log.Panicln("Server closed")
	} else if err != nil {
		log.Panic("Error starting the HTTP server:", err)
	}

	// err := http.ListenAndServeTLS(
	// 	config.ListenAddress+":"+config.ListenPort,
	// 	filepath.Join(config.CertDir, config.CertFile),
	// 	filepath.Join(config.CertDir, config.KeyFile),
	// 	nil,
	// )
}
