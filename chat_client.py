#!/usr/bin/env python3
"""
Script del Client Chat GUI Avanzato usando Tkinter
Corso: Programmazione di Reti - Università di Bologna
"""

import socket
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext, messagebox

def ricevi_messaggi():
    """Gestisce la ricezione dei messaggi dal server."""
    while True:
        try:
            msg = client_socket.recv(BUF_SIZE).decode("utf8")
            if not msg:
                break
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, msg + "\n")
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
        except OSError:  # Possibile che il client abbia lasciato la chat
            break
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore: {e}")
            break

def invia_messaggio(event=None):
    """Gestisce l'invio dei messaggi al server."""
    msg = user_message.get()
    user_message.set("")  # Pulisce il campo di input
    try:
        client_socket.send(bytes(msg, "utf8"))
        if msg == "(quit)":
            client_socket.close()
            chat_window.quit()
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")

def on_close(event=None):
    """Gestisce la chiusura della finestra della chat."""
    user_message.set("(quit)")
    invia_messaggio()

def connetti_al_server():
    """Gestisce la connessione al server della chat."""
    global client_socket
    SERVER_HOST = server_host.get()
    SERVER_PORT = port.get()
    
    if not SERVER_PORT:
        SERVER_PORT = 53000
    else:
        try:
            SERVER_PORT = int(SERVER_PORT)
        except ValueError:
            messagebox.showerror("Porta Non Valida", "La porta deve essere un numero intero.")
            return
    
    ADDR = (SERVER_HOST, SERVER_PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(ADDR)
        recv_thread = Thread(target=ricevi_messaggi)
        recv_thread.start()
        connect_button.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Errore di Connessione", f"Impossibile connettersi al server: {e}")

# Crea e configura la finestra della chat
chat_window = tk.Tk()
chat_window.title("Chat di Programmazione di Reti")

server_frame = tk.Frame(chat_window)
tk.Label(server_frame, text="Server Host:").pack(side=tk.LEFT)
server_host = tk.Entry(server_frame, width=20)
server_host.pack(side=tk.LEFT, padx=5)
tk.Label(server_frame, text="Porta:").pack(side=tk.LEFT)
port = tk.Entry(server_frame, width=5)
port.pack(side=tk.LEFT, padx=5)
connect_button = tk.Button(server_frame, text="Connetti", command=connetti_al_server)
connect_button.pack(side=tk.RIGHT)
server_frame.pack(pady=10, padx=10)

msg_frame = tk.Frame(chat_window)
user_message = tk.StringVar()  # Per i messaggi da inviare
scrollbar = tk.Scrollbar(msg_frame)

# Crea un widget ScrolledText per una migliore visualizzazione dei messaggi
chat_display = scrolledtext.ScrolledText(msg_frame, wrap=tk.WORD, height=15, width=50, yscrollcommand=scrollbar.set, state=tk.DISABLED)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
msg_frame.pack(pady=10, padx=10)

input_frame = tk.Frame(chat_window)
input_field = tk.Entry(input_frame, textvariable=user_message, width=40)
input_field.bind("<Return>", invia_messaggio)
input_field.pack(side=tk.LEFT, padx=5)
send_button = tk.Button(input_frame, text="Invia", command=invia_messaggio)
send_button.pack(side=tk.RIGHT)
input_frame.pack(pady=10, padx=10)

chat_window.protocol("WM_DELETE_WINDOW", on_close)

# Inizializza il socket
client_socket = None
BUF_SIZE = 1024

tk.mainloop()  # Avvia il loop della GUI
