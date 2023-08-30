import socket
import tkinter as tk

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Client")

        self.label_cid = tk.Label(master, text="Enter Client ID:")
        self.label_cid.pack()
        self.entry_cid = tk.Entry(master)
        self.entry_cid.pack()

        self.label_cip = tk.Label(master, text="Enter Client IP:")
        self.label_cip.pack()
        self.entry_cip = tk.Entry(master)
        self.entry_cip.pack()

        self.label_host = tk.Label(master, text="Enter IP of device you want to access:")
        self.label_host.pack()
        self.entry_host = tk.Entry(master)
        self.entry_host.pack()

        self.button_connect = tk.Button(master, text="Connect", command=self.connect)
        self.button_connect.pack()

        self.label_cwd = tk.Label(master, text="")
        self.label_cwd.pack()

        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.pack()

        self.label_command = tk.Label(master, text="Enter a command:")
        self.label_command.pack()
        self.entry_command = tk.Entry(master)
        self.entry_command.pack()

        self.button_send = tk.Button(master, text="Send", command=self.send)
        self.button_send.pack()

        self.button_modify = tk.Button(master, text="Modify", command=self.modify)
        self.button_modify.pack()

        self.button_exit = tk.Button(master, text="Exit", command=self.exit)
        self.button_exit.pack()

        self.client_socket = None
        self.cwd = None

    def connect(self):
        cid = self.entry_cid.get()
        cip = self.entry_cip.get()
        host = self.entry_host.get()
        port = 9999
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.cwd = self.client_socket.recv(1024).decode()
        self.label_cwd.config(text=self.cwd)

    def send(self):
        command = self.entry_command.get()
        self.client_socket.send(command.encode('utf-8'))
        output = self.client_socket.recv(1024).decode('utf-8')
        self.text_output.delete('1.0', tk.END)  # clear the output window
        self.text_output.insert(tk.END, output)
        self.cwd = self.client_socket.recv(1024).decode()
        self.label_cwd.config(text=self.cwd)

    def modify(self):
        selection = self.text_output.get(tk.SEL_FIRST, tk.SEL_LAST)
        filename = self.cwd.strip()  # use current working directory as filename
        command = f"echo {selection} > new.txt"
        self.entry_command.delete(0, tk.END)
        self.entry_command.insert(0, command)
        self.send()



    def exit(self):
        self.client_socket.send("exit".encode('utf-8'))
        self.client_socket.close()
        self.master.quit()

root = tk.Tk()
client_gui = ClientGUI(root)
root.mainloop()
