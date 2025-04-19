import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("TCP Server")
        self.master.geometry("400x500")
        
        # Поля ввода
        self.ip_label = tk.Label(master, text="IP:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(master)
        self.ip_entry.insert(0, "0.0.0.0")  # слушаем все интерфейсы
        self.ip_entry.pack()

        self.port_label = tk.Label(master, text="Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(master)
        self.port_entry.pack()

        # Кнопка старта
        self.start_btn = tk.Button(master, text="Start Server", command=self.start_server)
        self.start_btn.pack(pady=5)

        # Лог сообщений
        self.log = scrolledtext.ScrolledText(master, height=20)
        self.log.pack(padx=10, pady=10)

        self.server_socket = None
        self.running = False

    def log_message(self, message):
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)

    def start_server(self):
        if self.running:
            return

        try:
            ip = self.ip_entry.get()
            port = int(self.port_entry.get())
            
            # Создаем сокет
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Проверяем доступность порта
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                self.server_socket.bind((ip, port))
            except OSError:
                messagebox.showerror("Error", "Port is already in use!")
                return
                
            self.server_socket.listen(5)
            self.running = True
            self.start_btn.config(state="disabled")
            
            self.log_message(f"Server started on {ip}:{port}")
            
            # Запускаем поток для принятия подключений
            threading.Thread(target=self.accept_clients, daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.log_message(f"New connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            except:
                break

    def handle_client(self, client_socket, addr):
        while self.running:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.log_message(f"[{addr}] {message}")
            except:
                break
        client_socket.close()
        self.log_message(f"Connection closed: {addr}")

def main():
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()