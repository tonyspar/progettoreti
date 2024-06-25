#!/usr/bin/env python3
"""
Concurrent Chat Server Script
Course: Network Programming - University of Bologna
"""

import socket
from threading import Thread

def accetta_connessioni_client():
    """Gestisce l'ascolto delle connessioni in ingresso dai client."""
    while True:
        try:
            client_conn, client_addr = server.accept()
            print(f"Nuova connessione da {client_addr}")
            client_conn.send("Benvenuto! Per favore, inserisci il tuo nome:".encode("utf8"))
            indirizzi[client_conn] = client_addr
            Thread(target=gestore_client, args=(client_conn,)).start()
        except Exception as e:
            print(f"Errore nell'accettare la connessione: {e}")

def gestore_client(client):
    """Gestisce i messaggi provenienti da un singolo client."""
    try:
        nome = client.recv(BUF_SIZE).decode("utf8")
        benvenuto = f"Ciao {nome}! Digita (quit) per uscire dalla chat."
        client.send(benvenuto.encode("utf8"))
        notifica_tutti(f"{nome} si è unito alla chat!".encode("utf8"))
        client_list[client] = nome

        while True:
            messaggio = client.recv(BUF_SIZE)
            if messaggio.decode("utf8") != "(quit)":
                notifica_tutti(messaggio, f"{nome}: ")
            else:
                client.send("(quit)".encode("utf8"))
                client.close()
                del client_list[client]
                notifica_tutti(f"{nome} ha lasciato la chat.".encode("utf8"))
                break
    except Exception as e:
        print(f"Errore nel gestire il client: {e}")
        client.close()
        if client in client_list:
            del client_list[client]
            notifica_tutti(f"{nome} ha lasciato la chat a causa di un errore.".encode("utf8"))

def notifica_tutti(messaggio, prefisso=""):
    """Invia un messaggio a tutti i client connessi."""
    for sock in client_list:
        try:
            sock.send(prefisso.encode("utf8") + messaggio)
        except Exception as e:
            print(f"Errore nell'invio del messaggio a un client: {e}")

client_list = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUF_SIZE = 1024
ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Imposta SO_REUSEADDR
server.bind(ADDR)

if __name__ == "__main__":
    server.listen(5)
    print("Server in esecuzione, in attesa di connessioni...")
    try:
        accetta_thread = Thread(target=accetta_connessioni_client)
        accetta_thread.start()
        accetta_thread.join()
    except KeyboardInterrupt:
        print("Server interrotto dall'utente")
    except Exception as e:
        print(f"Errore nel thread di accettazione: {e}")
    finally:
        server.close()
