#!/usr/bin/env python3
"""
Script del Server Chat Concorrente
Corso: Programmazione di Reti - Università di Bologna
"""

import socket
from threading import Thread

def accetta_connessioni_client():
    """Ascolta le connessioni in ingresso dai client."""
    while True:
        try:
            client_conn, client_addr = server.accept()
            print(f"Nuova connessione da {client_addr}")
            client_conn.send("Benvenuto! Per favore, inserisci il tuo nome:".encode("utf8"))
            indirizzi[client_conn] = client_addr
            Thread(target=gestore_client, args=(client_conn,)).start()
        except Exception as e:
            print(f"Errore nell'accettare connessioni: {e}")
            break

def gestore_client(client):
    """Gestisce i messaggi di un singolo client."""
    try:
        nome = client.recv(BUF_SIZE).decode("utf8")
        benvenuto = f"Ciao {nome}! Digita (quit) per uscire dalla chat."
        client.send(benvenuto.encode("utf8"))
        notifica_tutti(f"{nome} si è unito alla chat!")
        client_list[client] = nome

        while True:
            messaggio = client.recv(BUF_SIZE)
            if messaggio.decode("utf8") != "(quit)":
                notifica_tutti(messaggio, f"{nome}: ")
            else:
                client.send("(quit)".encode("utf8"))
                client.close()
                del client_list[client]
                notifica_tutti(f"{nome} ha lasciato la chat.")
                break
    except Exception as e:
        print(f"Errore nella gestione del client {client}: {e}")
        if client in client_list:
            notifica_tutti(f"{client_list[client]} ha lasciato la chat.")
            del client_list[client]
    finally:
        client.close()

def notifica_tutti(messaggio, prefisso=""):
    """Invia un messaggio a tutti i client connessi."""
    for sock in client_list:
        try:
            sock.send(prefisso.encode("utf8") + messaggio)
        except Exception as e:
            print(f"Errore nell'invio del messaggio a {sock}: {e}")

client_list = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUF_SIZE = 1024
ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

if __name__ == "__main__":
    server.listen(5)
    print("Il server è in esecuzione e in attesa di connessioni...")
    accept_thread = Thread(target=accetta_connessioni_client)
    accept_thread.start()
    accept_thread.join()
    server.close()
