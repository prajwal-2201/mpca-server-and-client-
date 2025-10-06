# 💬 VanishLAN Messenger

**VanishLAN Messenger** is a lightweight, LAN-based messaging application built with Python.  
It allows users connected to the same local network to **chat in real time** — with messages that **automatically disappear after a set duration**.

---

## 🚀 Features

- 🖥️ **Real-time LAN messaging** (no internet required)  
- 🧨 **Self-destructing messages** — messages vanish after 5, 10, or 30 seconds  
- 👥 **Live user list** — see who’s online in real time  
- 💬 **Clean, modern GUI** built with Tkinter  
- 🔒 **No external dependencies** — runs purely on Python sockets

---

## 📂 Project Structure

```
VanishLAN/
│
├── serverfinal.py     # Server-side script — handles connections and message broadcasting
├── clientfinal.py     # Client-side GUI application — connects to server and sends messages
└── README.md          # Project documentation
```

---

## ⚙️ Setup & Usage

### 🖧 1. Start the Server

Run the server script on one system (the host):

```bash
python3 serverfinal.py
```

You’ll see:
```
[+] Server listening on port 12345
```

> 💡 Make sure your firewall allows incoming connections on port **12345**.

---

### 💻 2. Run the Client

On each client system (including the host, if desired):

```bash
python3 clientfinal.py
```

You’ll be prompted to:
- Enter the **server’s IP address** (LAN IP of the host)
- Choose your **username**

Once connected, the chat window appears.

---

## 🧭 How It Works

- Each client connects to the server using **TCP sockets**.  
- Messages are broadcast to all connected clients.  
- Each message includes a **self-destruct timer** (5, 10, or 30 seconds).  
- The message is displayed in the UI and automatically removed after the timer expires.  
- The server maintains and updates a live **list of connected users**.

---

## 🧰 Requirements

- Python 3.8+
- Tkinter (comes preinstalled with Python on most systems)

No external libraries needed.

---

## 🖼️ UI Preview

```
---------------------------------------
| VanishLAN Messenger                 |
---------------------------------------
| [Chat Window]          | [Online Users] |
|                        |                |
-------------------------------------------
| [Message Box] [Timer ▼] [Send Button]   |
-------------------------------------------
```

Dark-themed and minimal for comfortable long sessions.

---

## ⚡ Example Interaction

**Alice** → “Hi everyone!” (10s timer)  
**Bob** → “Hey Alice 👋” (5s timer)  
→ Messages automatically vanish after their timer runs out.

---

## 🛡️ Notes & Limitations

- Works only on **local networks (LAN/Wi-Fi)**.
- Does **not** store messages — all communication is ephemeral.
- All clients must be on the **same subnet** as the server.
- Basic error handling — best for personal, educational, or demo use.

---

## 🧑‍💻 Author

**Prajwal V**  
💡 Built for learning and experimentation with Python sockets and Tkinter.

---

## 🏷️ License

This project is open source and available under the **MIT License**.
