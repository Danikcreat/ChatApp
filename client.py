import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("TCP Client")
        self.master.geometry("400x500")

        # Поля ввода подключения
        self.ip_label = tk.Label(master, text="Server IP:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(master)
        self.ip_entry.pack()

        self.port_label = tk.Label(master, text="Server Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(master)
        self.port_entry.pack()

        # Кнопка подключения
        self.connect_btn = tk.Button(master, text="Connect", command=self.connect)
        self.connect_btn.pack(pady=5)

        # Лог сообщений
        self.log = scrolledtext.ScrolledText(master, height=15)
        self.log.pack(padx=10, pady=10)

        # Поле ввода сообщения
        self.msg_entry = tk.Entry(master)
        self.msg_entry.pack(pady=5)
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        # Кнопка отправки
        self.send_btn = tk.Button(master, text="Send", command=self.send_message)
        self.send_btn.pack()

        self.client_socket = None
        self.connected = False

    def log_message(self, message):
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)

    def connect(self):
        if self.connected:
            return

        try:
            ip = self.ip_entry.get()
            port = int(self.port_entry.get())
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))
            
            self.connected = True
            self.connect_btn.config(state="disabled")
            self.log_message(f"Connected to {ip}:{port}")
            
            # Запускаем поток для получения сообщений
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def send_message(self):
        if not self.connected:
            return
            
        message = self.msg_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode())
                self.log_message(f"You: {message}")
                self.msg_entry.delete(0, tk.END)
            except:
                self.log_message("Failed to send message")
                self.disconnect()

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.log_message(f"Received: {message}")
            except:
                break
        self.disconnect()

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.client_socket.close()
            self.connect_btn.config(state="normal")
            self.log_message("Disconnected from server")

def main():
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()