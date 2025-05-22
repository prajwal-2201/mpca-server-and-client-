import socket
import threading
import tkinter as tk
from tkinter import ttk, simpledialog
import time

HOST = input("Enter server IP address: ")
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = simpledialog.askstring("Username", "Enter your name:")

client.sendall(username.encode())

window = tk.Tk()
window.title("VanishLAN Messenger")
window.configure(bg="#1e1e1e")

messages_frame = tk.Frame(window, bg="#1e1e1e")
scrollbar = tk.Scrollbar(messages_frame)
msg_list = tk.Listbox(messages_frame, height=20, width=60, yscrollcommand=scrollbar.set,
                      bg="#2d2d2d", fg="white", font=("Segoe UI", 10))
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
messages_frame.pack(padx=10, pady=10)

users_frame = tk.LabelFrame(window, text="Online Users", fg="white", bg="#1e1e1e", font=("Segoe UI", 9))
user_listbox = tk.Listbox(users_frame, height=20, width=20, bg="#2d2d2d", fg="white", font=("Segoe UI", 9))
user_listbox.pack(padx=5, pady=5)
users_frame.pack(side=tk.RIGHT, padx=10)

entry_frame = tk.Frame(window, bg="#1e1e1e")
entry_field = tk.Entry(entry_frame, width=50, bg="#2d2d2d", fg="white", font=("Segoe UI", 10))
entry_field.pack(side=tk.LEFT, padx=(0, 5))

timer_var = tk.StringVar()
timer_menu = ttk.Combobox(entry_frame, textvariable=timer_var, values=["5", "10", "30"], width=3)
timer_menu.set("10")
timer_menu.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(entry_frame, text="Send", command=lambda: send_message(), bg="#444", fg="white")
send_button.pack(side=tk.LEFT)
entry_frame.pack(pady=(0, 10))

def send_message():
    msg = entry_field.get()
    if msg:
        timer = int(timer_var.get())
        full_msg = f"{username}: {msg}|||{timer}"
        client.sendall(full_msg.encode())
        entry_field.delete(0, tk.END)

def receive():
    while True:
        try:
            msg = client.recv(4096).decode()
            if msg.startswith("|USERLIST|"):
                user_listbox.delete(0, tk.END)
                for user in msg.replace("|USERLIST|", "").split(","):
                    user_listbox.insert(tk.END, user)
            else:
                message, timer = msg.split("|||")
                msg_list.insert(tk.END, message)
                window.after(int(timer) * 1000, lambda: msg_list.delete(tk.END))
        except:
            break

threading.Thread(target=receive, daemon=True).start()

window.mainloop()
